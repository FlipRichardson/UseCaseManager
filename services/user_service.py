"""
User Service - handles authentication and user management.
"""

from typing import Optional, Dict, Any, List
import bcrypt as bcrypt_lib
from models.base import SessionLocal
from models.user import User


class UserService:
    """
    Service for user authentication and management.
    """
    
    # Valid roles
    VALID_ROLES = ['reader', 'maintainer', 'admin']
    
    def __init__(self):
        pass
    
    def _get_session(self):
        """Get database session."""
        return SessionLocal()
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return bcrypt_lib.hashpw(
            password.encode('utf-8'), 
            bcrypt_lib.gensalt()
        ).decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            password_hash: Hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        return bcrypt_lib.checkpw(
            password.encode('utf-8'), 
            password_hash.encode('utf-8')
        )
    
    def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            User dict if authentication successful, None otherwise
        """
        db = self._get_session()
        try:
            # Find user by email
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                return None
            
            # Verify password
            if not self._verify_password(password, user.password_hash):
                return None
            
            # Return user info (without password hash!)
            return {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "name": user.name
            }
        finally:
            db.close()
    
    def create_user(self, email: str, password: str, role: str, name: str = None) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            email: Email address (must be unique)
            password: Plain text password (will be hashed)
            role: User role ('reader', 'maintainer', or 'admin')
            name: Optional display name
            
        Returns:
            Created user dict
            
        Raises:
            ValueError: If email exists, role is invalid, or validation fails
        """
        db = self._get_session()
        try:
            # Validate role
            if role not in self.VALID_ROLES:
                raise ValueError(f"Invalid role. Must be one of: {', '.join(self.VALID_ROLES)}")
            
            # Check if email already exists
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                raise ValueError(f"Email '{email}' already exists")
            
            # Validate email (basic check)
            if not email or '@' not in email:
                raise ValueError("Valid email address required")
            
            # Validate password
            if not password or len(password) < 4:
                raise ValueError("Password must be at least 4 characters")
            
            # Hash password
            password_hash = self._hash_password(password)
            
            # Create user
            user = User(
                email=email,
                password_hash=password_hash,
                role=role,
                name=name
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "name": user.name
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users (admin only in UI).
        
        Returns:
            List of user dicts
        """
        db = self._get_session()
        try:
            users = db.query(User).all()
            return [{
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "name": user.name
            } for user in users]
        finally:
            db.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User dict or None
        """
        db = self._get_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            return {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "name": user.name
            }
        finally:
            db.close()