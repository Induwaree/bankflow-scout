cat > README.md << 'EOF'
# BankFlow Scout

An AI agent that silently monitors a folder for bank statement files, automatically categorises transactions, detects anomalies, and generates a plain-English report — no manual review needed.

Built for the DataVita OpenClaw Challenge.

## The problem it solves

In financial operations, teams spend hours manually reviewing transaction exports looking for duplicates, unusual transfers, and miscategorised spend. I saw this firsthand while automating banking workflows at Pan Asia Banking Corporation. BankFlow Scout eliminates that manual step entirely.

Drop a CSV into the watched folder. The agent does the rest.

## What it does

- Watches a folder for new CSV bank statement files
- Parses and categorises every transaction automatically
- Detects duplicate transactions on the same day
- Detects suspiciously round-number transfers over £500
- Generates a structured report saved to the reports/ folder
- Prints a summary to the terminal in real time

## How to run it

1. Clone the repo
git clone https://github.com/Induwaree/bankflow-scout.git
cd bankflow-scout

2. Set up environment
python3 -m venv venv
source venv/bin/activate
pip install watchdog pandas

3. Run the agent
python3 agent.py

4. Drop a CSV into the documents/ folder
The agent detects it instantly and generates a report in reports/

## CSV format

date,description,amount,type
2025-01-03,Salary Payment,2500.00,credit
2025-01-05,Electricity Bill,120.50,debit

A sample file is included at documents/sample_transactions.csv

## Built with

- Python 3.9
- OpenClaw
- watchdog
- pandas
EOF