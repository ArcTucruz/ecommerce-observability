"""
Create completely fresh user in new database
"""
from app import create_app, db
from app.models.user import User
from app.models.cart import Cart

def create_fresh():
    app = create_app()
    
    with app.app_context():
        print("Creating brand new user...")
        
        # Create user
        user = User(
            username='admin',
            email='admin@example.com',
            full_name='Admin User'
        )
        user.set_password('admin123')
        
        db.session.add(user)
        db.session.commit()
        
        print(f"✅ User created (ID: {user.id})")
        
        # Create cart
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
        
        print("✅ Cart created")
        
        # TEST IMMEDIATELY in same session
        print("\n🧪 Testing password in same session...")
        if user.check_password('admin123'):
            print("  ✅ Works in same session!")
        else:
            print("  ❌ BROKEN in same session!")
            return
        
        # Close session and re-query
        db.session.close()
        
        print("\n🧪 Testing after session close...")
        fresh_user = User.query.filter_by(username='admin').first()
        if fresh_user.check_password('admin123'):
            print("  ✅ Works after re-query!")
        else:
            print("  ❌ BROKEN after re-query!")
            return
        
        # Test via UserService
        print("\n🧪 Testing via UserService...")
        from app.services.user_service import UserService
        test_user, error = UserService.authenticate_user('admin', 'admin123')
        
        if test_user:
            print("  ✅✅✅ ALL TESTS PASSED!")
            print("\n" + "="*60)
            print("USE THESE CREDENTIALS:")
            print("  Username: admin")
            print("  Password: admin123")
            print("="*60)
        else:
            print(f"  ❌ UserService FAILED: {error}")
            print("\n⚠️ Something is deeply broken with password hashing!")

if __name__ == '__main__':
    create_fresh()