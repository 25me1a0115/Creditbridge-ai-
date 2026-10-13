import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="CreditBridge AI",
    page_icon="💳",
    layout="wide",
)

st.title("💳 CreditBridge AI")
st.subheader("MSME Financial Readiness Assistant")
st.caption(
    "Prototype only: results are educational estimates, not an official credit score, "
    "loan approval, or financial advice."
)

with st.sidebar:
    st.header("Business details")
    business_name = st.text_input("Business name", value="Sample MSME")
    business_type = st.selectbox(
        "Business type",
        ["Retail", "Manufacturing", "Services", "Food business", "Other"],
    )
    monthly_revenue = st.number_input(
        "Average monthly revenue (₹)", min_value=0, value=300000, step=10000
    )
    monthly_expenses = st.number_input(
        "Average monthly operating expenses (₹)",
        min_value=0,
        value=210000,
        step=10000,
    )
    existing_emi = st.number_input(
        "Total existing monthly loan repayments (₹)",
        min_value=0,
        value=15000,
        step=1000,
    )
    loan_amount = st.number_input(
        "New loan amount being considered (₹)",
        min_value=0,
        value=300000,
        step=10000,
    )
    annual_interest = st.number_input(
        "Illustrative annual interest rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=12.0,
        step=0.5,
    )
    tenure_months = st.number_input(
        "Loan tenure (months)", min_value=1, max_value=120, value=36, step=1
    )

monthly_profit = monthly_revenue - monthly_expenses
profit_margin = (
    (monthly_profit / monthly_revenue) * 100 if monthly_revenue > 0 else 0.0
)

monthly_rate = annual_interest / 100 / 12
if loan_amount == 0:
    proposed_emi = 0.0
elif monthly_rate == 0:
    proposed_emi = loan_amount / tenure_months
else:
    proposed_emi = (
        loan_amount
        * monthly_rate
        * (1 + monthly_rate) ** tenure_months
        / ((1 + monthly_rate) ** tenure_months - 1)
    )

total_monthly_emi = existing_emi + proposed_emi
surplus_after_emi = monthly_profit - total_monthly_emi
repayment_burden = (
    (total_monthly_emi / monthly_revenue) * 100
    if monthly_revenue > 0
    else 0.0
)

# Transparent, illustrative rule-based indicator—not a credit score.
score = 0
if monthly_revenue > 0:
    score += 25
if monthly_profit > 0:
    score += 25
if profit_margin >= 10:
    score += 20
elif profit_margin > 0:
    score += 10
if repayment_burden <= 20:
    score += 30
elif repayment_burden <= 35:
    score += 20
elif repayment_burden <= 50:
    score += 10

if score >= 75:
    readiness_label = "Stronger indicators"
elif score >= 50:
    readiness_label = "Some areas to improve"
else:
    readiness_label = "Review finances carefully"

st.markdown(f"### Financial snapshot: {business_name}")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Monthly profit", f"₹{monthly_profit:,.0f}")
col2.metric("Profit margin", f"{profit_margin:.1f}%")
col3.metric("Estimated new EMI", f"₹{proposed_emi:,.0f}")
col4.metric("Illustrative readiness", f"{score}/100")

st.info(
    f"**Readiness interpretation:** {readiness_label}. "
    "This is a transparent demonstration indicator based only on the inputs above; "
    "it is not a lender's score or a prediction of loan approval."
)

left, right = st.columns(2)

with left:
    st.subheader("Monthly income and expenses")
    chart_data = pd.DataFrame(
        {
            "Category": ["Revenue", "Operating expenses", "Profit before loan EMIs"],
            "Amount (₹)": [monthly_revenue, monthly_expenses, monthly_profit],
        }
    )
    fig = px.bar(
        chart_data,
        x="Category",
        y="Amount (₹)",
        title="Illustrative monthly figures",
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Repayment picture")
    repayment_data = pd.DataFrame(
        {
            "Category": ["Existing EMIs", "Proposed EMI", "Surplus after EMIs"],
            "Amount (₹)": [
                existing_emi,
                proposed_emi,
                max(surplus_after_emi, 0),
            ],
        }
    )
    fig2 = px.bar(
        repayment_data,
        x="Category",
        y="Amount (₹)",
        title="Monthly repayment and surplus",
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Personalised improvement suggestions")
recommendations = []

if monthly_revenue <= 0:
    recommendations.append(
        "Enter reliable monthly revenue figures before interpreting the report."
    )
if monthly_profit <= 0:
    recommendations.append(
        "Current operating expenses are at or above revenue. Review costs and pricing "
        "before taking on additional repayments."
    )
elif profit_margin < 10:
    recommendations.append(
        "Your profit margin is below 10% in this illustrative assessment. Review "
        "avoidable costs, pricing and product-level profitability."
    )
else:
    recommendations.append(
        "Your entered figures show a positive operating margin. Keep consistent "
        "sales, expense and bank records to document this trend."
    )

if repayment_burden > 35:
    recommendations.append(
        "Estimated total monthly loan repayments are high relative to revenue. "
        "Compare a smaller loan amount or longer tenure, and check affordability carefully."
    )
else:
    recommendations.append(
        "Compare total repayments against actual monthly cash flow, including seasonal "
        "slowdowns and unexpected expenses."
    )

recommendations.append(
    "Prepare recent bank statements, sales records, expense records, existing-loan "
    "details and the documents required by your chosen lender."
)
recommendations.append(
    "Before applying, confirm eligibility, interest rate, fees, collateral rules and "
    "document requirements directly with the lender."
)

for item in recommendations:
    st.write(f"• {item}")

report = pd.DataFrame(
    [
        ["Business name", business_name],
        ["Business type", business_type],
        ["Monthly revenue (₹)", monthly_revenue],
        ["Monthly operating expenses (₹)", monthly_expenses],
        ["Monthly profit before loan EMIs (₹)", monthly_profit],
        ["Profit margin (%)", round(profit_margin, 2)],
        ["Existing monthly EMIs (₹)", existing_emi],
        ["Estimated proposed EMI (₹)", round(proposed_emi, 2)],
        ["Total monthly EMIs (₹)", round(total_monthly_emi, 2)],
        ["Surplus after EMIs (₹)", round(surplus_after_emi, 2)],
        ["Repayment burden as % of revenue", round(repayment_burden, 2)],
        ["Illustrative readiness indicator (out of 100)", score],
        ["Interpretation", readiness_label],
    ],
    columns=["Metric", "Value"],
)

st.subheader("Download your report")
st.download_button(
    "Download financial report (CSV)",
    data=report.to_csv(index=False).encode("utf-8"),
    file_name="creditbridge_financial_report.csv",
    mime="text/csv",
)

with st.expander("How is the readiness indicator calculated?"):
    st.write(
        "This prototype awards points for entering revenue, having positive profit, "
        "profit margin and estimated repayment burden. The weights are hand-designed "
        "for demonstration, not learned from lending outcomes and not validated against "
        "real borrowers. Do not use it for real lending decisions."
    )

st.caption(
    "Privacy note: this starter app does not require bank login, PAN, Aadhaar, account "
    "numbers or credit-bureau credentials. Use fictional data for demonstrations."
)
