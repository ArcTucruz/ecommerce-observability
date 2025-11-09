from datetime import datetime
from app import db

class Order(db.Model):
    """
    Order model - completed purchases
    """
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    status = db.Column(db.String(50), default='pending')  # pending, processing, shipped, delivered, cancelled
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert order object to dictionary"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'status': self.status,
            'total_amount': self.total_amount,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """
    OrderItem model - products in an order
    """
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)  # Store product name at time of order
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)  # Store price at time of order
    subtotal = db.Column(db.Float, nullable=False)
    
    # Relationships
    product = db.relationship('Product', backref='order_items')
    
    def to_dict(self):
        """Convert order item object to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price_at_purchase': self.price_at_purchase,
            'subtotal': self.subtotal
        }
    
    def __repr__(self):
        return f'<OrderItem order_id={self.order_id} product={self.product_name}>'

#**What this does:**
#- Creates `orders` table (completed purchases)
#- Creates `order_items` table (products in each order)
#- Stores snapshot of price at time of purchase
#- Tracks order status (pending, shipped, delivered, etc.)

## ✅ Current Progress - Models Complete!
#ecommerce-app/
#├── app/
#│   ├── __init__.py            ✅
#│   ├── models/
#│   │   ├── __init__.py        ✅
#│   │   ├── user.py            ✅ (User table)
#│   │   ├── product.py         ✅ (Product table)
#│   │   ├── cart.py            ✅ (Cart + CartItem tables)
#│   │   └── order.py           ✅ (Order + OrderItem tables)
#│   └── utils/
#│       ├── __init__.py        ✅
#│       └── logger.py          ✅