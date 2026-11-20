from pypdf import PdfReader
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_invoice_number(text):
    match = re.search(r'Invoice Number:\s*(\S+)', text)
    if match:
        return match.group(1)
    else:
        return None

def extract_supplier(text):
    match = re.search(r'Supplier:\s*(.*)', text)
    if match:
        return match.group(1).strip()
    else:
        return None

def extract_invoice_date(text):
    match = re.search(r'Invoice Date:\s*(.*)', text)
    if match:
        return match.group(1)
    else:
        return None

def extract_due_date(text):
    match = re.search(r'Due Date:\s*(.*)', text)
    if match:
        return match.group(1)
    else:
        return None

def extract_total_amount(text):
    match = re.search(r'Total Amount:\s*([\d.]+)', text)
    if match:
        return match.group(1)
    else:
        return None

def extract_invoice_data(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)

    invoice_number = extract_invoice_number(pdf_text)
    supplier = extract_supplier(pdf_text)
    issue_date = extract_invoice_date(pdf_text)
    due_date = extract_due_date(pdf_text)
    amount = extract_total_amount(pdf_text)

    issue_date = datetime.strptime(issue_date.strip(), '%Y-%m-%d')
    due_date = datetime.strptime(due_date.strip(), '%Y-%m-%d')
    amount = float(amount)

    invoice = {
        'invoice_number': invoice_number,
        'supplier': supplier,
        'amount': amount,
        'issue_date': issue_date,
        'due_date': due_date
    }
    return invoice

