import pandas as pd
import numpy as np


def reconcile_payments(invoices, payments):

    duplicate_invoice_mask = invoices['invoice_number'].duplicated(keep = False)
    duplicate_invoice_numbers = invoices.loc[duplicate_invoice_mask, 'invoice_number'].dropna().unique()

    payments_for_duplicated_invoice_mask = payments['invoice_number'].isin(duplicate_invoice_numbers)
    payments_for_duplicated_invoice = payments.loc[payments_for_duplicated_invoice_mask]

    non_duplicated_invoice_mask = ~payments_for_duplicated_invoice_mask
    payments_without_duplicated_invoices = payments.loc[non_duplicated_invoice_mask]

    missing_invoice_number_mask = payments['invoice_number'].isnull()
    payments_with_missing_invoice_number = payments.loc[missing_invoice_number_mask]

    invoice_not_found_mask = ~payments_without_duplicated_invoices['invoice_number'].isin(invoices['invoice_number']) & payments_without_duplicated_invoices['invoice_number'].notna()
    payments_with_invoice_not_found = payments_without_duplicated_invoices.loc[invoice_not_found_mask]

    payments_with_supplier = payments_without_duplicated_invoices.merge(invoices[['invoice_number', 'supplier']], on = 'invoice_number', how = 'inner')
    recipient_mismatch_mask = (payments_with_supplier['supplier'] != payments_with_supplier['recipient']) 
    payments_with_recipient_mismatch = payments_with_supplier.loc[recipient_mismatch_mask]

    payments_for_duplicated_invoice['review_reason'] = 'DUPLICATE_INVOICE'
    payments_with_missing_invoice_number['review_reason'] = 'MISSING_INVOICE_NUMBER'
    payments_with_invoice_not_found['review_reason'] = 'INVOICE_NOT_FOUND'
    payments_with_recipient_mismatch['review_reason'] = 'RECIPIENT_MISMATCH'

    all_payments_for_review = pd.concat([payments_for_duplicated_invoice, payments_with_missing_invoice_number, payments_with_invoice_not_found, payments_with_recipient_mismatch], ignore_index=True)
    all_payments_for_review = all_payments_for_review[['payment_id', 'invoice_number', 'recipient', 'supplier', 'amount', 'payment_date', 'review_reason']]

    valid_payments_mask = (
        ~payments_without_duplicated_invoices['payment_id'].isin(payments_with_missing_invoice_number['payment_id']) &
        ~payments_without_duplicated_invoices['payment_id'].isin(payments_with_invoice_not_found['payment_id']) &
        ~payments_without_duplicated_invoices['payment_id'].isin(payments_with_recipient_mismatch['payment_id'])
    )
    valid_payments = payments_without_duplicated_invoices.loc[valid_payments_mask]

    total_paid_per_invoice = valid_payments.groupby('invoice_number')['amount'].sum()

    invoice_report = invoices.copy()
    invoice_report['total_paid'] = invoice_report['invoice_number'].map(total_paid_per_invoice).fillna(0)
    invoice_report['remaining_amount'] = invoice_report['amount'] - invoice_report['total_paid'] 

    conditions = [
        invoice_report['total_paid'] == 0,
        invoice_report['remaining_amount'] == 0,
        invoice_report['remaining_amount'] > 0,
        invoice_report['remaining_amount'] < 0
    ]
    choices = ['UNPAID', 'PAID', 'UNDERPAID', 'OVERPAID']
    invoice_report['status'] = np.select(conditions, choices, default='FAIL')
    invoice_report = invoice_report[['invoice_number', 'supplier', 'amount', 'total_paid', 'remaining_amount', 'status']]

    invoice_report.loc[duplicate_invoice_mask, 'status'] = 'DUPLICATE'

    return invoice_report, all_payments_for_review

  