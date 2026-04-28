import streamlit as st

st.set_page_config(page_title="Portfolio Health Analyzer", page_icon="📂", layout="centered")

def calculate_portfolio_health(total_portfolio_outstanding, par30, par90,
                               write_off_rate, recovery_rate, active_loans,
                               average_loan_size, branch_count=1):

    score = 100

    if par30 > 15:
        score -= 30
    elif par30 > 10:
        score -= 20
    elif par30 > 5:
        score -= 10

    if par90 > 10:
        score -= 25
    elif par90 > 5:
        score -= 15
    elif par90 > 2:
        score -= 8

    if write_off_rate > 5:
        score -= 20
    elif write_off_rate > 2:
        score -= 10

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
        interpretation = "Portfolio appears stable but may require closer monitoring in selected areas."
    elif score >= 40:
        category = "Weak Portfolio Health"
        interpretation = "Portfolio quality shows elevated risk and should be reviewed more closely."
    else:
        category = "High Portfolio Stress"
        interpretation = "Portfolio health appears weak and may require immediate risk and collections review."

    return {
        "portfolio_health_score": score,
        "category": category,
        "interpretation": interpretation
    }

st.title("Portfolio Health Analyzer")
st.write("Assess loan portfolio quality using PAR30, PAR90, write-off rate, and recovery indicators.")

with st.form("portfolio_health_form"):
    total_portfolio_outstanding = st.number_input("Total Portfolio Outstanding", min_value=0.0, step=1000.0)
    par30 = st.number_input("PAR30 (%)", min_value=0.0, step=0.1)
    par90 = st.number_input("PAR90 / NPL (%)", min_value=0.0, step=0.1)
    write_off_rate = st.number_input("Write-Off Rate (%)", min_value=0.0, step=0.1)
    recovery_rate = st.number_input("Recovery Rate (%)", min_value=0.0, step=0.1)
    active_loans = st.number_input("Number of Active Loans", min_value=1, step=1)
    average_loan_size = st.number_input("Average Loan Size", min_value=0.0, step=1000.0)
    branch_count = st.number_input("Number of Branches", min_value=1, step=1)
    submitted = st.form_submit_button("Analyze Portfolio")

if submitted:
    result = calculate_portfolio_health(
        total_portfolio_outstanding, par30, par90,
        write_off_rate, recovery_rate, active_loans,
        average_loan_size, branch_count
    )

    st.success("Analysis Complete")
    st.metric("Portfolio Health Score", f"{result['portfolio_health_score']}/100")
    st.metric("Category", result['category'])
    st.write(f"**Interpretation:** {result['interpretation']}")

    st.info("Indicative output only. For a tailored portfolio review, contact Quant Vision Labs.")
    st.markdown("[Request Consultation](https://yourwebsite.com/request-consultation)")
