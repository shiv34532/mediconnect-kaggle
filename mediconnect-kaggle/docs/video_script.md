# 5-Minute Video Script

## MediConnect: AI Healthcare Access for Underserved Communities

---

### 0:00-0:30 | PROBLEM STATEMENT

**[Show: Rural clinic, long lines, language barriers]**

"Over 400 million people in underserved communities lack basic healthcare access. Language barriers, distance, and digital literacy gaps prevent millions from getting timely care. A patient in rural Guatemala with chest pain has no way to know if they need emergency care or can wait for a clinic appointment."

**[Show: Map with healthcare deserts highlighted]**

---

### 0:30-1:30 | ARCHITECTURE & WHY AGENTS

**[Show: Architecture diagram]**

"We built MediConnect, a multi-agent system using Google's Agent Development Kit. Why agents? Because healthcare requires specialized expertise—security, translation, triage, and scheduling—each handled by a dedicated agent."

**[Show: Agent boxes appearing]**

"The Orchestrator coordinates the pipeline: Security anonymizes patient data for HIPAA compliance, Translator handles 50+ languages, Triage analyzes symptoms, and Scheduler books appointments via MCP server."

**[Show: Data flow animation]**

---

### 1:30-3:00 | LIVE DEMO

**[Show: Kaggle notebook running]**

"Here's a real demo. A Spanish-speaking patient reports 'fiebre y dolor de cabeza'—fever and headache."

**[Show: Code executing]**

"First, the Security Agent anonymizes all PII, replacing names with secure hashes. Then the Translator detects Spanish and translates to English. The Triage Agent checks symptoms against our medical knowledge base—fever for 2 days recommends NON-URGENT care with primary care scheduling. The Scheduler Agent uses MCP to book a clinic appointment."

**[Show: Appointment confirmation]**

"The patient receives a confirmation in Spanish with their appointment details."

---

### 3:00-3:30 | SECURITY FEATURES

**[Show: Code with security functions]**

"Security is critical in healthcare. We implement SHA-256 anonymization, PII redaction with regex validation, Fernet encryption for data at rest, and comprehensive audit logging for HIPAA compliance."

**[Show: Before/after of anonymized data]**

"Real names become unrecoverable hashes. Phone numbers are redacted. Every access is logged."

---

### 3:30-4:30 | DEPLOYABILITY

**[Show: Terminal with commands]**

"MediConnect is built for real deployment. Our Dockerfile uses non-root users for security. The deploy script pushes to Google Cloud Run with auto-scaling."

**[Show: Cloud Run console]**

"One command: `bash deploy.sh` and the system is live. Health checks ensure reliability. The MCP server connects to real clinic management systems."

**[Show: curl to health endpoint]**

---

### 4:30-5:00 | IMPACT & CONCLUSION

**[Show: Potential users map]**

"This can help 400 million people access healthcare information in their language, get appropriate triage, and schedule appointments. It's open-source, extensible to any language or clinic system, and ready to deploy today."

**[Show: GitHub repo, call to action]**

"MediConnect: Agents for Good. Thank you."

---

## Technical Notes for Recording

- Use screen recording (OBS, Loom, or QuickTime)
- Record at 1080p minimum
- Speak clearly, pace yourself
- Show actual code execution, not static slides
- Include captions for accessibility
- Upload to YouTube as unlisted or public
