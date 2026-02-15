"""
Test authentication system
"""

from services.user_service import UserService

service = UserService()

print("="*60)
print("TESTING AUTHENTICATION")
print("="*60)

# Test 1: Valid login
print("\n1. Test valid login (admin)...")
user = service.authenticate("admin@example.com", "admin123")
if user:
    print(f"    Login successful!")
    print(f"     User: {user['name']} ({user['email']})")
    print(f"     Role: {user['role']}")
else:
    print("    Login failed")

# Test 2: Invalid password
print("\n2. Test invalid password...")
user = service.authenticate("admin@example.com", "wrongpassword")
if user:
    print("    Should have failed!")
else:
    print("    Correctly rejected invalid password")

# Test 3: Invalid email
print("\n3. Test invalid email...")
user = service.authenticate("nonexistent@example.com", "admin123")
if user:
    print("    Should have failed!")
else:
    print("    Correctly rejected invalid email")

# Test 4: Create new user
print("\n4. Test create new user...")
try:
    new_user = service.create_user(
        email="test@example.com",
        password="test123",
        role="reader",
        name="Test User"
    )
    print(f"    User created: {new_user['email']}")
except Exception as e:
    print(f"    Error: {e}")

# Test 5: Login with new user
print("\n5. Test login with newly created user...")
user = service.authenticate("test@example.com", "test123")
if user:
    print(f"    Login successful!")
    print(f"     User: {user['name']}")
    print(f"     Role: {user['role']}")
else:
    print("    Login failed")

# Test 6: Get all users
print("\n6. Get all users...")
all_users = service.get_all_users()
print(f"    Found {len(all_users)} users:")
for u in all_users:
    print(f"     - {u['email']} ({u['role']})")

print("\n" + "="*60)
print("ALL TESTS COMPLETE!")
print("="*60)