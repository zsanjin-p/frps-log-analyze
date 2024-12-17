
# FRPS 日志分析工具

此工具旨在增强 FRP (Fast Reverse Proxy) 的安全性，通过审查 FRPS 日志文件，列举连接次数最多数量的 IP 和服务。

## 功能特性
- 在frp 0.52-0.60测试通过，只要frp不改动当前（0.60版本）的日志格式都能适用
- 审查 FRPS 日志文件。
- 支持设置白名单 IP。
- 简洁的报告格式，一目了然哪个服务，哪个IP连接次数最多。
- 支持发送报告邮件。
- 仅支持ipv4

## 快速开始

1. 克隆仓库或下载项目文件。
   ```
   git clone https://github.com/zsanjin-p/frps-log-analyze
   ```

2. 修改 `.env` 环境变量文件，根据您的环境配置以下变量：

   - `FRPS_LOG_PATH`: FRPS 日志文件路径（必要）。
   - `MONITORED_NAMES`: 需要监控的服务名称（用逗号分隔）。留空表示监控所有名称。
   - `WHITELIST_IPS`: IP 白名单，逗号分隔。
   - `OUTPUT_PATH`: 报告保存分析结果的路径。
   - `RANK_LIMIT`: 结果中显示的排名前几的项目数量。
   - `SMTP_SERVER`: 用于发送电子邮件的 SMTP 服务器配置。
   - `SMTP_PORT`: 用于发送电子邮件的 SMTP 服务器配置。
   - `SMTP_USE_TLS`: 用于发送电子邮件的 SMTP 服务器配置。
   - `SMTP_USERNAME`: 用于发送电子邮件的 SMTP 服务器配置。
   - `SMTP_PASSWORD`: 用于发送电子邮件的 SMTP 服务器配置。
   - `EMAIL_SENDER`: 电子邮件的发件人。
   - `EMAIL_RECIPIENTS`: 电子邮件的收件人。



## 配置和使用

填写好.ENV文件，除了FRPS的日志位置必填，其他可以不填。
frps.toml中需要启用日志。
搭配计划任务程序，每天执行一次，因为frps.log只保留当天日志，隔天就归档。
收件效果（没截长图）
![image](https://github.com/user-attachments/assets/8d5cdc1b-41a3-472f-80da-681de8a1c2cc)

可搭配另一个开源项目使用[frps-log-ip-ban](https://github.com/zsanjin-p/frps-log-ip-ban)

## 许可证

本项目采用 BSD 2-Clause 或 3-Clause 许可证。

BSD 3-Clause License

Copyright (c) 2024, zsanjin
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the zsanjin nor the names of its contributors may be used
   to endorse or promote products derived from this software without specific
   prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## 贡献

如果您喜欢此项目，请考虑给我们一个星标（star）！⭐

