import pandas as pd
df=pd.read_csv('data/cleaned.csv')
df['Transaction_Date']=pd.to_datetime(df['Transaction_Date'])
df['Signup_Date']=pd.to_datetime(df['Signup_Date'])
col=['Transaction_ID', 'Customer_ID', 'Transaction_Date', 'Product', 'Category', 'Quantity', 'Unit_Price', 'Discount', 'Sales', 'Payment_Method', 'Returned', 'Revenue', 'Signup_Date', 'Country', 'Acquisition_Channel', 'Plan']

cus_df=df.groupby('Customer_ID').agg(
            Transaction =('Transaction_ID','count'),
            Total_Sales=('Sales', 'sum'),
            Quantity=('Quantity', 'sum'),
            First_Purchase=('Transaction_Date', 'min'),
            Last_Purchase=('Transaction_Date','max')
            ).reset_index()
overall_latest_transaction_date=df['Transaction_Date'].max()
cus_df['Lifespan_Days'] =overall_latest_transaction_date-cus_df['Last_Purchase']

cus_df['R_Score'] = pd.qcut(cus_df['Lifespan_Days'].rank(method='first'),5, labels=[5, 4, 3, 2, 1])
cus_df['F_Score'] = pd.qcut(cus_df['Transaction'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
cus_df['M_Score'] = pd.qcut(cus_df['Total_Sales'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

#Create Customer Segments
cus_df['R_Score'] = cus_df['R_Score'].astype(int)
cus_df['F_Score'] = cus_df['F_Score'].astype(int)
cus_df['M_score'] = cus_df['M_Score'].astype(int)

def assign_segment(row):
            R, F, M = row['R_Score'], row['F_Score'], row['M_Score']
            if R >= 4 and F >= 4 and M >= 4:
                return 'Champions'
            elif R >= 3 and F >= 4:
                return 'Loyal Customers'
            elif M >= 4:
                return 'Big Spenders'
            elif R <= 2 and F >= 3:
                return 'At Risk'
            elif R == 3:
                return 'Need Attention'
            elif R <= 2 and F <= 2 and M <= 2:
                return 'Lost / Low Value'
            else:
                return 'Other'  # catches anything not matching
cus_df['Segment'] = cus_df.apply(assign_segment, axis=1)

#Segment quality check
segment_summary = cus_df.groupby('Segment').agg(
                    Customer_Count=('Customer_ID', 'nunique'),
                    Total_Revenue=('Total_Sales', 'sum'),
                    Avg_Recency=('Lifespan_Days', 'mean'),
                    Avg_Frequency=('Transaction', 'mean'),
                    ).reset_index()

average_transactions_per_customer = cus_df['Transaction'].mean().round(2)
aov=cus_df['Total_Sales'].mean()/cus_df['Transaction'].mean()
average_lifespan=cus_df['Lifespan_Days'].mean()
purchase_frequency=average_transactions_per_customer/260 * 360
clv=aov * 9.94 * (260/365)

#Step 1: Customer Revenue <Total Sales per customer>ipa
#Step 2: Find the average<calculate:Average customer revenue>
#Step 3 — Customer Lifespan<Lifespan = Last Purchase − First Purchase>
#calculate:Average Lifespan
#Step 4 — Average Order Value (AOV)
#AOV = Total customer revenue ÷ Number of transactions
#Purchase Frequency<Average Transaction /(Average Lifespan x 360)
#CLV = AOV × Purchase Frequency × Customer Lifespan(Average Lifespan/365)
#Average customer value = Segment Revenue ÷ Segment Customers

#Calculate the mean of customer-level Sales
#print(cus_df[['Customer_ID','Total_Sales']].head(3))
#print(cus_df[['Customer_ID','Lifespan_Days']].tail(2))
print(cus_df['Total_Sales'].mean().round(2))
print(average_transactions_per_customer)
print(average_lifespan)
print(aov.round(2))
print(purchase_frequency.round(2))
print(clv)

#Average customer value = Segment Revenue ÷ Segment Customers
segment_summary['avg_clv']=(segment_summary['Total_Revenue']/segment_summary['Customer_Count']).round(2)
#print(segment_summary[['Segment','avg_clv']])


parato_df=cus_df.sort_values('Total_Sales',ascending=False).reset_index()
total_customer=cus_df['Customer_ID'].nunique()
ten_percent=total_customer * 10/100
ten_percent_custoemr_revenue=parato_df.loc[:136,'Total_Sales'].sum()
total_customer_revenue=parato_df['Total_Sales'].sum()
ans=ten_percent_custoemr_revenue/total_customer_revenue * 100
print(ans)
#print(total_customer_revenue)
#print(parato_df[['Customer_ID','Total_Sales']])

segment_summary['Revenue_Percent']=(segment_summary['Total_Revenue']/total_customer_revenue * 100).round(2)
#print(segment_summary[['Segment','Total_Revenue','Revenue_Percent']])

segment_summary['Customer_Percent']=(segment_summary['Customer_Count']/total_customer * 100).round(2)
#print(segment_summary[['Segment','Customer_Count','Customer_Percent']])

segment_summary['Revenue_Index']=(segment_summary['Revenue_Percent']/segment_summary['Customer_Percent']).round(2)
print(segment_summary[['Segment','Revenue_Index']])
