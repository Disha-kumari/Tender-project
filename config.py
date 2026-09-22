import pyodbc

SERVER = "DESKTOP-5OUD1G3"
DATABASE = "Tender_MRPL"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    print("✅ Database Connected Successfully")

except Exception as e:
    print("❌ Database Connection Failed")
    print(e)