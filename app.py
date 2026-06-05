import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration
st.set_page_config(page_title="AI-Powered Data Analytics Suite", layout="wide")

# Custom CSS styling (Fixes text visibility in dark mode by forcing black text)
st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f2f6 !important;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        color: #111111 !important;
    }
    .metric-box h3, .metric-box h2 {
        color: #111111 !important;
        margin: 0px;
    }
    .insight-box {
        background-color: #e8f4f8 !important;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2980b9;
        margin-bottom: 10px;
        color: #111111 !important;
    }
    .insight-box strong {
        color: #2980b9 !important;
    }
    /* Streamlit widgets text visibility fix */
    .stMarkdown, p, span {
        color: inherit;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI-Powered Smart Data Analytics Suite")
st.markdown("Apni CSV ya Excel file upload kijiye, automatic interactive charts banaiye aur AI-driven insights paaiye!")
st.markdown("---")

# 2. Advanced File Uploader (CSV aur Excel Dono Ka Support)
uploaded_file = st.file_uploader("Yahan apni file upload karein (CSV ya XLSX)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # File type check karke read karna
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # ------------------ SIDEBAR FILTERS ------------------
    st.sidebar.header("🎯 Data Filters")
    
    # City Filter
    selected_city = st.sidebar.multiselect("City Select Karen:", 
                                           options=df["City"].unique(), 
                                           default=df["City"].unique())
    
    # Category Filter
    selected_category = st.sidebar.multiselect("Category Select Karen:", 
                                               options=df["Category"].unique(), 
                                               default=df["Category"].unique())
    
    # Filter ke basis par data ko update karna
    filtered_df = df[df["City"].isin(selected_city) & df["Category"].isin(selected_category)]
    
    # ------------------ 3. KPI METRICS CARDS ------------------
    st.subheader("📈 Key Performance Indicators (KPI)")
    
    total_sales = filtered_df["Total_Sales"].sum()
    total_qty = filtered_df["Quantity"].sum()
    total_orders = filtered_df.shape[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-box'><h3>💰 Total Sales</h3><h2>₹{total_sales:,}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><h3>📦 Total Quantity Sold</h3><h2>{total_qty:,}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><h3>🛒 Total Orders</h3><h2>{total_orders:,}</h2></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # ------------------ 4. AUTOMATED AI INSIGHTS ENGINE ------------------
    st.subheader("💡 Automated AI Insights")
    
    if not filtered_df.empty:
        # Analytics logic se insights nikalna
        top_product = filtered_df.groupby("Product")["Total_Sales"].sum().idxmax()
        top_city = filtered_df.groupby("City")["Total_Sales"].sum().idxmax()
        avg_order_val = filtered_df["Total_Sales"].mean()
        top_payment = filtered_df.groupby("Payment_Method")["Total_Sales"].sum().idxmax()
        
        # Displaying Insights with dark-mode safe styling
        st.markdown(f"""
            <div class='insight-box'>
                <strong>🏆 Top Performing Product:</strong> {top_product} sabse zyada bikne wala product hai, jisne is filtered criteria me sabse zyada revenue generate kiya hai.
            </div>
            <div class='insight-box'>
                <strong>📍 Target Market Leader:</strong> Max revenue <strong>{top_city}</strong> sheher se aa raha hai. Is region me marketing badhane se sales aur grow ho sakti hain.
            </div>
            <div class='insight-box'>
                <strong>💳 Customer Behavior:</strong> Aapke customers sabse zyada <strong>{top_payment}</strong> mode ka use karke payment karna pasand kar rahe hain.
            </div>
            <div class='insight-box'>
                <strong>📊 Ticket Size:</strong> Aapka Average Order Value (AOV) <strong>₹{avg_order_val:,.2f}</strong> hai, yaani har customer lagbhag itne tak ki shopping kar raha hai.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Filters ke hisab se koi data nahi mila. Kripya filters badlein.")
        
    st.markdown("---")
    
    # ------------------ 5. DATA VISUALIZATION (CHARTS) ------------------
    st.subheader("📊 Visual Analytics")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Product-wise Sales Performance")
        fig_bar = px.bar(filtered_df, x="Product", y="Total_Sales", 
                         color="Category", title="Sales by Product & Category",
                         barmode="group", template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with chart_col2:
        st.markdown("#### Payment Method Preference")
        fig_pie = px.pie(filtered_df, values="Total_Sales", names="Payment_Method", 
                         title="Sales Share by Payment Method", hole=0.4,
                         template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown("---")
    
    # ------------------ 6. DATA TABLE VIEW & DOWNLOAD ------------------
    st.subheader("👀 Filtered Data Preview")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Filtered data ko download karne ka advanced button (In-memory Excel Converter)
    towrite = io.BytesIO()
    downloaded_file = filtered_df.to_excel(towrite, index=False, header=True, engine='openpyxl')
    towrite.seek(0)
    
    st.download_button(
        label="📥 Filtered Data Ko Excel Me Download Karen",
        data=towrite,
        file_name='filtered_analytics_report.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
else:
    st.info("Aapne jo 'sales_data.csv' banayi thi use upload kijiye ya koi bhi dusri Excel/CSV file upload karke test kijiye.")
    
