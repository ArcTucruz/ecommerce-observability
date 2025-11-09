"""
Fix testuser password
"""
from app import create_app, db
from app.models.user import User

def fix_password():
    app = create_app()
    
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        
        if not user:
            print("❌ User 'testuser' not found!")
            return
        
        print(f"Found user: {user.username}")
        print(f"Old password hash: {user.password_hash[:30]}...")
        
        # Set password properly
        user.set_password('password123')
        db.session.commit()
        
        print(f"\n✅ Password reset!")
        print(f"New password hash: {user.password_hash[:30]}...")
        
        # TEST PASSWORD IMMEDIATELY
        print("\n🧪 Testing password 'password123'...")
        if user.check_password('password123'):
            print("✅✅ PASSWORD WORKS! Try logging in now!")
        else:
            print("❌ Still broken - something is very wrong!")

if __name__ == '__main__':
    fix_password()