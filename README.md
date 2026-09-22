# MRPL Tender Commercial Evaluation System

A web-based application developed to streamline and automate the **commercial evaluation of procurement tenders** by managing tenders, vendors, quotations, commercial comparisons, negotiations, and report generation through a centralized system.

---

## 📌 About the Project

The **MRPL Tender Commercial Evaluation System** was developed as an internship project at **Mangalore Refinery and Petrochemicals Limited (MRPL)**.

Traditional tender commercial evaluation involves manually comparing quotations from multiple vendors, calculating commercial values, identifying the lowest commercial bidder (L1), maintaining negotiation records, and preparing evaluation reports. These activities can be time-consuming and prone to calculation and data-entry errors.

This project provides a centralized web-based platform to digitize these activities and maintain procurement information in a structured **Microsoft SQL Server** database.

---

## 🎯 Objectives

- Centralize tender, vendor, quotation, evaluation, and report information.
- Reduce manual effort involved in commercial evaluation.
- Automate quotation comparison and commercial calculations.
- Identify the lowest commercial bidder (L1).
- Maintain negotiation and evaluation records.
- Generate commercial evaluation reports in PDF format.
- Provide an interactive dashboard for monitoring procurement activities.

---

## ✨ Key Features

### 🔐 User Authentication
Secure login functionality for authorized users.

### 📋 Tender Management
Create and manage tender details including tender number, department, estimated cost, tender dates, and status.

### 🏢 Vendor Management
Maintain vendor information including company details, contact information, GST number, and other relevant details.

### 📦 Tender Item Management
Manage tender items, quantities, and estimated costs.

### 📄 Vendor Quotation Management
Store and manage vendor quotations and item-wise quoted rates.

### 📊 Commercial Evaluation
Automatically perform:

- Item-wise quotation comparison
- Commercial total calculation
- GST calculation
- Freight addition
- Discount deduction
- Grand Total calculation
- Vendor ranking
- L1 vendor identification

### 🤝 Negotiation Management
Maintain negotiation details and final negotiated prices.

### 📈 Dashboard
Display important procurement statistics such as:

- Total Departments
- Total Tenders
- Total Vendors
- Total Quotations
- Total Reports
- Tender Status

### 📑 Report Generation
Generate commercial evaluation reports in PDF format containing tender details, vendor information, quotation details, commercial calculations, and final totals.

---

## 🔄 System Workflow

```text
Login
   ↓
Dashboard
   ↓
Tender Selection
   ↓
Tender & Item Management
   ↓
Vendor Quotation Management
   ↓
Quotation Verification
   ↓
Commercial Evaluation
   ↓
Vendor Comparison & Ranking
   ↓
Negotiation
   ↓
Report Generation
🛠️ Technology Stack
Technology	Purpose
Python	Programming Language
Flask	Backend Framework
HTML5	Frontend Structure
CSS3	Styling
Bootstrap	Responsive UI
JavaScript	Client-side Functionality
Microsoft SQL Server	Database
PyODBC	Database Connectivity
ReportLab	PDF Generation
SQL Server Management Studio	Database Management
Visual Studio Code	Development Environment
🗄️ Database Design

The application uses Microsoft SQL Server as its relational database.

Major Tables
Users
Departments
Tenders
Item_Master
Tender_Items
Vendors
Vendor_Quotations
Commercial_Evaluation
Item_Wise_Evaluation
Negotiation
Reports

Foreign-key relationships are used to maintain referential integrity between related entities.

📁 Project Structure
Tender-project/
│
├── database/
├── PDFs_MRPL001/
├── PDFs_MRPL002/
├── reports/
├── static/
├── templates/
├── uploads/
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/Disha-kumari/Tender-project.git
2. Navigate to the Project Directory
cd Tender-project
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment

Windows:

venv\Scripts\activate
5. Install Dependencies
pip install -r requirements.txt
6. Configure SQL Server

Update the database connection settings in:

config.py

Ensure that the required Microsoft SQL Server database is available and accessible.

7. Run the Application
python app.py

Open the local Flask server URL displayed in the terminal to access the application.

📊 Project Testing

The application was tested using sample procurement data consisting of:

2 Tenders
MRPL001 – Carbon Steel Pipe Procurement
MRPL002 – Fire Water Pump Procurement
15 Vendors
10 Tender Items
30 Vendor Quotation PDFs
15 quotations for MRPL001
15 quotations for MRPL002

The system successfully performed quotation storage, commercial comparison, vendor ranking, L1 identification, and PDF report generation.

📄 Generated Reports

The system generates PDF reports containing:

Tender Information
Vendor Details
Item-wise Quotations
Commercial Calculations
GST
Freight
Discount
Grand Total
Delivery Period
Payment Terms
Authorized Signatory
🚀 Future Enhancements

The system can be further extended with:

ERP/SAP integration
Online vendor registration and approval
Automated email and SMS notifications
Digital signature support
OCR-based quotation data extraction
AI/ML-based vendor analysis
Advanced analytics and business intelligence dashboards
Mobile application support
Cloud deployment
Enhanced role-based access control
Integration with e-procurement platforms
⚠️ Current Limitations
The current implementation focuses primarily on the commercial evaluation stage.
The application currently operates in a local server environment.
ERP/SAP integration is not included.
Email and SMS notifications are not integrated.
Digital signatures and electronic approvals are not supported.
Online payment processing is not included.
The system requires a predefined vendor quotation structure for PDF data extraction.
👥 Project Team
Name	USN	Branch
Disha Kumari	NNM24IS074	Information Science and Engineering
Disha Naveen	NNM24IS075	Information Science and Engineering
Disha S Rao	NNM24IS076	Information Science and Engineering
Esha P Puthran	NNM24IS082	Information Science and Engineering
🏢 Internship

Mangalore Refinery and Petrochemicals Limited (MRPL)
Information Systems Department

Project: Tender Commercial Evaluation
Duration: 02 July 2026 – 31 July 2026
Institution: NMAM Institute of Technology, Nitte

📜 License

This project was developed as part of an academic internship project and is intended for educational and demonstration purposes.
