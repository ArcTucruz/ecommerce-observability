import logging
import uuid
from datetime import datetime
from app import db
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem

logger = logging.getLogger(__name__)

class OrderService:
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"ORD-{timestamp}-{unique_id}"
    
    @staticmethod
    def create_order(user_id, shipping_address, payment_method='credit_card'):
        """Create order from cart"""
        try:
            cart = Cart.query.filter_by(user_id=user_id).first()
            if not cart or not cart.items.count():
                return None, "Cart is empty"
            
            # Create order
            order = Order(
                user_id=user_id,
                order_number=OrderService.generate_order_number(),
                total_amount=cart.get_total(),
                shipping_address=shipping_address,
                payment_method=payment_method,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()
            
            # Create order items
            for cart_item in cart.items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    product_name=cart_item.product.name,
                    quantity=cart_item.quantity,
                    price_at_purchase=cart_item.product.price,
                    subtotal=cart_item.get_subtotal()
                )
                db.session.add(order_item)
                cart_item.product.reduce_stock(cart_item.quantity)
            
            # Clear cart
            CartItem.query.filter_by(cart_id=cart.id).delete()
            
            db.session.commit()
            logger.info(f"Order created: {order.order_number}")
            # Record metric
            try:
                from app.metrics import record_order
                record_order(order.total_amount)
            except:
                pass
            
            return order, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating order: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def get_user_orders(user_id):
        """Get all orders for a user"""
        try:
            orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
            return orders, None
        except Exception as e:
            return None, str(e)


#**Simple! Create orders and get order history.**

## ✅ Services Done!

#app/
#└── services/
#    ├── __init__.py             ✅
#    ├── user_service.py         ✅ (Register, Login)
#    ├── product_service.py      ✅ (CRUD products)
#    ├── cart_service.py         ✅ (Add/Remove cart)
#    └── order_service.py        ✅ (Create orders)