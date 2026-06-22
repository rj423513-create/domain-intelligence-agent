import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import whois
import dns.resolver
import random
import re
from urllib.parse import urlparse

st.set_page_config(page_title="SEO Domain Intelligence Agent", layout="wide")

st.title("🚀 SEO Domain Intelligence Agent")
st.markdown("### Multi-Website Enterprise SEO Analysis (Full Features + Core Web Vitals)")

with st.sidebar:
    st.header("Configuration")
    domains_input = st.text_area(
        "🌐 Enter Domain URLs (one per line)", 
        value="https://jeenweb.com",
        height=120
    )
    max_pages = st.slider("Max Pages to Crawl per Domain", 5, 100, 25)
    run_analysis = st.button("🚀 Start Full Multi-Website Analysis", type="primary")

def get_domain_info(domain):
    clean_domain = domain.replace("https://", "").replace("http://", "").rstrip("/").split("/")[0]
    try:
        w = whois.whois(clean_domain)
        creation = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        expiration = w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date
        ns = ", ".join(w.name_servers) if w.name_servers else "N/A"
        registrar = w.registrar or "N/A"
    except:
        creation, expiration, ns, registrar = "N/A", "N/A", "N/A", "N/A"

    try:
        mx_records = [str(r.exchange) for r in dns.resolver.resolve(clean_domain, 'MX')]
        mx_info = ", ".join(mx_records)
    except:
        mx_info = "N/A"

    robots = "Found" if requests.get(f"{domain.rstrip('/')}/robots.txt", timeout=8, headers={'User-Agent': 'Mozilla/5.0'}).status_code == 200 else "Not Found"
    sitemap = "Found" if requests.get(f"{domain.rstrip('/')}/sitemap.xml", timeout=8, headers={'User-Agent': 'Mozilla/5.0'}).status_code == 200 else "Not Found"
    ssl_status = "Valid (HTTPS)" if domain.startswith("https") else "HTTP Only"

    return {
        'Domain': domain,
        'Registrar': registrar,
        'Creation_Date': str(creation)[:10] if creation != "N/A" else "N/A",
        'Expiration_Date': str(expiration)[:10] if expiration != "N/A" else "N/A",
        'Name_Servers': ns,
        'MX_Records': mx_info,
        'SSL_Status': ssl_status,
        'robots.txt': robots,
        'sitemap.xml': sitemap,
        'Domain_Authority (DA)': 'N/A (Free version - needs Moz API)',
        'Page_Authority (PA)': 'N/A (Free version - needs Moz API)',
        'Domain_Rating (DR)': 'N/A (Free version - needs Ahrefs API)',
        'Bounce_Rate': 'N/A (Needs Google Analytics access)',
        'Timestamp': datetime.now().isoformat()
    }

def crawl_page(base_url, max_pages=25):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    visited = set()
    issues = []
    pages_data = []
    audit_data = []
    to_crawl = [base_url]
    
    while to_crawl and len(visited) < max_pages:
        current = to_crawl.pop(0)
        if current in visited: continue
        visited.add(current)
        
        try:
            start_time = time.time()
            resp = requests.get(current, headers=headers, timeout=12, allow_redirects=True)
            load_time = round(time.time() - start_time, 2)
            status = resp.status_code
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            title = soup.title.string.strip() if soup.title and soup.title.string else "Missing Title"
            meta = soup.find('meta', attrs={'name': 'description'})
            meta_desc = meta['content'].strip() if meta and meta.get('content') else "Missing Meta Description"
            h1 = soup.find('h1')
            h1_text = h1.get_text(strip=True) if h1 else "Missing H1"
            
            # Canonical
            canonical = soup.find('link', rel='canonical')
            canonical_status = canonical['href'] if canonical and canonical.get('href') else "Missing"
            
            # Social Meta (OG)
            og_title = soup.find('meta', property='og:title')
            og_desc = soup.find('meta', property='og:description')
            social_meta = "Present" if og_title or og_desc else "Missing"
