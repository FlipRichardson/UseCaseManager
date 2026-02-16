"""
Test permission system with agent
"""

from agent import run_agent
from agent.tool_executor import set_current_user
from services.user_service import UserService
from services import UseCaseService


print("="*80)
print("TESTING PERMISSION SYSTEM WITH AGENT")
print("="*80)

user_service = UserService()

# Test 1: Reader tries to create (should fail)
print("\n" + "─"*80)
print("TEST 1: Reader tries to create use case (should fail)")
print("─"*80)

reader = user_service.authenticate("reader@example.com", "reader123")
set_current_user(reader)
print(f"Logged in as: {reader['name']} (role: {reader['role']})")

response = run_agent(
    "Create a new use case called 'Test Permission' for Siemens Energy",
    verbose=False
)
print(f"\nResponse: {response[:200]}...")

# Test 2: Maintainer creates (should succeed)
print("\n" + "─"*80)
print("TEST 2: Maintainer creates use case (should succeed)")
print("─"*80)

maintainer = user_service.authenticate("maintainer@example.com", "maintainer123")
set_current_user(maintainer)
print(f"Logged in as: {maintainer['name']} (role: {maintainer['role']})")

response = run_agent(
    "Create a new use case called 'Maintainer Test' for Bosch in Manufacturing",
    verbose=False
)
print(f"\nResponse: {response[:200]}...")

# Test 3: Maintainer tries to delete (should fail - admin only)
print("\n" + "─"*80)
print("TEST 3: Maintainer tries to delete (should fail - admin only)")
print("─"*80)

response = run_agent(
    "Delete use case with ID 1",
    verbose=False
)
print(f"\nResponse: {response[:200]}...")

# Test 4: Admin deletes (should succeed)
print("\n" + "─"*80)
print("TEST 4: Admin deletes use case (should succeed)")
print("─"*80)

admin = user_service.authenticate("admin@example.com", "admin123")
set_current_user(admin)
print(f"Logged in as: {admin['name']} (role: {admin['role']})")

response = run_agent(
    "Delete use case with ID 1",
    verbose=False
)
print(f"\nResponse: {response[:200]}...")

# Test 5: Everyone can read
print("\n" + "─"*80)
print("TEST 5: Reader can view use cases (should succeed)")
print("─"*80)

set_current_user(reader)
print(f"Logged in as: {reader['name']} (role: {reader['role']})")

response = run_agent(
    "Show me all use cases for Siemens Energy",
    verbose=False
)
print(f"\nResponse: {response[:200]}...")

print("\n" + "="*80)
print("PERMISSION TESTS COMPLETE")
print("="*80)



service = UseCaseService()
user_service = UserService()

print("="*60)
print("DIRECT PERMISSION TESTS")
print("="*60)

# Test 1: Maintainer tries to delete directly
print("\nTest: Maintainer tries to delete use case #2...")
maintainer = user_service.authenticate("maintainer@example.com", "maintainer123")

try:
    result = service.delete_use_case(2, current_user=maintainer)
    print("FAILED: Delete should have been blocked!")
    print(f"Result: {result}")
except Exception as e:
    print(f"Correctly blocked: {e}")

# Test 2: Admin tries to delete directly
print("\nTest: Admin tries to delete use case #3...")
admin = user_service.authenticate("admin@example.com", "admin123")

try:
    result = service.delete_use_case(3, current_user=admin)
    print(f"Successfully deleted: {result['title']}")
except Exception as e:
    print(f"FAILED: Should have allowed delete!")
    print(f"Error: {e}")

print("\n" + "="*60)