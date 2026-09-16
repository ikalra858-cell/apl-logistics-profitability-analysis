# Customer, Product, and Profitability Performance Analysis in Supply Chain Operations

### An Exploratory Data Analysis and Profitability Intelligence Approach for Supply Chain Decision-Making

**Project Context:** APL Logistics (KWE Group)  
**Internship Organization:** Unified Mentor Private Limited  
**Domain:** Supply Chain Analytics | Customer Analytics | Profitability Analysis  
**Author:** Isha Kalra | BCA 3rd Year | Dewan V.S. Group of Institutions, Meerut

---

## 📌 Project Overview

In supply chain operations, high revenue does not necessarily translate into high profitability.

Discounting, customer-level performance, product mix, and regional differences can significantly affect margins. A business may generate substantial sales while simultaneously carrying loss-making customers, low-margin products, or inefficient market segments.

This project analyzes customer, product, category, discount, market, and regional profitability to identify where revenue is being generated, where profit is being created, and where profitability requires attention.

The project combines **data cleaning, financial validation, exploratory data analysis, profitability diagnostics, and an interactive Streamlit dashboard** to provide a decision-oriented view of supply chain performance.

---

## 🎯 Business Problem

Leadership needs visibility into the factors that influence profitability beyond headline sales figures.

The analysis addresses questions such as:

- Which customers contribute the most and least profit?
- How concentrated is profitability across products?
- Which products generate high revenue but operate below the overall margin?
- How does discounting relate to profitability?
- Which discount bands show the greatest margin pressure?
- Which categories require profitability monitoring?
- How do different markets and regions compare?
- Where does high revenue fail to translate into equally strong profit performance?

The objective is to move from **revenue-focused reporting toward profitability-focused decision-making**.

---

## 📊 Dataset Overview

The analysis is based on a supply chain operations dataset containing:

| Metric | Value |
|---|---:|
| Records | **180,519** |
| Variables | **40** |
| Customers | **20,652** |
| Products | **118** |
| Categories | **50** |
| Markets | **5** |
| Order Regions | **23** |
| Customer Countries analyzed | **2** |

### Financial Snapshot

| KPI | Result |
|---|---:|
| Total Sales | **36.78M** |
| Total Profit | **3.97M** |
| Overall Profit Margin | **10.78%** |
| Customer Value Index | **192.08** |
| Loss-Making Customers | **4,069 (19.70%)** |

> **Note:** The dataset does not contain a dedicated usable order-date field, so chronological revenue or profit trends are not presented. Discount-band comparisons are used where appropriate instead.

---

# 🔎 Key Findings

## 1. Revenue Does Not Equal Profit

The overall dataset generated approximately **36.78M in sales** and **3.97M in profit**, producing an overall profit margin of **10.78%**.

This demonstrates why sales volume alone is insufficient for evaluating business performance.

---

## 2. Customer Profitability Requires Attention

Out of **20,652 customers**, **4,069 customers (19.70%)** were loss-making.

These customers still generated approximately **19.34% of total sales**, while collectively contributing approximately **−1.08M in profit**.

This highlights a significant profitability-management opportunity: high sales activity can coexist with negative customer-level contribution.

Customer value tiers in the dashboard are **quartile-based analytical tiers**, rather than official business-defined customer classifications.

---

## 3. Product Profitability Is Highly Concentrated

The **top 10 products account for approximately 89.70% of total profit**.

At the same time, several high-revenue products operate below the overall **10.78%** profit margin.

### High-Revenue / Low-Margin Watchlist

| Product | Sales | Profit Margin |
|---|---:|---:|
| Under Armour Girls' Toddler Spine Surge Running Shoe | 1.27M | 9.95% |
| Nike Men's Free 5.0+ Running Shoe | 3.67M | 10.36% |
| Diamondback Women's Serene Classic Comfort Bike | 4.12M | 10.38% |
| Pelican Sunstream 100 Kayak | 3.10M | 10.45% |
| Dell Laptop | 663K | 10.51% |
| Smart watch | 117K | 10.70% |

These products are useful candidates for margin-focused review because their revenue scale can mask relatively weaker profitability.

