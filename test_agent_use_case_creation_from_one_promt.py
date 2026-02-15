from agent import run_agent

print("="*80)
print("TEST 7: Full Workflow - New Company from Scratch")
print("="*80)

run_agent(
    "I want to create a use case for a company called 'Mercedes-Benz' in the Automotive sector. "
    "The use case is 'Predictive Quality Control AI' for detecting manufacturing defects. "
    "Expected benefit is 30 percent reduction in quality issues. "
    "The person who proposed this is 'Dr. Andrea Fischer', who is the VP of Quality at Mercedes-Benz."
)

print("\n" + "="*80)
print("Verification: Show the created use case")
print("="*80)

run_agent("Show me all use cases for Mercedes-Benz")