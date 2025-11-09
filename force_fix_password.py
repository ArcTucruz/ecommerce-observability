"""
Force fix password with verification
"""
from app import create_app, db
from app.models.user import User

def force_fix():
    app = create_app()
    
    with app.app_context():
        # Get user
        user = User.query.filter_by(username='testuser').first()
        
        if not user:
            print("❌ User not found!")
            return
        
        print("Step 1: Current state")
        print(f"  Username: {user.username}")
        print(f"  Old hash: {user.password_hash[:40]}...")
        
        print("\nStep 2: Setting new password...")
        user.set_password('password123')
        
        print(f"  New hash: {user.password_hash[:40]}...")
        
        print("\nStep 3: Committing to database...")
        db.session.add(user)  # Explicitly add
        db.session.commit()
        print("  ✅ Committed!")
        
        print("\nStep 4: RE-QUERYING user from database...")
        # Close session and re-query to get fresh data
        db.session.expire_all()
        user = User.query.filter_by(username='testuser').first()
        
        print(f"  Hash after re-query: {user.password_hash[:40]}...")
        
        print("\nStep 5: Testing password...")
        if user.check_password('password123'):
            print("  ✅ Password WORKS!")
        else:
            print("  ❌ Password FAILED!")
            
        print("\nStep 6: Testing via UserService...")
        from app.services.user_service import UserService
        test_user, error = UserService.authenticate_user('testuser', 'password123')
        
        if test_user:
            print("  ✅✅ UserService login WORKS!")
        else:
            print(f"  ❌ UserService login FAILED: {error}")

if __name__ == '__main__':
    force_fix()