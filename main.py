from reconciliation import reconcile_payments
from pdf_extractor import extract_invoice_data
from pathlib import Path
import pandas as pd

invoice_source = 'pdf'

if invoice_source == 'csv':
    invoices = pd.read_csv('data/input/invoices/invoices.csv')

elif invoice_source == 'pdf':
    invoice_folder = Path('data/input/invoices')
    pdf_files = invoice_folder.glob('*.pdf')

    invoices_data = []
    for pdf_file in pdf_files:
        invoice = extract_invoice_data(pdf_file)
        invoices_data.append(invoice)

    invoices = pd.DataFrame(invoices_data)

else:
    raise ValueError('Unsupported invoice source')


payments = pd.read_csv('data/input/payments.csv')

invoice_report, all_payments_for_review = reconcile_payments(invoices, payments)

invoice_report.to_csv('data/output/invoice_report.csv', index=False, sep=';')
all_payments_for_review.to_csv('data/output/payments_for_review.csv', index=False, sep=';')
