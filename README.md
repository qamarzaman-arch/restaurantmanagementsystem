# Restaurant Management System

A full-featured, offline desktop invoicing and management software for restaurants.

## Features

- **Dashboard**: Real-time overview of daily sales, orders, and active tables with interactive charts (Pie, Bar, Line) for deep insights.
- **Customer Management**: Keep track of customer contact information and loyalty points.
- **Table Management**: Visual status and management of restaurant tables.
- **Menu Management**: Categorized menu items with easy CRUD operations.
- **Order & Billing**:
  - Table-based ordering system.
  - Interactive menu selection.
  - Automatic tax and discount calculations.
  - Multiple payment methods (Cash, Card, Online).
  - Professional PDF invoice generation.
- **Reporting & Insights**:
  - Sales summary with robust date filtering.
  - Advanced metrics like Average Order Value and Most Popular Item.
  - Export sales data to CSV for external analysis.
- **Security**:
  - Secure login system with hashed passwords.
  - Role-based access (Admin vs Staff).

## Technologies Used

- **Python 3.12**
- **PyQt6 & PyQt6-Charts**: For a modern GUI with interactive data visualizations.
- **SQLite**: For fast, offline data storage.
- **ReportLab**: For professional PDF generation.
- **Werkzeug**: For secure password hashing.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python src/main.py
   ```

3. **Default Credentials**:
   - **Username**: `admin`
   - **Password**: `admin123`

## Directory Structure

- `src/`: Source code
  - `database/`: Database logic and SQLite manager.
  - `ui/`: PyQt6 windows and widgets.
  - `logic/`: Business and billing logic.
  - `utils/`: Helpers (PDF generation).
- `tests/`: Test suites and UI verification scripts.
- `invoices/`: Generated PDF invoices.
- `reports/`: Exported sales reports.

## Development and Testing

To run tests:
```bash
pytest
```

To run UI verification (requires Xvfb or a display):
```bash
export PYTHONPATH=$PYTHONPATH:.
python tests/capture_ui.py
```
