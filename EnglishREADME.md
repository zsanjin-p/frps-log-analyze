# FRPS Log Analysis Tool

This tool is designed to enhance the security of FRP (Fast Reverse Proxy) by reviewing FRPS log files to list the IPs and services with the highest number of connections.

## Features
- Passed the FRP 0.52-0.60 test, as long as the FRP does not change the current (version 0.60) log format
- Review FRPS log files.
- Whitelist IPs can be set.
- Concise report format with at-a-glance visibility into which service and which IP has the most connections.
- Support for sending report emails.
- Only IPv4 is supported

## Get started quickly

1. Clone the repository or download the project file.
   ```
   git clone https://github.com/zsanjin-p/frps-log-analyze
   ```

2. Modify the '.env' environment variable file to configure the following variables according to your environment:

- 'FRPS_LOG_PATH': FRPS log file path (required).
   - 'MONITORED_NAMES': The name of the service to be monitored (separated by commas). Leave blank to monitor all names.
   - 'WHITELIST_IPS': IP whitelist, comma separated.
   - 'OUTPUT_PATH': The path where the report saves the analysis results.
   - 'RANK_LIMIT': The number of top items displayed in the results.
   - 'SMTP_SERVER': The SMTP server configuration used to send emails.
   - 'SMTP_PORT': The SMTP server configuration used to send emails.
   - 'SMTP_USE_TLS': The SMTP server configuration used to send emails.
   - 'SMTP_USERNAME': The SMTP server configuration used to send emails.
   - 'SMTP_PASSWORD': The SMTP server configuration used to send emails.
   - 'EMAIL_SENDER': The sender of the email.
   - 'EMAIL_RECIPIENTS': The recipient of the email.

## Configuration and Use

Fill it out. For ENV files, except for the FRPS log location, you can leave it unfilled.
Logging needs to be enabled in frps.toml.
With the scheduled task program, it is executed once a day, because the frps.log only keeps the log of the current day and archives it every other day.
Receiving effect (no truncated picture)
![image](https://github.com/user-attachments/assets/8d5cdc1b-41a3-472f-80da-681de8a1c2cc)
Can be used with another open source project [frps-log-ip-ban](https://github.com/zsanjin-p/frps-log-ip-ban)

## License

This project is licensed under a BSD 2-Clause or 3-Clause license.

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


## Contribute

If you like this project, please consider giving us a star!⭐
