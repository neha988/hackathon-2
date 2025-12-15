---
id: 001
title: Summarize Hackathon II spec
stage: general
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: nehak
command: Summarize file: Hackathon II - Todo Spec-Driven Development.md
labels: ["summary","spec"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - history/prompts/general/001-summarize-hackathon-ii.general.prompt.md
tests:
 - None
---

## Prompt

@"Hackathon II - Todo Spec-Driven Development.md" read this file and tell me in summarize and short what inside

## Response snapshot

The document is a hackathon specification ("Hackathon II") that defines a 5-phase spec-driven Todo app project. Key points:
- 5 phases: Phase I (in-memory Python CLI), Phase II (Full-stack Next.js + FastAPI + SQLModel + Neon DB), Phase III (AI chatbot using OpenAI ChatKit/Agents SDK + MCP tools), Phase IV (local Kubernetes with Minikube/Helm/kubectl-ai), Phase V (cloud deployment with Kafka/Dapr on DOKS).
- Includes requirements, deliverables, API specs, monorepo and CLAUDE.md guidelines, Dapr/Kafka architecture, submission rules, and bonus features.
- Primary deliverables: GitHub repo with /specs, CLAUDE.md, source for frontend/backend, README, demo video, and deployment instructions.

## Outcome

- ✅ Impact: PHR created; concise summary provided to the user.
- 🧪 Tests: None
- 📁 Files: history/prompts/general/001-summarize-hackathon-ii.general.prompt.md
- 🔁 Next prompts: Ask user if they want a per-phase detailed breakdown, implementation help, or extraction of deliverables.
- 🧠 Reflection: Completed short summary and logged PHR.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Provide a one-paragraph expanded summary or phase-by-phase bullets.
