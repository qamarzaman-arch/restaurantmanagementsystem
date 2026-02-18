from src.logic.billing import BillingLogic
from src.utils.pdf_generator import PDFGenerator
import os

def test_billing_and_pdf():
    # Test Billing Logic
    items = [
        {'price': 10.0, 'quantity': 2},
        {'price': 5.0, 'quantity': 1}
    ]
    res = BillingLogic.calculate_totals(items, tax_rate=5.0, discount_percent=10.0)
    # subtotal = 25.0
    # discount = 2.5
    # taxable = 22.5
    # tax = 1.125 -> 1.13
    # total = 23.625 -> 23.63
    print(f"Billing result: {res}")
    assert res['subtotal'] == 25.0
    assert res['discount'] == 2.5
    assert res['tax'] == 1.13 or res['tax'] == 1.12 # depending on rounding

    # Test PDF Generation
    order = {
        'id': 123,
        'created_at': '2023-10-27 10:00:00',
        'subtotal': 25.0,
        'discount': 2.5,
        'tax': 1.13,
        'total': 23.63,
        'items': [
            {'name': 'Pizza', 'quantity': 2, 'price': 10.0},
            {'name': 'Coke', 'quantity': 1, 'price': 5.0}
        ]
    }
    settings = {'restaurant_name': 'Test Cafe', 'address': '123 Street'}
    pdf_path = "test_invoice.pdf"
    PDFGenerator.generate_invoice(order, settings, pdf_path)

    if os.path.exists(pdf_path):
        print(f"PDF generated successfully at {pdf_path}")
        # os.remove(pdf_path)
    else:
        print("PDF generation failed")
        return False

    return True

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    if test_billing_and_pdf():
        print("Billing and PDF Tests Passed!")
    else:
        exit(1)
