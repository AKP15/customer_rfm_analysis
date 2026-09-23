# Customer Lifetime Value & RFM Analysis

## 📌 Project Overview

This project analyzes customer purchasing behavior to understand:

- Which customers generate the most revenue
- Which customer segments have the highest historical customer value
- How customer revenue is distributed across RFM segments
- How customer retention changes over time
- How concentrated revenue is among high-value customers
- What business actions could be considered for different customer segments

The project combines **RFM Analysis, Customer Lifetime Value (CLV), Pareto Analysis, and Cohort Retention Analysis**.

---

## 🎯 Business Questions

1. Who are the most valuable customers?
2. Which RFM segments contribute the most revenue?
3. How much revenue comes from high-value customers?
4. How concentrated is customer revenue?
5. How does customer retention change after the first purchase?
6. What strategies could be considered for different customer segments?

---

## 📂 Datasets

### Customers Dataset

Contains customer-level information:

- Customer_ID
- Signup_Date
- Country
- Acquisition_Channel
- Plan

### Transactions Dataset

Contains transaction-level information:

- Transaction_ID
- Customer_ID
- Transaction_Date
- Product
- Category
- Quantity
- Unit_Price
- Discount
- Sales
- Payment_Method
- Returned

---

## 🧹 Data Cleaning

The datasets contained several intentional data-quality issues.

### Customers

- Removed duplicate customer records
- Filled missing Country values
- Converted Signup_Date to datetime
- Standardized inconsistent Acquisition_Channel values

### Transactions

- Removed duplicate transactions
- Filled missing Discount values with 0
- Converted Transaction_Date to datetime
- Corrected negative Unit_Price
- Standardized Product names
- Verified Sales consistency

### Final Dataset

- Customers: **1,500**
- Customers with transactions: **1,392**
- Transactions: **10,000**
- Missing values: **0**
- Duplicate records: **0**

---

# 📊 Key Performance Indicators

| KPI | Value |
|---|---:|
| Registered Customers | 1,500 |
| Active Customers | 1,392 |
| Total Revenue | $5,295,350.54 |
| Average Customer Value | $3,804.13 |
| Average Transactions / Customer | 7.18 |
| Average Customer Lifespan | 260 days |
| Average Order Value | $529.54 |
| Purchase Frequency | 9.94 / year |

---

# 👥 RFM Analysis

Customers were segmented using:

- **Recency** — How recently the customer purchased
- **Frequency** — How often the customer purchased
- **Monetary** — How much the customer spent

The resulting segments were:

- Champions
- Big Spenders
- Loyal Customers
- At Risk
- Need Attention
- Lost / Low Value
- Other

---

# 💰 Revenue by RFM Segment

| Segment | Customers | Customer % | Revenue | Revenue % | Avg Historical CLV |
|---|---:|---:|---:|---:|---:|
| Champions | 224 | 16.09% | $1,683,453.22 | 31.79% | $7,515.42 |
| Big Spenders | 240 | 17.24% | $1,519,607.68 | 28.70% | $6,331.70 |
| Loyal Customers | 155 | 11.14% | $885,587.65 | 16.72% | $5,713.47 |
| Other | 295 | 21.19% | $543,628.97 | 10.27% | $1,842.81 |
| At Risk | 111 | 7.97% | $255,187.81 | 4.82% | $2,298.99 |
| Need Attention | 143 | 10.27% | $215,454.28 | 4.07% | $1,506.67 |
| Lost / Low Value | 224 | 16.09% | $192,430.93 | 3.63% | $859.07 |

---

# 🔎 Key Findings

### 1. High-value customers drive a large share of revenue

Champions and Big Spenders represent **33.33% of active customers** but contribute **60.49% of historical revenue**.

### 2. Champions have the highest historical customer value

Champions have an average historical customer value of approximately **$7,515**, the highest among all RFM segments.

### 3. Revenue is concentrated among high-value customers

The top **10% of customers generate approximately 29.66% of total revenue**.

Additionally, approximately **46.91% of customers generate 80% of revenue**.

### 4. Lost / Low Value customers contribute relatively little revenue

Lost / Low Value customers represent **16.09% of active customers** but contribute only **3.63% of revenue**.

### 5. Customer value differs significantly between segments

Average historical customer value ranges from approximately:

**$859 → $7,515**

This demonstrates substantial differences in customer economic value.

---

# 📈 Cohort Retention Analysis

Customers were grouped according to their **First Purchase Month**.

Retention was calculated using:

> Customers who purchased in a later period ÷ Customers in the original cohort

The cohort analysis shows how customer purchasing behavior changes over the months following the first purchase.

### Important observation

Retention generally decreases as the number of months since the first purchase increases.

However, retention can increase after declining because customers may skip months and return later.

Recent cohorts also contain fewer observable periods because they have not existed long enough to accumulate a complete retention history.

---

# 💡 Business Recommendations

### Champions

Prioritize retention through personalized loyalty benefits, early product access, and differentiated customer experiences because this segment contributes a disproportionately large share of historical revenue.

### Big Spenders

Use targeted cross-selling, personalized recommendations, and replenishment campaigns to encourage more frequent purchases.

### Loyal Customers

Strengthen loyalty through tiered rewards, milestone incentives, and referral programs designed to encourage continued purchasing.

### At Risk

Develop targeted win-back campaigns using personalized offers and product recommendations, while measuring reactivation and incremental revenue.

### Lost / Low Value

Use low-cost, scalable re-engagement campaigns and monitor incremental revenue before increasing investment in this segment.

---

# 📊 Dashboard

The final dashboard includes:

- KPI cards
- Revenue by RFM Segment
- Average Customer Value by RFM Segment
- Customer Share vs Revenue Share
- Cohort Retention Heatmap

---

# 🛠️ Tools & Skills

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Data Cleaning
- Exploratory Data Analysis (EDA)
- Customer Segmentation
- RFM Analysis
- Customer Lifetime Value
- Pareto Analysis
- Cohort Retention Analysis
- Data Visualization
- Business Analytics

---

# 📌 Important CLV Note

The CLV values in this project represent **historical customer value based on observed transaction revenue**.

They should not be interpreted as predictive future lifetime value.

A predictive CLV model would require additional assumptions or modeling of future purchasing behavior, churn probability, and expected customer lifespan.

---

## 👤 Project Type

**Portfolio Project — Customer Analytics / Data Analyst**

This project demonstrates the ability to transform raw customer and transaction data into actionable business insights using Python.
