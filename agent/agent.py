import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from agent.tools import tools
from agent.tool_executor import execute_tool


# Load environment variables
load_dotenv()

# Initialize OpenAI client (pointed at OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def run_agent(user_message: str, conversation_history: list = None, verbose: bool = False, max_rounds: int = 10):
    """
    Run the agent with multi-round tool calling support.
    
    This allows the agent to:
    1. First round: Call helper tools (get_all_industries, get_all_companies, etc.)
    2. Second round: Use the results to call action tools (filter_use_cases, create_use_case, etc.)
    
    Args:
        user_message (str): The user's question/command
        verbose (bool): If True, prints detailed execution info (default: True)
        max_rounds (int): Maximum number of tool-calling rounds (default: 2)
    
    Returns:
        str: The agent's final response
    """
    # Start with history or empty
    if conversation_history:
        messages = conversation_history.copy()
    else:
        messages = []

    # Add system message with tool usage instructions (only if starting new conversation)
    if not conversation_history:
        system_message = {
            "role": "system",
            "content": f"""You are a helpful assistant managing a use case database for AI/ML projects.

You have access to tools that interact with the database. Your job is to help users query, create, update, and delete use cases, companies, industries, and persons.

CRITICAL RULES - TOOL USAGE:
1. ALWAYS use tools to perform database operations
2. NEVER assume or fabricate success/failure of operations
3. When asked to create/update/delete/query, you MUST call the appropriate tool
4. Wait for the tool's actual response before telling the user what happened
5. If a tool returns an error (including permission errors), report it honestly
6. NEVER say "I've successfully [action]" unless a tool returned success
7. If you don't have permission, the tool will tell you - report that error to the user

DATABASE OPERATIONS - ALWAYS USE TOOLS:
- To view/query data → use get/filter tools
- To create data → use create tools
- To update data → use update tools  
- To delete data → use delete tools
- To link persons to use cases → use add_persons_to_use_case

PERMISSION SYSTEM:
- Some operations require specific permissions (maintainer or admin)
- The tools will check permissions automatically
- If denied, report the permission error clearly to the user
- Don't apologize excessively - just explain what permission is needed

RESPONSE STYLE:
- Be concise and helpful
- Present data clearly (use lists, grouping by category when appropriate)
- When operations succeed, confirm briefly
- When operations fail, explain why clearly
- Ask clarifying questions if the request is ambiguous

Available tools and their purposes:
{chr(10).join(f"- {tool['function']['name']}: {tool['function']['description'][:100]}..." for tool in tools)}

Remember: ALWAYS call the appropriate tool - never assume results!"""
        }
        messages.insert(0, system_message)

    # Add new user message
    messages.append({"role": "user", "content": user_message})
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"USER: {user_message}")
        print(f"{'='*60}")
    
    # Multi-round loop
    for round_num in range(1, max_rounds + 1):
        if verbose and round_num > 1:
            print(f"\n{'─'*60}")
            print(f"ROUND {round_num}")
            print(f"{'─'*60}")
        
        # Call LLM
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=messages,
            tools=tools,
            max_tokens=2000
        )
        
        assistant_message = response.choices[0].message
        
        # Check if agent wants to call tools
        if not assistant_message.tool_calls:
            # No more tools to call - return final answer
            if verbose:
                if round_num > 1:
                    print(f"\nNo more tools needed, generating final response...")
                else:
                    print(f"\nAgent responding directly (no tools needed)")
                print(f"\nAGENT RESPONSE:")
                print(f"{assistant_message.content}")
                print(f"{'='*60}\n")
            
            return assistant_message.content
        
        # Agent wants to call tools
        if verbose:
            print(f"\nAGENT: Calling {len(assistant_message.tool_calls)} tool(s)...")
        
        # Add assistant's message to history
        messages.append(assistant_message)
        
        # Execute each tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            arguments_str = tool_call.function.arguments
            
            # Parse arguments
            if arguments_str and arguments_str.strip():
                arguments = json.loads(arguments_str)
            else:
                arguments = {}
            
            if verbose:
                print(f"\n   Calling: {function_name}")
                if arguments:
                    print(f"      Arguments: {arguments}")
                else:
                    print(f"      Arguments: (none)")
            
            # Execute the tool
            result = execute_tool(function_name, arguments)
            
            # Display result
            if verbose:
                if isinstance(result, list):
                    print(f"   Returned {len(result)} item(s)")
                    if len(result) > 0 and len(result) <= 3:
                        # Show items if there are just a few
                        for item in result:
                            if isinstance(item, dict) and 'name' in item:
                                print(f"      - {item.get('name')} (ID: {item.get('id')})")
                elif isinstance(result, dict):
                    if "error" in result:
                        print(f"   Error: {result['error']}")
                    else:
                        print(f"   Success")
                else:
                    print(f"   Result: {result}")
            
            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
    
    # If we exit the loop, we hit max_rounds - make final call without tools
    if verbose:
        print(f"\n{'─'*60}")
        print(f"Generating final response (max rounds reached)...")
        print(f"{'─'*60}")
    
    final_response = client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet",
        messages=messages,
        max_tokens=2000
    )
    
    final_answer = final_response.choices[0].message.content
    
    if verbose:
        print(f"\nAGENT RESPONSE:")
        print(f"{final_answer}")
        print(f"{'='*60}\n")
    
    return final_answer