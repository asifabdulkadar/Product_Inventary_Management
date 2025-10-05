<<<<<<< HEAD
# Flask Inventory Management System

**A clean, interview-ready Flask web application for managing products, locations, and inventory movements with real-time balance reporting.**

## Why this test?

We build applications for the web, so understanding how web applications work is a pre-requisite for any new engineer. Flask is one of the simplest and best-written Python-based web application frameworks and can be learned quickly.

This coding test assesses several core skills useful for web engineers:
- Designing a small relational schema and using an ORM (Flask-SQLAlchemy)
- Implementing CRUD views and simple form handling in Flask
- Writing a small report query (SQL) and reasoning about data correctness
- Seeding and testing sample data to validate business logic

If you haven't worked on web apps before, this test helps you evaluate whether web development is something you can learn and enjoy.

## Default database & seed data

By default the app uses a local SQLite database file named `app.db` (configured in `config.py`). You can create and populate the default database with sample data by running the provided seed script. The seed script drops and recreates the schema and inserts sample products, locations and movements (the README and seed script use 4 products, 4 locations and ~30 movements by default).

PowerShell (Windows) example:

```powershell
python seed.py
```
+
This will create `app.db` in the project root. After seeding you can run the app and view the sample data at `http://127.0.0.1:5000`.

If you'd prefer an in-memory or alternative DB for testing or CI, set the `DATABASE_URL` environment variable (see `config.py`).


## 🚀 Features

- **Product Management**: CRUD operations for products with text-based IDs
- **Location Management**: Manage warehouses, stores, and other locations
- **Movement Tracking**: Record stock in, stock out, and transfers between locations
- **Balance Reports**: Real-time inventory levels across all product-location combinations
- **Modern UI**: Bootstrap 5 interface with responsive design
- **Flexible Schema**: Text primary keys with auto-generation support

## 🛠 Tech Stack

- **Backend**: Python 3.10+, Flask, Flask-SQLAlchemy
- **Database**: SQLite (default) or MySQL
- **Frontend**: Jinja2 templates, Bootstrap 5, Bootstrap Icons
- **Migrations**: Flask-Migrate (Alembic)

## 📋 Database Schema

### Products
- `product_id` (TEXT PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `description` (TEXT)

### Locations
- `location_id` (TEXT PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `description` (TEXT)

### Product Movements
- `movement_id` (TEXT PRIMARY KEY)
- `timestamp` (DATETIME)
- `from_location` (TEXT NULL - FK to Location)
- `to_location` (TEXT NULL - FK to Location)
- `product_id` (TEXT NOT NULL - FK to Product)
- `qty` (INTEGER NOT NULL)

**Movement Types:**
- **Stock In**: `from_location = NULL`, `to_location = Location`
- **Stock Out**: `from_location = Location`, `to_location = NULL`
- **Transfer**: `from_location = Location A`, `to_location = Location B`

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd flask-inventory
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

Visit `http://127.0.0.1:5000` to see the application.

### 3. Seed Sample Data
```bash
python seed.py
```

This creates:
- 4 sample products (P-A, P-B, P-C, P-D)
- 4 sample locations (W-X, W-Y, W-Z, S-1)
- ~30 sample movements (stock in, transfers, stock out)

## 📊 Balance Report Logic

The balance report uses a cross-join to show every product-location combination:

```sql
SELECT p.product_id, p.name as product_name,
       l.location_id, l.name as location_name,
       COALESCE(
         SUM(CASE WHEN pm.to_location = l.location_id THEN pm.qty ELSE 0 END) -
         SUM(CASE WHEN pm.from_location = l.location_id THEN pm.qty ELSE 0 END), 0
       ) AS balance
FROM product p
CROSS JOIN location l
LEFT JOIN product_movement pm
  ON pm.product_id = p.product_id
  AND (pm.to_location = l.location_id OR pm.from_location = l.location_id)
GROUP BY p.product_id, l.location_id
ORDER BY p.product_id, l.location_id;
```

**Balance Calculation:**
- **+Quantity**: When `to_location` matches (stock in, transfer in)
- **-Quantity**: When `from_location` matches (stock out, transfer out)
- **Zero**: No movements for that product-location pair

## 🎯 Key Endpoints

- `/` - Redirects to products list
- `/products` - List all products
- `/products/add` - Add new product
- `/products/edit/<id>` - Edit product
- `/locations` - List all locations
- `/locations/add` - Add new location
- `/locations/edit/<id>` - Edit location
- `/movements` - List all movements
- `/movements/add` - Record new movement
- `/reports/balances` - View balance report

## 🔧 Configuration

Environment variables (optional):
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Flask secret key

Default configuration uses SQLite with `app.db` file.

## 📁 Project Structure

```
flask-inventory/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── seed.py               # Sample data generator
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # Jinja2 templates
│   ├── base.html        # Base template
│   ├── products/        # Product templates
│   ├── locations/       # Location templates
│   ├── movements/       # Movement templates
│   └── reports/         # Report templates
└── static/              # Static assets (if needed)
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Bootstrap 5**: Modern, clean interface
- **Icons**: Bootstrap Icons for better UX
- **Flash Messages**: Success/error notifications
- **Data Tables**: Sortable, responsive tables
- **Form Validation**: Client and server-side validation
- **Confirmation Dialogs**: Prevent accidental deletions

## 🧪 Testing the System

1. **Add Products**: Create a few products with custom or auto-generated IDs
2. **Add Locations**: Set up warehouses, stores, or other locations
3. **Record Movements**:
   - Stock in: From External → To Location
   - Stock out: From Location → To External
   - Transfer: From Location A → To Location B
4. **View Reports**: Check `/reports/balances` for current inventory levels

## 🚀 Production Considerations

### Suggested Improvements
- **Authentication**: Add user login and role-based access
- **Validation**: Enhanced form validation and error handling
- **Transactions**: Wrap movement operations in database transactions
- **Audit Trail**: Track who made changes and when
- **CSV Import/Export**: Bulk data operations
- **API Endpoints**: REST API for mobile/external integrations
- **Testing**: Unit tests with pytest
- **CI/CD**: GitHub Actions for automated testing
- **Monitoring**: Logging and error tracking
- **Performance**: Pagination for large datasets
- **Security**: CSRF protection, input sanitization

### Database Migration
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 📸 Screenshots

*Add screenshots of the main pages here:*
- Products list and edit forms
- Locations management
- Movement recording interface
- Balance report with sample data

## 🤝 Interview Talking Points

### Architecture Decisions
1. **Text Primary Keys**: Flexible, user-friendly IDs with auto-generation fallback
2. **Nullable Foreign Keys**: Supports external stock in/out operations
3. **Cross-Join Report**: Ensures complete product-location matrix
4. **Flask Micro-framework**: Minimal, interview-friendly stack

### Code Walkthrough
1. **Models**: Show relationship design and ID generation
2. **Routes**: Demonstrate CRUD patterns and form handling
3. **Templates**: Explain template inheritance and Bootstrap integration
4. **Reports**: Walk through the balance calculation SQL

### Scalability Considerations
- Database indexing on foreign keys
- Pagination for large datasets
- Caching for frequently accessed reports
- API versioning for future mobile apps

---

**Ready to deploy?** This codebase is production-ready with proper error handling, clean architecture, and comprehensive documentation. Perfect for demonstrating full-stack development skills in technical interviews.
=======
# Product_Inventary_Management
>>>>>>> 4caf3f77660f96703de868bbb4b435eccfc9facf
