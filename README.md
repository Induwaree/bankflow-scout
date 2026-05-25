# BankFlow Scout

An OpenClaw skill that autonomously monitors a folder for bank statement files, categorises transactions, detects anomalies, and generates a plain-English report.

Built for the DataVita OpenClaw Challenge by Induwaree De Silva.

## The problem it solves

In financial operations, teams spend hours manually reviewing transaction exports looking for duplicates and unusual transfers. I saw this firsthand automating banking workflows at Pan Asia Banking Corporation. BankFlow Scout eliminates that manual step entirely.

Drop a CSV into the watched folder. OpenClaw does the rest.

## How OpenClaw powers this

BankFlow Scout is packaged as an OpenClaw skill (bankflow-scout.yaml). OpenClaw runs as a background daemon, triggers the scan action every 30 minutes via its heartbeat scheduler, and executes the analysis agent as a shell action. The agent runs autonomously without manual intervention.

## What it does

Watches a folder for new CSV bank statement files. Parses and categorises every transaction automatically into Salary, Utilities, Transfer, Contractor, Income, and Finance. Detects duplicate transactions on the same day and suspiciously round-number transfers over 500. Generates a structured plain-English report saved to the reports folder.

## How to run it

Install OpenClaw: npm install -g openclaw@latest

Clone the repo: git clone https://github.com/Induwaree/bankflow-scout.git

Set up Python: python3 -m venv venv && source venv/bin/activate && pip install watchdog pandas python-dotenv

Run directly: python3 agent.py

Install as OpenClaw skill: openclaw skills import bankflow-scout.yaml

Drop a CSV into documents/ and the agent generates a report in reports/ automatically.

## CSV format

date,description,amount,type
2025-01-03,Salary Payment,2500.00,credit
2025-01-05,Electricity Bill,120.50,debit

A sample file is included at documents/sample_transactions.csv

## Built with

OpenClaw, Python 3.9, watchdog, pandas, python-dotenv
