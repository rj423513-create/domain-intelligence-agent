import streamlit as st
import pandas as pd
from website_analyzer import analyze_domain
import time

st.set_page_config(page_title="Domain Intelligence Agent", layout="wide")
st.title("🚀 AI Domain Intelligence Agent")
st.markdown("**Bulk WHOIS + DNS + BuiltWith Analysis**")

if 'results' not in st.session_state:
    st.session_state.results = None
if 'domains' not in st.session_state:
    st.session_state.domains = []

input_method = st.radio("Input Method", ["Upload CSV/Excel", "Paste Domains"])

if input_method == "Upload CSV/Excel":
    uploaded = st.file_uploader("Upload domains.csv or .xlsx", type=["csv", "xlsx", "xls", "xlsb"])
    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded, engine='openpyxl')
            st.session_state.domains = df.iloc[:, 0].dropna().astype(str).str.strip().tolist()
            st.success(f"✅ Loaded {len(st.session_state.domains)} domains from file")
        except Exception as e:
            st.error(f"Error reading file: {e}")
else:
    text = st.text_area("Enter domains (one per line)")
    if text:
        st.session_state.domains = [d.strip() for d in text.split('\n') if d.strip()]

if st.button("🚀 Start Analysis", type="primary") and st.session_state.domains:
    with st.spinner("Analyzing domains... This may take time for large lists"):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, domain in enumerate(st.session_state.domains):
            status_text.info(f"Processing: {domain} ({i+1}/{len(st.session_state.domains)})")
            try:
                result = analyze_domain(domain)
                results.append(result)
            except Exception as e:
                results.append({"Domain": domain, "Error": str(e)})
            progress_bar.progress((i + 1) / len(st.session_state.domains))
        
        st.session_state.results = pd.DataFrame(results)
        st.success("✅ Analysis Completed!")
        
        # Display results
        st.dataframe(st.session_state.results, use_container_width=True)
        
        # Download button with proper Excel writer
        excel_buffer = pd.ExcelWriter('domain_report.xlsx', engine='openpyxl')
        st.session_state.results.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        
        with open('domain_report.xlsx', 'rb') as f:
            excel_data = f.read()
        
        st.download_button(
            label="📥 Download Full Excel Report",
            data=excel_data,
            file_name="domain_intelligence_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.caption("Backend: website_analyzer.py | Frontend: app.py | Made for your company • Pro version")