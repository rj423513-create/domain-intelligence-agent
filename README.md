# SEO Domain Intelligence Agent

**Multi-Website Enterprise SEO Analysis Tool**  
*Inspired by Screaming Frog + Semrush + WebPageTest*

---

## Features

- **Multi-Website Analysis** — Analyze multiple domains at once
- **Deep Crawling** — Crawl up to 100 pages per domain with on-page SEO checks
- **Domain Intelligence** — WHOIS, DNS records, SSL, robots.txt, sitemap
- **Technical Audit** — Core Web Vitals (LCP, FID, CLS), Page Speed, Missing Alt Text
- **SEO Issues Detection** — Title, Meta, H1, Broken Links, Server Errors (4xx/5xx)
- **Live Scanning Animation** — Beautiful real-time progress
- **Excel Export** — Full report with 4 sheets (Domain Info, Crawled Pages, SEO Issues, Technical Audit)
- **Clean & Modern UI** — GTmetrix-inspired dark theme

---

##  Quick Start

### 1. Install Dependencies

```bash
pip install streamlit pandas requests beautifulsoup4 whois dnspython openpyxl
## ✨ Features

- **Multi-source Analysis**: WHOIS, DNS Records (A, MX, NS, TXT), Tech Stack
- **Multiple Input Formats**: Supports `.csv`, `.xlsx`, `.xlsb`
- **Beautiful UI**: Built with Streamlit (Clean & Professional)
- **Live Progress**: See which domain is being processed
- **Professional Excel Report**: Auto-formatted with wide columns for full visibility
- **Error Handling**: Graceful failures with clear messages
- **No API Key Required**: Works completely with free public sources

---

## Project Structure

domain-intelligence-agent/<br>
├── agent/<br>
│   ├── app.py                 # Frontend (Streamlit UI)<br>
│   └── website_analyzer.py    # Backend (Core Logic<br>
├── requirements.txt<br>
├── .env.example<br>
├── README.md<br>
├── sample_domains.csv<br>
└── .gitignore<br>
text

## Technologies Used

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
