/* 
© 2025 Tejal Katalkar. All rights reserved. https://github.com/Tejalkatalkar
*/

-- Note:- 
-- Teure : How long a customer has been using the service.
-- Contract : how long the contract has been active.
-- Churn : Whether a customer left the company or not.

-- Business Questions: 
-- 1.Total number of customers
SELECT DISTINCT COUNT(*) AS Total_Customers
FROM Customers;

-- 2.Total male vs female customers 
SELECT Gender, count(*) as Total
FROM Customers
GROUP BY Gender;

-- 3.Check null values in each column
SELECT 
    SUM(CASE WHEN PhoneService IS NULL THEN 1 END) AS null_count
FROM Subscriptions;

-- 4.Calculate mean (Average) tenure of customers
SELECT AVG(Tenure) AS Avg_Tenure
FROM Customers;

-- 5.Calculate standard deviation MonthlyCharges of customers
SELECT STDDEV(MonthlyCharges) AS stddev_monthly_charges
FROM Billing;

-- 6.Average Churn rate of the Customers
SELECT 
    AVG(CASE WHEN Churn = 'Yes' 
	THEN 1 ELSE 0 END) AS churn_rate
FROM fact_customer_churn;

-- 7.Total Total churn vs active Customers
SELECT 
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN churn = 'No'  THEN 1 ELSE 0 END) AS active_customers,
    COUNT(*) AS Total_Customers
FROM Churn_Table;

-- 8.Most used contract type
SELECT contract, COUNT(*) AS total
FROM contracts
GROUP BY contract
ORDER BY total DESC
LIMIT 1;

-- 9.Most popular payment method
SELECT paymentmethod, COUNT(*) AS total
FROM contracts
GROUP BY paymentmethod
ORDER BY total DESC
LIMIT 1;

-- 10.payment methods with more than 1 customer
SELECT 
    paymentmethod,
    COUNT(*) AS total_customers
FROM contracts
GROUP BY paymentmethod
HAVING COUNT(*) > 1;

-- 11.Charges category based on Total Charges of customers
SELECT 
    CustomerID,
    SUM(TotalCharges) AS total_charges,
    CASE
        WHEN SUM(TotalCharges) > 2500 THEN 'High Total_Charges'
        ELSE 'Low Total_Charges'
    END AS charges_category
FROM Billing
GROUP BY CustomerID;

-- Customer Service Analysis
-- 12.customers with no phone service
SELECT Count(CustomerID) AS Unavailable_PhoneService
FROM Subscriptions
WHERE PhoneService = 'No';

-- 13.Customer with highest monthly charges
SELECT CustomerID, monthlycharges
FROM Billing
ORDER BY monthlycharges DESC
LIMIT 1;

-- 14.Customers with duplicate payment methods
SELECT paymentmethod, COUNT(*)
FROM contracts
GROUP BY paymentmethod
HAVING COUNT(*) > 1;

-- WINDOW FUNCTIONS
-- 15.Rank customers by monthly charges
SELECT 
    customerid,
    monthlycharges,
    DENSE_RANK() OVER (ORDER BY monthlycharges DESC) AS rank_no
FROM Billing;

-- 16.Customers whose monthly charges increased (Window Lag Example)
SELECT 
    customerid,
    monthlycharges,
    LAG(monthlycharges) OVER (PARTITION BY customerid ORDER BY billing_id) AS last_month,
    monthlycharges - LAG(monthlycharges) OVER (PARTITION BY customerid ORDER BY billing_id) AS diff
FROM billing;

-- Tech support analysis
-- 17.Find customers who have not taken Tech Support 
SELECT 	
    customerid,
    techsupport,
    CASE 
        WHEN techsupport = 'No' THEN 'Needs Support'
        ELSE 'Support Active'
    END AS support_status
FROM subscriptions;

-- Joins 
-- 18.INNER JOIN – Full customer profile
SELECT c.customerid, gender, tenure, monthlycharges, churn
FROM customers c
JOIN billing b USING(customerid)
JOIN churn_table ch USING(customerid);

-- 19.High-value customers 
SELECT c.customerid, c.tenure, b.totalcharges
FROM Customers c
RIGHT JOIN Billing b USING (customerid)
WHERE c.tenure > 24 AND b.totalcharges > 1000;

-- 20.FULL JOIN – Combine all customers & billing
SELECT c.customerid, b.billing_id
FROM customers c
FULL OUTER JOIN billing b USING(customerid);

-- 21.Fact table: full customer profile from all dimensions
SELECT 
    f.customerid,
    c.gender,
    ct.contract,
    s.internetservice,
    b.monthlycharges,
    ch.churn
FROM fact_customer_churn f
JOIN customers c USING(customerid)
JOIN contracts ct USING(contract_id)
JOIN subscriptions s USING(subscription_id)
JOIN billing b USING(billing_id)
JOIN churn_table ch USING(churn_id);

-- CTEs & SUBQUERIES 
-- 22.Customers with more than average monthly charges
WITH avg_val AS (
    SELECT AVG(monthlycharges) AS avg_charges
    FROM billing
)

SELECT customerid, monthlycharges
FROM billing, avg_val
WHERE monthlycharges > avg_val.avg_charges;

-- VIEW
-- 23.Create a view of high-value customers
CREATE VIEW high_value_customers AS
SELECT customerid, monthlycharges
FROM billing
WHERE monthlycharges > 100;

-- Use the view like a table (read the view)
SELECT * FROM high_value_customers;

-- CHURN vs CHARGES SEGMENTATION
-- 24.Does higher MonthlyCharges lead to higher churn?
SELECT 
    CASE 
        WHEN monthlycharges < 40 THEN 'Low'
        WHEN monthlycharges BETWEEN 40 AND 70 THEN 'Medium'
        ELSE 'High'
    END AS charge_segment,
    COUNT(*) AS total,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned,
    ROUND(
        100.0 * COUNT(CASE WHEN churn = 'Yes' THEN 1 END) / COUNT(*), 2
    ) AS churn_rate
FROM billing b
JOIN churn_table ch USING(customerid)
GROUP BY charge_segment;

-- 25.LIFETIME VALUE CALCULATION
SELECT 
    c.customerid,
    b.monthlycharges,
    c.tenure,
    (b.monthlycharges * c.tenure) AS lifetime_value
FROM customers c
JOIN billing b USING(customerid);
