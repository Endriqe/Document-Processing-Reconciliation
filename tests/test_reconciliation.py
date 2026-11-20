import pandas as pd
import pytest
from reconciliation import reconcile_payments 

@pytest.fixture
def invoices():
    return pd.DataFrame({
        'invoice_number': ['FV-001'],
        'supplier': ['ABC Ltd'],
        'amount': [100]
    })

@pytest.fixture
def payments():
    return pd.DataFrame({
        'payment_id': ['PAY-001'],
        'invoice_number': ['FV-001'],
        'recipient': ['ABC Ltd'],
        'amount': [100],
        'payment_date': ['2026-01-15']
    })

def test_fully_paid_invoice(invoices, payments):
    invoice_report, payments_for_review = reconcile_payments(invoices, payments)
    assert invoice_report['total_paid'].iloc[0] == 100
    assert invoice_report['remaining_amount'].iloc[0] == 0
    assert invoice_report['status'].iloc[0] == 'PAID'
    assert payments_for_review.empty


@pytest.fixture
def empty_payments():
    return pd.DataFrame(columns=[
        'payment_id',
        'invoice_number',
        'recipient',
        'amount',
        'payment_date'
    ])

def test_unpaid_invoice(invoices, empty_payments):
    invoice_report, payments_for_review = reconcile_payments(invoices, empty_payments)
    assert invoice_report['total_paid'].iloc[0] == 0
    assert invoice_report['remaining_amount'].iloc[0] == 100
    assert invoice_report['status'].iloc[0] == 'UNPAID'
    assert payments_for_review.empty


@pytest.fixture
def underpaid_payments():
    return pd.DataFrame({
        'payment_id': ['PAY-001'],
        'invoice_number': ['FV-001'],
        'recipient': ['ABC Ltd'],
        'amount': [60],
        'payment_date': ['2026-01-15']
    })

def test_underpaid_invoice(invoices, underpaid_payments):
    invoice_report, payments_for_review = reconcile_payments(invoices, underpaid_payments)
    assert invoice_report['total_paid'].iloc[0] == 60
    assert invoice_report['remaining_amount'].iloc[0] == 40
    assert invoice_report['status'].iloc[0] == 'UNDERPAID'
    assert payments_for_review.empty

@pytest.fixture
def overpaid_payments():
    return pd.DataFrame({
        'payment_id': ['PAY-001'],
        'invoice_number': ['FV-001'],
        'recipient': ['ABC Ltd'],
        'amount': [130],
        'payment_date': ['2026-01-15']
    })

def test_overpaid_invoice(invoices, overpaid_payments):
    invoice_report, payments_for_review = reconcile_payments(invoices, overpaid_payments)
    assert invoice_report['total_paid'].iloc[0] == 130
    assert invoice_report['remaining_amount'].iloc[0] == -30
    assert invoice_report['status'].iloc[0] == 'OVERPAID'
    assert payments_for_review.empty

@pytest.fixture
def duplicate_invoices():
    return pd.DataFrame({
        'invoice_number': ['FV-001', 'FV-001'],
        'supplier': ['ABC Ltd', 'ABC Ltd'],
        'amount': [100, 100]
    })

def test_duplicate_invoice(duplicate_invoices, payments):
    invoice_report, payments_for_review = reconcile_payments(duplicate_invoices, payments)
    assert payments_for_review['payment_id'].iloc[0] == 'PAY-001'
    assert payments_for_review['review_reason'].iloc[0] == 'DUPLICATE_INVOICE'
    assert invoice_report['status'].iloc[0] == 'DUPLICATE'
    assert len(payments_for_review) == 1

@pytest.fixture
def missing_invoice_number_payments():
    return pd.DataFrame({
        'payment_id': ['PAY-001'],
        'invoice_number': [None],
        'recipient': ['ABC Ltd'],
        'amount': [100],
        'payment_date': ['2026-01-15']
    })

def test_missing_invoice_number(invoices, missing_invoice_number_payments):
    invoice_report, payments_for_review = reconcile_payments(invoices, missing_invoice_number_payments)
    assert payments_for_review['payment_id'].iloc[0] == 'PAY-001'
    assert payments_for_review['review_reason'].iloc[0] == 'MISSING_INVOICE_NUMBER'
    assert invoice_report['status'].iloc[0] == 'UNPAID'
    assert len(payments_for_review) == 1

@pytest.fixture
def invoice_not_found_payments():
    return pd.DataFrame({
        'payment_id': ['PAY-001'],
        'invoice_number': ['FV-9999'],
        'recipient': ['ABC Ltd'],
        'amount': [100],
        'payment_date': ['2026-01-15']
    })

def test_invoice_not_found(invoices, invoice_not_found_payments):
    invoice_report, payments_for_review = reconcile_payments(invoices, invoice_not_found_payments)
    assert payments_for_review['payment_id'].iloc[0] == 'PAY-001'
    assert payments_for_review['review_reason'].iloc[0] == 'INVOICE_NOT_FOUND'
    assert invoice_report['status'].iloc[0] == 'UNPAID'
    assert len(payments_for_review) == 1

@pytest.fixture
def recipient_mismatch_payments():
    return pd.DataFrame({
        'payment_id': ['PAY-001'],
        'invoice_number': ['FV-001'],
        'recipient': ['XYZ Ltd'],
        'amount': [100],
        'payment_date': ['2026-01-15']
    })

def test_recipient_mismatch(invoices, recipient_mismatch_payments):
    invoice_report, payments_for_review = reconcile_payments(invoices, recipient_mismatch_payments)
    assert payments_for_review['payment_id'].iloc[0] == 'PAY-001'
    assert payments_for_review['supplier'].iloc[0] == 'ABC Ltd'
    assert payments_for_review['review_reason'].iloc[0] == 'RECIPIENT_MISMATCH'
    assert invoice_report['status'].iloc[0] == 'UNPAID'
    assert len(payments_for_review) == 1