---

## 4. Discounting Is Associated With Margin Compression

Profit margin declines as discount levels increase across the observed discount bands.

| Discount Band | Profit Margin |
|---|---:|
| No Discount | **13.09%** |
| 0–5% | **11.47%** |
| 5–10% | **11.34%** |
| 10–15% | **10.20%** |
| 15–20% | **9.59%** |
| 20–25% | **9.39%** |

The observed margin therefore falls from **13.09% without discounting to 9.39% at the 20–25% discount band**, a decline of approximately **3.71 percentage points**.

The **Discount Impact Ratio is approximately 18.67%**, representing the relative reduction in margin from the no-discount level to the discounted level.

> The Discount Impact Ratio should **not** be interpreted as 18.67% of profit being lost.

Loss rates do not increase monotonically with discount level, so the analysis does not claim that higher discounts automatically cause higher loss rates.

---

## 5. Market Performance Shows Scale vs. Efficiency Differences

Market-level profitability varies across the business.

| Market | Profit Margin | Loss Rate |
|---|---:|---:|
| Africa | 10.99% | 18.58% |
| Europe | 10.76% | 18.75% |
| LATAM | 10.93% | 18.58% |
| Pacific Asia | 10.37% | 18.92% |
| USCA | **11.14%** | 18.65% |

### Interpretation

- **Europe** leads in overall sales and total profit because of its scale.
- **USCA** records the highest market-level margin at **11.14%**.
- **Pacific Asia** has the lowest margin at **10.37%** and the highest observed loss rate at **18.92%**.

This distinction helps separate **scale performance from profitability efficiency**.

---

# 🧮 Core KPIs

The project uses the following profitability measures:

### Total Revenue

Total sales generated across the selected dataset.

### Total Profit

Aggregate profit across order items.

### Profit Margin

Profit relative to sales.

### Customer Value Index

Average profit contribution per customer.

### Category Margin

Arithmetic mean of category-level profit margins.

### Discount Impact Ratio

Relative reduction in profit margin between the no-discount baseline and discounted observations.

These metrics are implemented in the analytical workflow and reflected in the dashboard.

---

# 🔬 Methodology

The project follows a structured analytical workflow:

### 01 — Data Cleaning & Financial Validation

- Missing-value assessment
- Duplicate detection
- Financial consistency checks
- Validation of legitimate negative-profit observations
- Identification of redundant variables
- Verification of discount-related financial fields

### 02 — Revenue & Profit Overview

- Total sales
- Total profit
- Overall profit margin
- Profitability distribution
- Discount-band profitability comparison

### 03 — Product & Category Profitability

- Product-level profitability
- Category-level margin analysis
- Category profit contribution
- Category loss-rate analysis
- High-revenue / low-margin product identification

### 04 — Customer Contribution

- Customer-level sales and profit
- Top and bottom customers
- Loss-making customers
- Customer value tiers
- Customer segment contribution

### 05 — Discount Impact Diagnostics

- Discount-band comparison
- Margin analysis
- Average profit ratio
- Loss-rate analysis
- High-discount category review
- What-if discount scenarios

### 06 — Market & Regional Profit Analysis

- Market-level sales
- Market-level profit
- Profit margins
- Loss rates
- Customer-country analysis
- Regional profitability
- Scale vs. efficiency comparison

---

# 📈 Interactive Dashboard

The project includes a premium interactive **Streamlit dashboard** designed for profitability-focused exploration.

### Dashboard Title

> **APL Logistics — Profitability & Supply Chain Dashboard**

## Dashboard Modules

### 1. Revenue & Profit Overview

Provides an executive-level view of:

- Total Sales
- Total Profit
- Profit Margin
- Customer Value Index
- Category Margin
- Loss-making customers
- Dynamic analytical insights

---

### 2. Customer Value Dashboard

Explores:

- Total customer count
- Average profit per customer
- Top 10 customers by profit
- Bottom 10 customers by profit
- Customer value tiers
- Customer segment contribution
- Loss-making customer analysis
- Top 10 customer profit share

---

### 3. Product & Category Performance

Provides:

