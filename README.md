
# 🚀 Streamlit Uptime Monitor

## Problem
Free-tier Streamlit apps go to sleep, causing cold start latency (30–60 seconds), leading to poor user experience.

## Solution
Designed a scalable uptime monitoring system using GitHub Actions to periodically ping applications and keep them active.

---

## 🔥 Features
- Config-driven architecture (`apps.json`)
- Parallel health checks for multiple apps
- Retry mechanism with failure handling
- Timeout control to avoid hanging requests
- Redirect-aware HTTP validation (2xx & 3xx)
- Automatic scheduling via CI/CD (every 5 minutes)

---

## 🏗️ Architecture


GitHub Actions (Cron)
↓
Read apps.json
↓
Parallel Ping Engine
↓
Retry + Timeout Logic
↓
Status Output



---

## 🛠️ Tech Stack
- GitHub Actions (CI/CD)
- Bash (automation + networking)
- jq (JSON parsing)
- Streamlit (target apps)

---

## 📊 Impact
- Eliminated cold start delays (~40s → near 0s)
- Supports 15+ applications efficiently
- Zero-cost uptime monitoring solution

---

## ⚙️ Setup

1. Add app URLs in `config/apps.json`
2. Push to GitHub
3. GitHub Actions runs automatically

---

## 📌 Future Improvements
- Slack/Email alert integration
- Persistent logging (CSV/DB)
- Python async version using httpx
- Monitoring dashboard

---
