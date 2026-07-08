from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import inlineformset_factory
from .models import *

class CustomUserCreationForm(UserCreationForm):
    # Field definitions with precise clean CSS classes
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.com'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +123456789'}))
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique username'}),
            'role': forms.Select(attrs={'class': 'form-select'}), # Corrected to Bootstrap 5 form-select
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Explicitly style the internal security fields inherited from UserCreationForm
        if 'password1' in self.fields:
            self.fields['password1'].widget = forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter secure password'
            })
            self.fields['password1'].help_text = "" # Clears long Django text blocks safely
            self.fields['password1'].label = "Password"
            
        if 'password2' in self.fields:
            self.fields['password2'].widget = forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Repeat password'
            })
            self.fields['password2'].help_text = ""
            self.fields['password2'].label = "Confirm Password"

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Password'
    }))

class CategoryForm(forms.ModelForm):
    """Form configuration for inventory asset categorizations"""
    class Meta:
        model = Category
        fields = ['name', 'description', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Electronics, Groceries'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter category description...', 
                'rows': 3
            }),
            'status': forms.Select(choices=[(True, 'Active'), (False, 'Inactive')], attrs={
                'class': 'form-select'
            })
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Sony, Nestlé'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter brand profile...', 'rows': 3}),
            'status': forms.Select(choices=[(True, 'Active'), (False, 'Inactive')], attrs={'class': 'form-select'})
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'short_name', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Kilogram, Piece'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., kg, pc, box'}),
            'status': forms.Select(choices=[(True, 'Active'), (False, 'Inactive')], attrs={'class': 'form-select'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_code', 'barcode', 'category', 'brand', 'unit', 
            'name', 'description', 'image', 'purchase_price', 
            'selling_price', 'minimum_stock', 'status'
        ]
        widgets = {
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU-XXXX'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scan or enter barcode'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product notes...', 'rows': 2}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'minimum_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5'}),
            'status': forms.Select(choices=[(True, 'Active'), (False, 'Inactive')], attrs={'class': 'form-select'})
        }

class SupplierForm(forms.ModelForm):
    """Form configuration for vendor profiles and liability accounts tracking"""
    class Meta:
        model = Supplier
        fields = ['name', 'mobile', 'email', 'address', 'company_name', 'due_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'vendor@company.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Physical warehouse address'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Official corporate entity name'}),
            'due_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Initial opening balance due'}),
        }

class PurchaseForm(forms.ModelForm):
    """Form configuration for recording the main invoice receipt header from a supplier"""
    class Meta:
        model = Purchase
        fields = ['invoice_no', 'supplier', 'purchase_date', 'discount', 'paid_amount']
        widgets = {
            'invoice_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INV-XXXXXX'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control calculation-trigger', 'step': '0.01', 'value': '0.00'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control calculation-trigger', 'step': '0.01', 'value': '0.00'}),
        }

class PurchaseItemForm(forms.ModelForm):
    """Form configuration for a single product entry line row inside a purchase order receipt"""
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'purchase_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select product-selector'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity-field', 'min': '1', 'placeholder': 'Qty'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control price-field', 'step': '0.01', 'placeholder': 'Cost'}),
        }

# Generate an interactive Inline Formset for mapping dynamic lines onto a single Purchase master instance
PurchaseItemFormSet = inlineformset_factory(
    Purchase, 
    PurchaseItem, 
    form=PurchaseItemForm,
    extra=3,             # Renders 3 blank line rows to fill out by default
    can_delete=True      # Allows operators to remove excess lines
)