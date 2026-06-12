# Team Resource Board 🚀
**Cloud Computing Lab (CCL) Mini Project**

A collaborative, cloud-native platform for teams to organize and share resources (links, documents, and media). This project is designed to demonstrate core cloud computing service models: **IaaS, PaaS, DBaaS, Storage as a Service, and Security as a Service.**

---

## ☁️ Cloud Architecture (The "CCL" Mapping)

This project is built using a "Multi-Cloud" approach to satisfy lab requirements:

| Cloud Concept | Service Used | Description |
| :--- | :--- | :--- |
| **IaaS** | **Oracle Cloud VPS** | A dedicated virtual server running a health monitoring node (`iaas_status.py`) to demonstrate manual infrastructure management. |
| **PaaS** | **Render / Vercel** | The main FastAPI web application is hosted on a PaaS provider that manages the runtime environment and OS. |
| **DBaaS** | **Supabase (Postgres)** | All project data (boards, resources) is stored in a managed PostgreSQL database. |
| **Storage (SaaS)** | **Supabase Storage** | File uploads and documents are stored as a service using cloud object storage. |
| **Security (SaaS)** | **Supabase Auth** | Identity management is handled via JWT-based authentication and PostgreSQL Row Level Security (RLS). |

---

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Jinja2 Templates, Tailwind CSS, Alpine.js
- **Database:** PostgreSQL (Supabase)
- **Deployment:** Render (PaaS) + Oracle VPS (IaaS)

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.10+
- A Supabase Account (Free tier works perfectly)

### 2. Setup Database
1. Create a new project on [Supabase](https://supabase.com).
2. Go to the **SQL Editor** in Supabase and paste the contents of `supabase_schema.sql`.
3. Run the script to create the tables and security policies.

### 3. Clone and Install
```bash
# Navigate to project directory
cd team-resource-board

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration
1. Rename `.env.example` to `.env`.
2. Get your **Project URL** and **Anon Key** from Supabase (Project Settings > API) and add them to the `.env` file.

### 5. Start the Application
```bash
# Run the main web app
uvicorn app:app --reload
```
The app will be available at `http://localhost:8000`.

---

## 🖥️ IaaS Component (Oracle VPS)
To demonstrate **Infrastructure as a Service**, you can run the health monitor on your Oracle VPS:

1. SSH into your Oracle VPS.
2. Upload `iaas_status.py`.
3. Run: `python3 iaas_status.py`
4. Access the dashboard at `http://your-vps-ip:8080`.

### Telegram Health Bot on Oracle VPS
You can run a lightweight Telegram bot on Oracle VPS to monitor your Render app and send alerts.

1. Ensure your Render app has a public health endpoint:
	- `https://<your-render-domain>/healthz`
2. Create a Telegram bot using BotFather and get:
	- Bot token
	- Your chat ID
3. On Oracle VPS, set environment variables and run:

```bash
export TELEGRAM_BOT_TOKEN="<bot_token>"
export TELEGRAM_CHAT_ID="<your_chat_id>"
export HEALTHCHECK_URL="https://<your-render-domain>/healthz"
export STATUS_CHECK_INTERVAL_SEC="300"
export HOURLY_SUMMARY_INTERVAL_SEC="3600"

python3 telegram_health_bot.py
```

Supported commands in Telegram:
- `/status` : live health check
- `/ping` : connectivity check
- `/help` : command list

Notes:
- No SDK is required. The bot uses Telegram Bot API over plain HTTP.
- Your current web app implementation does not need route changes if `/healthz` already works.
- Keep the bot on Oracle and app on Render for resilient monitoring.

---

## 📝 Features
- [x] **Secure Login:** Only team members can access resources.
- [x] **Collaborative Boards:** Create boards for different projects/topics.
- [x] **Resource Types:** Support for Links and Document uploads.
- [x] **Role-Based Access:** Managed through Supabase RLS policies.
- [x] **Mobile Responsive:** Modern UI that works on all devices.

---

## 🌐 Deploy on Render (Recommended)

### 1. Create Service
1. Push this repository to GitHub.
2. In Render, create a new **Web Service** from the repo.

### 2. Build and Start Commands
- **Build Command:**
```bash
pip install -r requirements.txt
```
- **Start Command:**
```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

Use `0.0.0.0` and `$PORT` so Render can detect the listening port.
Do not use `--reload` in production.

### 3. Environment Variables
Add these in Render dashboard:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`
- `SECRET_KEY`
- `SUPABASE_STORAGE_BUCKET` (optional, default: `resource-files`)

### 4. Health Check
- **Health check path:** `/healthz`

The app includes this endpoint so Render can verify service readiness.

### 5. Verify Deployment
After deploy, test:
1. `/` dashboard page
2. `/login` authentication
3. board creation
4. resource upload/open
5. share-link flow
