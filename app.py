from nicegui import ui, app
from services.user_service import UserService

# init user service
user_service = UserService()

# Global storage for UI elements (can't be stored in app.storage)
ui_elements = {}  # ← ADD THIS LINE

@ui.page('/')
def index_page():
    """
    Entry point
    If the current user is set -> Main page
    If not -> Login page
    """
    if 'current_user' not in app.storage.user:
        app.storage.user['current_user'] = None  # set key as cookie

    if 'conversation_history' not in app.storage.user:
        app.storage.user['conversation_history'] = []  # inti history

    current_user = app.storage.user['current_user']

    if current_user:
        show_main_app()
    else:
        show_login_page()

def show_login_page():
    """  
    Login page or register page: Page with email, PW fields as well as log in and register buttons.
    """

    with ui.column().classes('w-full h-screen items-center justify-center'):
        # Creates a column that:
        # - Takes full width and height of browser window
        # - Centers everything inside both horizontally and vertically

        # Card for login form
        with ui.card().classes('w-96 p-8'):  # visible frame

            # labels for title and input question
            ui.label('UseCase Manager').classes('text-2xl font-bold mb-4')  # text size, bold, margin bottom
            ui.label('Please log in to continue').classes('text-gray-600 mb-6') # text color, margin buttom

            # Email input
            email_input = ui.input('Email', placeholder='user@example.com').classes('w-full')

            # Password input
            password_input = ui.input('Password', password=True, password_toggle_button=True).classes('w-full')

            # Error message placeholder
            # for invalid input
            error_label = ui.label('').classes('text-red-500 text-sm')  # error are red
            error_label.visible = False

            # Buttons row
            with ui.row().classes('w-full gap-2 mt-4'):
                ui.button('Login', on_click=lambda: handle_login(
                    email_input.value, 
                    password_input.value, 
                    error_label
                )).classes('flex-1')
                
                ui.button('Register', on_click=lambda: handle_register(
                    email_input.value, 
                    password_input.value, 
                    error_label
                )).classes('flex-1').props('outline')

            # Test credentials info
            with ui.expansion('Test Credentials', icon='info').classes('w-full mt-4'):
                ui.label('Reader: reader@example.com / reader123').classes('text-sm')
                ui.label('Maintainer: maintainer@example.com / maintainer123').classes('text-sm')
                ui.label('Admin: admin@example.com / admin123').classes('text-sm')

def handle_login(email : str, password : str, error_label):
    """  
    Handles login attempt (login button pressed)
    """
    # no email or no password provided
    if not email or not password:
        error_label.text = 'Please enter both email and password'
        error_label.visible = True
        return
    
    # if provided -> authenticate with user service
    user = user_service.authenticate(email, password)

    # if user is not None, i.e. its a valid user
    if user:
        # set user as current user
        app.storage.user['current_user'] = user

        # some welcome message
        ui.notify(f'Welcome, {user["name"]}!', type='positive')

        # reload index -> this time current user is set and the main application should load
        ui.navigate.to('/')  # Reload page (will show main app)

    else:
        
        # user is None -> no correct password/email -> stick on log in page
        error_label.text = 'Invalid email or password'
        error_label.visible = True

def handle_register(email: str, password: str, error_label): 
    """  
    Handles registration event.
    if the input is valid, i.e. email and password provided
    -> creates a reader, makes login (sets user in cookies),
    and reloads the index page. As the user is set now, the index with load the main page
    """
    # Validate inputs
    if not email or not password:
        error_label.text = 'Please enter both email and password'
        error_label.visible = True
        return
    
    # Create user (always as reader role)
    try:
        user = user_service.create_user(
            email=email,
            password=password,
            role='reader',  # New users are always readers
            name=email.split('@')[0].title()  # Use email prefix as name
        )
        
        # Auto-login after registration
        app.storage.user['current_user'] = user
        ui.notify(f'Account created! Welcome, {user["name"]}!', type='positive')
        ui.navigate.to('/')  # Reload page (will show main app)
        
    except ValueError as e:
        error_label.text = str(e)
        error_label.visible = True

