/* 
© 2025 Tejal Katalkar. All rights reserved. https://github.com/Tejalkatalkar
*/

-- Create Tables for storing Customer details
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID VARCHAR(10) PRIMARY KEY,
    Gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(5),
    Dependents VARCHAR(5),
    Tenure INT
);

-- Create Tables for storing Contracts details
CREATE TABLE IF NOT EXISTS Contracts (
    Contract_ID VARCHAR(10) PRIMARY KEY,
	tenure INT,
    CustomerID VARCHAR(10),
    Contract VARCHAR(30),
    PaperlessBilling VARCHAR(5),
    PaymentMethod VARCHAR(50),

    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Create Tables for storing Subscriptions details
CREATE TABLE IF NOT EXISTS Subscriptions (
    CustomerID VARCHAR(10),
    Subscription_ID VARCHAR(10) PRIMARY KEY,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(30),
    OnlineBackup VARCHAR(30),
    DeviceProtection VARCHAR(30),
    TechSupport VARCHAR(30),
    StreamingTV VARCHAR(30),
    StreamingMovies VARCHAR(30),
    
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Create Tables for storing Billing details
CREATE TABLE IF NOT EXISTS Billing (
    CustomerID VARCHAR(10),
    Billing_ID VARCHAR(10) PRIMARY KEY,
    MonthlyCharges DECIMAL(10,2),
    TotalCharges DECIMAL(10,2),

    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Create Tables for storing Churn_table details
CREATE TABLE IF NOT EXISTS Churn_table (
    CustomerID VARCHAR(10),
	Churn_ID VARCHAR(10) PRIMARY KEY,
    Churn VARCHAR(5),
	
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Create Tables for storing fact_customer_churn details
CREATE TABLE fact_customer_churn (
    CustomerID VARCHAR(10),
    Contract_ID VARCHAR(10),
    Billing_ID VARCHAR(10),
    Subscription_ID VARCHAR(10),
    Churn_ID VARCHAR(10),
    MonthlyCharges DECIMAL(10,2),
    TotalCharges DECIMAL(10,2),
    Churn VARCHAR(5),

    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (Contract_ID) REFERENCES Contracts(Contract_ID),
    FOREIGN KEY (Billing_ID) REFERENCES Billing(Billing_ID),
    FOREIGN KEY (Subscription_ID) REFERENCES Subscriptions(Subscription_ID),
    FOREIGN KEY (Churn_ID) REFERENCES Churn_table(Churn_ID)
);

-- Import data into Customers table
COPY Customers(CustomerID, Gender, SeniorCitizen, Partner, Dependents, Tenure)
FROM 'D:/Telco_Customer_Churn_Analysis/Customers.csv'
DELIMITER ','
CSV HEADER;

-- Import data into Contracts table
COPY Contracts(Contract_ID, tenure, CustomerID, Contract, PaperlessBilling, PaymentMethod)
FROM 'D:\Telco_Customer_Churn_Analysis\Contracts.csv'
DELIMITER ','
CSV HEADER;

-- Import data into Subscriptions Table
COPY Subscriptions(CustomerID, Subscription_ID, PhoneService, MultipleLines, InternetService, OnlineSecurity,
    OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies)
FROM 'D:\Telco_Customer_Churn_Analysis\Subscriptions.csv'
DELIMITER ','
CSV HEADER;

-- Import data into Billing Table
COPY Billing (CustomerID, Billing_ID, MonthlyCharges, TotalCharges)
FROM 'D:\Telco_Customer_Churn_Analysis\Billing.csv'
DELIMITER ','
CSV HEADER;

-- Import data into Churn_table
COPY Churn_table(CustomerID, Churn_ID, Churn)
FROM 'D:\Telco_Customer_Churn_Analysis\Churn_Tabels.csv'
DELIMITER ','
CSV HEADER;

-- Import data into fact_customer_churn Table
COPY fact_customer_churn(CustomerID, Contract_ID, Billing_ID, Subscription_ID, Churn_ID, MonthlyCharges, TotalCharges, Churn)
FROM 'D:\Telco_Customer_Churn_Analysis\Fact_Customer_Churn.csv .csv'
DELIMITER ','
CSV HEADER;

-- Basic SQL Queries
SELECT * FROM Customers;
SELECT * FROM Contracts;
SELECT * FROM Subscriptions;
SELECT * FROM Billing;
SELECT * FROM Churn_table;
SELECT * FROM fact_customer_churn;

-- Select specific columns
SELECT CustomerID, Gender FROM Customers;

-- Filters rows using where clause 
-- Customers with tenure less than 12 months
SELECT CustomerID, Tenure, Partner
FROM Customers
WHERE Tenure < 12;

-- Customers with tenure more than 12 months
SELECT CustomerID, Tenure, Partner
FROM Customers
WHERE Tenure > 12;

SELECT CustomerID, Internetservice
FROM subscriptions
WHERE Internetservice = 'DSL';

SELECT CustomerID, churn
FROM churn_table
WHERE churn = 'Yes';

-- Filter with multiple conditions
SELECT CustomerID
FROM Subscriptions
WHERE streamingtv = 'Yes' OR streamingmovies = 'Yes';

-- IN, BETWEEN, NOT IN, LIKE Operators
SELECT CustomerID, PaymentMethod
FROM Contracts
WHERE PaymentMethod IN ('Electronic check', 'Mailed check');

SELECT CustomerID, Contract
FROM Contracts
WHERE Contract NOT IN ('Month-to-month');

SELECT CustomerID, MonthlyCharges
FROM Billing
WHERE MonthlyCharges BETWEEN 30 AND 60;

SELECT CustomerID, PaymentMethod
FROM Contracts
WHERE PaymentMethod LIKE '%check%';

-- Aggregate Functions
-- Total Subscriptions
SELECT COUNT(*) AS Total_Subscriptions
FROM Subscriptions;

-- Total revenue collected & Average Monthly Charges
SELECT SUM(TotalCharges) AS Total_Revenue,AVG(MonthlyCharges) AS Avg_MonthlyCharges
FROM Billing;

-- Minimum Tenure & Maximum Tenure
SELECT MIN(Tenure) AS Min_Tenure,MAX(Tenure) AS Min_Tenure
FROM Customers;

-- Sorting results
SELECT CustomerID, MonthlyCharges
FROM Billing
ORDER BY MonthlyCharges;

SELECT CustomerID, MonthlyCharges
FROM Billing
ORDER BY MonthlyCharges DESC;

-- Each Contract with all PaymentMethods
SELECT contract,
       STRING_AGG(paymentmethod, ', ') AS paymentmethods
FROM contracts
GROUP BY contract;

-- Display a Limited number of records
SELECT * FROM Billing
LIMIT 5;

-- Get customer and Contract details with Inner Join 
SELECT 
    c.customerid, c.gender, c.partner,
    ct.contract, ct.paymentmethod
FROM customers c
INNER JOIN contracts ct
ON c.customerid = ct.customerid;
















