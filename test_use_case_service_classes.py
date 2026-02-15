from services import UseCaseService

v1_testing = False # base
v2_testing = False # get perons, get industry, get company -> for second iteration if needed
v3_testing = True # create industry, create company, create person, find_or_create_company/person

if v1_testing:
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
        print("    Use case not found")

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
        print(f"    Error: {e}")
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
            print(f"    Error: {e}")

    # Test 5: Filter use cases
    print("\n5. Testing filter_use_cases()...")
    try:
        filtered = service.filter_use_cases(status="new")
        print(f"   Found {len(filtered)} use cases with status 'new'")
        
        filtered_industry = service.filter_use_cases(industry_id=1)
        print(f"   Found {len(filtered_industry)} use cases in industry #1")
    except Exception as e:
        print(f"    Error: {e}")

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
                print(f"    Use case still exists!")
        except Exception as e:
            print(f"    Error: {e}")

    # Test 7: Validation
    print("\n7. Testing validation...")
    try:
        service.create_use_case(
            title="Should Fail",
            company_id=9999,  # Invalid
            industry_id=1
        )
        print("    Should have raised ValueError")
    except ValueError as e:
        print(f"   Correctly raised error: {e}")

    print("\n" + "="*60)
    print("ALL TESTS COMPLETE!")
    print("="*60)

if v2_testing:

    service = UseCaseService()

    print("="*60)
    print("TESTING NEW SERVICE METHODS")
    print("="*60)

    # Test 1: Get all industries
    print("\n1. Testing get_all_industries()...")
    industries = service.get_all_industries()
    print(f"    Found {len(industries)} industries:")
    for ind in industries:
        print(f"     - ID {ind['id']}: {ind['name']}")

    # Test 2: Get all companies
    print("\n2. Testing get_all_companies()...")
    companies = service.get_all_companies()
    print(f"    Found {len(companies)} companies:")
    for comp in companies[:5]:  # Show first 5
        print(f"     - ID {comp['id']}: {comp['name']} ({comp['industry_name']})")
    if len(companies) > 5:
        print(f"     ... and {len(companies) - 5} more")

    # Test 3: Get all persons
    print("\n3. Testing get_all_persons()...")
    persons = service.get_all_persons()
    print(f"    Found {len(persons)} persons:")
    for person in persons: 
        print(f"     - ID {person['id']}: {person['name']} - {person['role']} at {person['company_name']}")

    # Test 4: Get persons by use case
    print("\n4. Testing get_persons_by_use_case()...")
    # Try with use case ID 1 (adjust if needed)
    try:
        contributors = service.get_persons_by_use_case(1)
        print(f"    Use case #1 has {len(contributors)} contributor(s):")
        for person in contributors:
            print(f"     - {person['name']} ({person['role']})")
    except ValueError as e:
        print(f"   ℹ {e}")

    # Test with non-existent use case
    print("\n5. Testing error handling...")
    try:
        service.get_persons_by_use_case(9999)
        print("    Should have raised ValueError")
    except ValueError as e:
        print(f"    Correctly raised error: {e}")

    print("\n" + "="*60)
    print("ALL TESTS COMPLETE!")
    print("="*60)


    print("="*60)
    print("TESTING PERSON RELATIONSHIPS")
    print("="*60)

    # Test 1: Get all persons
    print("\n1. All persons in database:")
    persons = service.get_all_persons()
    for person in persons[:5]:
        print(f"   - {person['name']} ({person['role']}) at {person['company_name']}")
    print(f"   ... total {len(persons)} persons")

    # Test 2: Get contributors to specific use cases
    print("\n2. Who contributed to use case #1?")
    contributors = service.get_persons_by_use_case(1)
    for person in contributors:
        print(f"   - {person['name']} ({person['role']}) from {person['company_name']}")

    print("\n3. Who contributed to use case #5?")
    contributors = service.get_persons_by_use_case(5)
    for person in contributors:
        print(f"   - {person['name']} ({person['role']}) from {person['company_name']}")

    # Test 3: Filter use cases by person
    print("\n4. What use cases did person #1 contribute to?")
    use_cases = service.filter_use_cases(person_id=1)
    print(f"   Person #1 contributed to {len(use_cases)} use case(s):")
    for uc in use_cases:
        print(f"   - {uc['title']}")

    print("\n" + "="*60)
    print(" ALL PERSON TESTS PASSED!")
    print("="*60)

if v3_testing:
    # Quick test script
    from services import UseCaseService

    service = UseCaseService()

    print("Testing new service methods...")

    # Test 1: Find or create industry
    print("\n1. Find or create industry:")
    industry = service.find_or_create_industry("Automotive")
    print(f"   ✓ {industry}")

    # Test 2: Find or create company
    print("\n2. Find or create company:")
    company = service.find_or_create_company("Volkswagen", "Automotive")
    print(f"   ✓ {company}")

    # Test 3: Find or create person
    print("\n3. Find or create person:")
    person = service.find_or_create_person("Test Person", "Test Role", company['id'])
    print(f"   ✓ {person}")

    # Test 4: Create use case and link person
    print("\n4. Create use case:")
    uc = service.create_use_case(
        title="Test Use Case",
        company_id=company['id'],
        industry_id=industry['id']
    )
    print(f"   ✓ Use case created: {uc['id']}")

    # Test 5: Add person to use case
    print("\n5. Link person to use case:")
    result = service.add_persons_to_use_case(uc['id'], [person['id']])
    print(f"   ✓ {result}")

    print("\n✓ All tests passed!")