def refresh_use_case_table():
    """Refresh the use case table without reloading the page"""
    try:
        # Get current user and table reference
        current_user = app.storage.user.get('current_user')
        table = ui_elements.get('use_case_table')
        
        if not table:
            return  # Table not initialized yet
        
        # Fetch fresh data
        from services import UseCaseService
        service = UseCaseService()
        use_cases = service.get_all_use_cases(current_user=current_user)
        
        # Update table rows
        table.rows = use_cases
        table.update()
        
    except Exception as e:
        print(f"Error refreshing table: {e}")

async def send_message(message_input, chat_container):
    """Handle sending a message to the agent (async to prevent UI freeze)"""
    import asyncio
    from agent import run_agent
    from agent.tool_executor import set_current_user
    
    # Get message text
    user_message = message_input.value.strip()
    if not user_message:
        return
    
    # Clear input
    message_input.value = ''
    
    # Get current user and history
    current_user = app.storage.user.get('current_user')
    history = app.storage.user.get('conversation_history', [])
    
    # Set current user for agent permissions
    set_current_user(current_user)
    
    # Add user message to history
    history.append({
        'role': 'user',
        'content': user_message
    })
    
    # Display user message
    with chat_container:
        with ui.row().classes('w-full mb-2'):
            ui.label(user_message).classes(
                'bg-blue-500 text-white px-4 py-2 rounded-lg max-w-[80%] ml-auto'
            )
    
    # Show "Agent is thinking..." message
    with chat_container:
        thinking_row = ui.row().classes('justify-start mb-2')
        with thinking_row:
            thinking_label = ui.label('🤔 Agent is thinking...').classes(
                'bg-gray-100 px-4 py-2 rounded-lg border italic animate-pulse'
            )
    
    # Scroll to show thinking message
    chat_container.run_method('scrollTo', 0, 99999)
    
    # Run agent in background thread (prevents UI freeze)
    try:
        # Build conversation history
        agent_history = [msg for msg in history]
        
        # Run agent in executor (separate thread, non-blocking)
        agent_response = await asyncio.to_thread(
            run_agent,
            user_message,
            conversation_history=agent_history[:-1],
            verbose=True,
            max_rounds=10
        )
        
        # Remove "thinking..." message
        thinking_row.delete()
        
        # Add agent response to history
        history.append({
            'role': 'assistant',
            'content': agent_response
        })
        
        # Display agent message
        with chat_container:
            with ui.row().classes('justify-start mb-2'):
                ui.label(agent_response).classes(
                    'bg-white px-4 py-2 rounded-lg border max-w-[80%] whitespace-pre-wrap'
                )
        
        # Save history
        app.storage.user['conversation_history'] = history
        
        # Scroll to bottom
        chat_container.run_method('scrollTo', 0, 99999)

        # Refresh just the table
        await asyncio.sleep(0.3)  # Small delay
        refresh_use_case_table()
        
    except Exception as e:
        # Remove "thinking..." message
        thinking_row.delete()
        
        # Show error
        with chat_container:
            with ui.row().classes('justify-start mb-2'):
                ui.label(f'Error: {str(e)}').classes(
                    'bg-red-100 text-red-700 px-4 py-2 rounded-lg border border-red-300 max-w-[80%]'
                )

