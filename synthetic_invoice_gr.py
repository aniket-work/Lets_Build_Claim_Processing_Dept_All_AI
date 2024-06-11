from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Aniket Home Company Invoice', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def invoice_body(self, invoice_data, items, totals):
        self.set_font('Arial', '', 12)

        for line in invoice_data:
            self.cell(0, 10, line, 0, 1)

        self.ln(10)

        self.set_fill_color(200, 220, 255)
        self.cell(80, 10, 'Description', 1, 0, 'C', 1)
        self.cell(30, 10, 'Quantity', 1, 0, 'C', 1)
        self.cell(40, 10, 'Unit Price', 1, 0, 'C', 1)
        self.cell(40, 10, 'Total', 1, 1, 'C', 1)

        for item in items:
            self.cell(80, 10, item['description'], 1)
            self.cell(30, 10, str(item['quantity']), 1)
            self.cell(40, 10, f"${item['unit_price']:.2f}", 1)
            self.cell(40, 10, f"${item['total']:.2f}", 1)
            self.ln(10)

        self.ln(10)
        self.cell(150, 10, 'Subtotal', 1)
        self.cell(40, 10, f"${totals['subtotal']:.2f}", 1, 1)

        self.cell(150, 10, 'Tax (10%)', 1)
        self.cell(40, 10, f"${totals['tax']:.2f}", 1, 1)

        self.cell(150, 10, 'Total', 1)
        self.cell(40, 10, f"${totals['total']:.2f}", 1, 1)

        self.ln(10)
        self.cell(0, 10, 'Payment Methods:', 0, 1)
        self.cell(0, 10, 'Bank Transfer: Account Number 123456789', 0, 1)
        self.cell(0, 10, 'PayPal: paypal@anikethome.com', 0, 1)

        self.ln(10)
        self.cell(0, 10, 'Terms & Conditions:', 0, 1)
        self.multi_cell(0, 10,
                        'Payment is due within 30 days from the date of the invoice. Late payments may incur additional fees.')

def main():
    pdf = PDF()
    pdf.add_page()

    invoice_data = [
        "Aniket Home Company",
        "123 Main Street",
        "City, State, ZIP Code",
        "Phone: (123) 456-7890",
        "Email: info@anikethome.com",
        "",
        "Invoice Number: 001",
        "Date: 2024-06-11",
        "Due Date: 2024-07-11",
        "",
        "Bill To:",
        "John Doe",
        "456 Elm Street",
        "City, State, ZIP Code",
        "",
    ]

    items = [
        {"description": "Product 1", "quantity": 2, "unit_price": 50.00, "total": 100.00},
        {"description": "Product 2", "quantity": 1, "unit_price": 75.00, "total": 75.00},
        {"description": "Service 1", "quantity": 3, "unit_price": 30.00, "total": 90.00}
    ]

    totals = {
        "subtotal": 265.00,
        "tax": 26.50,
        "total": 291.50
    }

    pdf.invoice_body(invoice_data, items, totals)
    pdf.output("synthetic_data_gr/Aniket_Home_Company_Invoice.pdf")


if __name__ == "__main__":
    main()


