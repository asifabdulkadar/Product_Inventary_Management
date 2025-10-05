#!/usr/bin/env python3
"""
Seed script to populate the database with sample data for testing.
Run this after setting up the Flask app to create initial products, locations, and movements.
"""

from app import app, db
from models import Product, Location, ProductMovement
from datetime import datetime
import random

def seed_database():
    """Create sample data for testing the inventory system."""
    
    with app.app_context():
        # Drop and recreate all tables
        print("Dropping existing tables...")
        db.drop_all()
        db.create_all()
        
        # Create sample products
        print("Creating products...")
        products = [
            Product(product_id="P-A", name="Product A", description="High-quality widget A"),
            Product(product_id="P-B", name="Product B", description="Premium gadget B"),
            Product(product_id="P-C", name="Product C", description="Standard component C"),
            Product(product_id="P-D", name="Product D", description="Specialized tool D"),
        ]
        
        # Create sample locations
        print("Creating locations...")
        locations = [
            Location(location_id="W-X", name="Warehouse X", description="Main distribution center"),
            Location(location_id="W-Y", name="Warehouse Y", description="Secondary storage facility"),
            Location(location_id="W-Z", name="Warehouse Z", description="Regional hub"),
            Location(location_id="S-1", name="Store 1", description="Downtown retail location"),
        ]
        
        # Add products and locations to database
        for p in products:
            db.session.add(p)
        for l in locations:
            db.session.add(l)
        db.session.commit()
        
        # Create sample movements
        print("Creating movements...")
        movements = []
        
        # Initial stock-in movements
        for product in products:
            for location in locations[:2]:  # Stock in first 2 locations
                qty = random.randint(10, 50)
                movement = ProductMovement(
                    from_location=None,
                    to_location=location.location_id,
                    product_id=product.product_id,
                    qty=qty
                )
                movements.append(movement)
        
        # Some transfers between locations
        for _ in range(10):
            product = random.choice(products)
            from_loc, to_loc = random.sample(locations, 2)
            qty = random.randint(1, 15)
            movement = ProductMovement(
                from_location=from_loc.location_id,
                to_location=to_loc.location_id,
                product_id=product.product_id,
                qty=qty
            )
            movements.append(movement)
        
        # Some stock-out movements
        for _ in range(8):
            product = random.choice(products)
            from_loc = random.choice(locations)
            qty = random.randint(1, 10)
            movement = ProductMovement(
                from_location=from_loc.location_id,
                to_location=None,
                product_id=product.product_id,
                qty=qty
            )
            movements.append(movement)
        
        # Add all movements to database
        for m in movements:
            db.session.add(m)
        db.session.commit()
        
        print(f" Seed completed successfully!")
        print(f"   - {len(products)} products created")
        print(f"   - {len(locations)} locations created")
        print(f"   - {len(movements)} movements created")
        print(f"\nYou can now run the Flask app and view the data at http://127.0.0.1:5000")

if __name__ == "__main__":
    seed_database()
