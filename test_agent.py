"""
Quick test of the agent module.
"""

from agent import run_agent

print("="*60)
print("TESTING AGENT MODULE")
print("="*60)

# Quick smoke test
print("\nTest 1: Simple query")
run_agent("Show me all use cases", verbose=True)

print("\nTest 2: Multi-round query")
run_agent("Show me all Energy use cases", verbose=True)

print("\n" + "="*60)
print("Agent module working!")
print("="*60)