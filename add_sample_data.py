"""
Add sample products to the database
Run once: python add_sample_data.py
"""
from app import create_app, db
from app.models.product import Product

def add_sample_products():
    app = create_app()
    
    with app.app_context():
        # Check if products already exist
        if Product.query.count() > 0:
            print(f"⚠️ Database already has {Product.query.count()} products")
            response = input("Add more anyway? (y/n): ")
            if response.lower() != 'y':
                return
        
        products = [
            {
                'name': 'Gaming Laptop',
                'description': 'High-performance laptop with RTX 4070',
                'price': 1499.99,
                'stock_quantity': 15,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400'
            },
            {
                'name': 'Wireless Headphones',
                'description': 'Noise-cancelling over-ear headphones',
                'price': 299.99,
                'stock_quantity': 50,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
            },
            {
                'name': 'Smartphone Pro',
                'description': 'Latest flagship smartphone with 5G',
                'price': 999.99,
                'stock_quantity': 30,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400'
            },
            {
                'name': 'Mechanical Keyboard',
                'description': 'RGB mechanical gaming keyboard',
                'price': 149.99,
                'stock_quantity': 40,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400'
            },
            {
                'name': 'Gaming Mouse',
                'description': 'Wireless gaming mouse with 20,000 DPI',
                'price': 79.99,
                'stock_quantity': 60,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400'
            },
            {
                'name': '4K Monitor',
                'description': '27-inch 4K UHD gaming monitor, 144Hz',
                'price': 499.99,
                'stock_quantity': 20,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400'
            },
            {
                'name': 'Webcam HD',
                'description': '1080p webcam with auto-focus',
                'price': 89.99,
                'stock_quantity': 35,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1614624532983-4ce03382d63d?w=400'
            },
            {
                'name': 'USB-C Hub',
                'description': '7-in-1 USB-C hub with 4K HDMI',
                'price': 49.99,
                'stock_quantity': 80,
                'category': 'Accessories',
                'image_url': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400'
            },
            {
                'name': 'Laptop Stand',
                'description': 'Aluminum adjustable laptop stand',
                'price': 39.99,
                'stock_quantity': 45,
                'category': 'Accessories',
                'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400'
            },
            {
                'name': 'Desk Lamp LED',
                'description': 'Smart LED desk lamp with touch control',
                'price': 59.99,
                'stock_quantity': 55,
                'category': 'Accessories',
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400'
            },
            {
                'name': 'Portable SSD 1TB',
                'description': 'Fast external SSD with USB 3.2',
                'price': 129.99,
                'stock_quantity': 70,
                'category': 'Storage',
                'image_url': 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400'
            },
            {
                'name': 'Wireless Charger',
                'description': 'Fast wireless charging pad',
                'price': 29.99,
                'stock_quantity': 100,
                'category': 'Accessories',
                'image_url': 'https://images.unsplash.com/photo-1591290619762-9b49c29e9b2e?w=400'
            }
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f"✅ Added {len(products)} products to database!")
        print("\nProducts added:")
        for p in products:
            print(f"  - {p['name']}: ${p['price']}")

if __name__ == '__main__':
    add_sample_products()