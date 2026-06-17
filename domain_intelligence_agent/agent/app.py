import streamlit as st
import pandas as pd
from website_analyzer import analyze_domain
import time

st.set_page_config(page_title="Domain Intelligence Agent", layout="wide")
st.title("🚀 AI Domain Intelligence Agent")
st.markdown("**Bulk WHOIS + DNS + BuiltWith Analysis** — No API key required")

# Input
input_method = st.radio("Input Method", ["Upload CSV/Excel", "Paste Domains (one per line)"])

domains = []
if input_method == "Upload CSV/Excel":
    uploaded = st.file_uploader("Upload domains.csv or .xlsx (one domain per row in first column)", type=["csv", "xlsx"])
    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        domains = df.iloc[:, 0].dropna().astype(str).tolist()
else:
    text = st.text_area("Enter domains (one per line)", height=200)
    if text:
        domains = [d.strip() for d in text.split("\n") if d.strip()]

if st.button("🚀 Start Analysis", type="primary") and domains:
    with st.spinner(f"Analyzing {len(domains)} domains... This may take 1-3 minutes depending on count."):
        results = []
        progress_bar = st.progress(0)
        
        for i, domain in enumerate(domains):
            try:
                st.info(f"🔍 Processing: {domain}")
                result = analyze_domain(domain)
                results.append(result)
            except Exception as e:
                st.warning(f"Error with {domain}: {str(e)}")
                results.append({"Domain": domain, "Error": str(e)})
            progress_bar.progress((i + 1) / len(domains))
        
        df = pd.DataFrame(results)
        
        st.success(f"✅ Analysis Complete! {len(results)} domains processed.")
        st.dataframe(df, use_container_width=True)
        
        # Excel download
        excel_data = df.to_excel(index=False)
        st.download_button(
            label="📥 Download Full Excel Report",
            data=excel_data,
            file_name="domain_intelligence_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.info("💡 No API key needed — uses free public sources + smart fallbacks.")
st.caption("Pro AI Agent for your company • Built with ❤️")
