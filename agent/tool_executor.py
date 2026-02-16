"""
Tool executor. Maps tool names to actual service functions and executes them.
"""

from services import UseCaseService

# init service
service = UseCaseService()

# Global variable to track current user (set by UI)
current_user = None

# mapping
# Map function names to actual Python functions
tool_functions = {
    "get_all_use_cases": service.get_all_use_cases,
    "get_use_case_by_id": service.get_use_case_by_id,
    "create_use_case": service.create_use_case,
    "update_use_case": service.update_use_case,
    "update_use_case_status": service.update_use_case_status,
    "delete_use_case": service.delete_use_case,
    "filter_use_cases": service.filter_use_cases,
    "get_all_industries": service.get_all_industries,
    "get_all_companies": service.get_all_companies,
    "get_all_persons": service.get_all_persons,
    "get_persons_by_use_case": service.get_persons_by_use_case,
    "create_industry": service.create_industry,                
    "create_company": service.create_company,                  
    "create_person": service.create_person,                    
    "add_persons_to_use_case": service.add_persons_to_use_case 
}


def set_current_user(user):
    """
    Set the current user for permission checks.
    Should be called by the UI after login.
    
    Args:
        user (dict): User dict with id, email, role, name
    """
    global current_user
    current_user = user


def get_current_user():
    """Get the current logged-in user."""
    return current_user


def execute_tool(function_name : str, arguments : dict):
    """
    Execute a tool function by name with given arguments.
    
    Args:
        function_name (str): Name of the function to call
        arguments (dict): Dictionary of arguments to pass to the function
        
    Returns:
        Result from the function, or error dict if function unknown or execution fails
    """

    # check if function exists
    if function_name not in tool_functions.keys():
        return {"error" : f"Unknown function: {function_name}"}

    try: 
        actual_function = tool_functions[function_name]

        # Add current_user to arguments for all service methods
        # (All service methods now accept current_user parameter)
        arguments['current_user'] = current_user

        # call the function
        result = actual_function(**arguments)

        return result
    
    except Exception as e:
        return {"error" : str(e)}