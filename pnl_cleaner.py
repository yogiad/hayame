import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math # For math.ceil

# (Rest of your calculate_cleaner_needs function remains the same)
def calculate_cleaner_needs(job_revenue, cleaner_pay, transport_cost, supplies_cost,
                            hostel_cost_per_month, jobs_per_cleaner_per_day,
                            working_days_per_month, target_monthly_profit):
    """
    Calculates the number of cleaners needed to achieve a target monthly profit.
    Returns calculated values and potential error message.
    """
    # 1. Profit Per Job
    profit_per_job = job_revenue - cleaner_pay - transport_cost - supplies_cost

    # 2. Jobs Per Cleaner Per Month
    jobs_per_cleaner_per_month = jobs_per_cleaner_per_day * working_days_per_month

    # 3. Monthly Profit Per Cleaner (Before Hostel Cost)
    gross_profit_per_cleaner_per_month = profit_per_job * jobs_per_cleaner_per_month

    # 4. Monthly Profit Per Cleaner (After Hostel Cost)
    net_profit_per_cleaner_per_month = gross_profit_per_cleaner_per_month - hostel_cost_per_month

    # 5. Number of Cleaners Needed
    num_cleaners_needed = 0
    error_message = None

    if net_profit_per_cleaner_per_month <= 0:
        error_message = "Net profit per cleaner is zero or negative. Cannot achieve target profit with current inputs."
    else:
        num_cleaners_needed_raw = target_monthly_profit / net_profit_per_cleaner_per_month
        num_cleaners_needed = math.ceil(num_cleaners_needed_raw)

    return (profit_per_job, jobs_per_cleaner_per_month, gross_profit_per_cleaner_per_month,
            net_profit_per_cleaner_per_month, num_cleaners_needed, error_message)


st.set_page_config(layout="wide", page_title="Cleaner Staffing & Profitability Dashboard 🧹📈")

st.title("Cleaner Staffing & Profitability Dashboard 🧹📈")
st.write("Understand your operational costs and determine the number of cleaners needed to hit your monthly profit goals.")

st.sidebar.header("1. Job and Cost Inputs")

# Sidebar for inputs
with st.sidebar:
    st.subheader("Revenue and Direct Costs (per job)")
    job_revenue = st.number_input("Job Revenue (RM/job)", min_value=0.0, value=100.0, step=10.0, format="%.2f",
                                  help="Your charge per 4-hour job.")
    cleaner_pay = st.number_input("Cleaner Pay (RM/job)", min_value=0.0, value=35.0, step=5.0, format="%.2f",
                                  help="What you pay each cleaner/job.")
    transport_cost = st.number_input("Transport Cost (RM/job)", min_value=0.0, value=17.0, step=1.0, format="%.2f",
                                     help="Driver + petrol or allowance.")
    supplies_cost = st.number_input("Supplies Cost (RM/job)", min_value=0.0, value=3.0, step=1.0, format="%.2f",
                                    help="Cleaning materials.")

    st.subheader("Operational and Target Inputs")
    hostel_cost_per_month = st.number_input("Hostel Cost (RM/month/cleaner)", min_value=0.0, value=300.0, step=10.0, format="%.2f",
                                           help="Cost per cleaner for accommodation.")
    jobs_per_cleaner_per_day = st.number_input("Jobs per Cleaner/Day", min_value=1, value=2, step=1,
                                                help="How many jobs a cleaner can do daily.")
    working_days_per_month = st.number_input("Working Days per Month", min_value=1, value=26, step=1,
                                              help="Average working days per month.")
    target_monthly_profit = st.number_input("Target Monthly Profit (RM)", min_value=0.0, value=30000.0, step=1000.0, format="%.2f",
                                            help="Your desired monthly profit goal.")

st.markdown("---")
st.header("2. Calculation Results")

# Perform calculation
(profit_per_job, jobs_per_cleaner_per_month, gross_profit_per_cleaner_per_month,
 net_profit_per_cleaner_per_month, num_cleaners_needed, error_message) = calculate_cleaner_needs(
    job_revenue, cleaner_pay, transport_cost, supplies_cost,
    hostel_cost_per_month, jobs_per_cleaner_per_day,
    working_days_per_month, target_monthly_profit
)

# Display main result
if error_message:
    st.error(error_message)
    st.subheader("Adjust your inputs to achieve a positive net profit per cleaner.")
else:
    st.success(f"To achieve your target monthly profit of **RM {target_monthly_profit:,.2f}**, you'll need **{num_cleaners_needed} cleaners**.")

st.markdown("---")
st.header("3. Financial Insights & Visualizations")

