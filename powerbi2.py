import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('opportunity_analysis_sample_2000_rows.csv')  # Update with actual dataset path
        df['Order Date'] = pd.to_datetime(df['Order Date'])  # Ensure Order Date is a datetime object
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data()

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "Sales by Region", "Profit by Product Category", 
                                              "Order Status Summary", "Sales vs Discount Analysis", 
                                              "Top Customers by Revenue", "Sales Trend Over Time", 
                                              "Customer Segmentation", "Top Products by Sales"])

# Define filters
start_date = st.sidebar.date_input("Start Date", value=df['Order Date'].min())
end_date = st.sidebar.date_input("End Date", value=df['Order Date'].max())

# Filter data based on the selected date range
filtered_data = df[(df['Order Date'] >= pd.to_datetime(start_date)) & (df['Order Date'] <= pd.to_datetime(end_date))]

# Additional filters
selected_region = st.sidebar.multiselect("Select Region", options=filtered_data['Region'].unique(), default=filtered_data['Region'].unique())
selected_category = st.sidebar.multiselect("Select Product Category", options=filtered_data['Category'].unique(), default=filtered_data['Category'].unique())
selected_segment = st.sidebar.multiselect("Select Customer Segment", options=filtered_data['Customer Segment'].unique(), default=filtered_data['Customer Segment'].unique())

# Filter data based on additional selections
filtered_data = filtered_data[(filtered_data['Region'].isin(selected_region)) &
                              (filtered_data['Category'].isin(selected_category)) &
                              (filtered_data['Customer Segment'].isin(selected_segment))]

# Define each page
def home():
    st.title("Opportunity Analysis Dashboard")
    st.write("Welcome to the Multi-page App to visualize various insights from the Opportunity Analysis dataset.")

def sales_by_region():
    st.title("Sales by Region and Country")
    
    # Group by Region and Country
    region_sales = filtered_data.groupby(['Region', 'Country'])['Revenue ($)'].sum().reset_index()
    
    st.write("### Sales by Region")
    st.bar_chart(region_sales.set_index('Region')['Revenue ($)'])
    
    st.write("### Sales by Country")
    st.bar_chart(region_sales.set_index('Country')['Revenue ($)'])

def profit_by_category():
    st.title("Profit by Product Category")
    
    # Group by Product Category
    category_profit = filtered_data.groupby('Category')['Profit ($)'].sum().reset_index()
    
    st.write("### Profit by Category")
    st.bar_chart(category_profit.set_index('Category')['Profit ($)'])

def order_status_summary():
    st.title("Order Status Summary")
    
    # Count orders by status
    order_status = filtered_data['Order Status'].value_counts().reset_index()
    order_status.columns = ['Order Status', 'Count']
    
    # Pie Chart for Order Status
    fig, ax = plt.subplots()
    ax.pie(order_status['Count'], labels=order_status['Order Status'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    
    st.write("### Order Status Distribution")
    st.pyplot(fig)

def sales_vs_discount():
    st.title("Sales vs Discount Analysis")
    
    # Scatter plot for Sales vs Discount
    st.write("### Scatter Plot: Sales vs Discount")
    plt.figure(figsize=(10,6))
    plt.scatter(filtered_data['Discount (%)'], filtered_data['Revenue ($)'], alpha=0.5)
    plt.title('Sales vs Discount')
    plt.xlabel('Discount (%)')
    plt.ylabel('Revenue ($)')
    st.pyplot(plt)

    # Show Correlation
    correlation = filtered_data[['Revenue ($)', 'Discount (%)']].corr()
    st.write("### Correlation between Sales and Discount")
    st.table(correlation)

def top_customers_by_revenue():
    st.title("Top Customers by Revenue")
    
    # Group by Customer and Sum Revenue
    customer_revenue = filtered_data.groupby(['Customer ID', 'Customer Name'])['Revenue ($)'].sum().reset_index()
    top_customers = customer_revenue.sort_values(by='Revenue ($)', ascending=False).head(10)
    
    st.write("### Top 10 Customers by Revenue")
    st.bar_chart(top_customers.set_index('Customer Name')['Revenue ($)'])

def sales_trend_over_time():
    st.title("Sales Trend Over Time")
    
    # Group by Order Date
    sales_trend = filtered_data.groupby(filtered_data['Order Date'].dt.to_period('M'))['Revenue ($)'].sum().reset_index()
    sales_trend['Order Date'] = sales_trend['Order Date'].dt.to_timestamp()
    
    st.write("### Monthly Sales Trend")
    st.line_chart(sales_trend.set_index('Order Date')['Revenue ($)'])

def customer_segmentation():
    st.title("Customer Segmentation")
    
    # Group by Customer Segment
    customer_segment_sales = filtered_data.groupby('Customer Segment')['Revenue ($)'].sum().reset_index()
    
    st.write("### Sales by Customer Segment")
    st.bar_chart(customer_segment_sales.set_index('Customer Segment')['Revenue ($)'])

def top_products_by_sales():
    st.title("Top Products by Sales")
    
    # Group by Product Name
    product_sales = filtered_data.groupby(['Product Name'])['Revenue ($)'].sum().reset_index()
    top_products = product_sales.sort_values(by='Revenue ($)', ascending=False).head(10)
    
    st.write("### Top 10 Products by Sales")
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
