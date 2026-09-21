import pandas as pd
df=pd.read_csv('data/cleaned.csv')
df['Transaction_Date']=pd.to_datetime(df['Transaction_Date'])
df['Signup_Date']=pd.to_datetime(df['Signup_Date'])
col=['Transaction_ID', 'Customer_ID', 'Transaction_Date', 'Product', 'Category', 'Quantity', 'Unit_Price', 'Discount', 'Sales', 'Payment_Method', 'Returned', 'Revenue', 'Signup_Date', 'Country', 'Acquisition_Channel', 'Plan']

cus_df=df.groupby('Customer_ID').agg(
        Frequency =('Transaction_ID','count'),
        Monetary=('Sales', 'sum'),
        Quantity=('Quantity', 'sum'),
        First_Purchase=('Transaction_Date', 'min'),
        Last_Purchase=('Transaction_Date','max')
        ).reset_index()
#print(cus_df.head(5))
#print(cus_df.shape)
overall_latest_transaction_date=df['Transaction_Date'].max()
cus_df['Recency']=overall_latest_transaction_date-cus_df['Last_Purchase']
#print(cus_df.info())

cus_df['R_Score'] = pd.qcut(cus_df['Recency'].rank(method='first'),5, labels=[5, 4, 3, 2, 1])
cus_df['F_Score'] = pd.qcut(cus_df['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
cus_df['M_Score'] = pd.qcut(cus_df['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

cus_df['RFM_Score'] = (
        
            cus_df['R_Score'].astype(str) +
            cus_df['F_Score'].astype(str) +
            cus_df['M_Score'].astype(str)
                    )

#print(cus_df[['RFM_Score','R_Score','F_Score','M_Score']].head())

#Create Customer Segments
cus_df['R_Score'] = cus_df['R_Score'].astype(int)
cus_df['F_Score'] = cus_df['F_Score'].astype(int)
cus_df['M_Score'] = cus_df['M_Score'].astype(int)

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
#print(cus_df['Segment'].value_counts())

other_df=cus_df[cus_df['Segment'] == "Other"]
#print(other_df['R_Score'].value_counts())
#print(other_df['F_Score'].value_counts())
#print(other_df['M_Score'].value_counts())

#Segment Revenue Analysis
segment_revenue=cus_df.groupby('Segment')['Monetary'].sum()
#print(segment_revenue.sort_values(ascending=False))

#Segment quality check
segment_summary = cus_df.groupby('Segment').agg(
            Customer_Count=('Customer_ID', 'nunique'),
            Total_Revenue=('Monetary', 'sum'),
            Avg_Recency=('Recency', 'mean'),
            Avg_Frequency=('Frequency', 'mean'),
            Avg_Monetary=('Monetary', 'mean')
                            ).reset_index()

# Average revenue per customer = Total Revenue / Customer Count
segment_summary['Avg_Revenue_Per_Customer'] = (
            segment_summary['Total_Revenue'] / segment_summary['Customer_Count']
            )

# Reorder columns for readability
segment_summary = segment_summary[[
        'Segment', 'Customer_Count', 'Total_Revenue', 'Avg_Revenue_Per_Customer',
            'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary'
            ]]

segment_summary = segment_summary.sort_values('Total_Revenue', ascending=False)
segment_summary = segment_summary.round(2)
#print(segment_summary)

# Pareto analysis
pareto = cus_df[['Customer_ID', 'Monetary']].sort_values('Monetary', ascending=False).reset_index(drop=True)
# Cumulative % of total revenue
pareto['Cumulative_Revenue'] = pareto['Monetary'].cumsum()
total_revenue = pareto['Monetary'].sum()
pareto['Cumulative_Pct_Revenue'] = pareto['Cumulative_Revenue'] / total_revenue * 100
# Cumulative % of customers
pareto['Customer_Rank'] = pareto.index + 1
total_customers = len(pareto)
pareto['Cumulative_Pct_Customers'] = pareto['Customer_Rank'] / total_customers * 100

pareto[['Cumulative_Pct_Revenue', 'Cumulative_Pct_Customers']] = pareto[['Cumulative_Pct_Revenue', 'Cumulative_Pct_Customers']].round(2)
#print(pareto.head())
customers_for_80pct = (pareto['Cumulative_Pct_Revenue'] <= 80).sum() + 1
pct_of_base = customers_for_80pct / total_customers * 100
#print(f"{customers_for_80pct} customers ({pct_of_base:.2f}% of customer base) generate 80% of revenue")

#Customer Retention / cohort analysis 
df['Cohort_Month'] = df['Signup_Date'].dt.to_period('M')
df['Transaction_Month'] = df['Transaction_Date'].dt.to_period('M')
df['Period_Number'] = (df['Transaction_Month'] - df['Cohort_Month']).apply(lambda x: x.n)
cohort_data = df.groupby(['Cohort_Month', 'Period_Number'])['Customer_ID'].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index='Cohort_Month', columns='Period_Number', values='Customer_ID')
print(cohort_data)

#Find the January cohort size
jan_2024_cohort_size = df[df['Cohort_Month'] == '2024-01']['Customer_ID'].nunique()
print(jan_2024_cohort_size)

#Retention %
jan_df=cohort_data[cohort_data['Cohort_Month'] == '2024-01']
jan_df['Retention']=jan_df['Customer_ID']/jan_2024_cohort_size * 100
jan_df['Retention']=jan_df['Retention'].round(2)
#print(jan_df)

cus_df['First_Purchase_Month'] = cus_df['First_Purchase'].dt.to_period('M')
df['Purchase_Month']=df['Transaction_Date'].dt.to_period('M')
df_one=cus_df[['Customer_ID','First_Purchase','First_Purchase_Month']]
df_two=df[['Customer_ID','Transaction_Date','Purchase_Month']]
coho_df=df_one.merge(df_two,on='Customer_ID',how='inner')
coho_df['Period_Number']=(coho_df['Purchase_Month']-coho_df['First_Purchase_Month']).apply(lambda x: x.n)
coho_data = coho_df.groupby(['First_Purchase_Month', 'Period_Number'])['Customer_ID'].nunique().reset_index()
coho_pivot = coho_data.pivot(index='First_Purchase_Month',columns='Period_Number', values='Customer_ID')

fpm_jan=coho_data[coho_data['First_Purchase_Month'] == '2024-01']
fpm_jan['Retention']=fpm_jan['Customer_ID']/20 * 100
fpm_jan['Retention']=fpm_jan['Retention'].round(2)
fpm_pivot=fpm_jan.pivot(index='First_Purchase_Month',columns='Period_Number',values='Retention')
print(fpm_pivot)
