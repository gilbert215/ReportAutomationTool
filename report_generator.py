from groq import Groq
import gspread
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ── 1. GOOGLE SHEETS NODE (reads real data) ──────────────────────────────────
def read_student_data():
    gc = gspread.service_account(filename=os.path.expanduser("~/credentials.json"))
    sheet = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1HrMWTyd307YvCH6aUkBbHjH2ewgr9bmy28fkeYldSRI"
    ).sheet1

    rows = sheet.get_all_records()
    students = []
    for r in rows:
        students.append({
            "name": str(r.get("Name", "")),
            "attendance": str(r.get("Attendance", "")).upper() == "TRUE",
            "score": int(r.get("Score", 0)),
        })
    return students

# ── 2. CODE NODE (formats and summarises) ────────────────────────────────────
def process_student_data(students):
    total_scores = [s["score"] for s in students]
    avg_score = round(sum(total_scores) / len(total_scores), 1)
    at_risk = [s["name"] for s in students if s["score"] < 60]
    top_performers = [s["name"] for s in students if s["score"] >= 85]
    absent_students = [s["name"] for s in students if not s["attendance"]]
    attendance_rate = round(
        sum(1 for s in students if s["attendance"]) / len(students) * 100
    )
    return {
        "avg_score": avg_score,
        "at_risk": at_risk,
        "top_performers": top_performers,
        "absent_students": absent_students,
        "attendance_rate": attendance_rate,
        "total_students": len(students),
        "week": "Week 1",
        "course": "Inzira AI Summer Camp 2026",
    }

# ── 3. AI NODE (Groq API) ───────────────────────────────────────────────────
def generate_report(summary):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""You are an assistant helping a teacher at the Inzira AI Summer Camp in Kigali, Rwanda.

Here is this week's class summary data:
- Course: {summary['course']}
- Week: {summary['week']}
- Total students: {summary['total_students']}
- Class average score: {summary['avg_score']}%
- Attendance rate: {summary['attendance_rate']}%
- Top performers (score >= 85%): {', '.join(summary['top_performers']) if summary['top_performers'] else 'None'}
- Students needing support (score < 60%): {', '.join(summary['at_risk']) if summary['at_risk'] else 'None'}
- Absent students: {', '.join(summary['absent_students']) if summary['absent_students'] else 'None'}

Write a short, warm weekly progress report email for the lead teacher. Include:
1. A brief overall summary of how the class performed
2. A specific callout for top performers (encourage them)
3. Actionable suggestions for at-risk students
4. A note about absent students
5. A short encouraging closing line

Keep it under 200 words. Use a professional but warm tone.
Do NOT include a subject line in the body."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )
    return response.choices[0].message.content

# ── 4. SEND EMAIL NODE (real Gmail SMTP) ─────────────────────────────────────
def send_email(summary, report_text, recipient):
    sender = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"{summary['week']} Progress Report — {summary['course']}"

    body = report_text + "\n\n---\nGenerated automatically by AI Report Bot (Groq + Python)"
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

    print(f"  ✅ Email sent to {recipient}")

# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    RECIPIENT = "mrgilvex@gmail.com"

    print("\n🔄 Running workflow...")
    print("  [1/4] Reading student data from Google Sheets...")
    students = read_student_data()
    print(f"        Found {len(students)} students")

    print("  [2/4] Processing data...")
    summary = process_student_data(students)
    print(f"        Avg score: {summary['avg_score']}%, at-risk: {len(summary['at_risk'])}")

    print("  [3/4] Generating report with AI...")
    report = generate_report(summary)

    print("  [4/4] Sending email...")
    send_email(summary, report, RECIPIENT)

    print("\n" + "=" * 50)
    print("  📧 REPORT PREVIEW")
    print("=" * 50)
    print(report)
    print("=" * 50)
    print("  ✅ Workflow completed successfully")
    print("=" * 50 + "\n")