# Check if calculations are valid before displaying charts
if error_message is None:
    col_kpi_1, col_kpi_2, col_kpi_3 = st.columns(3)

    with col_kpi_1:
        st.metric(label="Profit Per Job", value=f"RM {profit_per_job:,.2f}")
    with col_kpi_2:
        st.metric(label="Net Profit Per Cleaner/Month", value=f"RM {net_profit_per_cleaner_per_month:,.2f}")
    with col_kpi_3:
        total_monthly_revenue_needed = (num_cleaners_needed * job_revenue * jobs_per_cleaner_per_month)
        st.metric(label="Estimated Total Monthly Revenue", value=f"RM {total_monthly_revenue_needed:,.2f}")


    st.markdown("---")
    st.subheader("Cost Breakdown Per Job")

    # Data for Cost Breakdown Pie Chart
    cost_data = {
        'Category': ['Cleaner Pay', 'Transport Cost', 'Supplies Cost', 'Profit (per job)'],
        'Amount': [cleaner_pay, transport_cost, supplies_cost, profit_per_job]
    }
    df_costs = pd.DataFrame(cost_data)

    fig_pie = px.pie(df_costs, values='Amount', names='Category',
                     title='Breakdown of Each RM100 Revenue Per Job',
                     hole=0.4, # Makes it a donut chart
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pie.update_traces(textinfo='percent+label', pull=[0, 0, 0, 0.05]) # Pull out profit slightly
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("Projected Monthly Financials (Based on Target)")

    # Data for Monthly Financials Stacked Bar Chart
    total_cleaner_pay_monthly = num_cleaners_needed * cleaner_pay * jobs_per_cleaner_per_month
    total_transport_cost_monthly = num_cleaners_needed * transport_cost * jobs_per_cleaner_per_month
    total_supplies_cost_monthly = num_cleaners_needed * supplies_cost * jobs_per_cleaner_per_month
    total_hostel_cost_monthly = num_cleaners_needed * hostel_cost_per_month

    monthly_financials_data = {
        'Financial Item': ['Cleaner Pay', 'Transport Cost', 'Supplies Cost', 'Hostel Cost', 'Target Profit'],
        'Amount': [total_cleaner_pay_monthly, total_transport_cost_monthly, total_supplies_cost_monthly,
                   total_hostel_cost_monthly, target_monthly_profit],
        # Add a common 'Category' column for the x-axis to ensure uniform length
        'Category': ['Monthly Overview'] * 5
    }
    df_monthly_financials = pd.DataFrame(monthly_financials_data)

    # REVISED px.bar call:
    fig_stacked_bar_px = px.bar(df_monthly_financials, x='Category', y='Amount',
                                color='Financial Item', # Each item gets a different color
                                title='Projected Monthly Financials Breakdown',
                                labels={'Amount':'Amount (RM)', 'Category':''}, # Label 'Category' as empty string
                                color_discrete_map={'Cleaner Pay': 'lightblue', 'Transport Cost': 'lightcoral',
                                                    'Supplies Cost': 'lightgreen', 'Hostel Cost': 'lightsalmon',
                                                    'Target Profit': 'lightseagreen'},
                                height=400) # Added height for better visualization

    # Add a line indicating total revenue
    total_monthly_revenue = df_monthly_financials['Amount'].sum() # Sum all components

    fig_stacked_bar_px.add_hline(y=total_monthly_revenue, line_dash="dot", line_color="navy",
                                 annotation_text=f"Total Revenue: RM {total_monthly_revenue:,.2f}",
                                 annotation_position="top left")
    fig_stacked_bar_px.update_layout(showlegend=True, barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':['Monthly Overview']}) # Ensure x-axis order
    st.plotly_chart(fig_stacked_bar_px, use_container_width=True)


    st.markdown("---")
    st.subheader("Revenue Flow to Net Profit (Monthly Waterfall)")

    # Data for Waterfall Chart (using Plotly Graph Objects for fine control)
    data = [
        go.Waterfall(
            name = "Profit Breakdown",
            orientation = "v",
            measure = ["absolute", "relative", "relative", "relative", "relative", "total"],
            x = ["Total Monthly Revenue", "Cleaner Pay Cost", "Transport Cost", "Supplies Cost", "Hostel Cost", "Net Profit"],
            textposition = "outside",
            text = [f"{total_monthly_revenue:,.2f}", f"-{total_cleaner_pay_monthly:,.2f}", f"-{total_transport_cost_monthly:,.2f}",
                    f"-{total_supplies_cost_monthly:,.2f}", f"-{total_hostel_cost_monthly:,.2f}", f"{target_monthly_profit:,.2f}"],
            y = [total_monthly_revenue, -total_cleaner_pay_monthly, -total_transport_cost_monthly,
                 -total_supplies_cost_monthly, -total_hostel_cost_monthly, target_monthly_profit],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            increasing={"marker":{"color":"#2ca02c"}}, # Green for positive (Revenue/Profit)
            decreasing={"marker":{"color":"#d62728"}} # Red for negative (Costs)
        )
    ]

    fig_waterfall = go.Figure(data=data)

    fig_waterfall.update_layout(
        title="Revenue Flow to Net Profit (Monthly)",
        showlegend=False,
        yaxis_title="Amount (RM)",
        xaxis_title="Financial Measure"
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)
