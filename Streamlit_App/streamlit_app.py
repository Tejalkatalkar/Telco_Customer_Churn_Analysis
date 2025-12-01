import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import psycopg2
from psycopg2.extras import RealDictCursor

import os

# PAGE CONFIG
st.set_page_config(
    page_title="ChurnAnalysis - Customer Retention Platform",
    layout="wide",
)

# CUSTOM CSS FOR STYLING
st.markdown("""
<style>

/* Remove Streamlit default padding */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 1rem !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    border-right: 1px solid #ddd;
}

/* Top navigation bar */
.top-bar {
    width: 100%;
    background-color: #0A244D;
    padding: 18px 30px;
    color: white;
    font-size: 22px;
    font-weight: 700;
    border-radius: 8px;
    margin-bottom: 20px;
}

.menu-links {
    float: right;
    font-size: 16px;
    margin-top: -28px;
}

.menu-links a {
    margin-left: 30px;
    text-decoration: none;
    color: #cde0ff;
}

.menu-links a:hover {
    color: #ffffff;
    text-decoration: underline;
}
            
/* Header blue gradient section */
.blue-box {
    background: linear-gradient(90deg, #0056D6, #0090FF);
    padding: 35px;
    color: white;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* White section box */
.section-box {
    background-color: #ffffff;
    padding: 20px 30px;
    border-radius: 10px;
    border: 1px solid #eee;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# TOP NAVIGATION BAR
st.markdown("""
<div class="top-bar">
    ChurnGuard
    <div class="menu-links">
        <a href="#">Home</a>
        <a href="#">Risk Analysis</a>
        <a href="#">Visual Dashboard</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# BLUE HEADER SECTION
st.markdown("""
<div class="blue-box">
    <h2 style="margin-bottom:5px;">Proactive Customer Retention Platform</h2>
    <p>Our AI-driven engine scores customers with high accuracy and adapts to your business needs.</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR NAVIGATION
st.sidebar.title("🗂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Risk Analysis", "Visual Dashboard", "Contact"])

# # HELPER FUNCTION
# def load_pickle(path):
#     if not os.path.exists(path):
#         st.error(f"❌ Missing file: {path}")
#         return None
#     return pickle.load(open(path, "rb"))

# # LOAD MODELS + SCALERS + ENCODERS
# log_model = load_pickle("models/logistic.pkl")
# rf_model = load_pickle("models/randomforest.pkl")
# scaler = load_pickle("models/scaler.pkl")

# encoders = {}
# if os.path.exists("encoders"):
#     for f in os.listdir("encoders"):
#         if f.endswith(".pkl"):
#             col = f.replace(".pkl", "")
#             encoders[col] = pickle.load(open(f"encoders/{f}", "rb"))
# else:
#     st.error("❌ Encoders folder missing")

def load_pickle(path):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"❌ Error loading {path}: {e}")
        return None

# -------- CORRECT PATHS FOR CODESPACES --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = os.path.join(BASE_DIR, "models")
ENCODERS_DIR = os.path.join(BASE_DIR, "encoders")

# LOAD MODELS
log_model = load_pickle(os.path.join(MODELS_DIR, "logistic.pkl"))
rf_model = load_pickle(os.path.join(MODELS_DIR, "randomforest.pkl"))
scaler   = load_pickle(os.path.join(MODELS_DIR, "scaler.pkl"))

# LOAD ENCODERS
encoders = {}

if os.path.exists(ENCODERS_DIR):
    for f in os.listdir(ENCODERS_DIR):
        if f.endswith(".pkl"):
            key = f.replace(".pkl", "")
            encoders[key] = load_pickle(os.path.join(ENCODERS_DIR, f))
else:
    st.error("❌ Encoders folder missing inside Streamlit_App/")

# HOME PAGE CONTENT
if page == "Home":

    st.markdown(
        """
        <style>
        .title {
            font-size: 40px;
            font-weight: 700;
            color: #4CAF50;
            text-align: center;
        }
        .subtitle {
            font-size: 22px;
            font-weight: 600;
            color: #333;
        }
        .section-title {
            font-size: 26px;
            font-weight: 700;
            margin-top: 20px;
            color: #1E88E5;
        }
        .content {
            font-size: 18px;
            line-height: 1.6;
            color: #444;
        }
        .highlight {
            background-color: #f0f9ff;
            padding: 10px;
            border-radius: 8px;
            border-left: 5px solid #2196F3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("📊 Customer Churn Prediction App")

    st.markdown("---")

    st.markdown('<div class="section-title">1. 📘 Introduction</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="content">
        Customer churn is a major challenge for telecom companies as it directly affects long-term revenue.  
        This project analyzes customer behavior patterns and predicts which customers are most likely to leave the service.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">2. What is Customer Churn?</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="content">
        <b>Customer Churn</b> refers to customers who discontinue or stop using your service.
        <br><br>
        <b>Types of Churn:</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="highlight">
        <ul>
            <li><b>Voluntary:</b> Customer leaves willingly due to poor service or better competitor offers.</li>
            <li><b>Involuntary:</b> Payment failures, service restrictions, or account closure.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-title">📐 Churn Rate Formula</div>
        <div class="highlight">
        <b>Churn Rate = (Customers Lost / Total Customers at Start) × 100</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

# INPUT FORM
if page == "Risk Analysis":
    st.title("📊 Churn Risk Analysis Dashboard")
    st.markdown(
        """
        <div class="subtitle">
        Predict if a customer is likely to churn using machine learning models.  
        Fill the form below to analyze customer churn risk instantly.
        </div>
        """,
        unsafe_allow_html=True,
    )


    with st.form("prediction_form"):

        st.subheader("👤 Customer Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
            Partner = st.selectbox("Partner", ["Yes", "No"])

        with col2:
            Dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.number_input("Tenure (months)", min_value=0, max_value=72)
            PhoneService = st.selectbox("Phone Service", ["Yes", "No"])

        with col3:
            MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
            InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

        st.write("---")
        st.subheader("🌐 Internet & Streaming Services")

        col4, col5, col6 = st.columns(3)

        with col4:
            OnlineSecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
            OnlineBackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])

        with col5:
            DeviceProtection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
            TechSupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])

        with col6:
            StreamingTV = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
            StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

        st.write("---")
        st.subheader("💵 Billing Information")

        col7, col8 = st.columns(2)

        with col7:
            PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
            PaymentMethod = st.selectbox(
                "Payment Method",
                ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
            )

        with col8:
            MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0)
            TotalCharges = st.number_input("Total Charges", min_value=0.0)

        submit = st.form_submit_button("🔍 Predict Churn", use_container_width=True)

