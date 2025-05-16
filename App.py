import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime


# Streamlit page configuration
st.set_page_config(page_title="Real-Time Health Watch", page_icon="⚕️", layout="wide")


# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY not found in .env file. Please add it and restart the app.")
    st.stop()
client = Groq(api_key=groq_api_key)

# Enhanced Mock Health Alerts with more variety and Telangana focus
mock_health_alerts = {
    "Telangana": [
        {
            "alert_id": "TG-20250516-HF01",
            "alert_type": "Hand, Foot, and Mouth Disease Advisory",
            "date": "2025-05-16",
            "details": "Several cases of Hand, Foot, and Mouth Disease reported in schools across Hyderabad. Parents and schools advised to monitor for symptoms.",
            "severity": "Medium",
            "affected_areas": ["Hyderabad"]
        },
        {
            "alert_id": "TG-20250515-VW02",
            "alert_type": "Seasonal Virus Warning",
            "date": "2025-05-15",
            "details": "Increase in common cold and flu cases reported statewide. Take necessary precautions and consult a doctor if symptoms worsen.",
            "severity": "Low",
            "affected_areas": ["Telangana"]
        },
        {
            "alert_id": "TG-20250514-WA03",
            "alert_type": "Waterborne Disease Alert",
            "date": "2025-05-14",
            "details": "Reports of potential water contamination in certain rural pockets of Nalgonda district. Residents advised to drink boiled or treated water.",
            "severity": "Medium",
            "affected_areas": ["Nalgonda (Rural)"]
        },
        {
            "alert_id": "TG-20250513-VC01",
            "alert_type": "COVID-19 Booster Drive",
            "date": "2025-05-13",
            "details": "Special COVID-19 booster vaccination camps being organized in urban centers of Telangana this week. Check local health centers for schedules.",
            "severity": "Low",
            "affected_areas": ["Hyderabad", "Warangal", "Karimnagar"]
        },
        {
            "alert_id": "TG-20250512-HT01",
            "alert_type": "Heatstroke Advisory",
            "date": "2025-05-12",
            "details": "High temperatures expected across Telangana for the next few days. Avoid strenuous outdoor activities during peak hours.",
            "severity": "High",
            "affected_areas": ["Telangana"]
        }
    ],
    "Andhra Pradesh": [
        {
            "alert_id": "AP-20250516-MV01",
            "alert_type": "Measles Vaccination Campaign",
            "date": "2025-05-16",
            "details": "Intensified measles vaccination campaign underway in several districts of Andhra Pradesh. Parents urged to get their children vaccinated.",
            "severity": "Medium",
            "affected_areas": ["Vijayawada", "Visakhapatnam", "Guntur"]
        }
    ],
    "Karnataka": [
        {
            "alert_id": "KA-20250516-AQ01",
            "alert_type": "Air Quality Alert",
            "date": "2025-05-16",
            "details": "Poor air quality reported in parts of Bengaluru due to increased pollution levels. Residents with respiratory issues advised to take precautions.",
            "severity": "Medium",
            "affected_areas": ["Bengaluru (Specific Areas)"]
        }
    ]
}

# Helper function for safe Groq API calls
def safe_groq_call(messages, model="Llama3-8b-8192"):
    try:
        response = client.chat.completions.create(messages=messages, model=model)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: Could not fetch response from Grok API. {str(e)}"

# Function to process alerts with Grok
def process_alert_with_grok(alert_type, details, region):
    # Explain the alert with regional context
    explain_prompt = f"Explain this public health alert in simple terms for people in {region}, India: '{alert_type}' - '{details}'"
    explanation = safe_groq_call([{"role": "user", "content": explain_prompt}])

    # Provide precautionary advice tailored to the region
    advice_prompt = f"Provide specific and practical precautionary advice for people in {region}, India, regarding this health alert: '{alert_type}' - '{details}'"
    advice = safe_groq_call([{"role": "user", "content": advice_prompt}])

    return explanation, advice

