# IncidentIQ — AI Incident Response Agent

IncidentIQ is a demonstration incident-response assistant that uses Hindsight as a long-term memory layer for production incidents.

## Problem
Production incidents often repeat patterns. Useful resolution context can be buried in incident reports and post-mortems.

## Hindsight integration
- **Retain:** stores symptoms, root causes, resolutions, runbooks and post-mortems.
- **Recall:** searches historical incident memory for relevant incidents.
- **Reflect:** reasons over stored memories and produces a response plan.

## Demo
1. Put your Hindsight API key in `.env`.
2. Run `streamlit run app.py`.
3. Click **Seed historical incidents**.
4. Wait a few seconds.
5. Click **Find similar incidents**.
6. Click **Generate response plan**.
7. Capture screenshots.

## Safety
The example incidents are synthetic demonstration data. IncidentIQ only recommends investigation/remediation steps; it does not execute production changes.

## Team
SAI NANDESH
SAI SHARAN
HARI OM
VAISHNAVI
SONAL
