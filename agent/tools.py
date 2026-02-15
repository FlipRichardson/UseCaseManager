"""
Tool definitions for the agent.
Each tool describes a function the agent can call to interact with the database.
Also for each tool a comprehensive description is given for how and in in which order the agent could use the tools if 
multiple calls are needed.
"""

# Tool 1: Get all use cases
tool_get_all_use_cases = {
    "type": "function",
    "function": {
        "name": "get_all_use_cases",
        "description": (
            "Retrieve all use cases from the database. "
            "Use this when the user wants to see all use cases, list use cases, "
            "or get an overview of everything in the system. "
            "Returns comprehensive information including title, description, status, "
            "company, and industry for each use case."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

# Tool 2: Get use case by ID
tool_get_use_case_by_id = {
    "type": "function",
    "function": {
        "name": "get_use_case_by_id",
        "description": (
            "Get detailed information about a specific use case by its ID number. "
            "Use this when the user mentions a specific use case number or ID "
            "(e.g., 'use case 5', 'UC #3', 'number 7'). "
            "Returns all details including title, description, status, company, industry, and benefits."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "use_case_id": {
                    "type": "integer",
                    "description": "The numeric ID of the use case to retrieve (e.g., 1, 2, 3, etc.)"
                }
            },
            "required": ["use_case_id"]
        }
    }
}

# Tool 3: Create use case
tool_create_use_case = {
    "type": "function",
    "function": {
        "name": "create_use_case",
        "description": (
            "Create a new use case in the database. "
            "Use this when the user wants to add a new use case, extract use cases from transcripts, "
            "or create entries based on workshop discussions. "
            "IMPORTANT: You must provide company_id and industry_id as integers. "
            "If the user mentions company/industry names, you may need to ask for clarification "
            "or reference existing data to find the correct IDs."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title/name of the use case (required, must not be empty). Be concise but descriptive."
                },
                "description": {
                    "type": "string",
                    "description": (
                        "Detailed description of what the use case involves, the problem it solves, "
                        "and how it works (optional but recommended)"
                    )
                },
                "expected_benefit": {
                    "type": "string",
                    "description": (
                        "Expected benefits, value, or outcomes of implementing this use case "
                        "(optional). Include quantitative metrics if available."
                    )
                },
                "company_id": {
                    "type": "integer",
                    "description": (
                        "ID of the company this use case belongs to (required). "
                        "This must be a valid company ID number from the database."
                    )
                },
                "industry_id": {
                    "type": "integer",
                    "description": (
                        "ID of the industry this use case belongs to (required). "
                        "This must be a valid industry ID number from the database."
                    )
                },
                "status": {
                    "type": "string",
                    "description": (
                        "Initial status for the use case (optional, defaults to 'new'). "
                        "Must be EXACTLY one of the valid status values listed in enum. "
                        "Map user's language/intent to these exact values: "
                        "'neu'/'new'→'new', 'in Prüfung'/'in review'→'in_review', "
                        "'genehmigt'/'approved'→'approved', 'in Arbeit'/'in progress'→'in_progress', "
                        "'fertig'/'done'/'completed'→'completed', 'archiviert'/'archived'→'archived'"
                    ),
                    "enum": ["new", "in_review", "approved", "in_progress", "completed", "archived"]
                }
            },
            "required": ["title", "company_id", "industry_id"]
        }
    }
}

