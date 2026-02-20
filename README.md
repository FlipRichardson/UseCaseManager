# UseCase Manager

AI-powered use case management system with agent assistance and role-based access control for workshop facilitation and use case tracking.

# Overview

UseCase Manager is a comprehensive system designed to help organizations manage and track AI/ML use cases discovered during workshops. It combines manual data entry with an AI agent that can create, query, and manage use cases through natural language conversation. The system includes automatic transcript processing to extract use cases from workshop transcripts.
Demonstration can be found in DEMO.ipynb (run init_dummy_database.py first).

## Features

### Use Case Management
- CRUD operations (Create, Read, Update, Delete) for creating use cases, industries, companies, and persons assigned
- Manual forms and AI-assisted creation via chat
- Status tracking (new, in_review, approved, in_progress, completed, archived)
- Contributor tracking (persons linked to use cases)
- Sortable, paginated table view

### Transcript Processing
- Upload workshop transcripts (.txt files)
- LLM-powered extraction of multiple use cases
- Automatic entity creation (use cases, companies, industries, persons)

### AI Agent Chat Interface
- Natural language interaction with the database
- Multi-round tool calling (up to 10 rounds per query)
- Full conversation history with context retention
- Verbose logging for debugging and transparency

### Role-Based Access Control
Three permission levels with complete UI adaptation:

**Reader:**
- View use cases and chat for read queries only
- No creation, editing, or deletion capabilities
- Automatically assigned for newly registered users

**Maintainer:**
- All Reader permissions
- Create, edit, and update use cases
- Manual CRUD forms and AI agent access
- Upload and process transcripts
- Cannot delete or archive use cases or manage users

**Admin:**
- All Maintainer permissions
- Delete and archive use cases
- User management (view all users, change roles)
- Full system access

### Authentication & Security
- Secure login with bcrypt password hashing
- Simple registration (new users default to Reader)
- Session-based user tracking
- Permission checks at both UI and service layers

## Technology 

**Frontend:**
- NiceGUI (Python-based web framework)
- Tailwind CSS for styling
- Async/await for responsive UI

**Backend:**
- Python 3.12
- SQLAlchemy ORM
- SQLite database

**AI/LLM:**
- Claude Sonnet 3.5 via OpenRouter API
- Multi-round tool calling
- Structured output extraction

**Authentication:**
- email and password
- no verification
- bcrypt password hashing
- Session-based storage

## Installation & Setup

### Prerequisites
- Python 3.12
- OpenRouter API key

### Step 1: Clone Repository
```bash
git clone 
cd UseCaseManager
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=your_api_key_here
```

To get an API key: https://openrouter.ai/

### Step 5: Initialize Database
```bash
python init_dummy_database.py
```

This creates the SQLite database with sample data and test users.

### Step 6: Run Application
```bash
python app.py
```

## Default Test Users

| Email | Password | Role | 
|-------|----------|------|
| reader@example.com | reader123 | Reader 
| maintainer@example.com | maintainer123 | Maintainer 
| admin@example.com | admin123 | Admin 

## Usage Examples

### Chat with the AI Agent

**Create a use case:**
```
"Create a use case for predictive maintenance at Bosch in the Manufacturing sector. 
Description: IoT sensors predict equipment failures. 
Expected benefit: Reduce downtime by 30%."
```

**Query use cases:**
```
"Show me all use cases for Siemens Energy"
"What use cases are in the Energy sector?"
"Which use cases are in progress?"
```

**Update use cases:**
```
"Change the status of use case 5 to approved"
"Add Anna Schmidt as a contributor to use case 3"
```

### Upload Workshop Transcript

1. Click **"Upload Transcript"** in the header (Maintainer/Admin only)
2. Select a `.txt` file containing workshop notes
3. Watch progress notifications as the system:
   - Extracts use cases using LLM
   - Creates each use case with the agent
   - Updates the table automatically

Sample transcripts available in: `test_data/transcripts/`

### Manual CRUD Forms

Expand the **"Create New Entities"** section to manually:
- Create industries
- Create companies (with industry selection)
- Create persons (with company selection)
- Create use cases (with cascading industry, company dropdowns)

### View & Edit Use Cases

1. Click the eye icon on any table row
2. View full details (all users)
3. Edit fields (Maintainer/Admin only)
4. Add contributors from the same company
5. Delete use case (Admin only)

