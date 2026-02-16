from nicegui import ui, app
from services.user_service import UserService

# init user service
user_service = UserService()

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
            
            # Logout button
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
            
            # Chat container (placeholder)
            with ui.card().classes('flex-1 p-4'):
                ui.label('Chat will go here').classes('text-gray-500')
        
        # RIGHT COLUMN - Table (40%)
        with ui.column().classes('flex-[2] gap-2'):
            ui.label('Use Cases').classes('text-lg font-bold')
            
            # Table container (placeholder)
            with ui.card().classes('flex-1 p-4'):
                ui.label('Table will go here').classes('text-gray-500')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title='UseCase Manager', 
        port=8080, 
        reload=False, 
        storage_secret='use-case-manager-secret-2025'
    )