# Tool 4: Update use case
tool_update_use_case = {
    "type": "function",
    "function": {
        "name": "update_use_case",
        "description": (
            "Update an existing use case. Only the fields you provide will be changed; "
            "all other fields remain unchanged. "
            "Use this when the user wants to modify, change, or edit a use case. "
            "You can update any combination of title, description, benefit, status, company, or industry."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "use_case_id": {
                    "type": "integer",
                    "description": "ID of the use case to update (required)"
                },
                "title": {
                    "type": "string",
                    "description": "New title (optional). If provided, must not be empty."
                },
                "description": {
                    "type": "string",
                    "description": "New description (optional)"
                },
                "expected_benefit": {
                    "type": "string",
                    "description": "New expected benefit (optional)"
                },
                "status": {
                    "type": "string",
                    "description": (
                        "New status (optional). Must be EXACTLY one of the valid values in enum. "
                        "Translate user's intent: 'neu'→'new', 'In Bewertung'/'zur Prüfung'→'in_review', "
                        "'genehmigt'/'freigegeben'→'approved', 'in Bearbeitung'/'in Arbeit'→'in_progress', "
                        "'abgeschlossen'/'fertig'→'completed', 'archiviert'→'archived'"
                    ),
                    "enum": ["new", "in_review", "approved", "in_progress", "completed", "archived"]
                },
                "company_id": {
                    "type": "integer",
                    "description": "New company ID (optional). Must be a valid company ID from the database."
                },
                "industry_id": {
                    "type": "integer",
                    "description": "New industry ID (optional). Must be a valid industry ID from the database."
                }
            },
            "required": ["use_case_id"]
        }
    }
}

# Tool 5: Update status (specialized)
tool_update_use_case_status = {
    "type": "function",
    "function": {
        "name": "update_use_case_status",
        "description": (
            "Update ONLY the status of a use case. This is a convenience function for status-only changes. "
            "Use this when the user wants to change, set, or update just the status "
            "(e.g., 'approve use case 5', 'mark case 3 as completed', 'set UC 7 to in progress'). "
            "CRITICAL: Always map the user's language/intent to one of the exact valid status values."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "use_case_id": {
                    "type": "integer",
                    "description": "ID of the use case whose status should be changed"
                },
                "status": {
                    "type": "string",
                    "description": (
                        "New status value. Must be EXACTLY one of the values in enum. "
                        "Language mapping examples: "
                        "German: 'neu'→'new', 'In Bewertung'/'In Prüfung'→'in_review', 'genehmigt'→'approved', "
                        "'in Bearbeitung'/'läuft'→'in_progress', 'abgeschlossen'/'fertig'/'erledigt'→'completed', "
                        "'archiviert'→'archived'. "
                        "English variants: 'reviewing'→'in_review', 'working on'/'ongoing'→'in_progress', "
                        "'done'/'finished'→'completed'"
                    ),
                    "enum": ["new", "in_review", "approved", "in_progress", "completed", "archived"]
                }
            },
            "required": ["use_case_id", "status"]
        }
    }
}

# Tool 6: Delete use case
tool_delete_use_case = {
    "type": "function",
    "function": {
        "name": "delete_use_case",
        "description": (
            "Permanently delete a use case from the database. "
            "Use this when the user explicitly wants to remove, delete, or eliminate a use case. "
            "WARNING: This action cannot be undone. The function returns information about "
            "the deleted use case for confirmation. "
            "Consider suggesting archiving instead of deletion when appropriate."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "use_case_id": {
                    "type": "integer",
                    "description": "ID of the use case to delete permanently"
                }
            },
            "required": ["use_case_id"]
        }
    }
}

# Tool 7: Filter use cases
tool_filter_use_cases = {
    "type": "function",
    "function": {
        "name": "filter_use_cases",
        "description": (
            "Filter and search use cases by various criteria. All filters are optional - "
            "you can use one or combine multiple filters. "
            "Use this when the user wants use cases matching specific conditions "
            "(e.g., 'show energy sector use cases', 'what's in progress', 'cases from company X'). "
            "Returns a list of use cases matching ALL provided filters (AND logic)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "industry_id": {
                    "type": "integer",
                    "description": (
                        "Filter by industry ID (optional). "
                        "Only return use cases belonging to this specific industry. "
                        "Must be a valid industry ID number from the database."
                    )
                },
                "company_id": {
                    "type": "integer",
                    "description": (
                        "Filter by company ID (optional). "
                        "Only return use cases belonging to this specific company. "
                        "Must be a valid company ID number from the database."
                    )
                },
                "status": {
                    "type": "string",
                    "description": (
                        "Filter by status (optional). Only return use cases with this exact status. "
                        "Must be EXACTLY one of the valid values in enum. "
                        "Map user's language: 'neu'/'new'→'new', 'in Bewertung'/'zur Prüfung'→'in_review', "
                        "'genehmigt'/'approved'→'approved', 'laufend'/'in Arbeit'/'in progress'→'in_progress', "
                        "'fertig'/'abgeschlossen'/'done'→'completed', 'archiviert'/'archived'→'archived'"
                    ),
                    "enum": ["new", "in_review", "approved", "in_progress", "completed", "archived"]
                },
                "person_id": {
                    "type": "integer",
                    "description": (
                        "Filter by person who contributed (optional). "
                        "Only return use cases that this specific person contributed to. "
                        "Must be a valid person ID number from the database."
                    )
                }
            },
            "required": []
        }
    }
}