# PREDICTION LOGIC & RESULTS
    if submit:

        input_data = {
            "gender": gender,
            "SeniorCitizen": SeniorCitizen,
            "Partner": Partner,
            "Dependents": Dependents,
            "tenure": tenure,
            "PhoneService": PhoneService,
            "MultipleLines": MultipleLines,
            "InternetService": InternetService,
            "OnlineSecurity": OnlineSecurity,
            "OnlineBackup": OnlineBackup,
            "DeviceProtection": DeviceProtection,
            "TechSupport": TechSupport,
            "StreamingTV": StreamingTV,
            "StreamingMovies": StreamingMovies,
            "Contract": Contract,
            "PaperlessBilling": PaperlessBilling,
            "PaymentMethod": PaymentMethod,
            "MonthlyCharges": MonthlyCharges,
            "TotalCharges": TotalCharges
        }

        df = pd.DataFrame([input_data])

        # Encoding
        for col in df.columns:
            if col in encoders:
                df[col] = encoders[col].transform(df[col])

        # Scaling
        df_scaled = scaler.transform(df) if scaler else df

        # Predictions
        rf_pred = rf_model.predict(df_scaled)[0]

        def label(pred):
            return "🛑 Churn" if pred == 1 else "🟢 No Churn"

        st.write("---")
        st.subheader("🎯 Prediction Results")

        st.success(f"**Random Forest:** {label(rf_pred)}")

        st.success("Prediction Completed ✔")
        
