# Restaurant Management & Invoicing System

A full-featured, offline desktop application for restaurant management, built with Python 3.12 and PyQt6.

## Features
- **Dashboard**: Real-time sales analytics and trends.
- **POS / Invoicing**: Fast order creation with cart management and automated PDF invoice generation.
- **KOT & Receipts**: Specialized support for Kitchen Order Tickets and Thermal Receipts.
- **Inventory Management**: Track stock levels with automated low-stock alerts.
- **Expense Tracking**: Manage daily restaurant operational costs.
- **User Management**: Role-based access control (Admin/Staff) with secure authentication.
- **Customer Loyalty**: Track customer history and loyalty points.
- **Database Maintenance**: Integrated backup and restore functionality.

## Prerequisites
- Python 3.12 or higher
- (Recommended) A virtual environment

## Installation

1. **Clone or Extract the Project**
   ```bash
   cd restaurantmanagementsystem
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the application, run:
```bash
python -m src.main
```

### Default Credentials
- **Admin**: `admin` / `admin123`
- **Staff**: `staff` / `staff123`

## Technical Details
- **GUI Framework**: PyQt6
- **Database**: SQLite3
- **Reports**: CSV Export & ReportLab (PDF)
- **Charts**: PyQt6-Charts
- **Security**: Werkzeug (Password Hashing)

## Local Development & Troubleshooting
If you encounter `QFont::setPointSize` warnings on Windows, the system has been updated to set a default font size of 10pt. These warnings are typically non-blocking. Ensure your display scaling settings are compatible with high-DPI applications.
