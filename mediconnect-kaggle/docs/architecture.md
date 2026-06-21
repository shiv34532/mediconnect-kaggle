# MediConnect Architecture Documentation

## System Overview

MediConnect uses a **Sequential Multi-Agent Architecture** powered by Google ADK.

## Agent Interaction Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   PATIENT       │────▶│   ORCHESTRATOR  │────▶│   SECURITY      │
│   INPUT         │     │   AGENT         │     │   AGENT         │
│                 │     │                 │     │                 │
│ • Symptoms      │     │ • Route request │     │ • Anonymize PII │
│ • Language      │     │ • Coordinate    │     │ • Hash names    │
│ • Location      │     │   pipeline      │     │ • Audit log     │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                       │
                              ┌──────────────────────┘
                              ▼
                       ┌─────────────────┐
                       │   TRANSLATOR    │
                       │   AGENT         │
                       │                 │
                       │ • Detect lang   │
                       │ • Translate     │
                       │ • Medical terms │
                       └────────┬────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   TRIAGE        │
                       │   AGENT         │
                       │                 │
                       │ • Symptom KB    │
                       │ • Drug checks   │
                       │ • Care level    │
                       └────────┬────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   SCHEDULER     │
                       │   AGENT         │
                       │                 │
                       │ • MCP Server    │
                       │ • List slots    │
                       │ • Book appt     │
                       └────────┬────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PATIENT       │
                       │   OUTPUT        │
                       │                 │
                       │ • Triage result │
                       │ • Appointment   │
                       │ • Care plan     │
                       └─────────────────┘
```

## Data Flow

1. **Input**: Patient submits symptoms in their language
2. **Security**: PII anonymized, audit log created
3. **Translation**: Non-English input translated to English for processing
4. **Triage**: Symptoms analyzed, care level recommended
5. **Scheduling**: If appointment needed, MCP server books slot
6. **Output**: Results translated back to patient's language

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Agent Framework | Google ADK | Multi-agent orchestration |
| Protocol | MCP | Tool/server integration |
| LLM | Gemini 2.5 Flash | Reasoning and generation |
| Security | Fernet (AES-128) | Encryption |
| Hashing | SHA-256 | Anonymization |
| Deployment | Docker + Cloud Run | Scalable hosting |