def show_use_case_details(use_case_data, current_user):
    """Show use case details in a dialog"""
    from services import UseCaseService
    from utils.permissions import check_permission
    
    service = UseCaseService()
    
    # Get full use case details
    use_case = service.get_use_case_by_id(use_case_data['id'], current_user=current_user)
    
    if not use_case:
        ui.notify('Use case not found', type='negative')
        return
    
    # Get contributors
    try:
        contributors = service.get_persons_by_use_case(use_case['id'], current_user=current_user)
    except:
        contributors = []
    
    # Check if user can edit
    can_edit = check_permission(current_user, 'update')
    can_delete = check_permission(current_user, 'delete')
    
    # Create dialog
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl'):
        # Header
        with ui.row().classes('w-full items-center justify-between mb-4'):
            ui.label('Use Case Details').classes('text-xl font-bold')
            ui.button(icon='close', on_click=dialog.close).props('flat round dense')
        
        # Content
        with ui.column().classes('w-full gap-4'):
            
            # ID (read-only always)
            ui.label(f'ID: {use_case["id"]}').classes('text-sm text-gray-600')
            
            # Title
            if can_edit:
                title_input = ui.input('Title', value=use_case['title']).classes('w-full')
            else:
                ui.label('Title').classes('text-sm font-medium text-gray-600')
                ui.label(use_case['title']).classes('text-lg')
            
            # Description
            if can_edit:
                desc_input = ui.textarea('Description', value=use_case.get('description', '')).classes('w-full')
            else:
                ui.label('Description').classes('text-sm font-medium text-gray-600')
                ui.label(use_case.get('description', 'N/A')).classes('')
            
            # Expected Benefit
            if can_edit:
                benefit_input = ui.textarea('Expected Benefit', value=use_case.get('expected_benefit', '')).classes('w-full')
            else:
                ui.label('Expected Benefit').classes('text-sm font-medium text-gray-600')
                ui.label(use_case.get('expected_benefit', 'N/A')).classes('')
            
            # Status
            if can_edit:
                status_options = ['new', 'in_review', 'approved', 'in_progress', 'completed', 'archived']
                status_select = ui.select(status_options, value=use_case['status'], label='Status').classes('w-full')
            else:
                ui.label('Status').classes('text-sm font-medium text-gray-600')
                ui.label(use_case['status'].replace('_', ' ').title()).classes('')
            
            # Company (read-only for now - could make dropdown later)
            ui.label('Company').classes('text-sm font-medium text-gray-600')
            ui.label(use_case['company_name']).classes('')
            
            # Industry (read-only)
            ui.label('Industry').classes('text-sm font-medium text-gray-600')
            ui.label(use_case['industry_name']).classes('')
            
            # Contributors
            ui.label('Contributors').classes('text-sm font-medium text-gray-600')
            if contributors:
                for person in contributors:
                    ui.label(f"• {person['name']} ({person['role']})").classes('text-sm')
            else:
                ui.label('No contributors listed').classes('text-sm italic text-gray-400')

            # Add person section (only if can edit)
            if can_edit:
                ui.separator().classes('my-2')
                ui.label('Add Contributor').classes('text-sm font-medium text-gray-600')
                
                # Get all persons from the same company
                all_persons = service.get_all_persons(current_user=current_user)
                
                # Filter to same company and exclude already added
                contributor_ids = {p['id'] for p in contributors}
                available_persons = [
                    p for p in all_persons 
                    if p['company_id'] == use_case['company_id'] and p['id'] not in contributor_ids
                ]
                
                if available_persons:
                    # Create dropdown options
                    person_options = {p['id']: f"{p['name']} ({p['role']})" for p in available_persons}
                    
                    with ui.row().classes('w-full gap-2 items-center'):
                        person_select = ui.select(
                            options=person_options,
                            label='Select person from company'
                        ).classes('flex-1')
                        
                        def add_person_to_use_case():
                            if not person_select.value:
                                ui.notify('Please select a person', type='warning')
                                return
                            
                            try:
                                result = service.add_persons_to_use_case(
                                    use_case['id'],
                                    [person_select.value],
                                    current_user=current_user
                                )
                                
                                # Get the person name for better feedback
                                person_name = person_options[person_select.value]
                                
                                ui.notify(
                                    f'{person_name} added successfully! Refresh to see changes.', 
                                    type='positive',
                                    position='top'
                                )
                                dialog.close()
                                
                            except Exception as e:
                                ui.notify(f'Error adding person: {e}', type='negative')
                        
                        ui.button('Add', on_click=add_person_to_use_case, icon='person_add').props('dense')
                else:
                    ui.label('No additional persons available from this company').classes('text-sm text-gray-400 italic')
            
            # Action buttons
            with ui.row().classes('w-full gap-2 mt-4'):
                if can_edit:
                    def update_use_case():
                        try:
                            service.update_use_case(
                                use_case_id=use_case['id'],
                                title=title_input.value,
                                description=desc_input.value,
                                expected_benefit=benefit_input.value,
                                status=status_select.value,
                                current_user=current_user
                            )
                            ui.notify('Use case updated successfully!', type='positive')
                            dialog.close()
                            ui.navigate.to('/')  # Refresh page
                        except Exception as e:
                            ui.notify(f'Error updating: {e}', type='negative')
                    
                    ui.button('Update', on_click=update_use_case, icon='save').classes('flex-1')
                
                if can_delete:
                    def delete_use_case():
                        try:
                            service.delete_use_case(use_case['id'], current_user=current_user)
                            ui.notify('Use case deleted successfully!', type='positive')
                            dialog.close()
                            ui.navigate.to('/')  # Refresh page
                        except Exception as e:
                            ui.notify(f'Error deleting: {e}', type='negative')
                    
                    ui.button('Delete', on_click=delete_use_case, icon='delete', color='red').props('outline')
                
                ui.button('Close', on_click=dialog.close).props('outline')
    
    dialog.open()

