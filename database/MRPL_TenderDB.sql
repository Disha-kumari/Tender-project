CREATE DATABASE Tender_MRPL;

USE Tender_MRPL;


CREATE TABLE Users
(
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(30) NOT NULL,
    email VARCHAR(100) NOT NULL
);


CREATE TABLE Departments
(
    department_id INT IDENTITY(1,1) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE Tenders
(
    tender_id INT IDENTITY(1,1) PRIMARY KEY,
    tender_number VARCHAR(20) NOT NULL UNIQUE,
    tender_name VARCHAR(200) NOT NULL,
    department_id INT NOT NULL,
    description VARCHAR(500),
    estimated_cost DECIMAL(18,2),
    tender_date DATE,
    closing_date DATE,
    status VARCHAR(20),

    FOREIGN KEY (department_id)
    REFERENCES Departments(department_id)
);


CREATE TABLE Item_Master
(
    item_id INT IDENTITY(1,1) PRIMARY KEY,
    item_code VARCHAR(20) NOT NULL UNIQUE,
    item_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    specification VARCHAR(250),
    unit VARCHAR(20)
);



CREATE TABLE Tender_Items
(
    tender_item_id INT IDENTITY(1,1) PRIMARY KEY,
    tender_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity DECIMAL(10,2),
    estimated_rate DECIMAL(18,2),
    estimated_amount DECIMAL(18,2),

    FOREIGN KEY (tender_id)
        REFERENCES Tenders(tender_id),

    FOREIGN KEY (item_id)
        REFERENCES Item_Master(item_id)
);


CREATE TABLE Vendors
(
    vendor_id INT IDENTITY(1,1) PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    GST_number VARCHAR(20),
    PAN_number VARCHAR(20),
    address VARCHAR(250)
);



CREATE TABLE Vendor_Quotations
(
    quotation_id INT IDENTITY(1,1) PRIMARY KEY,
    tender_item_id INT NOT NULL,
    vendor_id INT NOT NULL,
    quoted_rate DECIMAL(18,2),
    GST DECIMAL(5,2),
    freight DECIMAL(18,2),
    discount DECIMAL(18,2),
    total_amount DECIMAL(18,2),
    quotation_date DATE,

    FOREIGN KEY (tender_item_id)
        REFERENCES Tender_Items(tender_item_id),

    FOREIGN KEY (vendor_id)
        REFERENCES Vendors(vendor_id)
);


CREATE TABLE Commercial_Evaluation
(
    evaluation_id INT IDENTITY(1,1) PRIMARY KEY,
    tender_id INT NOT NULL,
    vendor_id INT NOT NULL,
    grand_total DECIMAL(18,2),
    overall_rank VARCHAR(10),
    evaluation_date DATE,

    FOREIGN KEY (tender_id)
        REFERENCES Tenders(tender_id),

    FOREIGN KEY (vendor_id)
        REFERENCES Vendors(vendor_id)
);


CREATE TABLE Item_Wise_Evaluation
(
    item_eval_id INT IDENTITY(1,1) PRIMARY KEY,
    tender_item_id INT NOT NULL,
    vendor_id INT NOT NULL,
    lowest_price DECIMAL(18,2),
    evaluation_date DATE,

    FOREIGN KEY (tender_item_id)
        REFERENCES Tender_Items(tender_item_id),

    FOREIGN KEY (vendor_id)
        REFERENCES Vendors(vendor_id)
);


CREATE TABLE Negotiation
(
    negotiation_id INT IDENTITY(1,1) PRIMARY KEY,
    tender_item_id INT NOT NULL,
    vendor_id INT NOT NULL,
    original_price DECIMAL(18,2),
    negotiated_price DECIMAL(18,2),
    final_price DECIMAL(18,2),
    negotiation_status VARCHAR(30),

    FOREIGN KEY (tender_item_id)
        REFERENCES Tender_Items(tender_item_id),

    FOREIGN KEY (vendor_id)
        REFERENCES Vendors(vendor_id)
);


CREATE TABLE Reports
(
    report_id INT IDENTITY(1,1) PRIMARY KEY,
    tender_id INT NOT NULL,
    user_id INT NOT NULL,
    generated_date DATE,
    report_file VARCHAR(255),

    FOREIGN KEY (tender_id)
        REFERENCES Tenders(tender_id),

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
);



INSERT INTO Departments (department_name)
VALUES
('Mechanical'),
('Electrical'),
('Instrumentation'),
('Civil'),
('Safety');

SELECT * FROM Departments;

INSERT INTO Users
(username,password,full_name,role,email)
VALUES
('admin','admin123','System Administrator','Admin','admin@mrpl.co.in'),

('procurement1','proc123','Rakesh Kumar','Procurement Officer','rakesh@mrpl.co.in'),

('engineer1','eng123','Anjali Rao','Engineer','anjali@mrpl.co.in');

SELECT * FROM Users;



INSERT INTO Vendors
(company_name, contact_person, phone, email, GST_number, PAN_number, address)

VALUES

('Tata Projects Ltd.','Rajesh Sharma','9876543210','sales@tataprojects.com','29ABCDE1234F1Z5','ABCDE1234F','Mumbai, Maharashtra'),

('Larsen & Toubro Ltd.','Amit Patel','9876543211','sales@larsentoubro.com','29ABCDE1234F2Z6','ABCDE1234G','Chennai, Tamil Nadu'),

('BHEL','Suresh Rao','9876543212','sales@bhel.com','29ABCDE1234F3Z7','ABCDE1234H','Hyderabad, Telangana'),

('Kirloskar Brothers Ltd.','Kiran Shetty','9876543213','sales@kbl.com','29ABCDE1234F4Z8','ABCDE1234J','Pune, Maharashtra'),

('Thermax Ltd.','Deepak Nair','9876543214','sales@thermax.com','29ABCDE1234F5Z9','ABCDE1234K','Pune, Maharashtra'),

('Siemens Ltd.','Vinay Gupta','9876543215','sales@siemens.com','29ABCDE1234F6Z1','ABCDE1234L','Bengaluru, Karnataka'),

('ABB India Ltd.','Arun Kumar','9876543216','sales@abb.com','29ABCDE1234F7Z2','ABCDE1234M','Bengaluru, Karnataka'),

('KEC International Ltd.','Rohan Singh','9876543217','sales@kec.com','29ABCDE1234F8Z3','ABCDE1234N','Mumbai, Maharashtra'),

('ISGEC Heavy Engineering Ltd.','Manoj Verma','9876543218','sales@isgec.com','29ABCDE1234F9Z4','ABCDE1234P','Yamunanagar, Haryana'),

('Jyoti Ltd.','Nitin Joshi','9876543219','sales@jyoti.com','29ABCDE1234F0Z5','ABCDE1234Q','Vadodara, Gujarat'),

('Bharat Forge Ltd.','Prakash Kulkarni','9876543220','sales@bharatforge.com','29ABCDE1234F1Z6','ABCDE1234R','Pune, Maharashtra'),

('Godrej & Boyce Mfg. Co. Ltd.','Sanjay Deshmukh','9876543221','sales@godrej.com','29ABCDE1234F2Z7','ABCDE1234S','Mumbai, Maharashtra'),

('Emerson Process Management India Pvt. Ltd.','Rahul Menon','9876543222','sales@emerson.com','29ABCDE1234F3Z8','ABCDE1234T','Pune, Maharashtra'),

('Honeywell Automation India Ltd.','Ajay Verma','9876543223','sales@honeywell.com','29ABCDE1234F4Z9','ABCDE1234U','Pune, Maharashtra'),

('Flowserve India Controls Pvt. Ltd.','Ramesh Iyer','9876543224','sales@flowserve.com','29ABCDE1234F5Z1','ABCDE1234V','Bengaluru, Karnataka');

SELECT * FROM Vendors;

INSERT INTO Item_Master
(item_code, item_name, category, specification, unit)

VALUES

('ITM001','Carbon Steel Pipe','Piping','ASTM A106 Grade B','Nos'),

('ITM002','Gate Valve','Valve','Class 150','Nos'),

('ITM003','Ball Valve','Valve','Stainless Steel','Nos'),

('ITM004','Butterfly Valve','Valve','Cast Iron','Nos'),

('ITM005','Pressure Gauge','Instrumentation','0-10 Bar','Nos'),

('ITM006','Centrifugal Pump','Pump','15 HP','Nos'),

('ITM007','Flange','Piping','Weld Neck','Nos'),

('ITM008','Gasket','Piping','Spiral Wound','Nos'),

('ITM009','Pipe Elbow','Piping','90 Degree','Nos'),

('ITM010','Pipe Reducer','Piping','Concentric','Nos');

SELECT * FROM Item_Master;


INSERT INTO Tenders
(
    tender_number,
    tender_name,
    department_id,
    description,
    estimated_cost,
    tender_date,
    closing_date,
    status
)

VALUES

(
    'MRPL001',
    'Carbon Steel Pipe Procurement',
    1,
    'Procurement of Carbon Steel Pipes and related accessories for Mechanical Maintenance Department.',
    24500000.00,
    '2026-07-01',
    '2026-07-20',
    'Open'
),

(
    'MRPL002',
    'Fire Water Pump Procurement',
    5,
    'Procurement of Fire Water Pumps and associated accessories for Safety Department.',
    19000000.00,
    '2026-07-05',
    '2026-07-25',
    'Open'
);

SELECT * FROM Tenders;


INSERT INTO Tender_Items
(tender_id, item_id, quantity, estimated_rate, estimated_amount)

VALUES

(1,1,100,5000,500000),

(1,2,50,3500,175000),

(1,3,60,4200,252000),

(1,4,40,3800,152000),

(1,5,25,2500,62500),

(1,6,10,85000,850000),

(1,7,80,1500,120000),

(1,8,100,250,25000),

(1,9,60,900,54000),

(1,10,30,1200,36000);

INSERT INTO Tender_Items
(tender_id, item_id, quantity, estimated_rate, estimated_amount)

VALUES

(2,1,80,5100,408000),

(2,2,30,3600,108000),

(2,3,40,4300,172000),

(2,4,25,3900,97500),

(2,5,20,2600,52000),

(2,6,8,90000,720000),

(2,7,60,1600,96000),

(2,8,80,260,20800),

(2,9,50,950,47500),

(2,10,25,1250,31250);

SELECT * FROM Tender_Items;


INSERT INTO Vendor_Quotations
(
    tender_item_id,
    vendor_id,
    quoted_rate,
    GST,
    freight,
    discount,
    total_amount,
    quotation_date
)

SELECT

    ti.tender_item_id,

    v.vendor_id,

    -- Different quoted rate for every vendor
    (ti.estimated_rate +
CASE (v.vendor_id % 5)
    WHEN 0 THEN -40
    WHEN 1 THEN 20
    WHEN 2 THEN -15
    WHEN 3 THEN 55
    ELSE 10
END) AS quoted_rate,

    -- GST
    18.00,

    -- Freight
    (500 + (v.vendor_id * 20)),

    -- Discount
    (v.vendor_id * 30),

    -- Total Amount
(
    (
        ti.quantity *
        (
            ti.estimated_rate +
            CASE (v.vendor_id % 5)
                WHEN 0 THEN -40
                WHEN 1 THEN 20
                WHEN 2 THEN -15
                WHEN 3 THEN 55
                ELSE 10
            END
        )
    )
    +
    (
        (
            ti.quantity *
            (
                ti.estimated_rate +
                CASE (v.vendor_id % 5)
                    WHEN 0 THEN -40
                    WHEN 1 THEN 20
                    WHEN 2 THEN -15
                    WHEN 3 THEN 55
                    ELSE 10
                END
            )
        ) * 18 / 100
    )
    +
    (500 + (v.vendor_id * 20))
    -
    (v.vendor_id * 30)
),
    '2026-07-10'

FROM Tender_Items ti

CROSS JOIN Vendors v

ORDER BY
ti.tender_item_id,
v.vendor_id;


SELECT COUNT(*) AS Total_Quotations
FROM Vendor_Quotations;


--Check the first few records:
--SELECT TOP 20 *
--FROM Vendor_Quotations
--ORDER BY tender_item_id, vendor_id;

/* ==========================================================
   MRPL Tender Commercial Evaluation System
   View All Tables
   ========================================================== */
   use Tender_MRPL;
------------------------------------------------------------
USE Tender_MRPL;

DELETE FROM Negotiation;
DELETE FROM Item_Wise_Evaluation;
DELETE FROM Commercial_Evaluation;
DELETE FROM Vendor_Quotations;


SELECT v.company_name, ti.tender_item_id, vq.quoted_rate
FROM Vendor_Quotations vq
JOIN Vendors v ON v.vendor_id = vq.vendor_id
JOIN Tender_Items ti ON ti.tender_item_id = vq.tender_item_id
ORDER BY ti.tender_item_id, vq.quoted_rate ASC


-- Randomize quoted_rate per vendor per item, then recompute total_amount
-- using each row's actual GST/freight/discount so totals stay consistent.

UPDATE vq
SET
    vq.quoted_rate = ROUND(
        vq.quoted_rate * (0.92 + (CAST(CHECKSUM(NEWID()) & 0x7FFFFFFF AS FLOAT) / 2147483647.0) * 0.16),
        2
    )
FROM Vendor_Quotations vq;

-- Recompute total_amount to match the new quoted_rate for every row
UPDATE vq
SET
    vq.total_amount = ROUND(
        (vq.quoted_rate * ti.quantity)
        + (vq.quoted_rate * ti.quantity * vq.GST / 100)
        + vq.freight
        - vq.discount,
        2
    )
FROM Vendor_Quotations vq
INNER JOIN Tender_Items ti
    ON ti.tender_item_id = vq.tender_item_id;


	SELECT v.company_name, ti.tender_item_id, vq.quoted_rate
FROM Vendor_Quotations vq
JOIN Vendors v ON v.vendor_id = vq.vendor_id
JOIN Tender_Items ti ON ti.tender_item_id = vq.tender_item_id
ORDER BY ti.tender_item_id, vq.quoted_rate ASC


