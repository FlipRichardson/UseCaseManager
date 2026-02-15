"""
Tool executor. Maps tool names to actual service functions and executes them.
"""

from services import UseCaseService

# init service
service = UseCaseService()

# mapping
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
    "get_persons_by_use_case": service.get_persons_by_use_case  
}

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

        # call the function
        result = actual_function(**arguments)

        return result
    
    except Exception as e:
        return {"error" : str(e)}