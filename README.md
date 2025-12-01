# 📡 Telco Customer Churn Analysis  
### End-to-End Data Analytics + Machine Learning + Streamlit App + PostgreSQL Star Schema

This project performs **complete churn analysis** for a telecom company using  
**Python, Machine Learning, Streamlit, PostgreSQL, and Power BI/Tableau**.
It covers the full data lifecycle — **EDA, data cleaning, modeling, dashboards, database schema design, and deployment**.



Try the live application here:
👉 

🚀 Live Demo: https://telcocustomerchurnanalysis-tejal.streamlit.app/
---

## 🚀 **Project Overview**

Customer churn is one of the biggest challenges for telecom companies.  
This project identifies **key churn drivers**, builds a **predictive ML model**, and offers **interactive dashboards** through a **Streamlit web app**.

You also designed a **Star Schema** and stored the cleaned dataset inside **PostgreSQL** for analytical querying.

---

## ✔ **Key Features**

### 🔹 **1. Data Cleaning & EDA**
- Handled missing values & outliers  
- Converted data types  
- Visualized patterns (churn %, tenure, monthly charges, contract type)  
- Feature correlations & insights  
- Exported cleaned data for modeling  

### 🔹 **2. Machine Learning Model**
- Train/Test split  
- Logistic Regression / Random Forest / XGBoost (choose based on performance)  
- Evaluation metrics: Accuracy, Precision, Recall, F1, ROC-AUC  
- Feature importance analysis  
- Model saved as `.pkl`

### 🔹 **3. Streamlit Application**
A fully interactive app with:

📊 **Dashboard:**  
- Churn distribution  
- Churn by contract  
- Monthly charges density  
- Tenure histogram  
- KPIs  

🤖 **Prediction Page:**  
- Enter customer details  
- Predict whether customer is at churn risk  
- Shows risk percentage  

📈 **Risk Analysis:**  
- Top churn indicators  
- High-risk customer segments  
- Insights summary  

🎨 **Custom UI:**  
- Top navigation bar  
- Styled sidebar  
- Card-style visual containers  

---

## 🏛 **4. PostgreSQL Star Schema**
### ⭐ Fact Table:
`fact_churn`  
- customer_id  
- tenure  
- monthly_charges  
- total_charges  
- churn_flag  
- contract_id  
- payment_id  
- internet_id  

### ⭐ Dimension Tables:
- `customers_Data`
- `contracts`
- `Subscriptions`
- `Billing`
- `Churn_Tables`
- 'Fact_Customer_Analysis_Dataset'

Benefits:
- Supports OLAP-style queries  
- Enables Power BI/Tableau dashboards  
- Faster aggregations  
- Clean separation between facts & dimensions  

---

## 📂 **Project Structure**

Telco-Customer-Churn/
│

├── CSV Data/
│ └── cleaned_telco_data.csv
│

├── notebooks/
│ ├── EDA.ipynb
│ ├── Data_Cleaning.ipynb
│ └── Model_Training.ipynb
│

├── streamlit_app/
│ ├── app.py
│ ├── model.pkl
│ ├── styles.css
│ └── utils.py
│
├── sql/
│ ├── star_schema.sql
│ ├── create_tables.sql
│ └── business_queries.sql
│

├── ERD_Diagram.png
├── requirements.txt
└── README.md

## 🛠 **Tech Stack Used**

### **Languages & Libraries**
- Python  
- Pandas, NumPy  
- Matplotlib, Seaborn  
- Scikit-Learn  
- Plotly  
- Streamlit  

### **Database**
- PostgreSQL  
- pgAdmin  
- Star Schema (Fact + Dimension tables)

### **Deployment**
- Streamlit  
- GitHub  

---

## 📈 **Business Insights (From Analysis)**

- Customers with **month-to-month contracts** churn the most  
- Higher churn among customers with **electronic check payment**  
- **Low tenure customers (< 12 months)** are high-risk  
- High churn for users with **Fiber optic internet**  
- **High monthly charges** strongly correlate with churn  

---

## ▶️ **How to Run the Project**

### **1. Clone the repository**
```bash
git clone https://github.com/your-username/Telco-Customer-Churn.git
cd Telco-Customer-Churn

2. Install dependencies
pip install -r requirements.txt

3. Run Streamlit App
streamlit run streamlit_app/app.py

4. Setup PostgreSQL (Optional)
psql -U postgres -f sql/star_schema.sql

✅ Conclusion
This end-to-end Telco Customer Churn project identifies key churn drivers using data cleaning, EDA, SQL star schema modeling, machine learning, and interactive dashboards. The Streamlit app enables churn prediction and visual analysis, while the Power BI dashboard provides business-friendly insights into customer behavior, trends, and high-risk segments. Overall, the project offers a complete, scalable solution that helps telecom companies understand churn patterns and take data-driven retention actions.
