# MediConnect: AI Healthcare Access for Underserved Communities

## Agents for Good - Kaggle Hackathon 2026

[![Kaggle](https://img.shields.io/badge/Kaggle-Submission-blue)](https://kaggle.com)
[![ADK](https://img.shields.io/badge/Google-ADK-orange)](https://developers.google.com/adk)
[![MCP](https://img.shields.io/badge/MCP-Server-green)](https://modelcontextprotocol.io)

---

## Problem Statement

Over **400 million people** in rural and underserved communities lack access to basic healthcare information, symptom triage, and appointment scheduling. Key barriers include:

- **Language barriers** - 7,000+ languages spoken globally; most health apps are English-only
- **Digital literacy gaps** - Complex interfaces exclude elderly and low-literacy populations
- **Distance to care** - Rural clinics are hours away; no pre-visit triage system
- **Cost of access** - Traditional telehealth requires smartphones and data plans

## Solution: MediConnect Multi-Agent System

MediConnect is a **Google ADK-powered multi-agent system** that provides:

1. **Intelligent Symptom Triage** - Evidence-based care level recommendation
2. **Real-time Translation** - 50+ languages for inclusive access
3. **Appointment Scheduling** - MCP server integration with clinic systems
4. **HIPAA-Compliant Security** - Anonymization, PII redaction, audit trails

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PATIENT INPUT                             │
│         (Text/Voice/SMS - Any Language)                      │
└──────────────────────┬────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT                              │
│         (Coordinates the entire pipeline)                    │
└──────────────────────┬────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────────┐
│   SECURITY   │ │TRANSLATOR│ │   TRIAGE     │ │  SCHEDULER   │
│    AGENT     │ │  AGENT   │ │   AGENT      │ │   AGENT      │
│              │ │          │ │              │ │              │
│ • Anonymize  │ │• 50+ Lang│ │• Symptom    │ │• MCP Server  │
│ • PII Redact │ │• Medical │ │  Analysis    │ │  Integration│
│ • Audit Log  │ │  Terms    │ │• Care Level  │ │• Book/Cancel│
│ • HIPAA      │ │• Cultural│ │  Recommend   │ │  Slots      │
│   Compliant  │ │  Sensitivity│              │ │              │
└──────────────┘ └──────────┘ └──────────────┘ └──────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              OUTPUT TO PATIENT                               │
│    (Translated, Triage Result, Appointment Confirmation)     │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Concepts Demonstrated

| Concept | Implementation | Evidence |
|---------|---------------|----------|
| **Agent/Multi-Agent System (ADK)** | `agents/orchestrator/agent.py` | SequentialAgent pipeline with 4 sub-agents |
| **MCP Server** | `agents/scheduler/mcp_server.py` | FastMCP server with 3 tools (list/book/cancel) |
| **Antigravity** | Video demo | Deployment to Cloud Run with `adk deploy` |
| **Security Features** | `agents/security/agent.py` + `shared/security.py` | SHA-256 anonymization, PII redaction, encryption |
| **Deployability** | `deployment/` + Video | Dockerfile, Cloud Run YAML, health checks |
| **Agent Skills** | `agents/translator/agent.py` + CLI | 50+ language support, `adk run` commands |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Google AI Studio API Key ([Get one free](https://aistudio.google.com/app/apikey))
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/mediconnect-agents.git
cd mediconnect-agents

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Run the orchestrator locally
adk run agents/orchestrator

# 5. Or run the web UI
adk web --host 0.0.0.0 --port 8000
```

### Kaggle Notebook

1. Upload this folder to Kaggle as a Dataset
2. Open `kaggle_notebook.ipynb`
3. Run all cells
4. See demo output in the notebook

---

## Project Structure

```
mediconnect-kaggle/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── kaggle_notebook.ipynb              # Main Kaggle notebook
│
├── agents/
│   ├── orchestrator/
│   │   └── agent.py                   # Main coordinator (SequentialAgent)
│   ├── triage/
│   │   ├── agent.py                   # Medical triage specialist
│   │   └── tools.py                   # Medical KB + drug interaction tools
│   ├── translator/
│   │   └── agent.py                   # 50+ language medical translator
│   ├── scheduler/
│   │   ├── agent.py                   # Appointment booking agent
│   │   └── mcp_server.py            # MCP Server (FastMCP)
│   └── security/
│       └── agent.py                   # HIPAA compliance + anonymization
│
├── shared/
│   ├── security.py                    # Encryption + PII masking utilities
│   └── utils.py                     # Common helper functions
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
│   ├── Dockerfile                     # Container definition
│   ├── cloudrun.yaml                  # Google Cloud Run config
│   └── deploy.sh                      # One-click deploy script
│
└── demo/
    └── README.md                      # Demo video guidelines
```

---

## Agent Details

### 1. Orchestrator Agent

The **central coordinator** that routes patient requests through the pipeline:

```python
from agents.orchestrator.agent import MediConnectOrchestrator

orchestrator = MediConnectOrchestrator()

patient = {
    "patient_id": "anon_12345",
    "language": "es",
    "symptoms": "fiebre, dolor de cabeza",
    "location": "rural_clinic_001"
}

result = orchestrator.process_patient_request(patient)
# Returns: triage level, translated response, appointment slot
```

### 2. Triage Agent

Evidence-based symptom analysis using medical knowledge base:

| Symptom | Triage Level | Action |
|---------|-------------|--------|
| Chest pain + shortness of breath | **EMERGENCY** | Call 911 immediately |
| Fever > 3 days | **URGENT** | Same-day urgent care |
| Mild headache | **SELF-CARE** | Rest, hydration, monitor |
| Cough + fever | **NON-URGENT** | Schedule primary care |

### 3. Translator Agent

Supports **50+ languages** including:
- Spanish, French, Arabic, Hindi, Mandarin
- Swahili, Portuguese, Bengali, Russian, Japanese
- Medical terminology preservation
- Cultural sensitivity flags

### 4. Scheduler Agent (MCP Server)

**MCP (Model Context Protocol)** server for clinic integration:

```python
# MCP Tools available:
list_available_slots(clinic_id, date)   # Query open slots
book_appointment(clinic_id, time, patient_id, reason)  # Book slot
cancel_appointment(appointment_id)      # Cancel booking
```

### 5. Security Agent

**HIPAA-compliant** data handling:

| Feature | Implementation |
|---------|---------------|
| Anonymization | SHA-256 hashing of names/phones |
| PII Redaction | Regex-based phone/SSN/email detection |
| Encryption | Fernet symmetric encryption |
| Audit Logging | All access logged with timestamps |
| Address Masking | Only city/region retained |

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_security.py -v

# Run with coverage
pytest --cov=agents tests/
```

---

## Deployment

### Option 1: Google Cloud Run (Recommended)

```bash
# One-click deploy
cd deployment
bash deploy.sh

# Or manually:
gcloud run deploy mediconnect   --source .   --region us-central1   --allow-unauthenticated
```

### Option 2: Docker Local

```bash
docker build -t mediconnect -f deployment/Dockerfile .
docker run -p 8000:8000 --env-file .env mediconnect
```

### Option 3: Kaggle Notebook

See `kaggle_notebook.ipynb` - run all cells in Kaggle environment.

---

## Video Submission

**5-Minute YouTube Video** covering:

| Timestamp | Content |
|-----------|---------|
| 0:00-0:30 | Problem: Healthcare access gap for 400M+ people |
| 0:30-1:30 | Architecture: Multi-agent diagram walkthrough |
| 1:30-3:00 | Demo: Spanish patient → triage → appointment booking |
| 3:00-3:30 | Security: Anonymization, PII redaction, audit logs |
| 3:30-4:30 | Deployability: `adk deploy` to Cloud Run live demo |
| 4:30-5:00 | Impact: Scale to millions, open-source, community-driven |

---

## Evaluation Criteria Mapping

### Category 1: The Pitch (30 points)

| Criteria | How We Address It |
|----------|-------------------|
| **Core Concept & Value (10)** | Healthcare for underserved communities; clear agent value proposition |
| **YouTube Video (10)** | 5-min video with problem, architecture, demo, build, deploy |
| **Writeup (10)** | This README + detailed Kaggle writeup with architecture diagrams |

### Category 2: The Implementation (70 points)

| Criteria | How We Address It |
|----------|-------------------|
| **Technical Implementation (50)** | Clean ADK architecture, MCP integration, meaningful agent use, clever tools |
| **Documentation (20)** | This README, architecture docs, setup instructions, deployment guide |

---

## License

MIT License - Open source for global health impact.

## Team

Built with passion for **Agents for Good**.

---

**Kaggle Writeup**: [Link to your Kaggle writeup]
**Live Demo**: [Link to Cloud Run deployment or GitHub]
**Video**: [Link to YouTube video]
