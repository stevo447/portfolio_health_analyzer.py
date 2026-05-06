import streamlit as st

# -------------------------
# Page Config (MUST BE FIRST)
# -------------------------
st.set_page_config(
    page_title="Portfolio Health Analyzer | Quant Vision Labs",
    page_icon="📂",
    layout="centered"
)

# -------------------------
# Hide Streamlit Default UI
# -------------------------
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Premium Styling
# -------------------------
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 950px;
    }

    h1, h2, h3 {
        color: #0B1B4D;
    }

    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover {
        background-color: #1D4ED8;
    }

    .stMetric {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
    }

    .stForm {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Logo (Centered)
# -------------------------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", width=300)

# -------------------------
# Title
# -------------------------
st.title("📂 Portfolio Health Analyzer")
st.write(
    "Assess loan portfolio quality using PAR30, PAR90, write-off rate, and recovery indicators."
)

# -------------------------
# Function
# -------------------------
def calculate_portfolio_health(
    total_portfolio_outstanding, par30, par90,
    write_off_rate, recovery_rate, active_loans,
    average_loan_size, branch_count=1
):

    score = 100

    # PAR30 impact
    if par30 > 15:
        score -= 30
    elif par30 > 10:
        score -= 20
    elif par30 > 5:
        score -= 10

    # PAR90 impact
    if par90 > 10:
        score -= 25
    elif par90 > 5:
        score -= 15
    elif par90 > 2:
        score -= 8

    # Write-offs
    if write_off_rate > 5:
        score -= 20
    elif write_off_rate > 2:
        score -= 10

    # Recoveries
    if recovery_rate >= 60:
        score += 5
    elif recovery_rate < 30:
        score -= 10

    score = max(min(score, 100), 0)

    if score >= 80:
        category = "Strong Portfolio Health"
        interpretation = "Portfolio indicators appear relatively strong."
    elif score >= 60:
        category = "Moderate Portfolio Health"
        interpretation = "Portfolio is stable but needs monitoring."
    elif score >= 40:
        category = "Weak Portfolio Health"
        interpretation = "Portfolio quality shows elevated risk."
    else:
        category = "High Portfolio Stress"
        interpretation = "Portfolio requires urgent review."

    return {
        "portfolio_health_score": score,
        "category": category,
        "interpretation": interpretation
    }

# -------------------------
# Form
# -------------------------
with st.form("portfolio_health_form"):
    total_portfolio_outstanding = st.number_input("Total Portfolio Outstanding (₦)", min_value=0.0, step=1000.0)
    par30 = st.number_input("PAR30 (%)", min_value=0.0, step=0.1)
    par90 = st.number_input("PAR90 / NPL (%)", min_value=0.0, step=0.1)
    write_off_rate = st.number_input("Write-Off Rate (%)", min_value=0.0, step=0.1)
    recovery_rate = st.number_input("Recovery Rate (%)", min_value=0.0, step=0.1)
    active_loans = st.number_input("Number of Active Loans", min_value=1, step=1)
    average_loan_size = st.number_input("Average Loan Size (₦)", min_value=0.0, step=1000.0)
    branch_count = st.number_input("Number of Branches", min_value=1, step=1)

    submitted = st.form_submit_button("Analyze Portfolio")

# -------------------------
# Results
# -------------------------
if submitted:

    result = calculate_portfolio_health(
        total_portfolio_outstanding, par30, par90,
        write_off_rate, recovery_rate, active_loans,
        average_loan_size, branch_count
    )

    st.success("Analysis Complete")

    st.metric("Portfolio Health Score", f"{result['portfolio_health_score']}/100")
    st.metric("Category", result['category'])

    st.subheader("Interpretation")
    st.write(result['interpretation'])

    st.info("Indicative output only. For a tailored portfolio review, contact Quant Vision Labs.")

    st.markdown("### Need Expert Review?")
    st.markdown("[Request Consultation](https://quantvisionlabs.com/request-consultation)")