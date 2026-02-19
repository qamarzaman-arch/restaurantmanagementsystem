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

## Packaging for Distribution (Windows)

To create a professional, standalone installer for Windows that does not require Python to be installed on the client machine:

### Step 1: Build the Executable
1. Open the project folder on a Windows machine.
2. Double-click `scripts/build_windows.bat`.
3. This will create a `dist/RestaurantOS` folder containing the application.

### Step 2: Create the Installer
1. Download and install [Inno Setup](https://jrsoftware.org/isdl.php).
2. Right-click `scripts/installer_setup.iss` and select "Compile".
3. Once finished, a professional installer named `RestaurantOS_Setup.exe` will be created in the `installer/` folder.

### No-Warning Distribution
Windows may show a "Windows protected your PC" (SmartScreen) warning for new, unsigned applications. To remove this for professional sale:
1. **Code Signing**: You should obtain a Code Signing Certificate (from vendors like DigiCert or Sectigo) and sign the generated `.exe` file using `signtool`.
2. **Reputation**: As more users install your software, Microsoft SmartScreen's reputation for your app will improve, and the warnings will eventually disappear even without signing (though signing is highly recommended for commercial software).
