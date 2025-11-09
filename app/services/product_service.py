import logging
from app import db
from app.models.product import Product

logger = logging.getLogger(__name__)

class ProductService:
    
    @staticmethod
    def create_product(name, price, description=None, stock_quantity=0, category=None):
        """Create product with validation"""
        try:
            # Validation: Price must be positive
            if price <= 0:
                logger.warning(f"❌ Product creation failed: Invalid price ${price} for '{name}' (must be > 0) → HTTP 400")
                return None, "Price must be greater than 0"
            
            # Validation: Stock can't be negative
            if stock_quantity < 0:
                logger.warning(f"❌ Product creation failed: Negative stock {stock_quantity} for '{name}' → HTTP 400")
                return None, "Stock quantity cannot be negative"
            
            # Validation: Name not empty
            if not name or len(name) < 2:
                logger.warning(f"❌ Product creation failed: Name too short (need 2+ chars) → HTTP 400")
                return None, "Product name must be at least 2 characters"
            
            product = Product(
                name=name,
                description=description,
                price=price,
                stock_quantity=stock_quantity,
                category=category
            )
            
            db.session.add(product)
            db.session.commit()
            
            logger.info(f"✅ Product created: '{name}' (ID: {product.id}, Price: ${price}, Stock: {stock_quantity}) → HTTP 201")
            return product, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"💥 Error creating product: {str(e)} → HTTP 500")
            return None, str(e)
    
    @staticmethod
    def get_all_products():
        """Get all active products"""
        try:
            products = Product.query.filter_by(is_active=True).all()
            logger.info(f"📦 Retrieved {len(products)} products → HTTP 200")
            return products, None
        except Exception as e:
            logger.error(f"💥 Error fetching products: {str(e)} → HTTP 500")
            return None, str(e)
    
    @staticmethod
    def get_product_by_id(product_id):
        """Get product by ID"""
        try:
            product = Product.query.get(product_id)
            if not product:
                logger.warning(f"❌ Product not found: ID {product_id} → HTTP 404")
                return None, "Product not found"
            
            logger.info(f"✅ Product retrieved: '{product.name}' (ID: {product_id}) → HTTP 200")
            return product, None
        except Exception as e:
            logger.error(f"💥 Error fetching product: {str(e)} → HTTP 500")
            return None, str(e)


## 🧪 Now Test and See BOTH!

#**Restart the app and try these scenarios:**

### Test 1: Weak Password

#Register with password: "123"

#**Log will show:**

#❌ Registration failed: Password too weak (only 3 chars, need 6+) → HTTP 400
#POST /api/users/register 400

#**You see BOTH: The reason AND the code!**

### Test 2: Wrong Login

#Try wrong password

#**Log will show:**

#❌ Login failed: Wrong password for user 'Yuli44' → HTTP 401
#POST /api/users/login 401

### Test 3: Out of Stock

#Try to add 999 laptops

#**Log will show:**

#❌ Add to cart failed: 'Laptop' out of stock! (Requested: 999, Available: 5) → HTTP 400
#OST /api/cart/2/add 400