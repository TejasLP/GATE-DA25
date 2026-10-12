CREATE DATABASE IF NOT EXISTS bank_db_div;
USE bank_db_div;

DROP TABLE IF EXISTS Borrower;
DROP TABLE IF EXISTS Loan;

-- Create Loan table[cite: 7]
CREATE TABLE Loan (
    loan_num VARCHAR(10) PRIMARY KEY,
    branch_name VARCHAR(50) NOT NULL,
    amount INT NOT NULL
);

-- Create Borrower table[cite: 7]
CREATE TABLE Borrower (
    customer_name VARCHAR(50) NOT NULL,
    loan_num VARCHAR(10) NOT NULL
);

-- Insert data into Loan table[cite: 7]
INSERT INTO Loan (loan_num, branch_name, amount) VALUES
('L11', 'Banjara Hills', 90000),
('L14', 'Kondapur', 50000),
('L15', 'SR Nagar', 40000),
('L22', 'SR Nagar', 25000),
('L23', 'Balanagar', 80000),
('L25', 'Kondapur', 70000),
('L19', 'SR Nagar', 65000);

-- Insert data into Borrower table[cite: 7]
INSERT INTO Borrower (customer_name, loan_num) VALUES
('Anand', 'L11'),
('Karteek', 'L11'),
('Karteek', 'L14'),
('Ankita', 'L15'),
('Gopal', 'L19'),
('Karteek', 'L22'),
('Karteek', 'L23'),
('Sunil', 'L23'),
('Sunil', 'L25');

-- Equivalent SQL query for the relational algebra division expression[cite: 7]
SELECT customer_name
FROM (
    SELECT DISTINCT b.customer_name, l.branch_name
    FROM Borrower b
    JOIN Loan l ON b.loan_num = l.loan_num
) AS customer_branches
GROUP BY customer_name
HAVING COUNT(DISTINCT branch_name) = (
    SELECT COUNT(DISTINCT branch_name) FROM Loan
);
