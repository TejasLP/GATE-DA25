CREATE DATABASE IF NOT EXISTS bank_db;
USE bank_db;

DROP TABLE IF EXISTS Loan;
CREATE TABLE Loan (
    loan_number VARCHAR(10) PRIMARY KEY,
    branch_name VARCHAR(50) NOT NULL,
    amount INT NOT NULL
);

INSERT INTO Loan (loan_number, branch_name, amount) VALUES
('L11', 'Banjara Hills', 90000),
('L14', 'Kondapur', 50000),
('L15', 'SR Nagar', 40000),
('L22', 'SR Nagar', 25000),
('L23', 'Balanagar', 80000),
('L25', 'Kondapur', 70000),
('L19', 'SR Nagar', 65000);

SELECT L1.loan_number
FROM Loan L1
WHERE L1.amount > (
    SELECT MAX(L2.amount)
    FROM Loan L2
    WHERE L2.branch_name = 'SR Nagar'
);
