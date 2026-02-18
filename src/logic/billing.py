class BillingLogic:
    @staticmethod
    def calculate_totals(items, tax_rate, discount_percent=0):
        """
        items: list of dicts with 'price' and 'quantity'
        tax_rate: percentage (e.g., 5.0)
        discount_percent: percentage (e.g., 10.0)
        """
        subtotal = sum(item['price'] * item['quantity'] for item in items)
        discount_amount = (subtotal * discount_percent) / 100
        taxable_amount = subtotal - discount_amount
        tax_amount = (taxable_amount * tax_rate) / 100
        total = taxable_amount + tax_amount

        return {
            'subtotal': round(subtotal, 2),
            'discount': round(discount_amount, 2),
            'tax': round(tax_amount, 2),
            'total': round(total, 2)
        }
