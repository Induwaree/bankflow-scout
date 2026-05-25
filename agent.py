import pandas as pd
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

DOCUMENTS_FOLDER = "documents"
REPORTS_FOLDER = "reports"
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
REPORT_TO = os.getenv("REPORT_TO")

def categorise(description):
    description = description.lower()
    if any(word in description for word in ["salary", "payroll", "wage"]):
        return "Salary"
    elif any(word in description for word in ["electricity", "water", "internet", "gas", "bill"]):
        return "Utilities"
    elif any(word in description for word in ["transfer", "cash"]):
        return "Transfer"
    elif any(word in description for word in ["contractor", "supplier", "vendor"]):
        return "Contractor"
    elif any(word in description for word in ["revenue", "sales", "income"]):
        return "Income"
    elif any(word in description for word in ["bonus", "loan", "repayment"]):
        return "Finance"
    else:
        return "Other"

def detect_anomalies(df):
    anomalies = []
    duplicates = df[df.duplicated(subset=["date", "description", "amount", "type"], keep=False)]
    if not duplicates.empty:
        for _, row in duplicates.drop_duplicates(subset=["date", "description", "amount"]).iterrows():
            anomalies.append(f"DUPLICATE: '{row['description']}' £{row['amount']} on {row['date']}")
    round_numbers = df[(df["amount"] % 500 == 0) & (df["amount"] >= 500) & (df["type"] == "debit")]
    for _, row in round_numbers.iterrows():
        anomalies.append(f"ROUND NUMBER: '{row['description']}' £{row['amount']} on {row['date']}")
    return anomalies

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = REPORT_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, REPORT_TO, msg.as_string())
        print(f"Report emailed to {REPORT_TO}")
    except Exception as e:
        print(f"Email failed: {e}")

def generate_report(filepath):
    print(f"\nNew file detected: {filepath}")

    df = pd.read_csv(filepath)
    df["amount"] = df["amount"].astype(float)
    df["category"] = df["description"].apply(categorise)

    total_in  = df[df["type"] == "credit"]["amount"].sum()
    total_out = df[df["type"] == "debit"]["amount"].sum()
    net       = total_in - total_out

    category_summary = df[df["type"] == "debit"].groupby("category")["amount"].sum()
    anomalies = detect_anomalies(df)

    report_lines = []
    report_lines.append("=" * 50)
    report_lines.append("BANKFLOW SCOUT — TRANSACTION REPORT")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"File: {os.path.basename(filepath)}")
    report_lines.append("=" * 50)
    report_lines.append(f"\nTOTAL IN:  £{total_in:,.2f}")
    report_lines.append(f"TOTAL OUT: £{total_out:,.2f}")
    report_lines.append(f"NET:       £{net:,.2f}")
    report_lines.append("\nSPEND BY CATEGORY:")
    for category, amount in category_summary.items():
        report_lines.append(f"  {category:<20} £{amount:,.2f}")
    report_lines.append(f"\nANOMALIES FOUND: {len(anomalies)}")
    if anomalies:
        for a in anomalies:
            report_lines.append(f"  ⚠️  {a}")
    else:
        report_lines.append("  None detected.")
    report_lines.append("\n" + "=" * 50)
    report_lines.append("\nPowered by OpenClaw — autonomous agent runtime")
    report_lines.append("BankFlow Scout | github.com/Induwaree/bankflow-scout")

    report = "\n".join(report_lines)
    print(report)

    report_filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, "w") as f:
        f.write(report)
    print(f"Report saved to: {report_filename}")

    subject = f"BankFlow Scout: {len(anomalies)} anomalies found in {os.path.basename(filepath)}"
    send_email(subject, report)

class StatementHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            time.sleep(1)
            generate_report(event.src_path)

if __name__ == "__main__":
    print("BankFlow Scout is running (via OpenClaw shell skill)...")
    print(f"Watching folder: {DOCUMENTS_FOLDER}/")
    print(f"Reports will be emailed to: {REPORT_TO}")
    print("Drop a CSV bank statement in to generate a report.\n")

    observer = Observer()
    observer.schedule(StatementHandler(), path=DOCUMENTS_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
