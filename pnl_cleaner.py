import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

# --- Configuration for Streamlit Page ---
st.set_page_config(
    layout="wide",  # Use wide layout for more space
    page_title="Cleaner Staffing & Profitability Dashboard 🧹📈",
    page_icon="💸" # A nice emoji for the browser tab
)

# --- Custom CSS for better aesthetics ---
st.markdown("""
<style>
    /* Main app container styling */
    .stApp {
        background-color: #f0f2f6; /* Light gray background */
        color: #333333; /* Darker text */
    }

    /* Sidebar styling */
    .stSidebar {
        background-color: #e6e8eb; /* Slightly darker sidebar */
        border-right: 1px solid #d1d3d8;
    }

    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50; /* Dark blue/gray for headings */
    }

    /* Metric cards styling */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4CAF50; /* Green left border for emphasis */
    }
    [data-testid="stMetric"] label {
        color: #555555; /* Label color */
    }
    [data-testid="stMetric"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.5rem; /* Larger value font size */
        font-weight: bold;
        color: #1a5276; /* Blueish for values */
    }

    /* Success message styling */
    .stSuccess {
        background-color: #e6ffe6;
        color: #1a5276;
        border-radius: 8px;
        padding: 15px;
        border-left: 6px solid #4CAF50;
        font-size: 1.1rem;
    }

    /* Error message styling */
    .stError {
        background-color: #ffe6e6;
        color: #c0392b;
        border-radius: 8px;
        padding: 15px;
        border-left: 6px solid #e74c3c;
        font-size: 1.1rem;
    }

    /* Input widgets styling */
    .stNumberInput, .stTextInput {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 8px;
        border: 1px solid #cccccc;
    }
</style>
""", unsafe_allow_html=True)


# --- Functions ---
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
        error_message = "Net profit per cleaner is zero or negative. Adjust inputs to achieve a positive profit per cleaner."
    else:
        num_cleaners_needed_raw = target_monthly_profit / net_profit_per_cleaner_per_month
        num_cleaners_needed = math.ceil(num_cleaners_needed_raw)

    return (profit_per_job, jobs_per_cleaner_per_month, gross_profit_per_cleaner_per_month,
            net_profit_per_cleaner_per_month, num_cleaners_needed, error_message)

# --- App Title and Description ---
st.title("Cleaner Staffing & Profitability Dashboard 🧹📈")
st.write("Optimize your cleaning business! Input your costs and goals to determine the ideal number of cleaners.")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("1. Business Model Inputs 📊")
    st.markdown("Adjust these values to see their impact on your staffing needs and profitability.")

    with st.expander("💰 Revenue & Direct Costs (Per Job)", expanded=True):
        job_revenue = st.number_input("Job Revenue (RM/job)", min_value=0.0, value=100.0, step=5.0, format="%.2f",
                                      help="Your charge per 4-hour cleaning job.")
        cleaner_pay = st.number_input("Cleaner Pay (RM/job)", min_value=0.0, value=35.0, step=2.0, format="%.2f",
                                      help="What you pay each cleaner per job.")
        transport_cost = st.number_input("Transport Cost (RM/job)", min_value=0.0, value=17.0, step=1.0, format="%.2f",
                                         help="Cost for driver and petrol, or allowance per job.")
        supplies_cost = st.number_input("Supplies Cost (RM/job)", min_value=0.0, value=3.0, step=0.5, format="%.2f",
                                        help="Cost of cleaning materials per job.")

    with st.expander("🗓️ Operational & Target Inputs", expanded=True):
        hostel_cost_per_month = st.number_input("Hostel Cost (RM/month/cleaner)", min_value=0.0, value=300.0, step=10.0, format="%.2f",
                                               help="Monthly accommodation cost per cleaner.")
        jobs_per_cleaner_per_day = st.number_input("Jobs per Cleaner/Day", min_value=1, max_value=5, value=2, step=1,
                                                    help="How many jobs a single cleaner can realistically complete daily.")
        working_days_per_month = st.number_input("Working Days per Month", min_value=1, max_value=31, value=26, step=1,
                                                  help="Average number of working days in a month.")
        target_monthly_profit = st.number_input("Target Monthly Profit (RM)", min_value=0.0, value=30000.0, step=500.0, format="%.2f",
                                                help="Your desired profit goal for the month.")

# --- Calculation and Main Results ---
st.markdown("---")
st.header("2. Projected Staffing & Profit Summary 🚀")

# Perform calculation
(profit_per_job, jobs_per_cleaner_per_month, gross_profit_per_cleaner_per_month,
 net_profit_per_cleaner_per_month, num_cleaners_needed, error_message) = calculate_cleaner_needs(
    job_revenue, cleaner_pay, transport_cost, supplies_cost,
    hostel_cost_per_month, jobs_per_cleaner_per_day,
    working_days_per_month, target_monthly_profit
)

# Display main result and KPIs
if error_message:
    st.error(error_message)
    st.info("Consider reducing costs or increasing revenue per job to make your business model profitable.")
