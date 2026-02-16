"""
Permission checking utilities for role-based access control.
"""

from typing import Dict, Any, Optional

class PermissionError(Exception):
    """  
    Error should be raised when a user doesnt have permission to do something.
    """
    pass

def check_permission(user: Optional[Dict[str, Any]], action: str) -> bool:
    """
    Check if user has permission for an action.
    
    Args:
        user: User dict with 'role' key (or None if not logged in)
        action: Action to check
            - 'read': View use cases, companies, etc.
            - 'write'/'create'/'edit'/'update': Create/edit use cases
            - 'delete'/'archive': Delete or archive use cases (ADMIN ONLY)
            - 'manage_users': Create/edit/delete users (ADMIN ONLY)
            
    Returns:
        True if user has permission, False otherwise
        
    Role Permissions:
        Reader: read only
        Maintainer: read, create, edit, update status
        Admin: full access (read, write, delete, archive, manage users)
    """
    if not user:
        return False  # Not logged in = no permissions
    
    # case insensitive
    role = user.get('role', '').lower()
    action = action.lower()
    
    # Everyone can read (if logged in)
    if action == 'read':
        return True
    
    # Write/Create/Edit/Update operations (Maintainer + Admin)
    if action in ['write', 'create', 'edit', 'update']:
        return role in ['maintainer', 'admin']
    
    # Delete and Archive operations, admin only
    if action in ['delete', 'archive']:
        return role == 'admin' 
    
    # User management (ADMIN ONLY)
    if action in ['manage_users', 'create_user', 'delete_user']:
        return role == 'admin'
    
    # Unknown action = deny
    return False


def require_permission(user: Optional[Dict[str, Any]], action: str) -> None:
    """
    Require user to have permission for an action.
    Raises PermissionError if user doesn't have permission.
    
    Args:
        user: User dict with 'role' key
        action: Action to check (same as check_permission)
        
    Raises:
        PermissionError: If user doesn't have required permission
        
    Example:
        >>> require_permission(current_user, 'delete')
        >>> # Proceeds if admin, raises PermissionError if not
    """
    if not check_permission(user, action):
        if not user:
            raise PermissionError("You must be logged in to perform this action")
        
        role = user.get('role', 'unknown')
        raise PermissionError(
            f"Your role '{role}' does not have permission to {action}. "
            f"Required: {_get_required_role(action)}"
        )


def _get_required_role(action: str) -> str:
    """Get human-readable required role for an action."""
    action = action.lower()
    
    if action == 'read':
        return "any logged-in user"
    elif action in ['write', 'create', 'edit', 'update']:
        return "maintainer or admin"
    elif action in ['delete', 'archive', 'manage_users', 'create_user', 'delete_user']:
        return "admin only"
    else:
        return "unknown"



