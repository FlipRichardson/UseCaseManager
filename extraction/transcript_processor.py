"""
Transcript Processor
Extracts use cases from workshop transcripts using two-step workflow:
1. LLM extracts natural language prompts
2. Agent executes prompts to create use cases in database
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from agent import run_agent

# Load environment
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

extraction_prompt = """
You are an expert at extracting use cases from workshop transcripts.

Your task is to read the transcript and create a natural language prompt for EACH use case 
that can be executed by an AI agent to create the use case in a database.

For each use case mentioned in the transcript, create a prompt following this template:
"Create a use case called '[TITLE]' for company '[COMPANY]' in the '[INDUSTRY]' sector. Description: [DETAILED DESCRIPTION]. Expected benefit: [SPECIFIC BENEFITS]. Contributors: [NAME (ROLE), NAME (ROLE)]"

INSTRUCTIONS:
1. Extract ALL use cases discussed in the transcript (there may be multiple)
2. For each use case, identify:
   - A clear, concise title
   - The company name (exactly as mentioned)
   - The industry/sector
   - A detailed description of what the use case does
   - The expected benefits (include metrics/percentages when mentioned)
   - All people who contributed ideas (with their roles)

3. Return ONLY a JSON array of prompt strings
4. Each prompt should be a complete, standalone instruction
5. Use exact quotes for percentages and metrics when available

EXAMPLE OUTPUT FORMAT:
[
  "Create a use case called 'Smart Grid Optimization' for company 'E.ON' in the 'Energy' sector. Description: Machine learning algorithms to optimize energy distribution in real-time based on consumption patterns and renewable energy availability. Expected benefit: Reduce energy waste by 15-20%, improve grid stability, better integration of renewable sources. Contributors: Lisa Müller (Innovation Manager), Thomas Klein (Data Science Lead)",
  "Create a use case called 'Predictive Maintenance for Wind Turbines' for company 'E.ON' in the 'Energy' sector. Description: IoT sensors combined with AI to predict maintenance needs before failures occur, reducing downtime. Expected benefit: 30% reduction in unplanned downtime, 20% longer equipment lifetime, lower maintenance costs. Contributors: Thomas Klein (Data Science Lead), Lisa Müller (Innovation Manager)"
]

CRITICAL: Return ONLY the JSON array, no other text, no markdown formatting, no preamble.
"""


def extract_prompts_from_transcript(transcript_text: str, verbose: bool = True):
    """
    Extract use case prompts from a workshop transcript.
    
    Args:
        transcript_text: The full transcript text
        verbose: Whether to print progress
        
    Returns:
        list: List of prompt strings for the agent
    """
    if verbose:
        print("\n" + "="*60)
        print("EXTRACTING USE CASE PROMPTS FROM TRANSCRIPT")
        print("="*60)
    
    # Call LLM with extraction prompt
    response = client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet",
        messages=[
            {"role": "system", "content": extraction_prompt},
            {"role": "user", "content": f"Extract use case prompts from this transcript:\n\n{transcript_text}"}
        ],
        max_tokens=3000,
        temperature=0.3  # Lower temp for consistent extraction
    )
    
    result = response.choices[0].message.content
    
    if verbose:
        print("\nLLM Response:")
        print(result[:300] + "..." if len(result) > 300 else result)
    
    # Parse JSON
    try:
        # Clean markdown formatting if present
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        
        prompts = json.loads(result)
        
        if verbose:
            print(f"\nSuccessfully extracted {len(prompts)} use case prompt(s)")
            print("\nExtracted prompts:")
            for i, prompt in enumerate(prompts, 1):
                print(f"\n{i}. {prompt[:100]}...")
        
        return prompts
        
    except json.JSONDecodeError as e:
        print(f"\nFailed to parse JSON: {e}")
        print(f"Raw response:\n{result}")
        return []
    

def process_transcript(transcript_text: str, verbose: bool = True):
    """
    Complete workflow: Extract prompts from transcript and create all use cases.
    
    Args:
        transcript_text: The workshop transcript
        verbose: Whether to print detailed progress
        
    Returns:
        dict: Summary of results
    """
    if verbose:
        print("\n" + "="*80)
        print("TRANSCRIPT PROCESSING WORKFLOW")
        print("="*80)
    
    # Step 1: Extract prompts
    prompts = extract_prompts_from_transcript(transcript_text, verbose=verbose)
    
    if not prompts:
        print("\nNo prompts extracted. Stopping.")
        return {"success": False, "prompts_extracted": 0, "use_cases_created": 0}
    
    # Step 2: Process each prompt with the agent
    if verbose:
        print("\n" + "="*80)
        print(f"CREATING {len(prompts)} USE CASE(S) VIA AGENT")
        print("="*80)
    
    results = []
    for i, prompt in enumerate(prompts, 1):
        if verbose:
            print(f"\n{'─'*80}")
            print(f"USE CASE {i}/{len(prompts)}")
            print(f"{'─'*80}")
            print(f"Prompt: {prompt[:150]}...")
            print()
        
        try:
            # Feed prompt to agent
            response = run_agent(prompt, verbose=verbose)
            results.append({"success": True, "prompt": prompt, "response": response})
            
            if verbose:
                print(f"\nUse case {i} created successfully")
        
        except Exception as e:
            if verbose:
                print(f"\nError creating use case {i}: {e}")
            results.append({"success": False, "prompt": prompt, "error": str(e)})
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    
    if verbose:
        print("\n" + "="*80)
        print("TRANSCRIPT PROCESSING COMPLETE")
        print("="*80)
        print(f"Prompts extracted: {len(prompts)}")
        print(f"Use cases created: {successful}/{len(prompts)}")
        print("="*80)
    
    return {
        "success": True,
        "prompts_extracted": len(prompts),
        "use_cases_created": successful,
        "results": results
    }

