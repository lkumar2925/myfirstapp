import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Load Dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('opportunity_analysis_sample_2000_rows.csv')
        df['Order Date'] = pd.to_datetime(df['Order Date'])  
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
# Load data
df = load_data()
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown('<p style="color: blue; font-weight: bold;">Created by: 24MAI0068-M.LIKHITH KUMAR</p>', unsafe_allow_html=True)
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "Sales by Region", "Profit by Product Category", 
                                              "Order Status Summary", "Sales vs Discount Analysis", 
                                              "Top Customers by Revenue", "Sales Trend Over Time", 
                                              "Customer Segmentation", "Top Products by Sales"])
# Define filters
start_date = st.sidebar.date_input("Start Date", value=df['Order Date'].min())
end_date = st.sidebar.date_input("End Date", value=df['Order Date'].max())
filtered_data = df[(df['Order Date'] >= pd.to_datetime(start_date)) & (df['Order Date'] <= pd.to_datetime(end_date))]
selected_region = st.sidebar.multiselect("Select Region", options=filtered_data['Region'].dropna().unique(), default=filtered_data['Region'].dropna().unique())
selected_category = st.sidebar.multiselect("Select Product Category", options=filtered_data['Category'].dropna().unique(),
                                            default=filtered_data['Category'].dropna().unique())
selected_segment = st.sidebar.multiselect("Select Customer Segment", options=filtered_data['Customer Segment'].dropna().unique(), 
                                          default=filtered_data['Customer Segment'].dropna().unique())
filtered_data = filtered_data[(filtered_data['Region'].isin(selected_region)) &
                              (filtered_data['Category'].isin(selected_category)) &
                              (filtered_data['Customer Segment'].isin(selected_segment))]
# Define each page
def home():
    st.markdown("<h1 style='color: purple;'>Welcome to the Opportunity Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: teal;'>Explore different insights by navigating through the pages.</p>", unsafe_allow_html=True)
def sales_by_region():
    st.markdown("<h2 style='color: navy;'>Sales by Region and Country</h2>", unsafe_allow_html=True)
    region_sales = filtered_data.groupby(['Region', 'Country'])['Revenue ($)'].sum().reset_index()
    st.markdown("<h3 style='color: blue;'>Sales by Region</h3>", unsafe_allow_html=True)
    st.bar_chart(region_sales.set_index('Region')['Revenue ($)'])
    st.markdown("<h3 style='color: green;'>Sales by Country</h3>", unsafe_allow_html=True)
    st.bar_chart(region_sales.set_index('Country')['Revenue ($)'])
def profit_by_category():
    st.markdown("<h2 style='color: orange;'>Profit by Product Category</h2>", unsafe_allow_html=True)
    category_profit = filtered_data.groupby('Category')['Profit ($)'].sum().reset_index()
    st.markdown("<h3 style='color: red;'>Profit by Category</h3>", unsafe_allow_html=True)
    st.bar_chart(category_profit.set_index('Category')['Profit ($)'])
def order_status_summary():
    st.markdown("<h2 style='color: darkred;'>Order Status Summary</h2>", unsafe_allow_html=True)
    order_status = filtered_data['Order Status'].value_counts().reset_index()
    order_status.columns = ['Order Status', 'Count']
    fig, ax = plt.subplots()
    ax.pie(order_status['Count'], labels=order_status['Order Status'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.markdown("<h3 style='color: purple;'>Order Status Distribution</h3>", unsafe_allow_html=True)
    st.pyplot(fig)
def sales_vs_discount():
    st.markdown("<h2 style='color: darkgreen;'>Sales vs Discount Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: teal;'>Scatter Plot: Sales vs Discount</h3>", unsafe_allow_html=True)
    plt.figure(figsize=(10,6))
    plt.scatter(filtered_data['Discount (%)'], filtered_data['Revenue ($)'], alpha=0.5)
    plt.title('Sales vs Discount')
    plt.xlabel('Discount (%)')
    plt.ylabel('Revenue ($)')
    st.pyplot(plt)
    correlation = filtered_data[['Revenue ($)', 'Discount (%)']].corr()
    st.markdown("<h3 style='color: blue;'>Correlation between Sales and Discount</h3>", unsafe_allow_html=True)
    st.table(correlation)
def top_customers_by_revenue():
    st.markdown("<h2 style='color: darkblue;'>Top Customers by Revenue</h2>", unsafe_allow_html=True)
    customer_revenue = filtered_data.groupby(['Customer ID', 'Customer Name'])['Revenue ($)'].sum().reset_index()
    top_customers = customer_revenue.sort_values(by='Revenue ($)', ascending=False).head(10)
    st.markdown("<h3 style='color: magenta;'>Top 10 Customers by Revenue</h3>", unsafe_allow_html=True)
    st.bar_chart(top_customers.set_index('Customer Name')['Revenue ($)'])
def sales_trend_over_time():
    st.markdown("<h2 style='color: olive;'>Sales Trend Over Time</h2>", unsafe_allow_html=True)
    sales_trend = filtered_data.groupby(filtered_data['Order Date'].dt.to_period('M'))['Revenue ($)'].sum().reset_index()
    sales_trend['Order Date'] = sales_trend['Order Date'].dt.to_timestamp()
    st.markdown("<h3 style='color: orange;'>Monthly Sales Trend</h3>", unsafe_allow_html=True)
    st.line_chart(sales_trend.set_index('Order Date')['Revenue ($)'])
def customer_segmentation():
    st.markdown("<h2 style='color: maroon;'>Customer Segmentation</h2>", unsafe_allow_html=True)
    customer_segment_sales = filtered_data.groupby('Customer Segment')['Revenue ($)'].sum().reset_index()
    st.markdown("<h3 style='color: violet;'>Sales by Customer Segment</h3>", unsafe_allow_html=True)
    st.bar_chart(customer_segment_sales.set_index('Customer Segment')['Revenue ($)'])
def top_products_by_sales():
    st.markdown("<h2 style='color: teal;'>Top Products by Sales</h2>", unsafe_allow_html=True)
    product_sales = filtered_data.groupby(['Product Name'])['Revenue ($)'].sum().reset_index()
    top_products = product_sales.sort_values(by='Revenue ($)', ascending=False).head(10)
    st.markdown("<h3 style='color: coral;'>Top 10 Products by Sales</h3>", unsafe_allow_html=True)
    st.bar_chart(top_products.set_index('Product Name')['Revenue ($)'])
# Page Navigation Logic
if page == "Home":
    home()
elif page == "Sales by Region":
    sales_by_region()
elif page == "Profit by Product Category":
    profit_by_category()
elif page == "Order Status Summary":
    order_status_summary()
elif page == "Sales vs Discount Analysis":
    sales_vs_discount()
elif page == "Top Customers by Revenue":
    top_customers_by_revenue()
elif page == "Sales Trend Over Time":
    sales_trend_over_time()
elif page == "Customer Segmentation":
    customer_segmentation()
elif page == "Top Products by Sales":
    top_products_by_sales()
