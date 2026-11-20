import pytest
from pathlib import Path
from pdf_extractor import extract_invoice_data
from datetime import datetime

@pytest.fixture
def invoice_001_pdf():
    return Path(__file__).parent.parent / 'data' / 'input' / 'invoices' / 'invoice_001.pdf'

def test_extract_invoice_data(invoice_001_pdf):
    invoice = extract_invoice_data(invoice_001_pdf)
    assert invoice['invoice_number'] == 'FV-1001'
    assert invoice['supplier'] == 'ABC Ltd'
    assert invoice['amount'] == 1500
    assert invoice['issue_date'] == datetime(2026, 1, 10)
    assert invoice['due_date'] == datetime(2026, 2, 10)

