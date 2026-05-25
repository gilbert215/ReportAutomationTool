# ReportAutomationTool

A fully automated AI report generator built in Python. It reads student data from Google Sheets, analyses performance metrics (averages, at‑risk students, top performers), generates a professional report using an AI language model (Groq/Llama 3.3), sends the report via Gmail SMTP, and runs automatically every Monday using a Linux cron job.

## Features
* **Google Sheets Integration:** Automatically pulls live data using a Google Service Account.
* **Data Transformation:** Calculates class averages, attendance rates, top performers, and flags at-risk students.
* **AI-Powered Insights:** Uses Groq API (Llama 3.3 70B) for lightning-fast text generation.
* **Email Delivery:** Automatically drafts and sends reports through Gmail SMTP.
* **Set-and-Forget Automation:** Completely hands-off scheduling via Linux Cron jobs.

## Architecture Pipeline
1. **Trigger (Cron Job):** Scheduled execution every Monday at 8:00 AM.
2. **Data Source (Google Sheets API):** Extracts student data dynamically.
3. **Transform (Python):** Analyzes metrics and prepares data summaries.
4. **AI Generation (Groq API):** Compiles raw stats into a professional text email.
5. **Output (Gmail SMTP):** Emails the completed document to specified recipients.

## Prerequisites
* Python 3.8+
* Google Cloud Console Account (for Sheets API access)
* Groq API Key
* Gmail account with 2-Step Verification enabled (to generate an App Password)

## Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ReportAutomationTool.git](https://github.com/YOUR_USERNAME/ReportAutomationTool.git)
   cd ReportAutomationTool
2. Install Dependencies:

python -m pip install -r requirements.txt

3. Set Up Google Credentials
Go to the Google Cloud Console.

Enable the Google Sheets API for your project.

Create a Service Account, generate a new JSON private key, and save it to your home directory as ~/credentials.json.

Open the JSON file, look for the client_email key, and copy that address string.

Open your target Google Sheet (Student Progress 2026) and use the Share menu to add that email string as a Viewer.


4. Create the Sheet Structure
Your target spreadsheet must have a sheet named Sheet1 containing at least these exact, case-sensitive column headers in Row 1:

Name

Attendance (Accepts TRUE or FALSE)

Score (Integer value)

5. Update Your Variables
Open your runner bash profile (run_report.sh) and supply your authentic system keys and account strings:

Bash
#!/bin/bash
export GROQ_API_KEY="gsk_your_actual_groq_key_here"
export GMAIL_ADDRESS="your.email@gmail.com"
export GMAIL_APP_PASSWORD="your_16_character_app_password"

# Navigate to code execution path
cd /home/yourusername/ReportAutomationTool
python report_generator.py >> ~/report_log.txt 2>&1
Make sure the script has permission to execute:

Bash
chmod +x run_report.sh
Cron Automation
To tie the automation string loop together seamlessly, register your bash engine file directly within the system crontab scheduler:

Bash
crontab -e
Add the following rule block at the bottom of your file to trigger execution automatically every Monday at 8:00 AM:

Plaintext
0 8 * * 1 /home/yourusername/ReportAutomationTool/run_report.sh
Verify your task entry is properly saved:

Bash
crontab -l
⚙️ Customization
Change the Recipient: Modify the RECIPIENT = "teacher@example.com" string inside report_generator.py.

Adjust Performance Thresholds: Change the filtering integer (< 60 or >= 85) located inside the process_student_data calculation blocks.

Update Model Selection: Swap out model="llama-3.3-70b-versatile" for other supported models like llama-3.1-8b-instant.


To open the script

nano report_generator.py

To learn the automation

python report_generator.py