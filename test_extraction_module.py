"""
Quick test of the extraction module
"""

from extraction import process_transcript

# Load a transcript
with open("test_data/transcripts/energy_workshop_transcript.txt", 'r', encoding='utf-8') as f:
    transcript = f.read()

# Process it
print("Testing extraction module...")
summary = process_transcript(transcript, verbose=True)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Success: {summary['success']}")
print(f"Prompts extracted: {summary['prompts_extracted']}")
print(f"Use cases created: {summary['use_cases_created']}")