from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .decorators import allowed_roles
from django.db import transaction

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


# --- Category MANAGEMENT ---
@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['admin'])
def category_list(request):
    """Handles both the display listing and the creation of inventory categories"""
    categories = Category.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm()
        
    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'admin_workspace/category_list.html', context)


# --- BRAND MANAGEMENT ---
@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['admin'])
def brand_list(request):
    brands = Brand.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand added successfully!")
            return redirect('brand_list')
    else:
        form = BrandForm()
    return render(request, 'admin_workspace/brand_list.html', {'brands': brands, 'form': form})

# --- UNIT MANAGEMENT ---
@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['admin'])
def unit_list(request):
    units = Unit.objects.all()
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Unit configuration added successfully!")
            return redirect('unit_list')
    else:
        form = UnitForm()
    return render(request, 'admin_workspace/unit_list.html', {'units': units, 'form': form})

# --- PRODUCT MANAGEMENT ---
@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['admin'])
def product_list(request):
    products = Product.objects.select_related('category', 'brand', 'unit').all().order_by('name')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # request.FILES handling is required for images
        if form.is_valid():
            form.save()
            messages.success(request, "Product master entry saved!")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'admin_workspace/product_list.html', {'products': products, 'form': form})

# --- SUPPLIEER MANAGEMENT ---
@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['admin'])
def supplier_list(request):
    """Manages secure supplier records creation and procurement ledger logging"""
    suppliers = Supplier.objects.all().order_by('company_name')
    
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier record registered successfully!")
            return redirect('supplier_list')
    else:
        form = SupplierForm()
        
    context = {
        'suppliers': suppliers,
        'form': form
    }
    return render(request, 'admin_workspace/supplier_list.html', context)

@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['admin'])
def purchase_list(request):
    """Lists history of wholesale transactions recorded in the application catalog"""
    purchases = Purchase.objects.select_related('supplier').all().order_by('-purchase_date', '-id')
    return render(request, 'admin_workspace/purchase_list.html', {'purchases': purchases})


@login_required(login_url='login')
@allowed_roles(allowed_roles_list=['admin'])
def purchase_create(request):
    """Handles master-detail inline formsets to commit bulk goods entries and adjust stock levels"""
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            try:
                # Open atomic thread block to enforce system data protection
                with transaction.atomic():
                    # 1. Temporarily hold the header instance to calculate sums
                    purchase = form.save(commit=False)
                    purchase.subtotal = 0
                    purchase.total_amount = 0
                    purchase.due_amount = 0
                    purchase.save()  # Requires an primary ID for item relations mapping
                    
                    # 2. Process formset inline row items
                    items = formset.save(commit=False)
                    subtotal_accumulator = 0
                    
                    for item in items:
                        item.purchase = purchase
                        # Compute item total price
                        item.total_price = item.quantity * item.purchase_price
                        item.save()
                        
                        subtotal_accumulator += item.total_price
                        
                        # 3. AUTO-INCREMENT PRODUCT LOGISTICS & AUDIT TRAIL LOGGING
                        product = item.product
                        previous_stock_level = product.current_stock
                        
                        # Increment product physical stock values
                        product.current_stock += item.quantity
                        product.save()
                        
                        # Record history instance in audit ledger
                        StockMovement.objects.create(
                            product=product,
                            transaction_type='PURCHASE',
                            quantity=item.quantity,
                            previous_stock=previous_stock_level,
                            current_stock=product.current_stock
                        )
                    
                    # 4. RE-CALCULATE AND COMMIT MASTER INVOICE LEDGER AMOUNTS
                    purchase.subtotal = subtotal_accumulator
                    discount_val = form.cleaned_data.get('discount', 0)
                    paid_val = form.cleaned_data.get('paid_amount', 0)
                    
                    purchase.total_amount = max(0, purchase.subtotal - discount_val)
                    purchase.due_amount = max(0, purchase.total_amount - paid_val)
                    purchase.save()
                    
                    # 5. ADJUST LIABILITIES BALANCE ON THE ASSOCIATED SUPPLIER RECORD
                    supplier = purchase.supplier
                    supplier.due_amount += purchase.due_amount
                    supplier.save()
                    
                messages.success(request, f"Purchase Invoice {purchase.invoice_no} processed. Stock updated successfully!")
                return redirect('purchase_list')
                
            except Exception as e:
                messages.error(request, f"An internal transaction failure occurred: {str(e)}")
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet()
        
    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'admin_workspace/purchase_create.html', context)