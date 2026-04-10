import streamlit as st
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Uptime Observatory",
    layout="wide",
    page_icon="🚀"
)

st.title("🚀 Uptime Observatory")
st.caption("Production-grade monitoring for deployed apps")

# ---------------- LOAD APPS ----------------
with open("config/apps.json", "r") as f:
    APPS = json.load(f)["apps"]

# ---------------- CORE CHECKER ----------------
def check_app(url):
    try:
        start = time.time()
        r = requests.get(url, timeout=10)
        latency = round((time.time() - start) * 1000, 2)

        return {
            "url": url,
            "status_code": r.status_code,
            "latency": latency,
            "status": "UP" if r.status_code in [200, 301, 302, 303] else "ISSUE"
        }

    except Exception:
        return {
            "url": url,
            "status_code": None,
            "latency": None,
            "status": "DOWN"
        }

# ---------------- RUN PARALLEL CHECKS ----------------
with st.spinner("Running health checks..."):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_app, APPS))

# ---------------- METRICS ----------------
up = sum(1 for r in results if r["status"] == "UP")
down = sum(1 for r in results if r["status"] == "DOWN")
issue = sum(1 for r in results if r["status"] == "ISSUE")

col1, col2, col3 = st.columns(3)

col1.metric("🟢 Healthy", up)
col2.metric("🔴 Down", down)
col3.metric("🟡 Issues", issue)

st.divider()

# ---------------- TABLE VIEW ----------------
st.subheader("📡 Service Health Matrix")

for r in results:
    if r["status"] == "UP":
        st.success(
            f"🟢 UP | {r['url']} | "
            f"{r['status_code']} | "
            f"{r['latency']} ms"
        )

    elif r["status"] == "ISSUE":
        st.warning(
            f"🟡 ISSUE | {r['url']} | "
            f"{r['status_code']} | "
            f"{r['latency']} ms"
        )

    else:
        st.error(
            f"🔴 DOWN | {r['url']} | NO RESPONSE"
        )

# ---------------- SLA INSIGHT PANEL ----------------
st.divider()
st.subheader("📊 System Insights")

total = len(results)
uptime_percent = round((up / total) * 100, 2)

st.metric("Uptime %", f"{uptime_percent}%")

if uptime_percent == 100:
    st.success("All systems operational 🚀")
elif uptime_percent >= 80:
    st.warning("Degraded performance detected")
else:
    st.error("Critical system instability")

# ---------------- AUTO REFRESH ----------------
st.caption("Auto-refresh every 60 seconds")

time.sleep(60)
st.rerun()
