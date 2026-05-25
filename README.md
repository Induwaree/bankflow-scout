# BankFlow Scout

An OpenClaw agent that autonomously monitors a folder for bank statement files, categorises every transaction, detects anomalies, and generates a plain-English report — no manual review needed.

Built for the DataVita OpenClaw Challenge by Induwaree De Silva.

## The problem it solves

In financial operations, teams spend hours manually reviewing transaction exports looking for duplicates, unusual transfers, and miscategorised spend. I saw this firsthand automating banking workflows at Pan Asia Banking Corporation (PABC). BankFlow Scout eliminates that manual step entirely.

Drop a CSV into the watched folder. OpenClaw does the rest.

## How OpenClaw powers this

The openclaw.json file is the heart of this project. It tells OpenClaw to watch the documents/ folder for new CSV files using a file_watch trigger, run the analysis agent automatically when a new file appears, and check for new statements every 30 minutes via a heartbeat scheduler.

OpenClaw is the orchestrator. agent.py is the tool it runs. The agent operates autonomously without manual intervention.

## What it does

OpenClaw detects a new CSV bank statement dropped into documents/, triggers agent.py to read and parse every transaction, categorises spend automatically into Salary, Utilities, Transfer, Contractor, Income, and Finance, detects duplicate transactions and round-number transfers over 500, and saves a structured plain-English report to reports/.

## How to run it

Install OpenClaw: npm install -g openclaw@latest

Clone: git clone https://github.com/Induwaree/bankflow-scout.git

Setup: python3 -m venv venv && source venv/bin/activate && pip install watchdog pandas python-dotenv

Run: openclaw run openclaw.json

Then drop any CSV into documents/ and the agent generates a report in reports/ automatically.

A sample file with planted anomalies is at documents/sample_transactions.csv

## Why this matters

Manual transaction review is tedious and error-prone. A duplicate payment or round-number transfer can indicate fraud — but catching it means reading every row. BankFlow Scout turns that into a background process. The agent watches, thinks, and reports. Humans only get involved when something needs attention.

## Built with

OpenClaw, Python 3.9, watchdog, pandas
