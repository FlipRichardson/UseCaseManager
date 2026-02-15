from typing import Optional, List, Dict, Any
from models.base import SessionLocal
from models import UseCase, Company, Industry, Person


class UseCaseService:
    """
    Layer that is intented to handle all interaction with the database for managin usecases. 
    CRUD operation.
    """
    def __init__(self):
        self.valid_status_values = [
            "new",
            "in_review",
            "approved",
            "in_progress",
            "completed",
            "archived"
        ]

    def _get_session(self):
        """Helper to get database session"""
        return SessionLocal()  # may get more complicated dont know, if so can be handeled centrally here
    
    def _validate_status(self, status : str) -> None:
        """
        Validate that a status value is allowed. Vlaid vlaues are: new, in_review, approved, 
        in_progress, completed, archived
        
        Args:
            status (str) : status to be validated

        Raises:
            ValueError: if status is not in valid values
        """
        if status not in self.valid_status_values:
            valid_status_valus = ", ".join(self.valid_status_values)
            raise ValueError(f"Given status '{status}' is not valid. Please choose one of the following status values '{valid_status_valus}'")
    
    def _use_case_to_dict(self, use_case : UseCase) -> Dict[str, Any]: 
        """
        Helper function translating a use case to a dict. 
        Args: 
            use_case : Use case object

        Returns: 
            Dict containing use case information EXCEPT persons involved: 
            - id (int)
            - title (str)
            - description (str)
            - expected_benefit (str)
            - company_id (int)
            - industry_id (int)
            - industry_name (str)
            - company_name (str)
        """
        return {
            "id": use_case.id,
            "title": use_case.title,
            "description": use_case.description,
            "expected_benefit": use_case.expected_benefit,
            "status": use_case.status,
            "company_id": use_case.company_id,
            "company_name": use_case.company.name,
            "industry_id": use_case.industry_id,
            "industry_name": use_case.industry.name
        }


    
    def get_all_use_cases(self) -> List[Dict[str, Any]]: 
        """  
        Retrieve all use cases from the database.
    
        Returns:
            List[Dict[str, Any]]: List of dictionaries, each containing:
                - id: Use case ID
                - title: Use case title
                - description: Detailed description
                - expected_benefit: Expected benefits
                - status: Current status
                - company_id: Associated company ID
                - company_name: Associated company name
                - industry_id: Associated industry ID
                - industry_name: Associated industry name
        """
        # get db
        db = self._get_session()

        # try to get all use cases and format them reasonably
        try: 
            use_cases = db.query(UseCase).all()
            return [self._use_case_to_dict(uc) for uc in use_cases]
        finally:
            db.close()

    def get_use_case_by_id(self, use_case_id : int) -> Optional[Dict[str, Any]]:
        """
        Retreive an use case dict by providing its ID. 

        Args:
            use_case_id (int) : use case id to get information for

        Returns:
            Dict[str, Any] : Dictionary about use case info
        """
        db = self._get_session()

        try: 
            matching_use_case = db.query(UseCase).filter(UseCase.id == use_case_id).first()

            if not matching_use_case:
                return None
            else:
                return self._use_case_to_dict(matching_use_case)
        finally:
            db.close()

    def create_use_case(self, title : str, company_id : int, industry_id : int, description : str = None, expected_benefit : str = None, status : str  = 'new') -> Dict[str, Any]:
        """  
        Create new use case in the database.

        Args: 
            title (str) : Use case title
            company_id (int) : Company identifier
            industry_id (int) : industry identifier
            description (Optional[str]) : Use case description, default None
            expected_benefit (OPtional[str]) : Expected benefit description, default None
            status (str) : use case's status value, default "new"

        Returns:
            Dict[str, Any] : Informatzion dictionary of use case created    
        """

        db = self._get_session()

        try:

            # checks
            # (1) is company existing?
            company = db.query(Company).filter(Company.id == company_id).first()
            if not company:
                raise ValueError(f"Company with ID {company_id} does not exist.")
            
            # (2) is industry existing?
            industry = db.query(Industry).filter(Industry.id == industry_id).first()
            if not industry:
                raise ValueError(f"Industry with ID {industry_id} does not exist.")
            
            # (3) title may not be empty
            if len(title) == 0: # TODO also check fro upper limit
                raise ValueError("Title must not be empty.")

            # (4) status in valid range
            self._validate_status(status)

            # if ok lets create a new use case
            new_use_case = UseCase(
                title = title,
                description = description, 
                expected_benefit = expected_benefit, 
                company_id = company_id, 
                industry_id = industry_id, 
                status = status
            )
            
            # add and save
            db.add(new_use_case)
            db.commit()
            db.refresh(new_use_case)

            return self._use_case_to_dict(new_use_case)
        
        except Exception as e:  # hope thats alright TODO check if rollback is correct or if there is no error handling needed
            db.rollback()
            raise e
        
        finally:
            db.close()

    def update_use_case(
            self, 
            use_case_id : int, 
            title : Optional[str] = None, 
            description : Optional[str] = None, 
            expected_benefit : Optional[str] = None, 
            status : Optional[str] = None, 
            company_id : Optional[int] = None, 
            industry_id : Optional[int] = None
            ) -> Dict[str, Any]:
        """ 
        Update an use case specified by use_case id. Only arguments provided will be updated. 

        Args:
            use_case_id (int): ID of the use case to update (required)
            title (Optional[str]): New title (default: None, no change)
            description (Optional[str]): New description (default: None, no change)
            expected_benefit (Optional[str]): New expected benefit (default: None, no change)
            status (Optional[str]): New status (default: None, no change)
            company_id (Optional[int]): New company ID (default: None, no change)
            industry_id (Optional[int]): New industry ID (default: None, no change)
        
        Returns:
            Dict[str, Any]: Dictionary containing the updated use case information
        """
        
        db = self._get_session()

        try: 
            # check if valid id
            use_case_in_question = db.query(UseCase).filter(UseCase.id == use_case_id).first()
            if not use_case_in_question:
                raise ValueError(f"Given Id {use_case_id} not found in database.")
            
            # updated parameter if provided
            # (1) Title
            if title is not None:
                if len(title) == 0:  # TODO also check for upper limit!
                    raise ValueError(f"Title must not be empty.")
                use_case_in_question.title = title
            
            # (2) Description
            if description is not None: 
                use_case_in_question.description = description
            
            # (3) Expected benefit
            if expected_benefit is not None:
                use_case_in_question.expected_benefit = expected_benefit
            
            # (4) Status
            if status is not None:
                self._validate_status(status)
                use_case_in_question.status = status

            # (5) Company id
            if company_id is not None: 
                # check if company exists
                company = db.query(Company).filter(Company.id == company_id).first()
                if not company:
                    ValueError(f"Company with ID {company_id} does not exist. ")
                use_case_in_question.company_id = company_id
            
            # (6) Industry
            if industry_id is not None:
                # check if industry exists
                industry = db.query(Industry).filter(Industry.id == industry_id).first()
                if not industry:
                    raise ValueError(f"Industry with ID {industry_id} does not exist. ")
            
            # save
            db.commit()
            db.refresh(use_case_in_question)

            return self._use_case_to_dict(use_case_in_question)
        
        except Exception as e: 
             db.rollback()
             raise e 
        
        finally:
            db.close()


    def update_use_case_status(self, use_case_id : int, status : str) -> Dict[str, Any]: 
        """ 
        Update the status of an use case specifed by the ID. 

        Args: 
            use_case_id (int) : ID of the use case to get a new status
            status (str) : New staus value
        Reurns:
            Dict[str, Any] : Updated use case .
        """
        return self.update_use_case(use_case_id = use_case_id, status = status)
    
    def delete_use_case(self, use_case_id : int) -> Dict[str, Any]:
        """ 
        Delete one use case from the database and returns its informatin  for the last time.

        Args:
            use_case_id (int) : I dod the use case to be deleted

        Returns:
            dict of informatin of te use case that has been deleted.
        """

        db = self._get_session()

        try: 
            # check if is is valid
            use_case_to_be_deleted = db.query(UseCase).filter(UseCase.id == use_case_id).first()
            if not use_case_to_be_deleted:
                raise ValueError(f"Use case with ID {use_case_id} not found in database.")
            
            use_case_dict = self._use_case_to_dict(use_case_to_be_deleted)  # for final returning it
            
            # do the deletion
            db.delete(use_case_to_be_deleted)
            db.commit()

            return use_case_dict

        except Exception as e:
            db.rollback()
            raise e

        finally:
            db.close()

    def filter_use_cases(
            self, 
            company_id : Optional[int] = None, 
            industry_id : Optional[int] = None, 
            status : Optional[str] = None, 
            person_id : Optional[int] = None
    ) -> List[Dict[str, Any]]: 
        """ 
        Filter use cases by various criteria.
        All filters are optional.
        
        Args:
            industry_id: Filter by industry ID (optional)
            company_id: Filter by company ID (optional)
            status: Filter by status (optional)
            person_id: Filter by person who contributed (optional)
            
        Returns:
            List of use cases matching the filters
        """

        db = self._get_session()

        try:

            query = db.query(UseCase)

            # uif company is provided
            if company_id is not None: 
                query = query.filter(UseCase.company_id == company_id)
            
            # filter industry
            if industry_id is not None: 
                query = query.filter(UseCase.industry_id == industry_id)

            # filer status
            if status is not None:  # no checks needed here
                query = query.filter(UseCase.status == status)

            # filter person
            if person_id is not None: 
                query = query.join(UseCase.persons).filter(Person.id == person_id)

            # run filter
            filtered_use_cases = query.all()

            return [self._use_case_to_dict(uc) for uc in filtered_use_cases]

        finally:
            db.close()

    def archive_use_case(self, use_case_id : int) -> Dict[str, Any]: 
        """
        Sets the status of a use case to archived. 

        Args: 
            use_case_id (int) : use case id of use case to be archived

        Returns:
            Dict[str, Any] : Dict of the use case that has been archived
        """ 
        return self.update_use_case_status(use_case_id, "archived")
    
    def get_all_industries(self) -> List[Dict[str, Any]]:
        """  
        Get all industries with their IDs and names.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing:
                - id: Industry ID
                - name: Industry name
        """
        db = self._get_session()

        try: 
            # return all industries as dictionaries
            industries = db.query(Industry).all()
            return [{"id": ind.id, "name": ind.name} for ind in industries]
        finally:
            db.close()

    def get_all_companies(self) -> List[Dict[str, Any]]: 
        """  
        Get all companies with their IDs, names, and industry information.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing:
                - id: Company ID
                - name: Company name
                - industry_id: Associated industry ID
                - industry_name: Associated industry name
        """
        db = self._get_session()

        try: 
            companies = db.query(Company).all()
            return [{
                "id": comp.id,
                "name": comp.name,
                "industry_id": comp.industry_id,
                "industry_name": comp.industry.name
            } for comp in companies]
        finally:
            db.close()

    def get_all_persons(self) -> List[Dict[str, Any]]: 
        """ 
        Get all persons with their IDs, names, roles, and company information.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing:
                - id: Person ID
                - name: Person name
                - role: Person's role/position
                - company_id: Associated company ID
                - company_name: Associated company name
        """
        db = self._get_session()

        try:
            
            persons = db.query(Person).all()
            return [{
                "id": person.id,
                "name": person.name,
                "role": person.role,
                "company_id": person.company_id,
                "company_name": person.company.name
            } for person in persons]
        finally:
            db.close()

    def get_persons_by_use_case(self, use_case_id : int) -> List[Dict[str, Any]]: 
        """  
        Get all persons who contributed to a specific use case.
        
        Args:
            use_case_id (int): ID of the use case
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing:
                - id: Person ID
                - name: Person name
                - role: Person's role/position
                - company_name: Associated company name
        """
        db = self._get_session()

        try: 
            use_case = db.query(UseCase).filter(UseCase.id == use_case_id).first()
            if not use_case:
                raise ValueError(f"Use case with ID {use_case_id} does not exist.")
            
            return [{
                "id": person.id,
                "name": person.name,
                "role": person.role,
                "company_name": person.company.name
            } for person in use_case.persons]

        finally:
            db.close()

    def create_industry(self, name: str) -> Dict[str, Any]:
        """
        Create a new industry.
        
        Args:
            name (str): Industry name
            
        Returns:
            Dict[str, Any]: Created industry with id and name
            
        Raises:
            ValueError: If industry with this name already exists
        """
        db = self._get_session()
        try:
            # Check if already exists
            existing = db.query(Industry).filter(Industry.name == name).first()
            if existing:
                raise ValueError(f"Industry '{name}' already exists with ID {existing.id}")
            
            # Create new
            industry = Industry(name=name)
            db.add(industry)
            db.commit()
            db.refresh(industry)
            
            return {"id": industry.id, "name": industry.name}
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def create_company(self, name: str, industry_id: int) -> Dict[str, Any]:
        """
        Create a new company.
        
        Args:
            name (str): Company name
            industry_id (int): ID of the industry this company belongs to
            
        Returns:
            Dict[str, Any]: Created company info
            
        Raises:
            ValueError: If company already exists or industry doesn't exist
        """
        db = self._get_session()
        try:
            # Check if industry exists
            industry = db.query(Industry).filter(Industry.id == industry_id).first()
            if not industry:
                raise ValueError(f"Industry with ID {industry_id} does not exist")
            
            # Check if company already exists
            existing = db.query(Company).filter(Company.name == name).first()
            if existing:
                raise ValueError(f"Company '{name}' already exists with ID {existing.id}")
            
            # Create new
            company = Company(name=name, industry_id=industry_id)
            db.add(company)
            db.commit()
            db.refresh(company)
            
            return {
                "id": company.id,
                "name": company.name,
                "industry_id": company.industry_id,
                "industry_name": industry.name
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def create_person(self, name: str, role: str, company_id: int) -> Dict[str, Any]:
        """
        Create a new person.
        
        Args:
            name (str): Person's name
            role (str): Person's role/position
            company_id (int): ID of the company this person works for
            
        Returns:
            Dict[str, Any]: Created person info
            
        Raises:
            ValueError: If company doesn't exist
        """
        db = self._get_session()
        try:
            # Check if company exists
            company = db.query(Company).filter(Company.id == company_id).first()
            if not company:
                raise ValueError(f"Company with ID {company_id} does not exist")
            
            # Create new person
            # duplicates are ok I guess
            person = Person(name=name, role=role, company_id=company_id)
            db.add(person)
            db.commit()
            db.refresh(person)
            
            return {
                "id": person.id,
                "name": person.name,
                "role": person.role,
                "company_id": person.company_id,
                "company_name": company.name
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def find_or_create_industry(self, name: str) -> Dict[str, Any]:
        """
        Find existing industry by name, or create if doesn't exist.
        Case-insensitive search.
        
        Args:
            name (str): Industry name
            
        Returns:
            Dict[str, Any]: Industry info (existing or newly created)
        """
        db = self._get_session()
        try:
            # Try to find existing (case-insensitive)
            industry = db.query(Industry).filter(
                Industry.name.ilike(name)
            ).first()
            
            if industry:
                return {"id": industry.id, "name": industry.name}
            
            # Create new
            industry = Industry(name=name)
            db.add(industry)
            db.commit()
            db.refresh(industry)
            
            return {"id": industry.id, "name": industry.name}
        finally:
            db.close()

    def find_or_create_company(self, name: str, industry_name: str) -> Dict[str, Any]:
        """
        Find existing company by name, or create if doesn't exist.
        Also ensures industry exists (creates if needed).
        Case-insensitive search.
        
        Args:
            name (str): Company name
            industry_name (str): Industry name
            
        Returns:
            Dict[str, Any]: Company info (existing or newly created)
        """
        db = self._get_session()
        try:
            # Try to find existing company
            company = db.query(Company).filter(
                Company.name.ilike(name)
            ).first()
            
            if company:
                return {
                    "id": company.id,
                    "name": company.name,
                    "industry_id": company.industry_id,
                    "industry_name": company.industry.name
                }
            
            # Need to create - first ensure industry exists
            industry = db.query(Industry).filter(
                Industry.name.ilike(industry_name)
            ).first()
            
            if not industry:
                industry = Industry(name=industry_name)
                db.add(industry)
                db.commit()
                db.refresh(industry)
            
            # Now create company
            company = Company(name=name, industry_id=industry.id)
            db.add(company)
            db.commit()
            db.refresh(company)
            
            return {
                "id": company.id,
                "name": company.name,
                "industry_id": company.industry_id,
                "industry_name": industry.name
            }
        finally:
            db.close()

    def find_or_create_person(self, name: str, role: str, company_id: int) -> Dict[str, Any]:
        """
        Find existing person by name and company, or create if doesn't exist.
        Updates role if person exists but role has changed.
        
        Args:
            name (str): Person's name
            role (str): Person's role/position
            company_id (int): Company ID
            
        Returns:
            Dict[str, Any]: Person info (existing or newly created)
        """
        db = self._get_session()
        try:
            # Try to find existing person at this company
            person = db.query(Person).filter(
                Person.name == name,
                Person.company_id == company_id
            ).first()
            
            if person:
                # Update role if different
                if person.role != role:
                    person.role = role
                    db.commit()
                    db.refresh(person)
                
                return {
                    "id": person.id,
                    "name": person.name,
                    "role": person.role,
                    "company_id": person.company_id,
                    "company_name": person.company.name
                }
            
            # Create new
            person = Person(name=name, role=role, company_id=company_id)
            db.add(person)
            db.commit()
            db.refresh(person)
            
            return {
                "id": person.id,
                "name": person.name,
                "role": person.role,
                "company_id": person.company_id,
                "company_name": person.company.name
            }
        finally:
            db.close()

    def add_persons_to_use_case(self, use_case_id: int, person_ids: List[int]) -> Dict[str, Any]:
        """
        Add persons to a use case (many-to-many relationship).
        Does NOT clear existing persons - only adds new ones.
        
        Args:
            use_case_id (int): ID of the use case
            person_ids (List[int]): List of person IDs to add
            
        Returns:
            Dict with use case info and linked persons
            
        Raises:
            ValueError: If use case doesn't exist
        """
        db = self._get_session()
        try:
            use_case = db.query(UseCase).filter(UseCase.id == use_case_id).first()
            if not use_case:
                raise ValueError(f"Use case with ID {use_case_id} does not exist")
            
            # Get current person IDs
            current_person_ids = {p.id for p in use_case.persons}
            
            # Add new persons
            added_count = 0
            for person_id in person_ids:
                if person_id not in current_person_ids:
                    person = db.query(Person).filter(Person.id == person_id).first()
                    if person:
                        use_case.persons.append(person)
                        added_count += 1
            
            db.commit()
            
            return {
                "use_case_id": use_case_id,
                "persons_added": added_count,
                "total_persons": len(use_case.persons)
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()



            
    def __repr__(self):
        return "<UseCaseService>"