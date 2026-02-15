from agent import run_agent

print("="*80)
print("COMPREHENSIVE AGENT TESTING - NEW TOOLS")
print("="*80)

# Test 1: Create new industry
print("\n" + "─"*80)
print("TEST 1: Create New Industry")
print("─"*80)
run_agent("Create a new industry called 'Automotive'")

# Test 2: Create new company (should create industry if needed)
print("\n" + "─"*80)
print("TEST 2: Create New Company")
print("─"*80)
run_agent("Create a new company called 'Volkswagen' in the Automotive industry")

# Test 3: Create new person
print("\n" + "─"*80)
print("TEST 3: Create New Person")
print("─"*80)
run_agent("Create a new person named 'Herbert Diess' with role 'CEO' at Volkswagen")

# Test 4: Create use case and link person (complex multi-step)
print("\n" + "─"*80)
print("TEST 4: Create Use Case with Person Link")
print("─"*80)
run_agent(
    "Create a use case called 'Autonomous Driving AI' for Volkswagen. "
    "Description: Development of AI systems for self-driving cars. "
    "Expected benefit: Safer roads and competitive advantage. "
    "Link Herbert Diess as a contributor."
)

# Test 5: Test with company that already exists
print("\n" + "─"*80)
print("TEST 5: Handle Existing Company")
print("─"*80)
run_agent("Create a use case called 'Smart Factory' for Siemens Energy")

# Test 6: Create multiple persons and link to use case
print("\n" + "─"*80)
print("TEST 6: Multiple Persons")
print("─"*80)
run_agent(
    "Create two new persons: 'Max Müller' as 'CTO' and 'Sarah Weber' as 'AI Lead', "
    "both at Bosch. Then create a use case 'Predictive Quality Control' for Bosch "
    "and link both persons to it."
)

# Test 7: Full workflow - new company from scratch
print("\n" + "─"*80)
print("TEST 7: Full Workflow - New Company from Scratch")
print("─"*80)
run_agent(
    "I want to create a use case for a company called 'BMW' in the Automotive sector. "
    "The use case is 'Battery Management AI' for optimizing electric vehicle batteries. "
    "Expected benefit is 20% longer battery life. "
    "The person who proposed this is 'Dr. Klaus Schmidt', who is the Head of Innovation at BMW."
)

# Test 8: Verify everything was created
print("\n" + "─"*80)
print("TEST 8: Verify Creations")
print("─"*80)
run_agent("Show me all companies in the Automotive industry")

print("\n" + "─"*80)
print("TEST 9: Show All Persons")
print("─"*80)
run_agent("Show me all persons at Volkswagen")

print("\n" + "="*80)
print("ALL TESTS COMPLETE!")
print("="*80)