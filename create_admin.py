"""
Create an admin user
"""
from app import create_app, db
from app.models.user import User
from app.models.cart import Cart

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            # Update existing user to admin
            admin.is_admin = True
            db.session.commit()
            print(f"✅ User 'admin' updated to admin status")
        else:
            # Create new admin user
            admin = User(
                username='admin',
                email='admin@ecommerce.com',
                full_name='Admin User',
                is_admin=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            # Create cart
            cart = Cart(user_id=admin.id)
            db.session.add(cart)
            db.session.commit()
            
            print(f"✅ Admin user created!")
        
        print(f"\nAdmin Login Credentials:")
        print(f"  Username: admin")
        print(f"  Password: admin123")
        print(f"  Is Admin: {admin.is_admin}")

if __name__ == '__main__':
    create_admin_user()