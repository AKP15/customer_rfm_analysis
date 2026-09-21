import pandas as pd
import numpy as np
df1=pd.read_csv('data/project5_customers.csv')
df2=pd.read_csv('data/project5_transactions.csv')


print(f'df1 shape {df1.shape} and df2 shape {df2.shape}')
print(f'df1 cols={df1.columns.tolist()} \nd2 cols={df2.columns.tolist()}')
#print(f'{df1.dtypes} - {df2.dtypes}')
#print(df1.isnull().sum())
#print(df2.isnull().sum())
#print(df1.duplicated().sum())
#print(df2.duplicated().sum())

print(df1['Customer_ID'].nunique())
print(df2['Customer_ID'].nunique())

min_df=df2[['Unit_Price', 'Sales']]
#for column in min_df.columns:
#    print(min_df[column].describe())

#df1 cleaning 
df1=df1.drop_duplicates()
df1['Country']=df1['Country'].fillna('Unknown')
df1['Signup_Date']=pd.to_datetime(df1['Signup_Date'])
#for column in df1.columns:
#    print(df1[column].value_counts())
df1['Acquisition_Channel']=df1['Acquisition_Channel'].str.strip().str.title()
#print(df1['Acquisition_Channel'].value_counts())
#print(df1['Customer_ID'].nunique())

#clean df2
df2=df2.drop_duplicates()
df2['Discount']=df2['Discount'].fillna(0)
df2['Transaction_Date']=pd.to_datetime(df2['Transaction_Date'])
df2['Product']=df2['Product'].str.strip().str.title()
#print(df2['Product'].value_counts())
#print(df2[df2['Unit_Price']<0][['Sales','Quantity', 'Unit_Price']])
df2['Unit_Price']=np.abs(df2['Unit_Price'])
df2['Revenue']=df2['Quantity']*df2['Unit_Price']*(1-df2['Discount'])
total_sale=df2['Sales'].sum()
total_revenue=df2['Revenue'].sum()
#print(df1.shape)
#print(df2.shape)
#print(df1.isnull().sum())
#print(df2.isnull().sum())
#print(total_revenue-total_sale)

df3=df2.merge(df1,on='Customer_ID',how='inner')
print(df3.shape)
print(df3.columns)
print(df3.isnull().sum())
df3.to_csv('data/cleaned.csv',index=False)
