# Streamlit Uptime Monitor 🚀

## Problem
Free-tier Streamlit apps go to sleep → cold start latency.

## Solution
Cron-based CI/CD pipeline using GitHub Actions to ping apps every 5 minutes.

## Features
- Supports multiple apps (scalable)
- Retry logic
- Config-driven (apps.json)

## Tech Stack
- GitHub Actions (CI/CD)
- Bash / Python
- Streamlit (apps)

## How it Works
Scheduler → Ping → Keep Alive

## Setup
1. Add your app URLs in config/apps.json
2. Push repo
3. GitHub Actions runs automatically