- Product-level margin analysis
- Product profitability rankings
- Category profitability
- Category loss-rate analysis
- Category performance heatmap
- High-revenue / low-margin product watchlist
- Reliability thresholds for small-volume groups
- Analytical category risk indicators

> Category Risk Score is an analytical dashboard indicator created for this project and should not be interpreted as an official APL Logistics KPI.

---

### 4. Discount Impact Analyzer

Explores:

- Discount bands
- Discount vs. profit margin
- Average profit ratio
- Loss rates
- Discount Impact Ratio
- High-discount category performance
- What-if discount scenarios

> What-if scenarios are illustrative analytical scenarios. They do not represent predictive forecasts and do not model future demand, elasticity, shipping costs, or other external effects.

---

### 5. Market & Regional Profitability

Analyzes:

- Market-level sales
- Market-level profit
- Profit margins
- Loss rates
- Profit contribution
- Regional profitability
- Customer-country performance
- Scale vs. efficiency

---

# 🎛️ Interactive Filters

The dashboard supports global filtering by:

- **Customer Segment**
- **Category**
- **Product**
- **Market**
- **Order Region**
- **Discount Rate**

The **Product** filter dynamically responds to the selected Category.

A reset option is also provided to return to the complete dataset view.

---

# 🛠️ Technology Stack

### Programming & Analysis

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

### Dashboard

- Streamlit
- Plotly
- Pandas
- NumPy

### Development Environment

- Jupyter Notebook
- VS Code

### Version Control

- Git
- GitHub

---

# 📁 Repository Structure

```text
Project 1/
│
├── dashboard/
│   ├── app.py
│   └── requirements.txt
│
├── data/
│   ├── processed/
│   └── raw/
│       └── APL_Logistics.csv
│
├── notebooks/
│   └── 01_final_dataset_audit.ipynb
│
├── outputs/
│   ├── figures/
│   │   ├── discount_vs_margin.png
│   │   ├── category_profitability.png
│   │   └── high_revenue_low_margin_products.png
│   │
│   └── tables/
│       ├── customer_profitability.csv
│       ├── product_profitability.csv
│       └── market_profitability.csv
│
├── research/
│   ├── Research Paper.pdf
│   └── Executive_Summary.pdf
│
├── src/
│   └── .gitkeep
│
├── .gitignore
└── README.md
```

---

# 📂 Project Artifacts

The repository contains supporting analytical outputs generated from the finalized analysis.

### Figures

- `discount_vs_margin.png`
- `category_profitability.png`
- `high_revenue_low_margin_products.png`

### Analytical Tables

- `customer_profitability.csv`
- `product_profitability.csv`
- `market_profitability.csv`

### Research Documentation

The `research/` directory contains:

- Detailed Research Paper
- Executive Summary for Government Stakeholders

---

# 🧹 Data Quality & Validation

The dataset was audited before analysis.

Key checks included:

- **11 missing values** identified
- **0 duplicate rows**
- No unexpected zero values in audited financial, pricing, and quantity fields
- Legitimate zero-discount observations retained
- Legitimate negative-profit observations retained
- Financial consistency checks performed
- Redundant variables identified
- No currency assumption made because the dataset does not contain a dedicated currency field

The project deliberately preserves legitimate loss-making observations because they are essential to profitability analysis.

---

# 💡 Business Recommendations

Based on the observed profitability patterns:

### 1. Margin-Aware Discount Governance

Monitor discount levels more closely, particularly the **20–25% discount band**, where the observed margin reaches its lowest level.

### 2. Review Loss-Making Customers

The **4,069 loss-making customers** represent a meaningful opportunity for customer-level profitability review.

### 3. Protect High-Profit Products

Products responsible for a large share of total profit should be monitored carefully to avoid profitability concentration risk.

### 4. Investigate High-Revenue / Low-Margin Products

The identified watchlist can support targeted pricing, cost, and commercial review.

### 5. Use Differentiated Market Strategies

- **Europe:** leverage scale while protecting margins.
- **USCA:** learn from stronger margin efficiency.
- **Pacific Asia:** investigate the combination of lower margin and higher loss rate.

### 6. Move Beyond Revenue-Only Reporting