# Custom CSS for a more engaging look
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f4f8;
        color: #333;
    }
    .container {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1 {
        color: #007bff;
        text-align: center;
        margin-bottom: 30px;
    }
    h3 {
        color: #28a745;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .alert-box {
        border: 1px solid #ffc107;
        background-color: #fff3cd;
        color: #85640a;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .explanation-box {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .advice-box {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .note {
        font-size: 0.8em;
        color: #777;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚕️ Real-Time Public Health Watch for India")

with st.container():
    st.markdown("### Select Your Region")
    regions = sorted(list(mock_health_alerts.keys()))
    region = st.selectbox("Choose a region:", regions)

    if st.button("Get Latest Health Information"):
        if region in mock_health_alerts and mock_health_alerts[region]:
            st.markdown(f"### <span style='color:#28a745;'>Current Health Updates for {region}</span>", unsafe_allow_html=True)
            for alert_data in mock_health_alerts[region]:
                with st.container():
                    st.markdown(f"<div class='alert-box'>**Alert:** {alert_data['alert_type']} ({alert_data['date']})</div>", unsafe_allow_html=True)
                    st.write(f"**Details:** {alert_data['details']}")
                    if "affected_areas" in alert_data and alert_data["affected_areas"]:
                        st.write(f"*Affected Areas*: {', '.join(alert_data['affected_areas'])}")

                    explanation, advice = process_alert_with_grok(alert_data['alert_type'], alert_data['details'], region)

                    st.markdown("<h4 style='color:#17a2b8;'>Explanation</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div class='explanation-box'>{explanation}</div>", unsafe_allow_html=True)

                    st.markdown("<h4 style='color:#28a745;'>Precautionary Advice</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div class='advice-box'>{advice}</div>", unsafe_allow_html=True)

                    st.markdown("---")
        else:
            st.info(f"No current health alerts found for {region}.")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='note'>**Note:** This application uses mock data for demonstration purposes. For real-time and comprehensive health alerts, integration with official health APIs (e.g., WHO, NCDC India) would be necessary.</p>", unsafe_allow_html=True)
st.markdown("<p class='note'>**Voice Output:** A text-to-speech feature is available locally but disabled in this cloud deployment due to environment limitations.</p>", unsafe_allow_html=True)
st.markdown("<p class='note'>Developed with Streamlit and Groq's LLaMA 3.</p>", unsafe_allow_html=True)

# --- Unique Extra Features ---
st.sidebar.title("⚙️ Additional Features")

# Severity Filter
st.sidebar.subheader("Filter by Severity")
selected_severities = st.sidebar.multiselect("Select alert severities:", ["Low", "Medium", "High"], default=["Medium", "High"])

# Date Filter
st.sidebar.subheader("Filter by Date")
today = datetime.now().date()
start_date = st.sidebar.date_input("Show alerts from:", today.replace(day=1))
end_date = st.sidebar.date_input("Show alerts until:", today)

filtered_alerts = {}
for reg, alerts in mock_health_alerts.items():
    filtered_alerts[reg] = [
        a for a in alerts
        if a['severity'] in selected_severities and
        datetime.strptime(a['date'], '%Y-%m-%d').date() >= start_date and
        datetime.strptime(a['date'], '%Y-%m-%d').date() <= end_date
    ]

if st.sidebar.checkbox("Show Filtered Alerts"):
    st.markdown("### <span style='color:#ff6f61;'>Filtered Health Updates</span>", unsafe_allow_html=True)
    if region in filtered_alerts and filtered_alerts[region]:
        for alert_data in filtered_alerts[region]:
            with st.container():
                st.markdown(f"<div class='alert-box' style='border-color:#ff6f61; background-color:#ffe0b2; color:#d84315;'>**Alert:** {alert_data['alert_type']} ({alert_data['date']}) - Severity: {alert_data['severity']}</div>", unsafe_allow_html=True)
                st.write(f"**Details:** {alert_data['details']}")
                if "affected_areas" in alert_data and alert_data["affected_areas"]:
                    st.write(f"*Affected Areas*: {', '.join(alert_data['affected_areas'])}")
                explanation, advice = process_alert_with_grok(alert_data['alert_type'], alert_data['details'], region)
                st.markdown("<h4 style='color:#ff9800;'>Explanation</h4>", unsafe_allow_html=True)
                st.markdown(f"<div class='explanation-box'>{explanation}</div>", unsafe_allow_html=True)
                st.markdown("<h4 style='color:#ffc107;'>Precautionary Advice</h4>", unsafe_allow_html=True)
                st.markdown(f"<div class='advice-box' style='background-color:#fff8e1; color:#795548;'>{advice}</div>", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info(f"No filtered alerts found for {region} based on your criteria.")

# Alert History
if 'alert_history' not in st.session_state:
    st.session_state['alert_history'] = []

if st.button("Log Current Alerts"):
    if region in mock_health_alerts and mock_health_alerts[region]:
        for alert in mock_health_alerts[region]:
            st.session_state['alert_history'].append({
                'region': region,
                'type': alert['alert_type'],
                'details': alert['details'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        st.sidebar.success("Current alerts logged in history!")
    else:
        st.sidebar.info("No alerts to log for the current region.")

if st.sidebar.checkbox("Show Alert History"):
    st.sidebar.subheader("Alert History")
    if st.session_state['alert_history']:
        for log in reversed(st.session_state['alert_history']):
            st.sidebar.write(f"**{log['type']}** ({log['region']}) - {log['timestamp']}")
            st.sidebar.write(f"*Details*: {log['details'][:50]}...")
            st.sidebar.markdown("---")
    else:
        st.sidebar.info("No alerts in history yet.")
