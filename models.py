from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def gen_id(prefix="id"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

class Product(db.Model):
    product_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)

    def __init__(self, product_id=None, name=None, description=None):
        self.product_id = product_id or gen_id("prod")
        self.name = name
        self.description = description

class Location(db.Model):
    location_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)

    def __init__(self, location_id=None, name=None, description=None):
        self.location_id = location_id or gen_id("loc")
        self.name = name
        self.description = description

class ProductMovement(db.Model):
    movement_id = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    from_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __init__(self, movement_id=None, from_location=None, to_location=None, product_id=None, qty=0):
        self.movement_id = movement_id or gen_id("mov")
        self.from_location = from_location
        self.to_location = to_location
        self.product_id = product_id
        self.qty = qty
#why this file is important:
# This file defines the database models for the application using SQLAlchemy ORM. It includes models for products, locations, and product movements, which are essential for tracking inventory and movements between locations.
# These models are used throughout the application to interact with the database, perform CRUD operations, and generate reports.
# The models also include helper functions for generating unique IDs, which are used as primary keys in the database tables.
# The db instance is created here and imported in the main application file (app.py) to initialize the database connection.
# if an interviewer asks you about the models.py file, you can explain that it defines the structure of the database tables and their relationships, which are crucial for the app's functionality.