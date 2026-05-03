# 🛡️ AI-Powered Intrusion Detection and Response System (IDS/IPS)

An advanced Intrusion Detection and Prevention System (IDS/IPS) that analyzes network traffic using machine learning, detects anomalies, prioritizes threats with intelligent scoring, and responds automatically.

This project simulates a real-world **Security Operations Center (SOC)** environment with detection, monitoring, alerting, and response capabilities.

---

## 🚀 Live Demo

🔗 *[coming up soon]*
📽️ *[coming up soon]*

---

## 📌 Key Features

### 🔍 Detection & Analysis

* Capture and parse `.pcap` traffic using `tshark`
* Extract network features (IP, protocol, port, packet size)
* Machine learning anomaly detection using Isolation Forest
* Identify suspicious and malicious activity

### 🚨 Alerting & Response

* Intelligent alert scoring system (Low → Critical)
* Automatic IP blocking for high-risk threats (`iptables`)
* Real-time alerts via Slack integration
* Incident logging and tracking

### 📊 SOC Dashboard

* Web-based dashboard (Flask + Tailwind CSS)
* Secure login authentication system
* Alert severity visualization (Critical, High, Medium, Low)
* Traffic statistics and top IP monitoring
* Alert filtering by severity

### 🗄️ Data & Storage

* SQLite database with SQLAlchemy ORM
* Persistent storage of logs, alerts, and blocked IPs
* Structured and scalable data handling

### 🔐 Security & Production

* Environment-based configuration (`.env`)
* Secure secret key handling
* Security headers (XSS, clickjacking protection)
* Production-ready deployment (Gunicorn)

---

## 🧠 Skills Demonstrated

* Network traffic analysis & packet inspection
* Machine learning for anomaly detection
* Threat detection engineering
* Incident response automation
* Backend development with Flask
* Authentication & session management
* Database design with SQLAlchemy
* Dashboard UI design with Tailwind CSS
* Deployment & production configuration

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Machine Learning:** scikit-learn (Isolation Forest)
* **Data Processing:** pandas, joblib
* **Network Analysis:** tshark (Wireshark CLI)
* **Database:** SQLite (SQLAlchemy)
* **Frontend:** Tailwind CSS
* **Security:** Flask-Login, Flask-Bcrypt
* **Alerts:** Slack API (`slack_sdk`)
* **Automation:** cron (Linux)
* **Deployment:** Gunicorn, Render

---

## 📂 Project Structure

```
ai-ids-ips/
│
├── dashboard/
│   ├── app.py                # Main Flask application (production-ready)
│   ├── models.py            # Database models
│   ├── auth.py              # Authentication logic
│   ├── scoring.py           # Alert scoring engine
│   ├── templates/
│   │   ├── index.html       # Dashboard UI
│   │   ├── login.html       # Login page
│   │   └── alerts.html      # Filtered alerts page
│
├── scripts/
│   ├── parse_pcap.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── response_automation.py
│
├── database/
│   └── init_db.py           # Database initialization
│
├── models/
│   └── isolation_forest.pkl
│
├── run_pipeline.py
├── requirements.txt
├── Procfile
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/lovetechcyber/ai-ids-ips.git
cd ai-ids-ips
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

### 4. Install tshark

```bash
sudo apt install tshark
```

Ensure it is available in your PATH.

---

### 5. Configure Environment Variables

Create `.env` file:

```env
SECRET_KEY=your-secure-secret-key
DATABASE_URL=sqlite:///ids.db
SLACK_BOT_TOKEN=your-slack-token
```

---

### 6. Initialize Database

```bash
python database/init_db.py
```

---

## 🧪 Usage

### Run Full Pipeline

```bash
python run_pipeline.py
```

---

### Start Dashboard

```bash
python dashboard/app.py
```

Visit:

```
http://localhost:5000
```

---

## 🌍 Deployment

### Using Gunicorn

```bash
gunicorn dashboard.app:app
```

---

### Deploy on Render

* Build Command:

```bash
pip install -r requirements.txt
```

* Start Command:

```bash
gunicorn dashboard.app:app
```

---

## 🚨 Alert Scoring System

Threats are evaluated using rule-based scoring:

| Factor               | Score |
| -------------------- | ----- |
| ML Anomaly Detection | +50   |
| Large Packet Size    | +20   |
| Suspicious Ports     | +20   |
| Repeated IP Behavior | +10   |

### Severity Levels

* 🔴 Critical (80+)
* 🟠 High (60–79)
* 🟡 Medium (30–59)
* 🟢 Low (<30)

High/Critical alerts trigger automatic blocking.

---

## ⏰ Automation

Run every hour:

```bash
crontab -e
```

```bash
0 * * * * cd /path/to/ai-ids-ips && python run_pipeline.py >> logs/pipeline.log 2>&1
```

---

## 🔒 Security Considerations

* Use environment variables for secrets
* Disable debug mode in production
* Use HTTPS in deployment
* Restrict access (IP allowlist recommended)
* Upgrade to PostgreSQL for scalability

---

## 📈 Future Improvements

* Real-time monitoring with WebSockets
* SIEM integration (ELK Stack)
* Role-Based Access Control (RBAC)
* Email/SMS alert notifications
* Docker containerization
* Cloud deployment (AWS/GCP)

---

## 📄 License

MIT License

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit pull requests.

---

## 👤 Author

**Okwubali Prince**
📧 [lovetechcyb@gmail.com](mailto:lovetechcyb@gmail.com)
🔗 https://github.com/lovetechcyber

---

## ⭐ If You Like This Project

Give it a star ⭐ and share your feedback!
