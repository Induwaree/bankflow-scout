import pandas as pd
import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DOCUMENTS_FOLDER = "documents"
REPORTS_FOLDER = "reports"

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

    # Check for duplicate transactions (same description + amount + type on same day)
    duplicates = df[df.duplicated(subset=["date", "description", "amount", "type"], keep=False)]
    if not duplicates.empty:
        for _, row in duplicates.drop_duplicates(subset=["date", "description", "amount"]).iterrows():
            anomalies.append(f"DUPLICATE: '{row['description']}' £{row['amount']} on {row['date']}")

    # Check for suspiciously round numbers over £500
    round_numbers = df[(df["amount"] % 500 == 0) & (df["amount"] >= 500) & (df["type"] == "debit")]
    for _, row in round_numbers.iterrows():
        anomalies.append(f"ROUND NUMBER: '{row['description']}' £{row['amount']} on {row['date']}")

    return anomalies

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

    report = "\n".join(report_lines)
    print(report)

    report_filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, "w") as f:
        f.write(report)
    print(f"\nReport saved to: {report_filename}")

class StatementHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            time.sleep(1)
            generate_report(event.src_path)

if __name__ == "__main__":
    print("BankFlow Scout is running...")
    print(f"Watching folder: {DOCUMENTS_FOLDER}/")
    print("Drop a CSV bank statement in to generate a report.\n")

    # Run once on existing files
    for filename in os.listdir(DOCUMENTS_FOLDER):
        if filename.endswith(".csv"):
            generate_report(os.path.join(DOCUMENTS_FOLDER, filename))

    observer = Observer()
    observer.schedule(StatementHandler(), path=DOCUMENTS_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
