## Day 1 (11.02. Evening)
- set up venv
- set up basic folder structure
- made plan and scoping
- set up git

## Day 2 (13.02.)
- implemented database classes in folder models
    - base
    - industry
    - company
    - person
    - usecase
- filled dummy database with dummy data
- tested agent calling - is connection working?
- implemented function call
    - get all use cases from dummy database
    - nothing more
- Agent connection was successfull
- Agent can call the function (get_all_use_cases) and returns them 
- Tested other prompts: 
    - sometimes agent still calls function, yet doesnt include the result in response
    - can filter results by its own (return only healthcare usecases)
- used Claude 3.5 sonnet
- decided to not further test other agents due to time constraints, can be done when encountering problems
- implemented CRUD layer in notebook
    - Class UseCaseService with many functions as
    - get_all_use_cases
    - get_use_case_by_id
    - create_use_case
    - update_use_case
    - update_use_case_status
    - delete_use_case
    - filter_use_cases
    - archive_use_case
    - and some helpers
- copied to python file

# Day 3 (14.02, Midday): 
- documentation and test service functions