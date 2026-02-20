# Architecture & Technical Decisions

## Strategic Approach

### Time Management Reality
- Available time: 5 working days (? if at all i have time for this)
- Limited daily hours due to job
- First assessment: Implementation of all features is not possible, even core ones are very hard, priorization needed

### Scope Definition

**In Scope (Must haves):**
- Core use case CRUD (create, read, update, delete)
- AI agent with natural language queries
- Multi-round tool calling (agent can gather info across multiple steps)
- Transcript extraction (LLM extracts use cases from workshop notes)
- Company/Industry/Person management
- Role-based access (Reader/Maintainer/Admin)
- Basic web UI (NiceGUI for speed)
- Status workflow (new → in_review → approved → in_progress → completed → archived)

**Out of Scope (should haves and nice to haves 8-14):**
- Relationships between use cases
- Industry-wide intelligence - not explicitly implemented but may partly work
- Evaluation and priorization 
- Road map generation
- use case library and inspiration - may work partly
- Multi transcript support
- Visualization

## Technology Plan

### Backend
- Python, probably throught the entire task
- Database: SQLite with SQLAlchemy
- LLM: OpenRouter API
  - Lets try OpenAI library with key
- LLM interaction: Agent can call function tat I implement for controlled agent-database interaction

### Frontend
- **Framework:** NiceGUI
  - Python based, hope for fast prototyping
  - Callback-based architecture 
  - Trade-off: Less polished than modern frameworks, but fits time constraints

### Procedure overview

User Input → Agent (LLM) → Tool Selection → Service Functions → Database
→ Agent returns output/result
               
**Components:**

1. **Database Layer**
   - SQL Achemiy wrapper class
   - Wrapper has functions to manipulate values, will be called only by service layer (and this one only by agent or user input)

2. **Service Layer**
   - CRUD operations, filtering, status management
   - Agaent or user can call these functions
   - Later: Frontend controller passes user input to this layers' functions

3. **Agent Layer**
   - LLM with function calling capability
   - Defined tool schemas for each service function (see section 2)
   - In discussion with user, may or may not call service functions, this makes inquiries / questions for specification possible
   - GOOD PROMPTING NEEDED for extraction of transcripts → When extracting from transcript, the agant can call functions (add/write to db) as often as needed

4. **Frontend Layer (NiceGUI)**
   - Handles user input, be it enter or buttom pressed events
   - acts as main controller, calls service functions or aganet calling service functions
   - this is going to be hard and time consuming, very basic working example here
   - log in screen with log in (check if user saved in user db, PW check with hash), user defined for session

## Prioritization

### Very Important
1. **Transcript Analysis & Use Case Extraction**
   - LLM-based extraction from text files
   - Calls functions to interact with database
   - good promting found
   - Some dummy transcripts to work with
   - needs to be done in conjunction with part 2, functions and db the agent can work with
   
2. **Company, Industry & Person Management**
   - Database wrapper 
      - with db interaction methods: write, delete, ..
      - possible: if not in part 3, filtering / printing
   - use case class
   
3. **Use Case CRUD via Agent**
   - Natural language interface for all methods from part 2/1 (service layer)
   - Filtering by company, industry, status, person
   - bring database in format the agent can use it as context
   
4. **Status Management**
   - Possible status: New → In Review → Approved → In Progress → Completed → Archived
   - Basically, extension to part 3: service layer extrension, agant extension that it can call service
   - Validation of allowed transitions, if time

5. **Conversational Interface**
   - Database to agant context necessary
   - agent may or may not call function with each answer for enabling user interaction
   - Function calling for database operations
   - testing of agent reliability

### Important - Medium
6. **Authentication & Authorization**
   - Three roles: Reader, Maintainer, Admin
   - Role-based access control in both agent and UI
   - Approach: Basic, no time for big approach
     - SQLite table for users (id, email, password_hash, role)
     - Simple login before main app
     - if register clicked, add to database
     - user added to session and passed to service functions as additional input, the service functions check the user role and act accordingly
   - This may be very time consuming, keep simple

### Medium Priority
7. **Modern Frontend with Agent Integration**
   - This is critical, may take hugh amount of time
   - NiceGUI for rapid development, needs to be done possibly in conjunction with part 6, maybe even before it
   - not fancy! i rather hope for something working
   - Login and registration pop up first, afterwards:
   - Chat interface for agent
   - Simple table view of use cases
   - Basic manual CRUD via buttons/rightclick
   - Admin panel: if admin logged in: list of users, withoption to change roles, very basic
   - **Trade-off:** This might be so time consuming, modern ... 

### Should-Have - Low Priority
If first steps implemented well, maybe some possible, but further definition needed, unsharp features
8. Cross-industry intelligence features
9. Use case relationships
10. Evaluation & prioritization

### Nice-to-Have - Low Priority
Same as should haves, maybe visualizations would be nice.
11. Roadmap generation
12. Advanced search/similarity
13. Visualizations

### Risks
1. **LLM reliability** 
   - Low experience with agents
   - Start with proof-of-concept early
   - Test thoroughly before building dependent features

2. **Frontend time problematic** 
   - Rather very basic but working, dont aim high here

3. **Bidirectional sync**
   - from experience, here are bugs included when going for performance
   - First approach, update view / chat history after event happend
   - Possible trade off here

## Plan for now, day 1 ( will be updated)

- first plan into issues
- create test transcripts 
- create basic database wrapper
- manual agent testing
   - agent extracts all information and returns them
   - agant can call a function and passes right input
- one first service function
- Entry successfully added to database
- next steps to be added


## Open Questions / Decisions Pending
- Agent conversation memory/context handling
- How much validation in service layer vs. trusting LLM
- Error handling strategy for LLM failures