else:
    st.success(f"🎉 **Success!** To achieve your target monthly profit of **RM {target_monthly_profit:,.2f}**, you'll need approximately **{num_cleaners_needed} cleaners**.")

    st.markdown("#### Key Performance Indicators (KPIs)")
    # Adjusted to 5 columns for the new KPI
    col_kpi_1, col_kpi_2, col_kpi_3, col_kpi_4, col_kpi_5 = st.columns(5)

    with col_kpi_1:
        st.metric(label="💰 Profit Per Job", value=f"RM {profit_per_job:,.2f}")
    with col_kpi_2:
        st.metric(label="💼 Net Profit Per Cleaner/Month", value=f"RM {net_profit_per_cleaner_per_month:,.2f}")
    with col_kpi_3:
        st.metric(label="🗓️ Jobs Per Cleaner/Month", value=f"{jobs_per_cleaner_per_month} jobs")
    
    # Calculate Total Jobs Per Month
    total_jobs_per_month = num_cleaners_needed * jobs_per_cleaner_per_month
    with col_kpi_4: # Added this new column
        st.metric(label="📊 Total Jobs Per Month", value=f"{total_jobs_per_month:,.0f} jobs")

    with col_kpi_5: # This is now the 5th column
        total_monthly_revenue_needed = (num_cleaners_needed * job_revenue * jobs_per_cleaner_per_month)
        st.metric(label="💵 Estimated Total Monthly Revenue", value=f"RM {total_monthly_revenue_needed:,.2f}")


# --- Financial Visualizations ---
st.markdown("---")
st.header("3. Detailed Financial Visualizations 📈")

if error_message:
    st.warning("Charts are not available when the business model is unprofitable. Please adjust inputs.")
else:
    # --- Cost Breakdown Per Job (Pie Chart) ---
    st.subheader("Cost & Profit Breakdown Per Job")
    st.write("Visualizing how each RM100 of revenue from a single job is distributed among costs and profit.")

    cost_data = {
        'Category': ['Cleaner Pay', 'Transport Cost', 'Supplies Cost', 'Profit (per job)'],
        'Amount': [cleaner_pay, transport_cost, supplies_cost, profit_per_job]
    }
    df_costs = pd.DataFrame(cost_data)

    fig_pie = px.pie(df_costs, values='Amount', names='Category',
                     title='Breakdown of Each Job\'s Revenue (RM)',
                     hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pie.update_traces(textinfo='percent+label', pull=[0, 0, 0, 0.05])
    fig_pie.update_layout(showlegend=True, title_x=0.5) # Center title
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # --- Projected Monthly Financials (Stacked Bar Chart) ---
    st.subheader("Projected Monthly Financials (Based on Target Cleaners)")
    st.write(f"This chart shows the total monthly costs and your target profit for **{num_cleaners_needed} cleaners**.")

    total_cleaner_pay_monthly = num_cleaners_needed * cleaner_pay * jobs_per_cleaner_per_month
    total_transport_cost_monthly = num_cleaners_needed * transport_cost * jobs_per_cleaner_per_month
    total_supplies_cost_monthly = num_cleaners_needed * supplies_cost * jobs_per_cleaner_per_month
    total_hostel_cost_monthly = num_cleaners_needed * hostel_cost_per_month

    monthly_financials_data = {
        'Financial Item': ['Cleaner Pay', 'Transport Cost', 'Supplies Cost', 'Hostel Cost', 'Target Profit'],
        'Amount': [total_cleaner_pay_monthly, total_transport_cost_monthly, total_supplies_cost_monthly,
                   total_hostel_cost_monthly, target_monthly_profit],
        'Category': ['Monthly Overview'] * 5
    }
    df_monthly_financials = pd.DataFrame(monthly_financials_data)

    fig_stacked_bar_px = px.bar(df_monthly_financials, x='Category', y='Amount',
                                color='Financial Item',
                                title='Projected Monthly Financials Breakdown',
                                labels={'Amount':'Amount (RM)', 'Category':''},
                                color_discrete_map={'Cleaner Pay': '#5DADE2', 'Transport Cost': '#F4D03F',
                                                    'Supplies Cost': '#58D68D', 'Hostel Cost': '#AF7AC5',
                                                    'Target Profit': '#27AE60'}, # More distinct colors
                                height=450)

    total_monthly_revenue = df_monthly_financials['Amount'].sum()

    fig_stacked_bar_px.add_hline(y=total_monthly_revenue, line_dash="dot", line_color="#C0392B", # Red line
                                 annotation_text=f"Total Revenue: RM {total_monthly_revenue:,.2f}",
                                 annotation_position="top left",
                                 annotation_font_color="#C0392B")
    fig_stacked_bar_px.update_layout(showlegend=True, barmode='stack', title_x=0.5,
                                     xaxis={'categoryorder':'array', 'categoryarray':['Monthly Overview']})
    st.plotly_chart(fig_stacked_bar_px, use_container_width=True)

    st.markdown("---")

    # --- Revenue Flow to Net Profit (Monthly Waterfall) ---
    st.subheader("Monthly Revenue Flow to Net Profit")
    st.write("Understand how total revenue is reduced by various costs to arrive at your net profit.")

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
            connector = {"line":{"color":"#666666"}},
            increasing={"marker":{"color":"#28B463"}}, # Darker green for positive
            decreasing={"marker":{"color":"#E74C3C"}} # Darker red for negative
        )
    ]

    fig_waterfall = go.Figure(data=data)

    fig_waterfall.update_layout(
        title="Monthly Revenue Flow: From Gross to Net Profit",
        showlegend=False,
        yaxis_title="Amount (RM)",
        xaxis_title="Financial Measure",
        title_x=0.5 # Center title
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.info("💡 **Tip:** Adjust the input values in the sidebar to see how changes in your business model affect staffing and profitability in real-time!")
