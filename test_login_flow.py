"""
Test the EXACT login flow that the API uses
"""
from app import create_app, db
from app.services.user_service import UserService

def test_login():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Testing Login Flow")
        print("=" * 60)
        
        # Test with exact same function the API uses
        username = 'testuser'
        password = 'password123'
        
        print(f"\nAttempting login with:")
        print(f"  Username: '{username}'")
        print(f"  Password: '{password}'")
        
        user, error = UserService.authenticate_user(username, password)
        
        print("\n" + "=" * 60)
        if user:
            print("✅✅ LOGIN SUCCESSFUL!")
            print(f"  User ID: {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
        else:
            print("❌❌ LOGIN FAILED!")
            print(f"  Error: {error}")
        print("=" * 60)

if __name__ == '__main__':
    test_login()