# Tool 8: Get all industries
tool_get_all_industries = {
    "type": "function",
    "function": {
        "name": "get_all_industries",
        "description": (
            "Get a complete list of all industries with their IDs and names. "
            "CRITICAL: When a user mentions an industry by NAME (e.g., 'IT', 'Energy', 'Healthcare', "
            "'Energie', 'Gesundheitswesen'), you MUST call this function FIRST to find the industry_id, "
            "THEN use that ID in subsequent calls to filter_use_cases, create_use_case, or update_use_case. "
            "This is a TWO-STEP process: (1) Call get_all_industries to map name→ID, (2) Use the ID. "
            "Example: User says 'Show me Energy sector use cases' → Call get_all_industries() → "
            "Find that Energy has id=1 → Then call filter_use_cases(industry_id=1)"
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

# Tool 9: Get all companies
tool_get_all_companies = {
    "type": "function",
    "function": {
        "name": "get_all_companies",
        "description": (
            "Get a complete list of all companies with their IDs, names, and industry information. "
            "CRITICAL: When a user mentions a company by NAME, "
            "you MUST call this function FIRST to find the company_id and industry_id, "
            "THEN use those IDs in subsequent calls to create_use_case, update_use_case, or filter_use_cases. "
            "This is a TWO-STEP process: (1) Call get_all_companies to map name→IDs, (2) Use the IDs. "
            "Example: User says 'Create a use case for Siemens' → Call get_all_companies() → "
            "Find that Siemens Energy has id=1, industry_id=1 → Then call create_use_case(company_id=1, industry_id=1)"
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

# Tool 10: Get all persons
tool_get_all_persons = {
    "type": "function",
    "function": {
        "name": "get_all_persons",
        "description": (
            "Get a complete list of all persons with their IDs, names, roles, and company information. "
            "Use this when the user asks about people, contributors, or who works where. "
            "When a user mentions a person by name and you need their person_id for filtering, "
            "call this function first to find the ID, then use it in filter_use_cases(person_id=...). "
            "Example: User says 'Show me use cases that Anna worked on' → Call get_all_persons() → "
            "Find Anna's ID → Call filter_use_cases(person_id=...)"
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

# Tool 11: Get persons by use case
tool_get_persons_by_use_case = {
    "type": "function",
    "function": {
        "name": "get_persons_by_use_case",
        "description": (
            "Get all persons who contributed to a specific use case. "
            "Use this when the user asks 'Who worked on use case X?', 'Who contributed to...?', "
            "'Show me the people involved in...', or similar questions about contributors. "
            "Returns a list of persons with their names, roles, and company information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "use_case_id": {
                    "type": "integer",
                    "description": "The ID of the use case to get contributors for"
                }
            },
            "required": ["use_case_id"]
        }
    }
}

# Combine all tools into a list
tools = [
    tool_get_all_use_cases,
    tool_get_use_case_by_id,
    tool_create_use_case,
    tool_update_use_case,
    tool_update_use_case_status,
    tool_delete_use_case,
    tool_filter_use_cases,
    tool_get_all_industries,      
    tool_get_all_companies,        
    tool_get_all_persons,          
    tool_get_persons_by_use_case 
]