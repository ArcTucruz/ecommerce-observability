from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
    User model - represents registered users
    """
    __tablename__ = 'users'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (connections to other tables)
    cart = db.relationship('Cart', backref='user', uselist=False, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the password (for security)"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary (for JSON responses)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

#**What this does:**
#- Creates `users` table in database
#- Stores username, email, password (hashed for security!)
#- Has methods to set/check passwords
#- Connects to Cart and Orders

#**Current Progress:**

#ecommerce-app/
#├── venv/                    ✅
#├── app/
#│   ├── __init__.py         ✅
#│   ├── utils/
#│   │   ├── __init__.py     ✅
#│   │   └── logger.py       ✅
#│   └── models/
#│       ├── __init__.py     ✅
#│       └── user.py         ✅
#├── static/                  (empty for now)
#├── logs/                    (will be auto-created)
#├── .env                     ✅
#└── requirements.txt         ✅