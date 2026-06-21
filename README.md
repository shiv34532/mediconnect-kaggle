# MediConnect: AI Healthcare Access for Underserved Communities

> **Agents for Good — Kaggle Hackathon 2026**

---

## The Problem

Over **400 million people** in rural and underserved communities lack access to basic healthcare. Language barriers, distance to clinics, and low digital literacy make it worse. A patient with chest pain in rural Guatemala has no way to know if they need emergency care or can wait for a clinic appointment.

## What We Built

MediConnect is a **multi-agent AI system** that helps patients get the right care at the right time — in their own language, with their privacy protected.

### How It Works

A patient describes their symptoms. The system routes them through four specialized agents:

```
Patient Input (Any Language)
    ↓
┌─────────────────┐
│  Security Agent │  → Anonymizes PII, HIPAA compliance
└────────┬────────┘
         ↓
┌─────────────────┐
│ Translator Agent│  → Detects language, translates symptoms
└────────┬────────┘
         ↓
┌─────────────────┐
│  Triage Agent   │  → Analyzes symptoms, recommends care level
└────────┬────────┘
         ↓
┌─────────────────┐
│ Scheduler Agent │  → Books appointment via MCP server
└────────┬────────┘
         ↓
Patient Output (Their Language + Appointment)
```

### Example Flow

**Maria, 29, speaks Spanish only.** She enters: *"fiebre, dolor de cabeza, tos desde hace 2 días"*

1. **Security** → Her name becomes `6cea57c2fb6cbc2a`. Phone hashed. Region kept for clinic routing.
2. **Translator** → Detects Spanish. Translates to "fever, headache, cough for 2 days".
3. **Triage** → Checks medical KB. Returns: **NON-URGENT** — schedule primary care within 1-3 days.
4. **Scheduler** → Books next available slot at Sunrise Community Health. Confirmation: **APPT-A3F5B7E2**.

Maria gets her result in Spanish, with clear next steps.

---

## Key Concepts Demonstrated

| Concept | Implementation | Where |
|---------|---------------|-------|
| **Agent / Multi-Agent System (ADK)** | SequentialAgent pipeline with 4 sub-agents | `agents/orchestrator/agent.py` |
| **MCP Server** | FastMCP server with 5 tools for clinic scheduling | `agents/scheduler/mcp_server.py` |
| **Security Features** | SHA-256 anonymization, Fernet AES-128 encryption, PII redaction, audit logs | `agents/security/agent.py`, `shared/security.py` |
| **Deployability** | Dockerfile, Cloud Run YAML, deploy script | `deployment/` |
| **Agent Skills** | 50+ language support, CLI deployment | `agents/translator/agent.py`, `deployment/deploy.sh` |
| **Antigravity** | Cloud deployment demo | Video |

---

## Project Structure

```
mediconnect-kaggle/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── kaggle_notebook.ipynb              # Main Kaggle notebook (all demos)
│
├── agents/
│   ├── orchestrator/
│   │   └── agent.py                   # Main coordinator (SequentialAgent)
│   ├── triage/
│   │   ├── agent.py                   # Medical triage specialist
│   │   └── tools.py                   # BMI, pediatric tools
│   ├── translator/
│   │   └── agent.py                   # 50+ language medical translator
│   ├── scheduler/
│   │   ├── agent.py                   # Appointment booking agent
│   │   └── mcp_server.py            # MCP Server (FastMCP, 5 tools)
│   └── security/
│       └── agent.py                   # HIPAA compliance + anonymization
│
├── shared/
│   ├── security.py                    # Encryption + PII masking utilities
│   └── utils.py                     # Common helpers
│
├── tests/
│   ├── test_triage.py                 # Unit tests for triage agent
│   ├── test_scheduler.py              # MCP server tests
│   └── test_security.py               # Security feature tests
│
├── docs/
│   ├── architecture.md                # Detailed architecture docs
│   ├── deployment.md                  # Deployment instructions
│   └── video_script.md                # 5-minute video script
│
├── deployment/
│   ├── Dockerfile                     # Container definition (non-root user)
│   ├── cloudrun.yaml                  # Google Cloud Run config
│   └── deploy.sh                      # One-click deploy script
│
└── demo/
    └── README.md                      # Demo video guidelines
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Google AI Studio API Key ([Get one free](https://aistudio.google.com/app/apikey))

### Installation

```bash
# Clone the repo
git clone https://github.com/shivam983/mediconnect-agents.git
cd mediconnect-agents

# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate        # Mac/Linux
# or: venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Run Locally

```bash
# Run the web UI
adk web --host 0.0.0.0 --port 8000

# Or run the orchestrator directly
adk run agents/orchestrator
```

### Run Tests

```bash
# All tests
python tests/test_triage.py
python tests/test_scheduler.py
python tests/test_security.py

# Or with pytest
pytest tests/
```

### Deploy to Cloud Run

```bash
cd deployment
bash deploy.sh
```

---

## Demo Results

From Kaggle notebook execution:

| Component | Result | Status |
|-----------|--------|--------|
| Security Agent | Patient data anonymized (SHA-256 hashes) | ✅ |
| Triage Agent | Symptoms analyzed (EMERGENCY/URGENT/NON-URGENT/SELF-CARE) | ✅ |
| Translator Agent | Spanish detected, 50+ languages supported | ✅ |
| MCP Server | Appointment booked with confirmation code | ✅ |
| Encryption | Fernet AES-128 round-trip successful | ✅ |
| Unit Tests | All critical tests passed | ✅ |

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Agent Framework | Google ADK | Multi-agent orchestration |
| Protocol | MCP (Model Context Protocol) | Tool/server integration |
| LLM | Gemini 2.5 Flash | Reasoning and generation |
| Security | Fernet (AES-128), SHA-256 | Encryption, anonymization |
| Deployment | Docker + Google Cloud Run | Scalable hosting |

---

## Impact

This system can help **400+ million people**:
- Access healthcare information in their native language
- Get appropriate symptom triage before visiting clinics
- Schedule appointments at nearby facilities
- Maintain privacy through HIPAA-compliant data handling

---

## Links

- **Kaggle Writeup:** [Your Kaggle writeup link]
- **Video Demo:** [Your YouTube video link]
- **Live Demo:** [Your Cloud Run deployment link]

---

## License

MIT License — Open source for global health impact.

---

Built for **Agents for Good** 🌍
