import os
import re
from collections import Counter
import logging
from datetime import datetime
import platform
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Load environment variables from .env file
load_dotenv()

# Ensure logs directory exists
logs_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Generate log filename based on current date
log_file = os.path.join(logs_dir, f'frps_analyzer_{datetime.now().strftime("%Y%m%d")}.log')

# Initialize logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # File handler in append mode
        logging.FileHandler(log_file, mode='a', encoding='utf-8'),
        # Console handler
        logging.StreamHandler()
    ]
)

def get_smtp_config():
    """
    Retrieve SMTP configuration from environment variables
    从环境变量获取SMTP配置
    """
    return {
        'server': os.getenv('SMTP_SERVER'),
        'port': int(os.getenv('SMTP_PORT', 465)),
        'use_tls': os.getenv('SMTP_USE_TLS', 'True').lower() == 'true',
        'username': os.getenv('SMTP_USERNAME'),
        'password': os.getenv('SMTP_PASSWORD'),
        'sender': os.getenv('EMAIL_SENDER'),
        'recipients': os.getenv('EMAIL_RECIPIENTS', '').split(',')
    }

def send_email(subject, content, is_error=False):
    """
    Send email with given subject and content
    发送电子邮件，支持错误标记
    """
    smtp_config = get_smtp_config()
    
    try:
        msg = MIMEMultipart()
        msg['From'] = Header(smtp_config['sender'])
        msg['To'] = Header(','.join(smtp_config['recipients']))
        msg['Subject'] = Header(f"{'[ERROR] ' if is_error else ''}{subject}")
        
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        with smtplib.SMTP_SSL(smtp_config['server'], smtp_config['port']) as server:
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
        
        logging.info(f"Email sent successfully: {subject}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

def get_env_variables():
    """
    Get configuration variables from environment, with platform-specific defaults
    获取环境变量配置，支持跨平台默认路径
    """
    if platform.system() == 'Windows':
        default_log_path = 'C:\\frp\\frps.log'
    else:
        default_log_path = '/var/log/frps.log'
    
    frps_log_path = os.getenv('FRPS_LOG_PATH', default_log_path)
    monitored_names = [name.strip() for name in os.getenv('MONITORED_NAMES', '').split(',') if name.strip()]
    whitelist_ips = [ip.strip() for ip in os.getenv('WHITELIST_IPS', '').split(',') if ip.strip()]
    output_path = os.getenv('OUTPUT_PATH', os.getcwd())
    rank_limit = int(os.getenv('RANK_LIMIT', '20'))
    
    return frps_log_path, monitored_names, whitelist_ips, output_path, rank_limit

def parse_log_line(line):
    """
    Parse single log line to extract connection info
    解析日志行，提取连接信息
    """
    if '[I]' not in line:
        return None
    
    pattern1 = r'\[[\w]+\] \[([\w\.-]+)\] get a user connection \[([\d\.]+):\d+\]'
    pattern2 = r'\[[\w]+\] \[[\w]+\] \[([\w\.-]+)\] get a user connection \[([\d\.]+):\d+\]'
    
    match1 = re.search(pattern1, line)
    match2 = re.search(pattern2, line)
    
    if match1:
        return {
            'name': match1.group(1),
            'ip': match1.group(2)
        }
    elif match2:
        return {
            'name': match2.group(1),
            'ip': match2.group(2)
        }
    return None

def analyze_logs(log_path, monitored_names, whitelist_ips):
    """
    Analyze log file and count connections
    分析日志文件，统计连接信息
    """
    name_counter = Counter()
    ip_counter = Counter()
    combination_counter = Counter()
    
    logging.info(f"Starting log analysis from: {log_path}")
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = parse_log_line(line)
                if not parsed:
                    continue
                
                name = parsed['name']
                ip = parsed['ip']
                
                if ip in whitelist_ips:
                    continue
                
                if monitored_names and name not in monitored_names:
                    continue
                
                name_counter[name] += 1
                ip_counter[ip] += 1
                combination_counter[f"{name}-{ip}"] += 1
    
    except Exception as e:
        logging.error(f"Error reading log file: {e}")
        return None
    
    return name_counter, ip_counter, combination_counter

def get_ranked_results(counter, limit):
    """
    Get top ranked results from counter
    获取计数器的排名结果
    """
    return [(item, count) for item, count in counter.most_common(limit)]

def format_results_for_email(results):
    """
    Format analysis results for email content
    格式化分析结果为邮件内容
    """
    content = "FRPS Analysis Results\n\n"
    for section, ranked_items in results.items():
        if not ranked_items:
            continue
        content += f"\n{section}:\n"
        content += "-" * 50 + "\n"
        for rank, (item, count) in enumerate(ranked_items, 1):
            content += f"Rank {rank}: {item} (Count: {count})\n"
        content += "-" * 50 + "\n"
    return content

def write_results(output_path, results):
    """
    Write analysis results to log file
    将分析结果写入日志文件
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path(output_path) / f'frps_analysis_{timestamp}.log'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for section, ranked_items in results.items():
            if not ranked_items:
                continue
            f.write(f"\n{section}:\n")
            f.write("-" * 50 + "\n")
            for rank, (item, count) in enumerate(ranked_items, 1):
                f.write(f"Rank {rank}: {item} (Count: {count})\n")
            f.write("-" * 50 + "\n")
    
    logging.info(f"Results written to: {output_file}")
    return output_file

def main():
    """
    Main execution function for log analysis
    日志分析的主执行函数
    """
    start_time = datetime.now()
    logging.info("Starting FRPS log analyzer")
    
    try:
        # Get environment variables
        log_path, monitored_names, whitelist_ips, output_path, rank_limit = get_env_variables()
        
        logging.info(f"Configuration: Log path: {log_path}")
        logging.info(f"Monitored names: {monitored_names}")
        logging.info(f"Whitelist IPs: {whitelist_ips}")
        logging.info(f"Rank limit: {rank_limit}")
        
        # Analyze logs
        analysis_result = analyze_logs(log_path, monitored_names, whitelist_ips)
        if not analysis_result:
            error_msg = "Analysis failed - Could not analyze logs"
            logging.error(error_msg)
            send_email("FRPS Analysis Failed", error_msg, is_error=True)
            return
        
        name_counter, ip_counter, combination_counter = analysis_result
        
        # Prepare ranked results
        results = {
            'Most Frequent Names': get_ranked_results(name_counter, rank_limit),
            'Most Frequent IPs': get_ranked_results(ip_counter, rank_limit),
            'Most Frequent Combinations': get_ranked_results(combination_counter, rank_limit)
        }
        
        # Write results to file
        output_file = write_results(output_path, results)
        
        # Send email with results
        email_content = format_results_for_email(results)
        send_email("FRPS Analysis Results", email_content)
        
        # Record audit information
        end_time = datetime.now()
        duration = end_time - start_time
        audit_info = f"""
Analysis Audit Information:
-------------------------
Start Time: {start_time}
End Time: {end_time}
Duration: {duration}
Output File: {output_file}
Status: Success
"""
        logging.info(audit_info)
        
    except Exception as e:
        error_msg = f"Analysis failed with error: {str(e)}"
        logging.error(error_msg)
        send_email("FRPS Analysis Failed", error_msg, is_error=True)
        
        # Record audit information for failure
        end_time = datetime.now()
        duration = end_time - start_time
        audit_info = f"""
Analysis Audit Information:
-------------------------
Start Time: {start_time}
End Time: {end_time}
Duration: {duration}
Status: Failed
Error: {str(e)}
"""
        logging.error(audit_info)

if __name__ == "__main__":
    main()
