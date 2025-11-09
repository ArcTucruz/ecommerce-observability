import logging
from app import db
from app.models.cart import Cart, CartItem
from app.models.product import Product

logger = logging.getLogger(__name__)

class CartService:
    
    @staticmethod
    def get_cart(user_id):
        """Get user's cart"""
        try:
            cart = Cart.query.filter_by(user_id=user_id).first()
            if not cart:
                cart = Cart(user_id=user_id)
                db.session.add(cart)
                db.session.commit()
                logger.info(f"🛒 New cart created for user {user_id}")
            return cart, None
        except Exception as e:
            logger.error(f"💥 Error fetching cart: {str(e)} → HTTP 500")
            return None, str(e)
    
    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        """Add product to cart with stock validation"""
        try:
            # Validation: Quantity must be positive
            if quantity <= 0:
                logger.warning(f"❌ Add to cart failed: Invalid quantity {quantity} (must be > 0) → HTTP 400")
                return None, "Quantity must be at least 1"
            
            cart, error = CartService.get_cart(user_id)
            if error:
                return None, error
            
            product = Product.query.get(product_id)
            if not product:
                logger.warning(f"❌ Add to cart failed: Product ID {product_id} not found → HTTP 404")
                return None, "Product not found"
            
            # Stock validation
            if not product.is_in_stock(quantity):
                logger.warning(f"❌ Add to cart failed: '{product.name}' out of stock! (Requested: {quantity}, Available: {product.stock_quantity}) → HTTP 400")
                return None, f"Product out of stock (available: {product.stock_quantity})"
            
            # Check if item already in cart
            cart_item = CartItem.query.filter_by(
                cart_id=cart.id, product_id=product_id
            ).first()
            
            if cart_item:
                new_quantity = cart_item.quantity + quantity
                if not product.is_in_stock(new_quantity):
                    logger.warning(f"❌ Add to cart failed: Not enough stock for '{product.name}' (Want: {new_quantity}, Available: {product.stock_quantity}) → HTTP 400")
                    return None, f"Not enough stock (available: {product.stock_quantity})"
                cart_item.quantity = new_quantity
                logger.info(f"🛒 Cart updated: '{product.name}' quantity → {new_quantity} (User: {user_id}) → HTTP 200")
            else:
                cart_item = CartItem(
                    cart_id=cart.id,
                    product_id=product_id,
                    quantity=quantity
                )
                db.session.add(cart_item)
                logger.info(f"🛒 Added to cart: '{product.name}' x{quantity} (User: {user_id}, Price: ${product.price}) → HTTP 200")
            
            # Record metric
            try:
                from app.metrics import record_cart_addition
                record_cart_addition()
            except:
                pass
            
            db.session.commit()
            return cart, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"💥 Error adding to cart: {str(e)} → HTTP 500")
            return None, str(e)
    
    @staticmethod
    def remove_from_cart(user_id, product_id):
        """Remove product from cart"""
        try:
            cart, error = CartService.get_cart(user_id)
            if error:
                return None, error
            
            cart_item = CartItem.query.filter_by(
                cart_id=cart.id, product_id=product_id
            ).first()
            
            if not cart_item:
                logger.warning(f"❌ Remove failed: Product ID {product_id} not in cart (User: {user_id}) → HTTP 404")
                return None, "Item not in cart"
            
            product_name = cart_item.product.name
            db.session.delete(cart_item)
            
            db.session.commit()
            
            logger.info(f"🛒 Removed from cart: '{product_name}' (User: {user_id}) → HTTP 200")
            return cart, None
        except Exception as e:
            db.session.rollback()
            logger.error(f"💥 Error removing from cart: {str(e)} → HTTP 500")
            return None, str(e)