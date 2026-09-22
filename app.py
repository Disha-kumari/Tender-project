# ==============================
# app.py (PART 1)
# MRPL Tender Commercial Evaluation System
# ==============================

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pyodbc
import os
from werkzeug.utils import secure_filename
from datetime import datetime

# ==============================
# FLASK CONFIGURATION
# ==============================

app = Flask(__name__)
app.secret_key = "mrpl_secret_key_2026"

UPLOAD_FOLDER = "static/uploads"
REPORT_FOLDER = "static/generated_reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# ==============================
# SQL SERVER CONNECTION
# ==============================

SERVER = "Disha"
DATABASE = "Tender_MRPL"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)

def get_connection():
    return pyodbc.connect(connection_string)


# ==============================
# DATABASE HELPER
# ==============================

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    data = None

    if fetch:
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    else:
        conn.commit()

    cursor.close()
    conn.close()

    return data


# ==============================
# HOME
# ==============================

@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Users
        WHERE username=?
        AND password=?
    """,(username,password))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:

        session["user_id"] = user.user_id
        session["username"] = user.username
        session["full_name"] = user.full_name
        session["role"] = user.role

        return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        error="Invalid Username or Password"
    )


# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# ==============================
# DASHBOARD
# ==============================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Total Tenders
    # -------------------------

    cursor.execute("SELECT COUNT(*) FROM Tenders")
    total_tenders = cursor.fetchone()[0]

    # -------------------------
    # Total Vendors
    # -------------------------

    cursor.execute("SELECT COUNT(*) FROM Vendors")
    total_vendors = cursor.fetchone()[0]

    # -------------------------
    # Total Quotations
    # -------------------------

    cursor.execute("SELECT COUNT(*) FROM Vendor_Quotations")
    total_quotes = cursor.fetchone()[0]

    # -------------------------
    # Total Reports
    # -------------------------

    cursor.execute("SELECT COUNT(*) FROM Reports")
    total_reports = cursor.fetchone()[0]

    # -------------------------
    # Recent Tenders
    # -------------------------

    cursor.execute("""

        SELECT
            t.tender_id,
            t.tender_number,
            t.tender_name,
            d.department_name,
            t.status

        FROM Tenders t

        INNER JOIN Departments d

        ON t.department_id=d.department_id

        ORDER BY t.tender_date DESC

    """)

    tenders=[]

    rows=cursor.fetchall()

    for row in rows:

        tenders.append({

            "tender_id":row.tender_id,
            "tender_number":row.tender_number,
            "tender_name":row.tender_name,
            "department_name":row.department_name,
            "status":row.status

        })

    cursor.close()
    conn.close()

    return render_template(

        "dashboard.html",

        full_name=session["full_name"],
        role=session["role"],

        total_tenders=total_tenders,
        total_vendors=total_vendors,
        total_quotes=total_quotes,
        total_reports=total_reports,

        tenders=tenders

    )

# ==============================
# TENDER LIST
# ==============================

@app.route("/tenders")
def tender_list():

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            t.tender_id,
            t.tender_number,
            t.tender_name,
            d.department_name,
            t.estimated_cost,
            t.closing_date,
            t.status

        FROM Tenders t

        INNER JOIN Departments d

        ON t.department_id=d.department_id

        ORDER BY t.tender_date DESC

    """)

    tenders=[]

    rows=cursor.fetchall()

    for row in rows:

        tenders.append({

            "tender_id":row.tender_id,
            "tender_number":row.tender_number,
            "tender_name":row.tender_name,
            "department_name":row.department_name,
            "estimated_cost":row.estimated_cost,
            "closing_date":row.closing_date,
            "status":row.status

        })

    cursor.close()
    conn.close()

    return render_template(

        "tender_list.html",

        tenders=tenders,

        full_name=session["full_name"],

        role=session["role"]

    )


# ==============================
# VIEW TENDER
# ==============================