## Project Structure
```
UseCaseManager/
├── agent/                          # AI agent with tool calling
│   ├── agent.py                   # Main agent loop with LLM calls
│   ├── tools.py                   # Tool definitions for agent
│   └── tool_executor.py           # Tool execution and permissions
│
├── extraction/                     # Transcript processing
│   └── transcript_processor.py    # LLM-based use case extraction
│
├── models/                         # SQLAlchemy database models
│   ├── base.py                    # Database configuration
│   ├── use_case.py                # UseCase, Industry, Company, Person
│   └── user.py                    # User authentication model
│
├── services/                       # Business logic layer
│   ├── use_case_service.py        # CRUD operations with permissions
│   └── user_service.py            # Authentication and user management
│
├── utils/                          # Utilities
│   └── permissions.py             # Permission checking functions
│
├── test_data/                      # Sample data
│   └── transcripts/               # Example workshop transcripts
│       ├── energy_workshop_transcript.txt
│       ├── manufacturing_workshop_transcript.txt
│       └── healthcare_workshop_transcript.txt
│
├── notebooks/                      # Jupyter notebooks (exploration)
│   └── [development notebooks]    # POC and experimentation
│
├── Test files (root - to be organized):
│   ├── test_agent.py              # Agent functionality tests
│   ├── test_auth.py               # Authentication tests
│   ├── test_permissions.py        # Permission system tests
│   ├── test_extraction_module.py  # Transcript processing tests
│   ├── test_use_case_service_classes.py  # Service layer tests
│   ├── test_agent_use_case_creation_from_one_promt.py
│   └── test_agent_company_industry_person_creation.py
│
├── Documentation:
│   ├── README.md                  # This file (main documentation)
│   ├── TESTING.md                 # Comprehensive test documentation
│   ├── Test-Documentation.md      # Additional test notes
│   ├── architecture-and-plan.md   # Initial architecture decisions
│   └── day-to-day-documentation.md  # Development journal
│
├── Main application files:
│   ├── app.py                     # NiceGUI web interface (MAIN ENTRY)
|   ├── DEMO.ipynb                 # Demonstration of all features besides app.py
│   ├── init_comprehensive_db.py   # Database initialization script
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables (not in git)
│   ├── .env.example               # Environment template
│   ├── .gitignore                 # Git ignore rules
│   └── use_cases.db               # SQLite database (generated)
│
└── Development artifacts:
    ├── agent_proof_of_concept.ipynb  # Agent POC notebook
    ├── test_db.ipynb              # Database exploration
    └── frontend/                  # Early UI experiments (deprecated)
```

**Note:** Test files are currently in the root directory for quick iteration during development. In a production refactor, these would be organized into the `tests/` directory.

## Development Artifacts

Several files in the root directory are development artifacts from the iterative development process:

**Test Files:**
- Various `test_*.py` files were created during development for quick testing
- All tests documented in `TESTING.md`

**Documentation Files:**
- `architecture-and-plan.md` - Initial planning and architecture decisions
- `day-to-day-documentation.md` - Development journal and progress tracking
- `Test-Documentation.md` - Additional testing notes

**Notebooks:**
- `agent_proof_of_concept.ipynb` - Initial agent POC
- `test_db.ipynb` - Database schema exploration
- Located in root for historical reference

These artifacts origin from the iterative development process and are retained for reference. A production cleanup would organize tests properly and archive development notebooks.

## Architecture Decisions

### Why NiceGUI?
- Python-native 
- Rapid prototyping for demo purposes
- Easy integration with Python backend

### Why SQLite?
- Zero configuration
- Single file database
- Good for demo and development
- Easy to reset and reinitialize

### Agent Architecture
- Multi-round tool calling enables complex workflows
- Service layer enforces permissions consistently
- Conversation history maintains context

## Development Notes, Known Issues & Limitations

**Testing:**
- Comprehensive testing document: `TESTING.md`
- All features tested across three roles

**Database:**
- No database migrations system implemented
- Manual schema updates required for changes

**Authentication:**
- Simple session storage 
- No password reset functionality
- No email verification
- Sessions don't persist across server restarts

**File Upload:**
- Only `.txt` files supported for transcripts
- No support for PDF, DOCX, or other formats
- No OCR for scanned documents
- Large files may cause long wait times

**UI:**
- Chat history cleared on logout
- No conversation export functionality

**Agent Behavior:**
- Occasional hallucinations
- May require multiple attempts for complex queries
- No confidence scores on responses

### Functional Gaps

**Use Case Management:**
- No versioning/history of changes
- Can't restore deleted use cases
- No bulk operations (delete multiple, export selection)
- No advanced filtering (date ranges, multiple criteria)
- No tags or custom categories
- No date/time tracking

**Data Import/Export:**
- No CSV import
- No export to Excel/PDF
- No backup/restore functionality
- No data migration tools

**Search:**
- Basic filtering only
- No full-text search
- No semantic search across descriptions
- No saved searches/filters

### Performance 

**Response Times:**
- Agent responses: 5-15 seconds (depends on LLM)
- Transcript processing: 30-60 seconds per transcript

**Scalability:**
- Single-threaded NiceGUI server
- Not designed for many concurrent users

## Testing Coverage

**Current State:**
- [x] All major features tested manually
- [x] All three roles tested comprehensively
- [ ] No automated unit tests
- [ ] No integration tests

## Context

This project was developed as part of an AI Engineer assessment.
**Time Investment:** ~ 4 - 5 days  