Profitability should be evaluated alongside sales volume when assessing customers, products, categories, and markets.

---

# 🚀 Running the Dashboard Locally

### 1. Clone the repository

```bash
git clone https://github.com/ikalra858-cell/apl-logistics-profitability-analysis
```

### 2. Navigate to the project directory

```bash
cd "Project 1"
```

### 3. Install dashboard dependencies

```bash
pip install -r dashboard/requirements.txt
```

### 4. Launch the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser.

---

# 🌐 Deployed Application

The Streamlit dashboard will be deployed after the final repository setup.

https://apl-logistics-profitability-analysis-fehg9tfpgvoebvwnhmnz96.streamlit.app/

---

# 📄 Research Paper

The detailed research paper is available in the `research/` directory of this repository.

It covers:

- Business problem
- Research objectives
- Dataset and methodology
- Data cleaning and validation
- KPI definitions
- Customer profitability
- Product and category performance
- Discount impact diagnostics
- Market and regional analysis
- Delivery and shipping performance
- Limitations
- Recommendations
- Dashboard implementation
- Conclusion and future scope

---

# 🏛️ Executive Summary

A separate Executive Summary has been prepared for government stakeholders.

It presents the project in a concise, decision-oriented format covering:

- Business problem
- Dataset scope
- Core KPIs
- Key profitability findings
- Customer and product risks
- Discount impact
- Market differences
- Recommendations
- Dashboard value

The Executive Summary is available in the `research/` directory.

---

# 🎥 Project Feedback

The project feedback video will be added as part of the internship submission requirements.

https://youtu.be/4TVMFk8xSE0

---

# 🎓 Internship Context

This project was developed as part of the **Machine Learning Internship at Unified Mentor Private Limited**.

The project applies analytical and machine-learning-oriented thinking to a real-world supply chain profitability problem, with emphasis on:

- Data understanding
- Data validation
- Exploratory analysis
- Business-oriented KPI development
- Profitability diagnostics
- Interactive dashboard development
- Decision-focused communication

---

# ⚠️ Analytical Limitations

The findings should be interpreted within the limitations of the dataset.

### No Time Dimension

The dataset does not contain a dedicated usable order-date field. Therefore, the project does not claim chronological trends.

### Limited Cost Context

There is no dedicated shipping-cost field, so direct shipping-cost impact on profitability cannot be quantified.

### Observational Analysis

The analysis identifies relationships and patterns in the available data. It does not establish causality.

### Currency

The dataset does not provide a dedicated currency field, so monetary values are presented without assuming a specific currency.

### Small Groups

Some product, category, regional, or geographic groups may have relatively low transaction volumes. Reliability thresholds are therefore used where appropriate.

### Customer Tiers

Customer value tiers are analytical quartile-based groupings created for this project and are not official business classifications.

---

# 🔮 Future Scope

Potential extensions include:

- Incorporating time-series data for trend and seasonality analysis
- Adding detailed logistics cost information
- Customer lifetime value modeling
- Predictive customer profitability
- Discount-response modeling
- Profitability forecasting
- Advanced anomaly detection
- Optimization-based pricing and discount recommendations
- Integration with live operational data

---

# 🏁 Conclusion

This project demonstrates how supply chain data can be transformed into actionable profitability intelligence.

The analysis shows that **revenue alone does not provide a complete picture of business performance**. Customer profitability, product concentration, discount levels, category margins, and market efficiency all contribute to understanding the true economic performance of operations.

By combining validated analytical results with an interactive Streamlit dashboard, the project provides a practical framework for exploring **where value is created, where margin pressure exists, and where profitability requires attention**.

> **The objective is not simply to understand how much the business sells, but how profitably it operates.**

---

# 👩‍💻 Author

### Isha Kalra

**BCA 3rd Year**  
Dewan V.S. Group of Institutions, Meerut

**Project:** Customer, Product, and Profitability Performance Analysis in Supply Chain Operations

**Domain:** Supply Chain Analytics | Customer Analytics | Profitability Analysis

---

⭐ If you find this project useful, feel free to explore the analysis, dashboard, and supporting research documentation.