@app.route("/view_tender/<int:tender_id>")
def view_tender(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    initial_step = request.args.get("step", 1, type=int)

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Tender Details
    # -------------------------

    cursor.execute("""

        SELECT

            t.tender_id,
            t.tender_number,
            t.tender_name,
            d.department_name,
            t.description,
            t.estimated_cost,
            t.tender_date,
            t.closing_date,
            t.status

        FROM Tenders t

        INNER JOIN Departments d

        ON t.department_id=d.department_id

        WHERE t.tender_id=?

    """,(tender_id,))

    row=cursor.fetchone()

    tender={

        "tender_id":row.tender_id,
        "tender_number":row.tender_number,
        "tender_name":row.tender_name,
        "department_name":row.department_name,
        "description":row.description,
        "estimated_cost":row.estimated_cost,
        "tender_date":row.tender_date,
        "closing_date":row.closing_date,
        "status":row.status

    }

    # -------------------------
    # Tender Items
    # -------------------------

    cursor.execute("""

        SELECT

            ti.tender_item_id,
            im.item_code,
            im.item_name,
            im.specification,
            im.unit,
            ti.quantity,
            ti.estimated_rate,
            ti.estimated_amount

        FROM Tender_Items ti

        INNER JOIN Item_Master im

        ON ti.item_id=im.item_id

        WHERE ti.tender_id=?

        ORDER BY ti.tender_item_id

    """,(tender_id,))

    items=[]

    rows=cursor.fetchall()

    for row in rows:

        items.append({

            "tender_item_id":row.tender_item_id,
            "item_code":row.item_code,
            "item_name":row.item_name,
            "specification":row.specification,
            "unit":row.unit,
            "quantity":row.quantity,
            "estimated_rate":row.estimated_rate,
            "estimated_amount":row.estimated_amount

        })
    # -------------------------
    # Vendors
    # -------------------------

    cursor.execute("""
        SELECT
            vendor_id,
            company_name,
            contact_person
        FROM Vendors
        ORDER BY company_name
    """)

    rows = cursor.fetchall()

    vendors = []

    for row in rows:
        vendors.append({
            "vendor_id": row.vendor_id,
            "company_name": row.company_name,
            "contact_person": row.contact_person
        })

    cursor.execute("""
        SELECT DISTINCT vq.vendor_id
        FROM Vendor_Quotations vq
        INNER JOIN Tender_Items ti
            ON ti.tender_item_id = vq.tender_item_id
        WHERE ti.tender_id = ?
    """, (tender_id,))

    uploaded_vendor_ids = {
        row.vendor_id for row in cursor.fetchall()
    }

    # -------------------------
    # Vendor Quotations
    # -------------------------

    cursor.execute("""

        SELECT

            vq.quotation_id,
            v.vendor_id,
            v.company_name,

            im.item_code,
            im.item_name,

            ti.tender_item_id,
            ti.quantity,

            vq.quoted_rate,
            vq.GST,
            vq.freight,
            vq.discount,
            vq.total_amount,
            vq.quotation_date

        FROM Vendor_Quotations vq

        INNER JOIN Tender_Items ti
            ON vq.tender_item_id = ti.tender_item_id

        INNER JOIN Item_Master im
            ON ti.item_id = im.item_id

        INNER JOIN Vendors v
            ON v.vendor_id = vq.vendor_id

        WHERE ti.tender_id = ?

        ORDER BY
            v.company_name,
            im.item_name

    """, (tender_id,))

    quotations = []

    rows = cursor.fetchall()

    for row in rows:

        quotations.append({

            "quotation_id": row.quotation_id,
            "vendor_id": row.vendor_id,
            "company_name": row.company_name,
            "item_code": row.item_code,
            "item_name": row.item_name,
            "tender_item_id": row.tender_item_id,
            "quantity": row.quantity,
            "quoted_rate": float(row.quoted_rate),
            "GST": float(row.GST),
            "freight": float(row.freight),
            "discount": float(row.discount),
            "total_amount": float(row.total_amount),
            "quotation_date": row.quotation_date

        })

    # -------------------------
    # Commercial Evaluation
    # -------------------------

    cursor.execute("""

        SELECT

            v.vendor_id,
            v.company_name,

            SUM(vq.total_amount) AS grand_total

        FROM Vendor_Quotations vq

        INNER JOIN Vendors v
            ON v.vendor_id = vq.vendor_id

        INNER JOIN Tender_Items ti
            ON ti.tender_item_id = vq.tender_item_id

        WHERE ti.tender_id = ?

        GROUP BY
            v.vendor_id,
            v.company_name

        ORDER BY
            grand_total ASC

    """, (tender_id,))

    vendor_totals = []

    rows = cursor.fetchall()

    rank = 1

    for row in rows:

        vendor_totals.append({

            "rank": rank,
            "vendor_id": row.vendor_id,
            "company_name": row.company_name,
            "grand_total": float(row.grand_total)

        })

        rank += 1

    # -------------------------
    # Best Vendor
    # -------------------------

    if len(vendor_totals) > 0:

        best_vendor = vendor_totals[0]

    else:

        best_vendor = None

    # -------------------------
    # Item-wise comparison (grouped by item, L1 flagged per item)
    # -------------------------

    items_comparison = {}

    for q in quotations:

        tid = q["tender_item_id"]

        if tid not in items_comparison:

            items_comparison[tid] = {
                "tender_item_id": tid,
                "item_code": q["item_code"],
                "item_name": q["item_name"],
                "quantity": q["quantity"],
                "quotes": []
            }

        items_comparison[tid]["quotes"].append({
            "vendor_id": q["vendor_id"],
            "company_name": q["company_name"],
            "quoted_rate": q["quoted_rate"],
            "total_amount": q["total_amount"]
        })

    items_comparison = list(items_comparison.values())


    for entry in items_comparison:

        entry["quotes"].sort(key=lambda x: x["total_amount"])

        for i, qt in enumerate(entry["quotes"]):

            qt["is_l1"] = (i == 0)

        # -------------------------
    # Negotiation Details
    # -------------------------

    cursor.execute("""

        SELECT
            n.tender_item_id,
            n.vendor_id,
            v.company_name,
            n.original_price,
            n.negotiated_price,
            n.final_price

        FROM Negotiation n

        INNER JOIN Tender_Items ti
            ON ti.tender_item_id = n.tender_item_id

        INNER JOIN Vendors v
            ON v.vendor_id = n.vendor_id

        WHERE ti.tender_id = ?

    """, (tender_id,))

    negotiations = {}

    for row in cursor.fetchall():

        negotiations[row.tender_item_id] = {
            "company_name": row.company_name,
            "original_price": float(row.original_price),
            "negotiated_price": float(row.negotiated_price),
            "final_price": float(row.final_price)
        }

    cursor.close()
    conn.close()

    return render_template(

        "view_tender.html",

        tender=tender,
        items=items,
        vendors=vendors,
        uploaded_vendor_ids=uploaded_vendor_ids,
        quotations=quotations,
        vendor_totals=vendor_totals,
        best_vendor=best_vendor,
        items_comparison=items_comparison,
        negotiations=negotiations,
        initial_step=initial_step,

        full_name=session["full_name"],
        role=session["role"]

    )


   

# ===========================================
# UPLOAD VENDOR QUOTATION
# ===========================================

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload_quotation/<int:tender_id>", methods=["POST"])
def upload_quotation(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if "quotation_file" not in request.files:

        flash("No file selected")
        return redirect(url_for("view_tender", tender_id=tender_id))

    file = request.files["quotation_file"]

    vendor_id = request.form.get("vendor_id")

    if not vendor_id:

        flash("Missing vendor for this upload")
        return redirect(url_for("view_tender", tender_id=tender_id))

    if file.filename == "":

        flash("Please choose a PDF")
        return redirect(url_for("view_tender", tender_id=tender_id))

    if not allowed_file(file.filename):

        flash("Only PDF files are allowed")
        return redirect(url_for("view_tender", tender_id=tender_id))

    # Namespace the saved filename by tender + vendor so uploads from
    # different vendors never overwrite each other.
    safe_name = secure_filename(file.filename)
    filename = f"tender{tender_id}_vendor{vendor_id}_{safe_name}"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    session["uploaded_pdf"] = filepath
    session["upload_vendor_id"] = int(vendor_id)

    flash("Quotation uploaded successfully.")

    return redirect(
        url_for(
            "ocr_verification",
            tender_id=tender_id
        )
    )

#  delete route
@app.route("/delete_upload/<int:tender_id>", methods=["POST"])
def delete_upload(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    filepath = session.get("uploaded_pdf")

    if filepath and os.path.exists(filepath):
        os.remove(filepath)

    session.pop("uploaded_pdf", None)
    session.pop("upload_vendor_id", None)

    flash("Uploaded file removed. You can upload again.")

    return redirect(url_for("view_tender", tender_id=tender_id, step=3))  

# after upload delete
@app.route("/delete_vendor_quotation/<int:tender_id>/<int:vendor_id>", methods=["POST"])
def delete_vendor_quotation(tender_id, vendor_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Vendor_Quotations
        WHERE vendor_id=?
        AND tender_item_id IN (
            SELECT tender_item_id FROM Tender_Items WHERE tender_id=?
        )
    """, (vendor_id, tender_id))

    conn.commit()
    cursor.close()
    conn.close()

    # Remove the saved PDF(s) for this vendor+tender too
    prefix = f"tender{tender_id}_vendor{vendor_id}_"

    for fname in os.listdir(app.config["UPLOAD_FOLDER"]):
        if fname.startswith(prefix):
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], fname))

    flash("Vendor quotation deleted. You can upload a new PDF for this vendor.")

    return redirect(url_for("view_tender", tender_id=tender_id, step=3))

# ===========================================
# OCR VERIFICATION
# ===========================================

import pdfplumber
import re


@app.route("/ocr_verification/<int:tender_id>")
def ocr_verification(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if "uploaded_pdf" not in session or "upload_vendor_id" not in session:

        flash("Upload quotation first")
        return redirect(
            url_for(
                "view_tender",
                tender_id=tender_id
            )
        )

    filepath = session["uploaded_pdf"]
    vendor_id = session["upload_vendor_id"]

    extracted_text = ""

    with pdfplumber.open(filepath) as pdf:

        for page in pdf.pages:

            txt = page.extract_text()

            if txt:

                extracted_text += txt + "\n"

    # The vendor is whichever one the officer clicked "Upload PDF" under
    # in Step 3 -- trust that selection rather than trying to parse the
    # company name back out of the PDF text, which is unreliable.
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT vendor_id, company_name FROM Vendors WHERE vendor_id=?",
        (vendor_id,)
    )
    vendor_row = cursor.fetchone()
    vendor_name = vendor_row.company_name if vendor_row else "Unknown Vendor"

    # Items on this tender, so the officer can key in / confirm a quoted
    # rate for each one against what they see in the PDF.
    cursor.execute("""

        SELECT
            ti.tender_item_id,
            im.item_code,
            im.item_name,
            im.unit,
            ti.quantity

        FROM Tender_Items ti

        INNER JOIN Item_Master im
            ON ti.item_id = im.item_id

        WHERE ti.tender_id = ?

        ORDER BY ti.tender_item_id

    """, (tender_id,))

    tender_items = []

    for row in cursor.fetchall():

        # Best-effort: your quotation PDFs list items as
        # "<Sl.No.> <Item Description> <Qty> <Unit Price> <Total>" on one
        # line, with no item code printed anywhere. Match on the item
        # name instead, and grab the *first* of the two trailing numbers
        # (unit price), not the second (line total).
        suggested_rate = ""

        line_match = re.search(
            re.escape(row.item_name)
            + r"\s+[\d,]+(?:\.\d+)?\s+([\d,]+\.\d{2})\s+[\d,]+\.\d{2}",
            extracted_text,
            re.IGNORECASE
        )

        if line_match:
            suggested_rate = line_match.group(1).replace(",", "")

        tender_items.append({
            "tender_item_id": row.tender_item_id,
            "item_code": row.item_code,
            "item_name": row.item_name,
            "unit": row.unit,
            "quantity": float(row.quantity),
            "suggested_rate": suggested_rate
        })

    cursor.close()
    conn.close()

    quotation_no = ""

    quotation_date = ""

    grand_total = ""

    gst = ""

    freight = ""

    discount = ""

    quotation_match = re.search(
        r"Quotation\s*No\.?[:\-]?\s*(\S+)",
        extracted_text,
        re.IGNORECASE
    )

    if quotation_match:

        quotation_no = quotation_match.group(1).strip()



    date_match = re.search(
        r"Quotation\s*Date[:\-]?\s*(\d{1,2})[-/](\d{1,2})[-/](\d{4})",
        extracted_text,
        re.IGNORECASE
    )

    if date_match:

        # Convert DD-MM-YYYY (as printed on the vendor PDF) to the
        # YYYY-MM-DD format an <input type="date"> requires to display
        # a pre-filled value.
        day, month, year = date_match.groups()

        quotation_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"



    total_match = re.search(
        r"Grand\s*Total[:\-]?\s*([\d,]+\.\d+)",
        extracted_text,
        re.IGNORECASE
    )

    if total_match:

        grand_total = total_match.group(1)



    gst_match = re.search(
        r"GST[:\-]?\s*([\d,]+\.\d+)",
        extracted_text,
        re.IGNORECASE
    )

    if gst_match:

        gst = gst_match.group(1)



    freight_match = re.search(
        r"Freight[:\-]?\s*([\d,]+\.\d+)",
        extracted_text,
        re.IGNORECASE
    )

    if freight_match:

        freight = freight_match.group(1)



    discount_match = re.search(
        r"Discount[:\-]?\s*([\d,]+\.\d+)",
        extracted_text,
        re.IGNORECASE
    )

    if discount_match:

        discount = discount_match.group(1)



    return render_template(

        "ocr_verification.html",

        tender_id=tender_id,

        vendor_id=vendor_id,

        vendor_name=vendor_name,

        tender_items=tender_items,

        quotation_no=quotation_no,

        quotation_date=quotation_date,

        grand_total=grand_total,

        gst=gst,

        freight=freight,

        discount=discount,

        extracted_text=extracted_text

    )

# ===========================================
# SAVE OCR DATA
# ===========================================

@app.route("/save_quotation/<int:tender_id>", methods=["POST"])
def save_quotation(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    vendor_id = int(request.form["vendor_id"])

    quotation_date = request.form["quotation_date"]

    gst = float(request.form["gst"] or 0)

    freight = float(request.form["freight"] or 0)

    discount = float(request.form["discount"] or 0)

    for key in request.form:

        if key.startswith("rate_") and request.form[key].strip() != "":

            tender_item_id = int(key.split("_")[1])

            quoted_rate = float(request.form[key])

            cursor.execute("""

            SELECT quantity

            FROM Tender_Items

            WHERE tender_item_id=?

            """,(tender_item_id,))

            quantity = float(cursor.fetchone()[0])

            base_amount = quoted_rate * quantity

            gst_amount = base_amount * gst / 100

            total = base_amount + gst_amount + freight - discount

            # Replace any earlier quotation this vendor already gave for
            # this item, instead of stacking duplicate rows.
            cursor.execute("""

            DELETE FROM Vendor_Quotations

            WHERE tender_item_id=? AND vendor_id=?

            """,(tender_item_id, vendor_id))

            cursor.execute("""

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

            VALUES(?,?,?,?,?,?,?,?)

            """,(

                tender_item_id,
                vendor_id,
                quoted_rate,
                gst,
                freight,
                discount,
                total,
                quotation_date

            ))

    conn.commit()

    cursor.close()

    conn.close()

    session.pop("uploaded_pdf", None)
    session.pop("upload_vendor_id", None)

    flash("Quotation Saved Successfully")

    return redirect(

        url_for(

            "view_tender",

            tender_id=tender_id,

            step=5

        )

    )


# ===========================================
# COMMERCIAL EVALUATION
# ===========================================

@app.route("/commercial_evaluation/<int:tender_id>")
def commercial_evaluation(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        v.vendor_id,

        v.company_name,

        SUM(vq.total_amount) AS grand_total

    FROM Vendor_Quotations vq

    INNER JOIN Vendors v

    ON v.vendor_id=vq.vendor_id

    INNER JOIN Tender_Items ti

    ON ti.tender_item_id=vq.tender_item_id

    WHERE ti.tender_id=?

    GROUP BY

        v.vendor_id,

        v.company_name

    ORDER BY

        grand_total ASC

    """,(tender_id,))

    rows = cursor.fetchall()

    cursor.execute("""

    DELETE FROM Commercial_Evaluation

    WHERE tender_id=?

    """,(tender_id,))

    rank = 1

    for row in rows:

        cursor.execute("""

        INSERT INTO Commercial_Evaluation(

        tender_id,

        vendor_id,

        grand_total,

        overall_rank,

        evaluation_date

        )

        VALUES(?,?,?,?,GETDATE())

        """,(

            tender_id,

            row.vendor_id,

            row.grand_total,

            rank

        ))

        rank += 1

    conn.commit()

    cursor.close()

    conn.close()

    flash("Commercial Evaluation Completed")

    return redirect(
    url_for(
        "view_tender",
        tender_id=tender_id,
        step=6
    )
)

# ===========================================
# ITEM WISE L1
# ===========================================

@app.route("/itemwise_l1/<int:tender_id>")
def itemwise_l1(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM Item_Wise_Evaluation

    WHERE tender_item_id IN(

    SELECT tender_item_id

    FROM Tender_Items

    WHERE tender_id=?

    )

    """,(tender_id,))

    cursor.execute("""

    SELECT

    tender_item_id

    FROM Tender_Items

    WHERE tender_id=?

    """,(tender_id,))

    items = cursor.fetchall()

    for item in items:

        cursor.execute("""

        SELECT TOP 1

        vendor_id,

        total_amount

        FROM Vendor_Quotations

        WHERE tender_item_id=?

        ORDER BY total_amount ASC

        """,(item.tender_item_id,))

        lowest = cursor.fetchone()

        if lowest:

            cursor.execute("""

            INSERT INTO Item_Wise_Evaluation(

            tender_item_id,

            vendor_id,

            lowest_price,

            evaluation_date

            )

            VALUES(?,?,?,GETDATE())

            """,(

                item.tender_item_id,

                lowest.vendor_id,

                lowest.total_amount

            ))

    conn.commit()

    cursor.close()

    conn.close()

    flash("Item Wise L1 Generated")
    return redirect(
    url_for(
        "view_tender",
        tender_id=tender_id,
        step=6
    )
)

# ===========================================
# NEGOTIATION
# ===========================================

@app.route("/save_negotiation/<int:tender_id>", methods=["POST"])
def save_negotiation(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    # Remove previous negotiation for this tender
    cursor.execute("""
        DELETE FROM Negotiation
        WHERE tender_item_id IN (
            SELECT tender_item_id
            FROM Tender_Items
            WHERE tender_id = ?
        )
    """, (tender_id,))

    for key in request.form:

        if key.startswith("negotiated_"):

            value = request.form[key].strip()

            if value == "":
                continue

            tender_item_id = int(key.split("_")[1])
            negotiated_price = float(value)

            cursor.execute("""
                SELECT TOP 1
                    vendor_id,
                    total_amount
                FROM Vendor_Quotations
                WHERE tender_item_id = ?
                ORDER BY total_amount ASC
            """, (tender_item_id,))

            row = cursor.fetchone()

            if row:

                print("Saving:", tender_item_id, negotiated_price)

                cursor.execute("""
                    INSERT INTO Negotiation
                    (
                        tender_item_id,
                        vendor_id,
                        original_price,
                        negotiated_price,
                        final_price,
                        negotiation_status
                    )
                    VALUES (?,?,?,?,?,?)
                """, (
                    tender_item_id,
                    row.vendor_id,
                    float(row.total_amount),
                    negotiated_price,
                    negotiated_price,
                    "Completed"
                ))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Negotiation Saved Successfully")

    return redirect(
        url_for(
            "view_tender",
            tender_id=tender_id,
            step=7
        )
    )

# ===========================================
# GENERATE REPORT
# ===========================================

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


@app.route("/generate_report/<int:tender_id>")
def generate_report(tender_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        tender_number,
        tender_name

    FROM Tenders

    WHERE tender_id=?

    """,(tender_id,))

    tender = cursor.fetchone()

    if tender is None:

        cursor.close()
        conn.close()

        flash("Tender not found")
        return redirect(url_for("tender_list"))

    # Recompute and persist the commercial evaluation ranking here rather
    # than relying on a separate step, since generating the report is the
    # point where the officer expects the final ranking to be locked in.
    cursor.execute("""

    SELECT

        v.vendor_id,
        v.company_name,
        SUM(vq.total_amount) AS grand_total

    FROM Vendor_Quotations vq

    INNER JOIN Vendors v
        ON v.vendor_id = vq.vendor_id

    INNER JOIN Tender_Items ti
        ON ti.tender_item_id = vq.tender_item_id

    WHERE ti.tender_id=?

    GROUP BY v.vendor_id, v.company_name

    ORDER BY grand_total ASC

    """,(tender_id,))

    ranked = cursor.fetchall()

    cursor.execute(
        "DELETE FROM Commercial_Evaluation WHERE tender_id=?",
        (tender_id,)
    )

    rank = 1

    for r in ranked:

        cursor.execute("""

        INSERT INTO Commercial_Evaluation(
            tender_id, vendor_id, grand_total, overall_rank, evaluation_date
        )
        VALUES(?,?,?,?,GETDATE())

        """,(tender_id, r.vendor_id, r.grand_total, rank))

        rank += 1

    conn.commit()

    if not ranked:

        cursor.close()
        conn.close()

        flash("No vendor quotations exist for this tender yet. Upload quotations before generating a report.")
        return redirect(url_for("view_tender", tender_id=tender_id, step=3))

    # Item-wise L1: for every item on this tender, whichever vendor quoted
    # the lowest total for THAT item -- this is what actually goes on the
    # report, since procurement is awarded item-by-item, not to one
    # overall "winning" vendor.
    cursor.execute("""

    SELECT
        ranked_quotes.item_code,
        ranked_quotes.item_name,
        ranked_quotes.quantity,
        COALESCE(negv.company_name, ranked_quotes.company_name) AS company_name,
        ranked_quotes.quoted_rate,
        COALESCE(neg.final_price, ranked_quotes.total_amount) AS total_amount

    FROM (

        SELECT

            ti.tender_item_id,
            im.item_code,
            im.item_name,
            ti.quantity,
            v.company_name,
            vq.quoted_rate,
            vq.total_amount,
            vq.vendor_id,

            ROW_NUMBER() OVER (
                PARTITION BY ti.tender_item_id
                ORDER BY vq.total_amount ASC, v.vendor_id ASC
            ) AS rn

        FROM Tender_Items ti

        INNER JOIN Item_Master im
            ON im.item_id = ti.item_id

        INNER JOIN Vendor_Quotations vq
            ON vq.tender_item_id = ti.tender_item_id

        INNER JOIN Vendors v
            ON v.vendor_id = vq.vendor_id

        WHERE ti.tender_id = ?

    ) ranked_quotes

    LEFT JOIN Negotiation neg
        ON neg.tender_item_id = ranked_quotes.tender_item_id

    LEFT JOIN Vendors negv
        ON negv.vendor_id = neg.vendor_id

    WHERE ranked_quotes.rn = 1

    ORDER BY ranked_quotes.tender_item_id

    """,(tender_id,))

    rows = cursor.fetchall()

    pdf_name = f"Report_{tender_id}.pdf"

    pdf_path = os.path.join(

        app.config["REPORT_FOLDER"],

        pdf_name

    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(

        Paragraph(

            "<b>MRPL Tender Commercial Evaluation Report</b>",

            styles["Heading1"]

        )

    )

    elements.append(

        Paragraph(

            f"Tender Number : {tender.tender_number}",

            styles["Normal"]

        )

    )

    elements.append(

        Paragraph(

            f"Tender Name : {tender.tender_name}",

            styles["Normal"]

        )

    )

    elements.append(

        Paragraph("<br/>",styles["Normal"])

    )

    elements.append(

        Paragraph(

            "<b>Item-wise L1 (Lowest) Vendor Summary</b>",

            styles["Heading2"]

        )

    )

    elements.append(
        Paragraph("<br/>",styles["Normal"])
    )

    cell_style = styles["Normal"].clone("cell")
    cell_style.fontSize = 8
    cell_style.leading = 10

    data = [

        [

            "Item Code",

            "Item Name",

            "Qty",

            "L1 Vendor",

            "Rate (₹)",

            "Total (₹)"

        ]

    ]

    grand_total = 0

    for row in rows:

        data.append([

            row.item_code,

            Paragraph(row.item_name, cell_style),

            str(row.quantity),

            Paragraph(row.company_name, cell_style),

            f"{row.quoted_rate:,.2f}",

            f"{row.total_amount:,.2f}"

        ])

        grand_total += row.total_amount

    data.append([

        "", "", "", "", "Grand Total", f"₹ {grand_total:,.2f}"

    ])

    table = Table(
        data,
        colWidths=[55,95,30,140,65,80]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.grey),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("ALIGN",(0,0),(-1,0),"CENTER"),

            ("ALIGN",(0,1),(0,-1),"CENTER"),
            ("ALIGN",(2,1),(2,-1),"CENTER"),
            ("ALIGN",(4,1),(-1,-1),"RIGHT"),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

            ("FONTSIZE",(0,0),(-1,-1),8),

            ("BACKGROUND",(0,1),(-1,-2),colors.beige),

            ("BACKGROUND",(0,-1),(-1,-1),colors.lightgrey),

            ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),

            ("SPAN",(0,-1),(3,-1))

        ])

    )

    elements.append(table)

    doc.build(elements)

    cursor.execute("""

    INSERT INTO Reports(

        tender_id,

        user_id,

        generated_date,

        report_file

    )

    VALUES(?,?,GETDATE(),?)

    """,(

        tender_id,

        session["user_id"],

        pdf_name

    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Report Generated Successfully")

    return redirect(

        url_for(

            "download_report",

            filename=pdf_name

        )

    )


# ===========================================
# DOWNLOAD REPORT
# ===========================================

from flask import send_from_directory


@app.route("/download_report/<filename>")
def download_report(filename):

    return send_from_directory(

        app.config["REPORT_FOLDER"],

        filename,

        as_attachment=True

    )


# ===========================================
# RUN APPLICATION
# ===========================================

if __name__ == "__main__":

    app.run(

        debug=True

    )