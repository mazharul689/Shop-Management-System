# Shop Management System

A comprehensive **Shop Management System** built with **Django** that streamlines inventory management, purchasing, sales operations, customer relationship management, and business reporting. The system is designed for retail businesses, grocery stores, pharmacies, electronics shops, and other small-to-medium enterprises that require efficient day-to-day operational management.

---

## 🚀 Features

### Authentication & Authorization

* Custom User Model based on Django `AbstractUser`
* Role-based access control
* Admin and Shopkeeper roles
* Secure authentication and session management

### Dashboard

* Sales overview
* Purchase overview
* Revenue analytics
* Profit/Loss summary
* Low-stock alerts
* Top-selling products
* Recent transactions

### Product Management

* Category Management
* Brand Management
* Unit Management
* Product CRUD Operations
* Product Images
* Barcode Support
* Stock Monitoring
* Low Stock Notifications

### Supplier Management

* Supplier Profiles
* Contact Information
* Due Tracking
* Purchase History

### Customer Management

* Customer Profiles
* Purchase History
* Loyalty Points
* Discount Tracking
* Return History
* Customer Ledger

### Purchase Management

* Purchase Entry
* Multiple Product Purchases
* Supplier Selection
* Due Management
* Purchase History
* Purchase Reports

### Sales Management (POS)

* Fast Product Search
* Customer Selection
* Multi-Item Sales
* Invoice Generation
* Discount Management
* Due Collection
* Sales History

### Inventory Management

* Real-Time Stock Tracking
* Stock Movement History
* Inventory Valuation
* Stock Adjustments
* Product Returns

### Reporting & Analytics

* Daily Sales Reports
* Weekly Sales Reports
* Monthly Sales Reports
* Yearly Sales Reports
* Purchase Reports
* Product-Wise Sales Reports
* Supplier Reports
* Customer Reports
* Profit & Loss Reports

---

## 🏗 System Architecture

### User Roles

#### Admin

* Manage Shopkeepers
* Manage Categories
* Manage Brands
* Manage Units
* Manage Products
* Manage Suppliers
* Manage Customers
* Manage Purchases
* View Sales Records
* View Reports
* Monitor Inventory
* Manage Expenses

#### Shopkeeper

* View Product Inventory
* Create Customers
* Process Sales
* Process Returns
* View Personal Sales History
* Search Customers
* Monitor Product Stock

---

## 🗄 Database Design

### Core Models

| Model                   | Purpose                     |
| ----------------------- | --------------------------- |
| CustomUser              | User Authentication & Roles |
| Category                | Product Categories          |
| Brand                   | Product Brands              |
| Unit                    | Product Measurement Units   |
| Product                 | Product Information & Stock |
| Supplier                | Supplier Management         |
| Customer                | Customer Records            |
| Purchase                | Purchase Transactions       |
| PurchaseItem            | Purchase Details            |
| Sale                    | Sales Transactions          |
| SaleItem                | Sales Details               |
| ProductReturn           | Return Management           |
| StockMovement           | Inventory Tracking          |
| LoyaltyPointTransaction | Customer Reward Tracking    |
| Expense                 | Expense Management          |

---

## ⚙️ Technology Stack

### Backend

* Django
* Python

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

### Database

* SQLite (Development)
* PostgreSQL (Production Recommended) [Future Planning]

### Tools

* Git
* GitHub
* VS Code

---

## 📈 Profit & Loss Calculation

```text
Profit = Total Sales Revenue
       - Product Cost
       - Business Expenses
```

The system generates:

* Daily Profit/Loss
* Weekly Profit/Loss
* Monthly Profit/Loss
* Yearly Profit/Loss

---

## 🔒 Security Features

* Django Authentication System
* CSRF Protection
* Session Security
* Password Hashing
* Role-Based Permissions
* Form Validation
* Input Sanitization

---

## 🚦 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/shop-management-system.git
cd shop-management-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

---

## 📋 Development Roadmap

### Phase 1

* Authentication
* Role Management
* Dashboard

### Phase 2

* Category Module
* Brand Module
* Unit Module
* Product Module

### Phase 3

* Supplier Module
* Customer Module

### Phase 4

* Purchase Management

### Phase 5

* Sales & POS Module

### Phase 6

* Inventory Tracking

### Phase 7

* Reports & Analytics

### Phase 8

* Testing & Optimization

---

## 🔮 Future Enhancements

* Barcode Scanner Integration
* QR Code Support
* SMS Notifications
* WhatsApp Notifications
* Multi-Branch Support
* Product Expiry Management
* Mobile Application
* REST API Integration
* Cloud Backup
* Multi-Currency Support
* VAT & Tax Configuration

---

## 🤝 Contributing

Contributions are welcome. Please fork the repository, create a feature branch, and submit a pull request for review.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Md. Mazharul Islam**

Software Engineer | Django Developer | Angular Developer

For questions, suggestions, or collaboration opportunities, feel free to open an issue or submit a pull request.