# VISUAL DASHBOARD PAGE
if page == "Visual Dashboard":
    st.title("📊 Churn Visual Dashboard")

    # Load CSV
    try:
        df = pd.read_csv(
            r"https://github.com/Tejalkatalkar/Telco_Customer_Churn_Analysis/blob/main/Streamlit_App/CSV/Cleaned_Cust_data.csv"
        )
        st.success("CSV Loaded Successfully!")
    except:
        st.error("CSV file path incorrect. Please check the file path.")
        st.stop()

    st.markdown("---")


# FUNCTION TO CREATE OUTLINE BOX
    def card_container():
        return st.container(border=True)


# Create compact columns
    col1, col2 = st.columns(2)

# LEFT — PIE CHART 

    with col1:
        with card_container():
            st.subheader("🟦 Churn Distribution")

            churn_counts = df["Churn"].value_counts()

            fig1 = px.pie(
                values=churn_counts.values,
                names=churn_counts.index,
                hole=0.45,
                color=churn_counts.index,
                color_discrete_map={"Yes": "red", "No": "blue"},
            )

            fig1.update_layout(
                title="",
                height=260,
                margin=dict(l=5, r=5, t=20, b=20)
            )

            st.plotly_chart(fig1, use_container_width=True)
# Conclusion
            st.markdown("**📌 Conclusion:** Majority customers did **not churn**, but churned customers are still significant.")


# RIGHT — BAR CHART 
    with col2:
        with card_container():
            st.subheader("📑 Churn by Contract")

            contract_churn = df.groupby(["Contract", "Churn"]).size().reset_index(name="Count")

            fig2 = px.bar(
                contract_churn,
                x="Contract",
                y="Count",
                color="Churn",
                barmode="group",
                color_discrete_map={"Yes": "red", "No": "blue"}
            )

            fig2.update_layout(
                title="",
                height=260,
                margin=dict(l=5, r=5, t=20, b=20)
            )

            st.plotly_chart(fig2, use_container_width=True)

# Conclusion
            st.markdown("**📌 Conclusion:** Month-to-month customers churn the most; long-term contracts reduce churn.")


    st.markdown("---")


# Next row of visuals
    col3, col4 = st.columns(2)

# LEFT — KDE PLOT 
    with col3:
        with card_container():
            st.subheader("💰 Monthly Charges")

            plt.figure(figsize=(8, 6.5))
            sns.kdeplot(data=df, x="MonthlyCharges", hue="Churn", fill=True)
            st.pyplot(plt)

# Conclusion
            st.markdown("**📌 Conclusion:** Higher monthly charges lead to a higher probability of churn.")

# RIGHT — HISTOGRAM
    with col4:
        with card_container():
            st.subheader("⏳ Tenure Distribution")

            fig4 = px.histogram(
                df,
                x="tenure",
                color="Churn",
                nbins=40,
                opacity=0.6,
            )

            fig4.update_layout(
                title="",
                height=260,
                margin=dict(l=5, r=5, t=20, b=20)
            )

            st.plotly_chart(fig4, use_container_width=True)
# Conclusion
            st.markdown("**📌 Conclusion:** New customers (0–12 months) churn more; long-tenure customers stay loyal.")


# CONTACT PAGE
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="contact",   # or "contact" if you create it
        user="postgres",       # your username
        password="admin",  # add your password
        port="5432"
    )

if page == "Contact":
    st.title("📞 Contact Us")

    st.markdown("Feel free to reach out for support or feedback!")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submit_contact = st.form_submit_button("Send Message")

    if submit_contact:
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO contact_messages (name, email, message)
                VALUES (%s, %s, %s)
            """, (name, email, message))

            conn.commit()
            cursor.close()
            conn.close()

            st.success("Your message has been sent successfully ✔")

        except Exception as e:
            st.error("❌ Failed to send message")
            st.error(str(e))



