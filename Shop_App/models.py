from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

# ==========================================
# 1. AUTHENTICATION & USER MANAGEMENT
# ==========================================

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('shopkeeper', 'Shopkeeper'),
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='shopkeeper')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ==========================================
# 2. MASTER DATA CONFIGURATIONS
# ==========================================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True, help_text="Active/Inactive")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.short_name})"


# ==========================================
# 3. SUPPLIER & CUSTOMER MANAGEMENT
# ==========================================

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.company_name if self.company_name else self.name


class Customer(models.Model):
    customer_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)
    total_purchase = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_return = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.name} ({self.mobile})"


# ==========================================
# 4. PRODUCT MANAGEMENT
# ==========================================

class Product(models.Model):
    product_code = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    minimum_stock = models.IntegerField(default=5)
    current_stock = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ==========================================
# 5. PURCHASING MODULE
# ==========================================

class Purchase(models.Model):
    invoice_no = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchases')
    purchase_date = models.DateField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *edit, **kwargs):
        # Programmatically calculate due amount before saving
        self.due_amount = self.total_amount - self.paid_amount
        super().save(*edit, **kwargs)

    def __str__(self):
        return f"PO-{self.invoice_no}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchase_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.purchase_price
        super().save(*args, **kwargs)


# ==========================================
# 6. SALES & POS MODULE
# ==========================================

class Sale(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile_banking', 'Mobile Banking'),
    )
    invoice_no = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales', blank=True, null=True)
    shopkeeper = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')

    def save(self, *args, **kwargs):
        self.due_amount = self.grand_total - self.paid_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"INV-{self.invoice_no}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sale_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Stored for historical profit reporting")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


# ==========================================
# 7. RETURNS & INVENTORY TRACKING
# ==========================================

class ProductReturn(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    return_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    returned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return for {self.sale.invoice_no}"


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('adjustment', 'Manual Adjustment'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    transaction_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    previous_stock = models.IntegerField()
    current_stock = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type} ({self.quantity})"


# ==========================================
# 8. EXPENSES
# ==========================================

class Expense(models.Model):
    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - ${self.amount}"