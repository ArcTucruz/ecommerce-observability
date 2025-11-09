"""
Check registered users in database
"""
from app import create_app, db
from app.models.user import User

def list_users():
    app = create_app()
    
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("❌ No users found in database!")
            return
        
        print(f"\n✅ Found {len(users)} user(s):\n")
        print("-" * 60)
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Full Name: {user.full_name}")
            print(f"Created: {user.created_at}")
            print("-" * 60)

if __name__ == '__main__':
    list_users()