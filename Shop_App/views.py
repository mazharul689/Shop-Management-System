from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .decorators import allowed_roles

# ==========================================
# 1. USER AUTHENTICATION WORKFLOWS
# ==========================================

def register_user(request):
    """
    View for Administrative profiles to register new system users.
    Maps parameters cleanly into the unified authform template context.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created successfully for {user.username}!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    # Context variables mapped precisely to your template layout placeholders
    context = {
        'form': form,
        'title': 'Registration Form',
        'h2': 'Create an Account',
        'p': 'Register new administrators or shopkeepers to manage daily operations.',
        'btn': 'Register User',
        'a_t': 'Already have an account?',
        'a_b': 'Login here',
        'url': '/login/'  # Resolves to your standard login path
    }
    
    return render(request, 'auth/register.html', context)


def login_user(request):
    """
    Universal processing checkpoint for all user logins.
    Injects custom parameters into your shared template structure.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
        
    # Context variables tailored for user entry validation
    context = {
        'form': form,
        'title': 'Login Form',
        'h2': 'Welcome Back',
        'p': 'Please log in to access your role-based dashboard application workspace.',
        'btn': 'Sign In',
        'a_t': 'Need to add a new team member?',
        'a_b': 'Register here',
        'url': '/register/'  # Resolves to your user creation path
    }
        
    return render(request, 'auth/login.html', context)


def logout_user(request):
    """ Clears active sessions securely """
    logout(request)
    messages.info(request, "You have logged out successfully.")
    return redirect('login')


# ==========================================
# 2. CORE ROUTING & SECURED DASHBOARDS
# ==========================================

@login_required(login_url='login')
def dashboard_router(request):
    """
    Acts as an internal traffic manager immediately upon authorization.
    Protects user experience by mapping roles to explicitly restricted paths.
    """
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'shopkeeper':
        return redirect('shopkeeper_dashboard')
    else:
        messages.error(request, "Unidentified role configuration.")
        return redirect('login')


@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['admin'])
def admin_dashboard(request):
    """
    Administrative Command Workspace.
    Protected strictly against non-admin escalation vectors.
    """
    # Analytics data references will integrate here during Phase 7 (Reports)
    return render(request, 'admin_workspace/dashboard.html')


@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['shopkeeper'])
def shopkeeper_dashboard(request):
    """
    Shopkeeper Point-of-Sale Hub.
    Protected strictly against administrative operational views.
    """
    # Live transaction feeds will integrate here during Phase 5 (Sales/POS)
    return render(request, 'shopkeeper_workspace/dashboard.html')