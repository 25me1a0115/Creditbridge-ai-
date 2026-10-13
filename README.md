# Creditbridge-ai-
business_name = st.text_input("Business Name")

monthly_revenue = st.number_input(
    "Monthly Revenue (₹)",
    min_value=0.0,
    value=300000.0,
    step=1000.0
)