def show_main_app():
    """  
    main application. is loaded by index page if user is set correctly.
    This needs to be filled step by step.
    """
    current_user = app.storage.user.get('current_user')
    
    # Import here to avoid circular imports
    from utils.permissions import check_permission
    
    # === HEADER ===
    with ui.header().classes('items-center justify-between px-6'):
        ui.label('UseCase Manager').classes('text-xl font-bold')
        
        with ui.row().classes('gap-4 items-center'):
            # User info
            with ui.row().classes('gap-2 items-center'):
                ui.icon('person').classes('text-2xl')
                ui.label(current_user['name']).classes('font-medium')
                
                # Role badge
                role_color = {
                    'reader': 'bg-gray-500',
                    'maintainer': 'bg-blue-500', 
                    'admin': 'bg-red-500'
                }.get(current_user['role'], 'bg-gray-500')
                
                ui.label(current_user['role'].upper()).classes(
                    f'{role_color} text-white px-3 py-1 rounded text-sm'
                )
            
            # Upload Transcript button (only for maintainer/admin)
            if check_permission(current_user, 'create'):
                async def handle_upload(e):
                    import asyncio
                    
                    try:
                        # Read uploaded file (async!)
                        content = (await e.file.read()).decode('utf-8')
                        
                        from extraction.transcript_processor import extract_prompts_from_transcript
                        from agent import run_agent
                        from agent.tool_executor import set_current_user
                        
                        set_current_user(current_user)
                        
                        # Step 1: Extract prompts
                        ui.notify('📄 Extracting use cases from transcript...', type='info', position='top')
                        
                        # Run extraction in background
                        prompts = await asyncio.to_thread(
                            extract_prompts_from_transcript,
                            content,
                            verbose=False
                        )
                        
                        if not prompts:
                            ui.notify('No use cases found in transcript', type='warning')
                            return
                        
                        ui.notify(f'✓ Found {len(prompts)} use case(s). Creating them...', type='positive', position='top')
                        
                        # Step 2: Process each prompt with agent
                        successful = 0
                        
                        for i, prompt in enumerate(prompts, 1):
                            ui.notify(
                                f'Creating use case {i}/{len(prompts)}...', 
                                type='info',
                                position='top',
                                timeout=2000
                            )
                            
                            try:
                                # Run agent in background
                                await asyncio.to_thread(
                                    run_agent,
                                    prompt,
                                    conversation_history=None,
                                    verbose=True,
                                    max_rounds=10
                                )
                                successful += 1
                                
                            except Exception as e:
                                print(f"Error creating use case {i}: {e}")
                                # Continue with next use case
                        
                        # Final notification
                        if successful == len(prompts):
                            ui.notify(
                                f'🎉 Success! Created all {successful} use case(s)!',
                                type='positive',
                                position='top',
                                timeout=5000
                            )
                        else:
                            ui.notify(
                                f'⚠️ Created {successful}/{len(prompts)} use case(s). Check console for errors.',
                                type='warning',
                                position='top',
                                timeout=5000
                            )
                        
                        # Refresh table to show new use cases
                        refresh_use_case_table()
                        
                    except Exception as error:
                        ui.notify(f'Error processing transcript: {error}', type='negative')
                        import traceback
                        print(traceback.format_exc())

                
                ui.upload(
                    on_upload=handle_upload,
                    auto_upload=True,
                    label='Upload Transcript'
                ).props('flat color=white accept=.txt').tooltip('Upload workshop transcript (.txt)')
            
            # Logout button (OUTSIDE the if block, at the same level)
            def logout():
                app.storage.user['current_user'] = None
                app.storage.user['conversation_history'] = []
                ui.notify('Logged out successfully', type='info')
                ui.navigate.to('/')
            
            ui.button('Logout', on_click=logout, icon='logout').props('flat color=white')
    
    # === MAIN CONTENT AREA ===
    with ui.row().classes('w-full h-full gap-4 p-4'):
        
        # LEFT COLUMN - Chat (60%)
        with ui.column().classes('flex-[3] gap-2'):
            ui.label('Chat with AI Agent').classes('text-lg font-bold')
            
            # Chat messages container
            chat_container = ui.column().classes('flex-1 overflow-auto p-4 bg-gray-50 rounded max-h-[500px]')
            
            with chat_container:
                # Get conversation history
                if 'conversation_history' not in app.storage.user:
                    app.storage.user['conversation_history'] = []
                
                history = app.storage.user['conversation_history']
                
                # Display existing messages
                if not history:
                    # no history yet
                    ui.label('Start a conversation with the AI agent...').classes('text-gray-400 italic')

                else:

                    # fill history
                    for msg in history:
                        if msg['role'] == 'user':
                            # User message (right-aligned, blue)

                            with ui.row().classes('w-full mb-2'):
                                ui.label(msg['content']).classes(
                                    'bg-blue-500 text-white px-4 py-2 rounded-lg max-w-[80%] ml-auto'
                                )
                        else:
                            # Agent message (left-aligned, gray)
                            with ui.row().classes('justify-start mb-2'):
                                ui.label(msg['content']).classes(
                                    'bg-white px-4 py-2 rounded-lg border max-w-[80%] whitespace-pre-wrap'
                                )
            
            # Input area at bottom
            #with ui.row().classes('gap-2 items-end'):
            with ui.row().classes('w-full gap-2 items-end'):
                message_input = ui.input('Type your message...').classes('flex-1').props('outlined')
                
                # Enable pressing Enter to send (async)
                message_input.on('keydown.enter', lambda: send_message(message_input, chat_container))

                send_btn = ui.button('Send', icon='send', on_click=lambda: send_message(message_input, chat_container))
        
        # RIGHT COLUMN - Table (40%)
        with ui.column().classes('flex-[2] gap-2'):
            with ui.row().classes('w-full items-center justify-between'):
                ui.label('Use Cases').classes('text-lg font-bold')
                
                # Refresh button
                ui.button(icon='refresh', on_click=refresh_use_case_table).props('flat dense').tooltip('Refresh table')
            
            # Table
            from services import UseCaseService
            service = UseCaseService()
            
            try:
                use_cases = service.get_all_use_cases(current_user=current_user)
                
                # Table columns
                columns = [
                    {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left', 'sortable': True},
                    {'name': 'title', 'label': 'Title', 'field': 'title', 'align': 'left', 'sortable': True},
                    {'name': 'company', 'label': 'Company', 'field': 'company_name', 'align': 'left', 'sortable': True},
                    {'name': 'status', 'label': 'Status', 'field': 'status', 'align': 'left', 'sortable': True},
                    {'name': 'actions', 'label': '', 'field': 'id', 'align': 'center'},  # Actions column
                ]
                
                # Create table
                table = ui.table(
                    columns=columns,
                    rows=use_cases,
                    row_key='id',
                    pagination={'rowsPerPage': 10, 'sortBy': 'id'}
                ).classes('w-full')

                # Store table reference in global dict (can't use app.storage for UI elements)
                ui_elements['use_case_table'] = table
                
                # Add "View" button to each row
                table.add_slot('body-cell-actions', '''
                    <q-td :props="props">
                        <q-btn flat dense round icon="visibility" size="sm" color="primary" @click="$parent.$emit('view', props.row)" />
                    </q-td>
                ''')
                
                # Handle view button click
                table.on('view', lambda e: show_use_case_details(e.args, current_user))
                
            except Exception as e:
                ui.label(f'Error loading use cases: {e}').classes('text-red-500')

    # === CREATION FORMS SECTION (Below main content) ===
    # Only show to users with create permission
    if check_permission(current_user, 'create'):
        
        ui.separator().classes('my-6')
        
        ui.label('Create New Entities').classes('text-xl font-bold mb-4')
        
        with ui.row().classes('w-full gap-4'):
            # Left column - Simple entities
            with ui.column().classes('flex-1 gap-2'):
                
                # Create Industry
                with ui.expansion('Create Industry', icon='category').classes('w-full'):
                    with ui.column().classes('gap-2 p-2'):
                        industry_name = ui.input('Industry Name', placeholder='e.g., Automotive').classes('w-full')
                        
                        def create_industry():
                            try:
                                service.create_industry(industry_name.value, current_user=current_user)
                                ui.notify(f'Industry "{industry_name.value}" created!', type='positive', timeout=3000)
                                industry_name.value = ''
                                # No need to refresh page - industries don't affect the table
                            except Exception as e:
                                ui.notify(f'Error: {e}', type='negative')
                        
                        ui.button('Create Industry', on_click=create_industry, icon='add')
                
                # Create Company
                with ui.expansion('Create Company', icon='business').classes('w-full'):
                    with ui.column().classes('gap-2 p-2'):
                        company_name = ui.input('Company Name', placeholder='e.g., Tesla').classes('w-full')
                        
                        # Get industries for dropdown
                        industries = service.get_all_industries(current_user=current_user)
                        industry_options = {ind['id']: ind['name'] for ind in industries}
                        
                        company_industry = ui.select(
                            options=industry_options,
                            label='Industry'
                        ).classes('w-full')
                        
                        def create_company():
                            try:
                                if not company_industry.value:
                                    ui.notify('Please select an industry', type='warning')
                                    return
                                
                                service.create_company(
                                    company_name.value, 
                                    company_industry.value,
                                    current_user=current_user
                                )
                                ui.notify(f'Company "{company_name.value}" created!', type='positive')
                                company_name.value = ''
                            except Exception as e:
                                ui.notify(f'Error: {e}', type='negative')
                        
                        ui.button('Create Company', on_click=create_company, icon='add')
                
                # Create Person
                with ui.expansion('Create Person', icon='person_add').classes('w-full'):
                    with ui.column().classes('gap-2 p-2'):
                        person_name = ui.input('Person Name', placeholder='e.g., John Doe').classes('w-full')
                        person_role = ui.input('Role', placeholder='e.g., CTO').classes('w-full')
                        
                        # Get companies for dropdown
                        companies = service.get_all_companies(current_user=current_user)
                        company_options = {comp['id']: comp['name'] for comp in companies}
                        
                        person_company = ui.select(
                            options=company_options,
                            label='Company'
                        ).classes('w-full')
                        
                        def create_person():
                            try:
                                if not person_company.value:
                                    ui.notify('Please select a company', type='warning')
                                    return
                                
                                service.create_person(
                                    person_name.value,
                                    person_role.value,
                                    person_company.value,
                                    current_user=current_user
                                )
                                ui.notify(f'Person "{person_name.value}" created!', type='positive')
                                person_name.value = ''
                                person_role.value = ''
                            except Exception as e:
                                ui.notify(f'Error: {e}', type='negative')
                        
                        ui.button('Create Person', on_click=create_person, icon='add')
            
            # Right column - Use Case creation
            with ui.column().classes('flex-1 gap-2'):
                
                with ui.expansion('Create Use Case', icon='note_add').classes('w-full'):
                    with ui.column().classes('gap-2 p-2'):
                        uc_title = ui.input('Title', placeholder='Use Case Title').classes('w-full')
                        uc_desc = ui.textarea('Description', placeholder='Detailed description...').classes('w-full')
                        uc_benefit = ui.textarea('Expected Benefit', placeholder='Expected benefits...').classes('w-full')
                        
                        # Dropdowns
                        uc_company = ui.select(
                            options=company_options,
                            label='Company'
                        ).classes('w-full')
                        
                        uc_industry = ui.select(
                            options=industry_options,
                            label='Industry'
                        ).classes('w-full')
                        
                        status_options = ['new', 'in_review', 'approved', 'in_progress', 'completed']
                        uc_status = ui.select(
                            options=status_options,
                            value='new',
                            label='Status'
                        ).classes('w-full')
                        
                        def create_use_case_manual():
                            try:
                                if not uc_title.value:
                                    ui.notify('Title is required', type='warning')
                                    return
                                if not uc_company.value or not uc_industry.value:
                                    ui.notify('Company and Industry are required', type='warning')
                                    return
                                
                                service.create_use_case(
                                    title=uc_title.value,
                                    company_id=uc_company.value,
                                    industry_id=uc_industry.value,
                                    description=uc_desc.value,
                                    expected_benefit=uc_benefit.value,
                                    status=uc_status.value,
                                    current_user=current_user
                                )
                                ui.notify(f'Use case "{uc_title.value}" created!', type='positive')
                                uc_title.value = ''
                                uc_desc.value = ''
                                uc_benefit.value = ''
                                refresh_use_case_table()  # Refresh just the table
                            except Exception as e:
                                ui.notify(f'Error: {e}', type='negative')
                        
                        ui.button('Create Use Case', on_click=create_use_case_manual, icon='add').classes('w-full')

    # === USER MANAGEMENT SECTION (Admin only) ===
    if check_permission(current_user, 'manage_users'):
        
        ui.separator().classes('my-6')
        
        ui.label('User Management').classes('text-xl font-bold mb-4')
        
        # Get all users
        from services.user_service import UserService
        user_service = UserService()
        all_users = user_service.get_all_users()
        
        # User table
        user_columns = [
            {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left'},
            {'name': 'email', 'label': 'Email', 'field': 'email', 'align': 'left'},
            {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left'},
            {'name': 'role', 'label': 'Role', 'field': 'role', 'align': 'left'},
            {'name': 'actions', 'label': 'Actions', 'field': 'id', 'align': 'center'},
        ]
        
        user_table = ui.table(
            columns=user_columns,
            rows=all_users,
            row_key='id'
        ).classes('w-full')
        
        # Add role change buttons to each row
        user_table.add_slot('body-cell-actions', '''
            <q-td :props="props">
                <q-btn-group flat>
                    <q-btn flat dense size="sm" label="Reader" @click="$parent.$emit('set_role', {user_id: props.row.id, role: 'reader'})" :color="props.row.role === 'reader' ? 'primary' : 'grey'" />
                    <q-btn flat dense size="sm" label="Maintainer" @click="$parent.$emit('set_role', {user_id: props.row.id, role: 'maintainer'})" :color="props.row.role === 'maintainer' ? 'primary' : 'grey'" />
                    <q-btn flat dense size="sm" label="Admin" @click="$parent.$emit('set_role', {user_id: props.row.id, role: 'admin'})" :color="props.row.role === 'admin' ? 'primary' : 'grey'" />
                </q-btn-group>
            </q-td>
        ''')
        
        # Handle role change
        def change_user_role(e):
            user_id = e.args['user_id']
            new_role = e.args['role']
            
            try:
                # Update user role in database
                from models.base import SessionLocal
                from models.user import User
                
                db = SessionLocal()
                try:
                    user = db.query(User).filter(User.id == user_id).first()
                    if user:
                        old_role = user.role
                        user.role = new_role
                        db.commit()
                        ui.notify(f'User {user.email} role changed from {old_role} to {new_role}', type='positive')
                        ui.navigate.to('/')  # Refresh
                    else:
                        ui.notify('User not found', type='negative')
                finally:
                    db.close()
                    
            except Exception as error:
                ui.notify(f'Error changing role: {error}', type='negative')
        
        user_table.on('set_role', change_user_role)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title='UseCase Manager', 
        port=8080, 
        reload=False, 
        storage_secret='use-case-manager-secret-2025'
    )
