from services import UseCaseService

print("="*60)
print("TESTING UseCaseService FROM PYTHON MODULE")
print("="*60)

# Initialize service
service = UseCaseService()
print("\nService initialized successfully")

# Test 1: Get all use cases
print("\n1. Testing get_all_use_cases()...")
use_cases = service.get_all_use_cases()
print(f"   Found {len(use_cases)} use cases")
if use_cases:
    print(f"   First use case: {use_cases[0]['title']}")

# Test 2: Get use case by ID
print("\n2. Testing get_use_case_by_id()...")
uc = service.get_use_case_by_id(1)
if uc:
    print(f"   Retrieved use case #{uc['id']}: {uc['title']}")
    print(f"     Company: {uc['company_name']}")
    print(f"     Status: {uc['status']}")
else:
    print("   ✗ Use case not found")

# Test 3: Create use case
print("\n3. Testing create_use_case()...")
try:
    new_uc = service.create_use_case(
        title="TEST - Service Layer Test",
        description="Testing the service from Python module",
        expected_benefit="Verify everything works",
        company_id=1,
        industry_id=1,
        status="new"
    )
    print(f"   Created use case #{new_uc['id']}: {new_uc['title']}")
    test_id = new_uc['id']
except Exception as e:
    print(f"   ✗ Error: {e}")
    test_id = None

# Test 4: Update use case
if test_id:
    print("\n4. Testing update_use_case()...")
    try:
        updated = service.update_use_case(
            use_case_id=test_id,
            status="in_progress",
            description="Updated description"
        )
        print(f"   Updated use case #{updated['id']}")
        print(f"     New status: {updated['status']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

# Test 5: Filter use cases
print("\n5. Testing filter_use_cases()...")
try:
    filtered = service.filter_use_cases(status="new")
    print(f"   Found {len(filtered)} use cases with status 'new'")
    
    filtered_industry = service.filter_use_cases(industry_id=1)
    print(f"   Found {len(filtered_industry)} use cases in industry #1")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Delete the test use case
if test_id:
    print("\n6. Testing delete_use_case()...")
    try:
        deleted = service.delete_use_case(test_id)
        print(f"   Deleted use case: {deleted['title']}")
        
        # Verify it's gone
        check = service.get_use_case_by_id(test_id)
        if check is None:
            print(f"   Verified deletion (returns None)")
        else:
            print(f"   ✗ Use case still exists!")
    except Exception as e:
        print(f"   ✗ Error: {e}")

# Test 7: Validation
print("\n7. Testing validation...")
try:
    service.create_use_case(
        title="Should Fail",
        company_id=9999,  # Invalid
        industry_id=1
    )
    print("   ✗ Should have raised ValueError")
except ValueError as e:
    print(f"   Correctly raised error: {e}")

print("\n" + "="*60)
print("ALL TESTS COMPLETE!")
print("="*60)