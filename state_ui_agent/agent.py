# agent.py - Ecommerce State Management
from pydantic import BaseModel
from typing import List, Dict, Optional

class Product(BaseModel):
    id: str
    title: str
    price: int
    image: str

class CartItem(BaseModel):
    id: str
    title: str
    price: int
    qty: int

class UIState(BaseModel):
    current_page: str = "home"
    last_search: str = ""
    cart: List[CartItem] = []

    def snapshot(self):
        return {
            "current_page": self.current_page,
            "last_search": self.last_search or "None",
            "cart_count": sum(item.qty for item in self.cart),
            "cart_items": [item.dict() for item in self.cart],
        }

# Enhanced product catalog
PRODUCT_CATALOG = [
    # Laptops
    Product(id="laptop-1", title="Basic Laptop", price=45000, image="https://via.placeholder.com/200x150/4CAF50/white?text=Basic+Laptop"),
    Product(id="laptop-2", title="Gaming Laptop", price=75000, image="https://via.placeholder.com/200x150/FF5722/white?text=Gaming+Laptop"),
    Product(id="laptop-3", title="Pro Laptop", price=95000, image="https://via.placeholder.com/200x150/2196F3/white?text=Pro+Laptop"),
    
    # Phones
    Product(id="phone-1", title="Basic Phone", price=15000, image="https://via.placeholder.com/200x150/9C27B0/white?text=Basic+Phone"),
    Product(id="phone-2", title="Pro Phone", price=35000, image="https://via.placeholder.com/200x150/E91E63/white?text=Pro+Phone"),
    Product(id="phone-3", title="Flagship Phone", price=55000, image="https://via.placeholder.com/200x150/3F51B5/white?text=Flagship+Phone"),
    
    # Headphones
    Product(id="headphone-1", title="Wired Headphones", price=2000, image="https://via.placeholder.com/200x150/795548/white?text=Wired"),
    Product(id="headphone-2", title="Wireless Headphones", price=5000, image="https://via.placeholder.com/200x150/607D8B/white?text=Wireless"),
    Product(id="headphone-3", title="Premium Headphones", price=8000, image="https://via.placeholder.com/200x150/009688/white?text=Premium"),
    
    # Tablets  
    Product(id="tablet-1", title="Basic Tablet", price=25000, image="https://via.placeholder.com/200x150/FF9800/white?text=Basic+Tablet"),
    Product(id="tablet-2", title="Pro Tablet", price=45000, image="https://via.placeholder.com/200x150/F44336/white?text=Pro+Tablet"),
    
    # Accessories
    Product(id="accessory-1", title="Wireless Mouse", price=1500, image="https://via.placeholder.com/200x150/8BC34A/white?text=Mouse"),
    Product(id="accessory-2", title="Keyboard", price=3000, image="https://via.placeholder.com/200x150/CDDC39/black?text=Keyboard"),
    Product(id="accessory-3", title="Webcam", price=4000, image="https://via.placeholder.com/200x150/FFC107/black?text=Webcam"),
]

def get_all_products() -> List[Product]:
    """Get all available products"""
    return PRODUCT_CATALOG

def do_search(state: UIState, query: str) -> List[Product]:
    """Search products by query"""
    state.current_page = "search_results"
    state.last_search = query or ""
    
    if not query:
        return PRODUCT_CATALOG
    
    query_lower = query.lower()
    filtered_products = []
    
    for product in PRODUCT_CATALOG:
        if (query_lower in product.title.lower() or 
            query_lower in product.id.lower() or
            any(keyword in product.title.lower() for keyword in query_lower.split())):
            filtered_products.append(product)
    
    return filtered_products if filtered_products else PRODUCT_CATALOG

def find_cart_item(state: UIState, pid: str) -> Optional[CartItem]:
    """Find item in cart by product ID"""
    for item in state.cart:
        if item.id == pid:
            return item
    return None

def add_to_cart(state: UIState, product: Dict):
    """Add product to cart or increment quantity if exists"""
    existing = find_cart_item(state, product["id"])
    if existing:
        existing.qty += 1
    else:
        state.cart.append(CartItem(
            id=product["id"], 
            title=product["title"], 
            price=int(product["price"]), 
            qty=1
        ))

def remove_from_cart(state: UIState, pid: str):
    """Remove one item or decrease quantity"""
    existing = find_cart_item(state, pid)
    if not existing:
        return
    
    existing.qty -= 1
    if existing.qty <= 0:
        state.cart = [item for item in state.cart if item.id != pid]

def remove_all_from_cart(state: UIState, pid: str):
    """Remove all items of this type from cart"""
    state.cart = [item for item in state.cart if item.id != pid]

def cart_subtotal(state: UIState) -> int:
    """Calculate total cart value"""
    return sum(item.price * item.qty for item in state.cart)

def checkout(state: UIState) -> int:
    """Process checkout and clear cart"""
    total = cart_subtotal(state)
    state.cart = []
    state.current_page = "checkout_success"
    return total