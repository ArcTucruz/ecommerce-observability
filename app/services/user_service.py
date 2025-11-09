import logging
from app import db
from app.models.user import User
from app.models.cart import Cart

logger = logging.getLogger(__name__)

class UserService:
    
    @staticmethod
    def create_user(username, email, password, full_name=None):
        """Register a new user with validation"""
        try:
            # Validation: Username length
            if len(username) < 3:
                logger.warning(f"❌ Registration failed: Username too short ('{username}' - only {len(username)} chars, need 3+)")
                return None, "Username must be at least 3 characters"
            
            # Validation: Password strength
            if len(password) < 6:
                logger.warning(f"❌ Registration failed: Password too weak for user '{username}' (only {len(password)} chars, need 6+)")
                return None, "Password must be at least 6 characters"
            
            # Validation: Email format
            if '@' not in email or '.' not in email:
                logger.warning(f"❌ Registration failed: Invalid email format ('{email}')")
                return None, "Invalid email format"
            
            # Check if username exists
            if User.query.filter_by(username=username).first():
                logger.warning(f"❌ Registration failed: Username '{username}' already exists (HTTP 400)")
                return None, "Username already exists"
            
            # Check if email exists
            if User.query.filter_by(email=email).first():
                logger.warning(f"❌ Registration failed: Email '{email}' already registered (HTTP 400)")
                return None, "Email already exists"
            
            # Create user
            user = User(username=username, email=email, full_name=full_name)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Create cart
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()
            
            logger.info(f"✅ User registered successfully: '{username}' (ID: {user.id}, Email: {email}) → HTTP 201")
            
            # Record metric
            try:
                from app.metrics import record_user_registration
                record_user_registration()
            except:
                pass
            
            return user, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"💥 Error creating user: {str(e)} → HTTP 500")
            return None, str(e)
    
    @staticmethod
    def authenticate_user(username, password):
        """Login user with detailed logging"""
        try:
            logger.info(f"🔐 Login attempt for username: '{username}'")
            
            user = User.query.filter_by(username=username).first()
            
            if not user:
                logger.warning(f"❌ Login failed: User '{username}' not found in database → HTTP 401")
                try:
                    from app.metrics import record_login
                    record_login(success=False)
                except:
                    pass
                return None, "Invalid credentials"
            
            if not user.check_password(password):
                logger.warning(f"❌ Login failed: Wrong password for user '{username}' → HTTP 401")
                try:
                    from app.metrics import record_login
                    record_login(success=False)
                except:
                    pass
                return None, "Invalid credentials"
            
            logger.info(f"✅ Login successful: '{username}' (ID: {user.id}) → HTTP 200")
            
            try:
                from app.metrics import record_login
                record_login(success=True)
            except:
                pass
            
            return user, None
            
        except Exception as e:
            logger.error(f"💥 Server error during login: {str(e)} → HTTP 500")
            return None, str(e)
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                logger.warning(f"❌ User not found: ID {user_id} → HTTP 404")
                return None, "User not found"
            
            logger.info(f"✅ User retrieved: '{user.username}' (ID: {user_id}) → HTTP 200")
            return user, None
        except Exception as e:
            logger.error(f"💥 Error fetching user: {str(e)} → HTTP 500")
            return None, str(e)