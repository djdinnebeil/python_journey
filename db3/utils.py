from crud import get_products_paginated

def view_all_products(per_page=10):
    page = 1
    while True:
        products = get_products_paginated(page=page, per_page=per_page)
        if not products:
            break  # No more products to show
        print(f'Page {page}:')
        for product in products:
            print(product)
        page += 1