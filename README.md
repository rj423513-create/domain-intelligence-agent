# 🚀 Domain Intelligence Agent

**Bulk WHOIS + DNS + BuiltWith Analysis Tool** 

A professional AI-powered agent to analyze 50-100+ domains in one click.

---

## ✨ Features

- **Multi-source Analysis**: WHOIS, DNS Records (A, MX, NS, TXT), Tech Stack
- **Multiple Input Formats**: Supports `.csv`, `.xlsx`, `.xlsb`
- **Beautiful UI**: Built with Streamlit (Clean & Professional)
- **Live Progress**: See which domain is being processed
- **Professional Excel Report**: Auto-formatted with wide columns for full visibility
- **Error Handling**: Graceful failures with clear messages
- **No API Key Required**: Works completely with free public sources

---

## 📁 Project Structure

domain-intelligence-agent/
├── agent/
│   ├── app.py                 # Frontend (Streamlit UI)
│   └── website_analyzer.py    # Backend (Core Logic)
├── requirements.txt
├── .env.example
├── README.md
├── sample_domains.csv
└── .gitignore
text

## 🛠️ Technologies Used

Python 3
Streamlit (UI)
pandas + openpyxl (Excel handling)
python-whois
dnspython (DNS Records)
requests + BeautifulSoup (BuiltWith fallback)

## How to Run
1. `pip install -r requirements.txt`
2. `streamlit run agent/app.py`

Supports .csv, .xlsx, .xlsb files.

Created by Rudra Patel.
