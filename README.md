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
