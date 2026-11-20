# Document Processing & Reconciliation System

## Project Overview

A Python-based document processing and payment reconciliation system designed to automate invoice data extraction and identify payment discrepancies.

The application supports two invoice input formats: CSV files and text-based PDF documents. It extracts invoice information, compares invoices against payment records, identifies inconsistencies, and generates reports for further review.

The goal of the project is to reduce manual work in invoice processing and make payment reconciliation more efficient and structured.

## Features

- **Multiple Input Formats** – supports invoice data from CSV files and text-based PDF documents.
- **PDF Data Extraction** – extracts invoice numbers, supplier names, invoice dates, due dates, and total amounts using `pypdf` and regular expressions.
- **Payment Reconciliation** – compares invoice records with payment data and calculates total amounts paid and outstanding balances.
- **Payment Validation** – identifies payment discrepancies and categorizes transactions requiring manual review.
- **Invoice Status Classification** – assigns statuses such as `PAID`, `UNPAID`, `UNDERPAID`, `OVERPAID`, and `DUPLICATE`.
- **Automated Reporting** – generates CSV reports containing invoice reconciliation results and payments requiring manual review.
- **Automated Testing** – includes unit tests written with `pytest` to verify the reconciliation logic and PDF extraction.

## Technologies

- **Python** – application logic and data processing.
- **Pandas** – data manipulation, merging, filtering, and reconciliation.
- **pypdf** – text extraction from PDF documents.
- **Regular Expressions (re)** – extraction of structured information from invoice text.
- **Pytest** – automated testing.
- **Git & GitHub** – version control and project management.

## Project Structure

```text
Document Processing & Reconciliation/
│
├── data/
│   ├── input/
│   │   ├── invoices/
│   │   │   ├── invoices.csv
│   │   │   ├── invoice_001.pdf
│   │   │   └── invoice_002.pdf
│   │   │
│   │   └── payments.csv
│   │
│   └── output/
│       ├── invoice_report.csv
│       └── payments_for_review.csv
│
├── tests/
│   ├── test_reconciliation.py
│   └── test_pdf_extractor.py
│
├── main.py
├── reconciliation.py
├── pdf_extractor.py
├── requirements.txt
└── .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd "Document Processing & Reconciliation"
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment.

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

4. Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

### 1. Prepare Input Data

Place invoice files in:

```text
data/input/invoices/
```

The folder can contain:
- `invoices.csv` – invoice records in CSV format.
- PDF invoice documents – text-based PDF files supported by the extraction module.

Place payment records in:

```text
data/input/payments.csv
```

### 2. Select Invoice Input Format

Open `main.py` and select the desired invoice source:

```python
invoice_source = 'csv'
```

For PDF extraction, use:

```python
invoice_source = 'pdf'
```

### 3. Run the Application

From the project root directory, execute:

```bash
python main.py
```

The application processes the selected invoice source, reconciles the invoices against payment records, and generates the output reports.

## Output Reports

The application generates two CSV reports in `data/output/`.

### invoice_report.csv

Contains invoice reconciliation results, including:

| Column | Description |
|---|---|
| `invoice_number` | Invoice identifier |
| `supplier` | Supplier name |
| `amount` | Original invoice amount |
| `total_paid` | Total amount of valid payments |
| `remaining_amount` | Outstanding invoice balance |
| `status` | Reconciliation status |

Possible invoice statuses:

- `PAID` – invoice has been fully paid.
- `UNPAID` – no valid payments have been recorded.
- `UNDERPAID` – the total paid amount is lower than the invoice amount.
- `OVERPAID` – the total paid amount exceeds the invoice amount.
- `DUPLICATE` – duplicate invoice number detected.

### payments_for_review.csv

Contains payment transactions that require manual verification.

Possible review reasons:

- `DUPLICATE_INVOICE` – payment is associated with a duplicated invoice number.
- `MISSING_INVOICE_NUMBER` – payment has no invoice number.
- `INVOICE_NOT_FOUND` – referenced invoice does not exist in the invoice records.
- `RECIPIENT_MISMATCH` – payment recipient does not match the supplier listed on the invoice.

## Testing

The project includes automated tests covering the reconciliation process and PDF extraction.

Run all tests from the project root:

```bash
python -m pytest -v
```

Tests cover scenarios such as:
- Fully paid, unpaid, underpaid, and overpaid invoices.
- Duplicate invoice numbers.
- Missing invoice numbers in payment records.
- Payments referencing non-existent invoices.
- Recipient and supplier mismatches.
- Successful extraction of invoice data from PDF documents.

## Limitations

- PDF extraction supports text-based PDF documents. Scanned documents requiring OCR are not supported.
- PDF extraction relies on predefined invoice field labels and expected text formats.
- Supplier and recipient names are compared directly; variations in company names are not automatically normalized.
- Payments with identified discrepancies are excluded from automatic reconciliation and placed in the manual review report.

## Project Purpose

This project was developed as a practical application of Python programming, data processing, document extraction, and automated testing.

It demonstrates how different input formats can be integrated into a single processing workflow and how repetitive reconciliation tasks can be automated using Python.