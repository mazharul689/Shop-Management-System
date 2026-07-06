def dynamic_sidebar_menu(request):
    """
    Dynamically generates the sidebar menu structure based on 
    the active session user's role configuration.
    """
    # Fallback to an empty list if the visitor is not logged in
    if not request.user.is_authenticated:
        return {'sidebar_menu': []}
        
    user_role = request.user.role
    
    # 1. Define menus available exclusively to the Admin
    admin_menus = [
        {
            'title': 'Dashboard',
            'icon': 'bi-speedometer2',
            'url_name': 'admin_dashboard',
            'submenus': []
        },
        {
            'title': 'Master Configuration',
            'icon': 'bi-sliders',
            'url_name': None,
            'submenus': [
                {'title': 'Category Management', 'url_name': 'category_list', 'icon': 'bi-tags'},
                {'title': 'Brand Management', 'url_name': 'brand_list', 'icon': 'bi-bookmark-star'},
                {'title': 'Unit Management', 'url_name': 'unit_list', 'icon': 'bi-rulers'},
                {'title': 'Product Master', 'url_name': 'product_list', 'icon': 'bi-box-seam'},
            ]
        },
        {
            'title': 'Operations',
            'icon': 'bi-shuffle',
            'url_name': None,
            'submenus': [
                {'title': 'Suppliers', 'url_name': 'supplier_list', 'icon': 'bi-truck'},
                {'title': 'Purchases', 'url_name': 'purchase_list', 'icon': 'bi-cart-check'},
                {'title': 'Expenses', 'url_name': 'expense_list', 'icon': 'bi-wallet2'},
            ]
        },
    ]

    # 2. Define menus available to the Shopkeeper
    shopkeeper_menus = [
        {
            'title': 'POS Terminal',
            'icon': 'bi-cart-dash',
            'url_name': 'shopkeeper_dashboard',
            'submenus': []
        },
        {
            'title': 'Customer & Sales',
            'icon': 'bi-people',
            'url_name': None,
            'submenus': [
                {'title': 'Manage Customers', 'url_name': 'customer_list', 'icon': 'bi-person-vcard'},
                {'title': 'Sales History', 'url_name': 'sales_history', 'icon': 'bi-clock-history'},
            ]
        },
    ]

    # Assign final template rendering variable depending on role verification
    if user_role == 'admin':
        active_menu = admin_menus
    elif user_role == 'shopkeeper':
        active_menu = shopkeeper_menus
    else:
        active_menu = []

    return {
        'sidebar_menu': active_menu
    }