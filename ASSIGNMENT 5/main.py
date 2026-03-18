from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

# Data 

class OrderRequest(BaseModel):
    customer_name: str
    product_id: int
    quantity: int

# database 

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"}
]

orders = []

# Create Order

@app.post("/orders")
def create_order(order: OrderRequest):

    order_id = len(orders) + 1

    new_order = {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "product_id": order.product_id,
        "quantity": order.quantity
    }

    orders.append(new_order)

    return {
        "message": "Order placed successfully",
        "order": new_order
    }

# Q1 — Search Products

@app.get("/products/search")
def search_products(keyword: str):

    results = [
        product for product in products
        if keyword.lower() in product["name"].lower()
    ]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(results),
        "products": results
    }

# Q2 — Sort Products

@app.get("/products/sort")
def sort_products(
    sort_by: str = "price",
    order: str = "asc"
):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    sorted_products = sorted(
        products,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }

# Q3 — Pagination

@app.get("/products/page")
def paginate_products(
    page: int = 1,
    limit: int = 2
):

    start = (page - 1) * limit
    end = start + limit

    paginated_products = products[start:end]

    total_products = len(products)
    total_pages = (total_products + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_products": total_products,
        "total_pages": total_pages,
        "products": paginated_products
    }

# Q4 — Search Orders

@app.get("/orders/search")
def search_orders(customer_name: str):

    results = [
        order for order in orders
        if customer_name.lower() in order["customer_name"].lower()
    ]

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }

# Q5 — Sort by Category then Price

@app.get("/products/sort-by-category")
def sort_by_category():

    sorted_products = sorted(
        products,
        key=lambda x: (x["category"].lower(), x["price"])
    )

    return {
        "message": "Products sorted by category then price",
        "products": sorted_products
    }

# Q6 — Browse Products

@app.get("/products/browse")
def browse_products(
    keyword: str | None = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    result = products

    # Search
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # Sort
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    result = sorted(
        result,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    # Pagination
    total_found = len(result)

    start = (page - 1) * limit
    end = start + limit

    paginated_products = result[start:end]

    total_pages = (total_found + limit - 1) // limit

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paginated_products
    }
@app.get("/orders/page")
def paginate_orders(
    page: int = 1,
    limit: int = 3
):

    start = (page - 1) * limit
    end = start + limit

    paginated_orders = orders[start:end]

    total_orders = len(orders)
    total_pages = (total_orders + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_orders": total_orders,
        "total_pages": total_pages,
        "orders": paginated_orders
    }



# Get Product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    return {"error": "Product not found"}
