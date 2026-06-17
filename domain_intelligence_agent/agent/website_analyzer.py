import whois
import dns.resolver
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)
from config import BUILTWITH_API_KEY, RATE_LIMIT_DELAY

logger = logging.getLogger(__name__)

def safe_request(url, timeout=10):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; DomainAgent/1.0)"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception as e:
        logger.warning(f"Request failed {url}: {e}")
        return None

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "Registrar": w.registrar or "N/A",
            "Creation_Date": str(w.creation_date)[:10] if w.creation_date else "N/A",
            "Expiration_Date": str(w.expiration_date)[:10] if w.expiration_date else "N/A",
            "Name_Servers": ", ".join(w.name_servers) if w.name_servers else "N/A",
            "Emails": ", ".join(w.emails) if w.emails else "N/A",
        }
    except:
        return {"Error": "WHOIS failed"}

def get_dns_records(domain):
    records = {"A": [], "MX": [], "NS": [], "TXT": []}
    try:
        for rtype in records.keys():
            answers = dns.resolver.resolve(domain, rtype, lifetime=5)
            for rdata in answers:
                if rtype == "MX":
                    records[rtype].append(f"{rdata.preference} {rdata.exchange}")
                else:
                    records[rtype].append(str(rdata))
    except:
        pass
    return {k: ", ".join(v) if v else "N/A" for k, v in records.items()}

def get_builtwith_info(domain):
    # Try API first (optional)
    if BUILTWITH_API_KEY:
        try:
            url = f"https://api.builtwith.com/free1/api.json?KEY={BUILTWITH_API_KEY}&LOOKUP={domain}"
            resp = safe_request(url)
            if resp:
                data = resp.json()
                return {"Tech_Stack_Count": len(data.get("groups", [])), "Categories": str(data.get("categories", []))}
        except:
            pass
    # Fallback scrape - works without API
    try:
        resp = safe_request(f"https://builtwith.com/{domain}")
        if resp:
            soup = BeautifulSoup(resp.text, 'html.parser')
            techs = [t.get_text(strip=True) for t in soup.select(".techLink, .tech-name")[:15]]
            return {"Tech_Stack": ", ".join(techs)[:800] or "N/A"}
    except:
        pass
    return {"Tech_Stack": "N/A (scraping fallback used)"}

def analyze_domain(domain: str):
    logger.info(f"Analyzing {domain}...")
    time.sleep(RATE_LIMIT_DELAY)
    
    whois_data = get_whois_info(domain)
    dns_data = get_dns_records(domain)
    built_data = get_builtwith_info(domain)
    
    result = {"Domain": domain}
    result.update(whois_data)
    result.update(dns_data)
    result.update(built_data)
    return result
