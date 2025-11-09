"""
Test if werkzeug password hashing works at all
"""
from werkzeug.security import generate_password_hash, check_password_hash

def test_werkzeug():
    print("Testing werkzeug password hashing directly...")
    print("="*60)
    
    password = 'admin123'
    
    # Generate hash
    print(f"Password: {password}")
    password_hash = generate_password_hash(password)
    print(f"Hash generated: {password_hash[:50]}...")
    
    # Test correct password
    print(f"\n🧪 Testing correct password '{password}'...")
    result = check_password_hash(password_hash, password)
    print(f"   Result: {result}")
    if result:
        print("   ✅ WORKS!")
    else:
        print("   ❌ BROKEN!")
        return False
    
    # Test wrong password
    print(f"\n🧪 Testing wrong password 'wrongpass'...")
    result = check_password_hash(password_hash, 'wrongpass')
    print(f"   Result: {result}")
    if not result:
        print("   ✅ Correctly rejected!")
    else:
        print("   ❌ Should have rejected!")
        return False
    
    print("\n" + "="*60)
    print("✅✅ Werkzeug itself works fine!")
    return True

if __name__ == '__main__':
    if test_werkzeug():
        print("\nWerkzeug is OK. Problem is in User model!")
    else:
        print("\nWerkzeug is BROKEN. Need to reinstall!")