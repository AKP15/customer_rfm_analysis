import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(pareto['Customer_Rank'], pareto['Monetary'], color='steelblue', alpha=0.6)
ax1.set_xlabel('Customer Rank (by Revenue)')
ax1.set_ylabel('Revenue per Customer', color='steelblue')

ax2 = ax1.twinx()
ax2.plot(pareto['Customer_Rank'], pareto['Cumulative_Pct_Revenue'], color='darkorange', linewidth=2)
ax2.axhline(80, color='red', linestyle='--', alpha=0.5)
ax2.set_ylabel('Cumulative % of Revenue', color='darkorange')

plt.title('Pareto Analysis: Revenue Concentration by Customer')
plt.tight_layout()
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))

sns.heatmap(
            retention_pivot,
            annot=True,          # show the % values in each cell
            fmt='.1f',           # 1 decimal place
            cmap='YlGnBu',       # yellow (low) → green → blue (high) — classic cohort look
            vmin=0, vmax=100,    # fix color scale 0-100% so cohorts compare fairly
            linewidths=0.5,
            linecolor='white',
            cbar_kws={'label': 'Retention %'}
                                        )

plt.title('Customer Retention Cohort Analysis', fontsize=14, pad=12)
plt.xlabel('Months Since First Purchase (Period Number)')
plt.ylabel('First Purchase Month (Cohort)')
plt.tight_layout()
plt.show()
