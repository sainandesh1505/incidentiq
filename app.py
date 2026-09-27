import os
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()
st.set_page_config(page_title="IncidentIQ", page_icon="🚨", layout="wide")
st.title("🚨 IncidentIQ")
st.caption("AI Incident Response Agent — learn from previous incidents with Hindsight")

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "incidentiq")

if not API_KEY:
    st.error("HINDSIGHT_API_KEY is missing. Add it to your .env file.")
    st.stop()

client = Hindsight(base_url=BASE_URL, api_key=API_KEY)

try:
    client.create_bank(
        bank_id=BANK_ID,
        name="IncidentIQ",
        mission="Remember production incidents, root causes, successful resolutions, runbooks, and post-mortems so future incidents can be resolved faster."
    )
except Exception:
    pass

DEMO_INCIDENTS = [
    {
        "id": "INC-101", "service": "Payment API", "severity": "SEV-1",
        "symptoms": "Payment API returned HTTP 503 errors and checkout requests failed.",
        "root_cause": "The database connection pool was exhausted during a traffic spike.",
        "resolution": "Increased the database connection pool limit, restarted affected API instances, and monitored connection usage.",
        "runbook": "payment-api-db-connections",
        "postmortem": "Traffic increased faster than the configured database connection capacity."
    },
    {
        "id": "INC-102", "service": "User Authentication", "severity": "SEV-2",
        "symptoms": "Users intermittently received HTTP 504 responses during login.",
        "root_cause": "Authentication requests timed out because the identity-provider connection pool was saturated.",
        "resolution": "Raised connection limits, recycled stale connections, and added monitoring for pool saturation.",
        "runbook": "auth-provider-timeouts",
        "postmortem": "Connection saturation was not visible in the primary authentication dashboard."
    },
    {
        "id": "INC-103", "service": "Order Service", "severity": "SEV-1",
        "symptoms": "Order creation latency increased sharply and requests began failing.",
        "root_cause": "A slow database query occupied worker threads and the service queue grew.",
        "resolution": "Rolled back the query change, restarted overloaded workers, and added a database query latency alert.",
        "runbook": "order-db-latency",
        "postmortem": "The deployment introduced a query regression without a latency guardrail."
    },
]

def format_incident(x):
    return f"""Production incident {x['id']}
Service: {x['service']}
Severity: {x['severity']}
Symptoms: {x['symptoms']}
Root cause: {x['root_cause']}
Resolution: {x['resolution']}
Runbook: {x['runbook']}
Post-mortem: {x['postmortem']}"""

with st.sidebar:
    st.header("Demo setup")
    if st.button("🧠 Seed historical incidents", use_container_width=True):
        bar = st.progress(0)
        for i, incident in enumerate(DEMO_INCIDENTS, 1):
            client.retain(bank_id=BANK_ID, content=format_incident(incident))
            bar.progress(i / len(DEMO_INCIDENTS))
        st.success("Historical incidents sent to Hindsight.")
        st.caption("Wait a few seconds for memory processing before recalling.")

    st.divider()
    st.markdown("### Hindsight flow")
    st.write("**Retain → Recall → Reflect**")

tab1, tab2 = st.tabs(["🚨 New Incident", "📚 Example History"])

with tab1:
    st.subheader("Investigate a new production incident")
    new_incident = st.text_area(
        "Incident description",
        value="Payment API is returning 503 errors during checkout. Customers cannot complete payments.",
        height=130
    )

    if st.button("🔎 Find similar incidents", type="primary", use_container_width=True):
        if new_incident.strip():
            try:
                result = client.recall(
                    bank_id=BANK_ID,
                    query=f"Find previous production incidents similar to this incident. Focus on symptoms, root causes, resolutions, and runbooks. New incident: {new_incident}",
                    budget="mid"
                )
                st.session_state["recall_result"] = result
            except Exception as e:
                st.error(f"Recall failed: {e}")

    result = st.session_state.get("recall_result")
    if result:
        st.markdown("### 🔍 Relevant historical experience")
        memories = getattr(result, "results", [])
        if not memories:
            st.info("No relevant memories found. Seed the demo incidents and wait a few seconds.")
        for memory in memories[:5]:
            st.info(getattr(memory, "text", str(memory)))

    if st.button("🤖 Generate response plan", use_container_width=True):
        if new_incident.strip():
            try:
                response = client.reflect(
                    bank_id=BANK_ID,
                    query=f"""You are IncidentIQ, an incident response assistant.
Analyze this new production incident using remembered historical incidents.
Return: 1. Most relevant historical incident(s), 2. likely root cause,
3. investigation steps, 4. previously successful resolution steps,
5. relevant runbook(s), 6. a caution about what must be verified before changes.
New incident: {new_incident}""",
                    budget="mid"
                )
                st.session_state["reflect_result"] = response
            except Exception as e:
                st.error(f"Reflect failed: {e}")

    response = st.session_state.get("reflect_result")
    if response:
        st.markdown("### 🧠 Memory-aware response")
        st.write(getattr(response, "text", str(response)))

with tab2:
    st.subheader("Synthetic incident history used for the demo")
    for incident in DEMO_INCIDENTS:
        with st.expander(f"{incident['id']} — {incident['service']} — {incident['severity']}"):
            st.write(f"**Symptoms:** {incident['symptoms']}")
            st.write(f"**Root cause:** {incident['root_cause']}")
            st.write(f"**Resolution:** {incident['resolution']}")
            st.write(f"**Runbook:** `{incident['runbook']}`")
            st.write(f"**Post-mortem:** {incident['postmortem']}")

st.divider()
st.caption("IncidentIQ is a demonstration system. It does not autonomously execute production changes.")
