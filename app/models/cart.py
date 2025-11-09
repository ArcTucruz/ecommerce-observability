from datetime import datetime
from app import db

class Cart(db.Model):
    """
    Cart model - one cart per user
    """
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_total(self):
        """Calculate total cart value"""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items)
    
    def to_dict(self):
        """Convert cart object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total': self.get_total(),
            'item_count': self.get_item_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Cart user_id={self.user_id}>'


class CartItem(db.Model):
    """
    CartItem model - individual items in a cart
    """
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='cart_items')
    
    def get_subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.product.price * self.quantity
    
    def to_dict(self):
        """Convert cart item object to dictionary"""
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'subtotal': self.get_subtotal(),
            'added_at': self.added_at.isoformat() if self.added_at else None
        }
    
    def __repr__(self):
        return f'<CartItem product_id={self.product_id} quantity={self.quantity}>'