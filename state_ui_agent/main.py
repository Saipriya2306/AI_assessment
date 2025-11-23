# Enhanced Ecommerce AI Assistant - main.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fasthtml.common import *
from agent import UIState, do_search, add_to_cart, remove_from_cart, remove_all_from_cart, checkout, cart_subtotal, get_all_products
from ui import home_page, search_page, cart_page, checkout_page
from ai_assistant import process_ai_request
import asyncio

# Global state for demo
state = UIState()

# FastHTML app with custom CSS
css = """
    body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        margin: 0; 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    .header { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; 
        padding: 1.5rem; 
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .container { 
        max-width: 1200px; 
        margin: 0 auto; 
        padding: 30px 20px; 
    }
    .product-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); 
        gap: 25px; 
        margin: 30px 0; 
    }
    .product-card { 
        background: white; 
        border-radius: 15px; 
        box-shadow: 0 8px 25px rgba(0,0,0,0.1); 
        overflow: hidden; 
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
        position: relative;
    }
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    .product-card:hover { 
        transform: translateY(-8px); 
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    .product-image { 
        width: 100%; 
        height: 220px; 
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        color: #64748b;
    }
    .product-info { padding: 25px; }
    .product-title { 
        font-size: 1.3rem; 
        font-weight: 600; 
        margin-bottom: 12px; 
        color: #1a202c;
        line-height: 1.4;
    }
    .product-price { 
        font-size: 1.4rem; 
        color: #2b6cb0; 
        font-weight: 700; 
        margin-bottom: 15px; 
    }
    .product-actions { display: flex; gap: 10px; align-items: center; }
    .btn { 
        padding: 12px 20px; 
        border: none; 
        border-radius: 8px; 
        cursor: pointer; 
        font-weight: 600; 
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    .btn-primary { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; 
    }
    .btn-primary:hover { 
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    .btn-secondary { background: #f8f9fa; color: #6c757d; border: 1px solid #dee2e6; }
    .btn-danger { background: #dc3545; color: white; }
    .search-bar { width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 16px; }
    .chat-container { 
        position: fixed; 
        bottom: 90px; 
        right: 20px; 
        width: 380px; 
        max-height: 500px; 
        background: white; 
        border-radius: 15px; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.2); 
        z-index: 1000;
        border: 1px solid #e2e8f0;
        display: flex;
        flex-direction: column;
    }
    .chat-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 12px 12px 0 0; }
    .chat-messages { 
        flex: 1; 
        max-height: 300px; 
        padding: 15px; 
        overflow-y: auto; 
        border-bottom: 1px solid #e2e8f0;
    }
    .chat-input { padding: 15px; }
    .message { 
        margin-bottom: 12px; 
        padding: 10px 15px; 
        border-radius: 12px;
        max-width: 85%;
        word-wrap: break-word;
    }
    .message.user { 
        background: linear-gradient(135deg, #e6f3ff, #cce7ff); 
        margin-left: auto; 
        text-align: right;
        color: #2b6cb0;
    }
    .message.bot { 
        background: #f8fafc; 
        margin-right: auto;
        border-left: 3px solid #667eea;
        color: #2d3748;
    }
    .cart-badge { background: #dc3545; color: white; border-radius: 50%; padding: 2px 6px; font-size: 12px; margin-left: 5px; }
    .quantity-display { font-size: 14px; color: #28a745; font-weight: bold; }
    #chat-toggle { cursor: pointer !important; user-select: none; -webkit-user-select: none; }
    #chat-toggle:hover { background: #5a6fd8 !important; transform: translateY(-2px); }
    .chat-container { border: 1px solid #ddd; }
    .message { white-space: pre-wrap; word-wrap: break-word; }
    
    /* AI Assistant Drawer Styles */
    .ai-drawer {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 380px;
        max-height: 500px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        z-index: 1000;
        border: 1px solid #e2e8f0;
        display: none;
        flex-direction: column;
        transform: translateY(20px);
        opacity: 0;
        transition: all 0.3s ease;
    }
    .ai-drawer.open {
        display: flex;
        transform: translateY(0);
        opacity: 1;
    }
    .ai-drawer-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.1);
        z-index: 999;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        pointer-events: none;
    }
    .ai-drawer-overlay.active {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
    }
"""

app, rt = fast_app(hdrs=[Style(css)])

@rt("/")
def home():
    products = get_all_products()
    cart_count = sum(item.qty for item in state.cart)
    return home_page(products, cart_count, state.cart)

@rt("/search")
async def search(req):
    q = req.query_params.get("q", "")
    products = do_search(state, q) if q else get_all_products()
    cart_count = sum(item.qty for item in state.cart)
    return search_page(products, q, state.cart, cart_count)

@rt("/add")
async def add(req):
    try:
        form = await req.form()
        pid = form.get("id")
        title = form.get("title")
        price = form.get("price")
        
        if not (pid and title and price):
            return Div("Error: Missing product information", 
                      A("Back", href="/", cls="btn btn-secondary"))
            
        product = {"id": pid, "title": title, "price": int(price)}
        add_to_cart(state, product)
        
        # Return updated page or redirect
        return RedirectResponse("/", status_code=303)
        
    except Exception as e:
        return Div(f"Error: {str(e)}", A("Back", href="/", cls="btn btn-secondary"))

@rt("/remove")
async def remove(req):
    try:
        form = await req.form()
        pid = form.get("id")
        if pid:
            remove_from_cart(state, pid)
        return RedirectResponse("/cart", status_code=303)
    except Exception as e:
        return Div(f"Error: {str(e)}", A("Back", href="/cart", cls="btn btn-secondary"))

@rt("/cart")
def show_cart():
    subtotal = cart_subtotal(state)
    cart_count = sum(item.qty for item in state.cart)
    return cart_page(state.cart, subtotal, cart_count)

@rt("/checkout")
async def do_checkout():
    total = checkout(state)
    return checkout_page(total)

@rt("/clear-cart", methods=["GET", "POST"])
async def clear_cart():
    state.cart = []
    return RedirectResponse("/", status_code=303)

@rt("/ai-chat", methods=["POST"])
async def ai_chat(req):
    try:
        form = await req.form()
        user_input = form.get("message", "").strip()
        
        if not user_input:
            return {"error": "Empty message"}
            
        # Get available products for AI context
        available_products = [
            {"id": p.id, "title": p.title, "price": p.price} 
            for p in get_all_products()
        ]
        
        # Process with AI assistant
        ai_result = await process_ai_request(user_input, state, available_products)
        
        # Execute the action
        response_message = ai_result.get("ai_response", "I understand your request.")
        
        if ai_result["action"] == "add":
            product_id = ai_result.get("product_id")
            if product_id:
                # Find and add product
                for product in available_products:
                    if product["id"] == product_id:
                        add_to_cart(state, product)
                        response_message = f"✅ Added {product['title']} to your cart!"
                        break
        
        elif ai_result["action"] == "remove":
            product_id = ai_result.get("product_id")
            if product_id:
                # Find the item in cart before removing
                item_to_remove = None
                for item in state.cart:
                    if item.id == product_id:
                        item_to_remove = item
                        break
                
                if item_to_remove:
                    remove_from_cart(state, product_id)
                    response_message = f"✅ Removed {item_to_remove.title} from your cart!"
                else:
                    response_message = "❌ That item is not in your cart."
            else:
                response_message = "❌ Please specify which item to remove."
        
        elif ai_result["action"] == "remove_all":
            product_id = ai_result.get("product_id")
            if product_id:
                # Find the item in cart before removing
                item_to_remove = None
                for item in state.cart:
                    if item.id == product_id:
                        item_to_remove = item
                        break
                
                if item_to_remove:
                    remove_all_from_cart(state, product_id)
                    response_message = f"✅ Completely removed all {item_to_remove.title} from your cart!"
                else:
                    response_message = "❌ That item is not in your cart."
            else:
                response_message = "Please specify which item you'd like to remove from your cart."
        
        elif ai_result["action"] == "clear_cart":
            state.cart = []
            response_message = "🗑️ Cart cleared successfully!"
            
        elif ai_result["action"] == "view_cart":
            if state.cart:
                cart_items = [f"• {item.title} (₹{item.price:,}) x{item.qty}" for item in state.cart]
                total = cart_subtotal(state)
                response_message = f"🛒 Your cart:\n" + "\n".join(cart_items) + f"\n\n💰 Total: ₹{total:,}"
            else:
                response_message = "🛒 Your cart is empty."
        
        return {
            "response": response_message,
            "cart_count": sum(item.qty for item in state.cart)
        }
        
    except Exception as e:
        return {"error": f"Sorry, I couldn't process that: {str(e)}"}

@rt("/chat.js")
def chat_js():
    js_content = """
    let chatOpen = false;
    
    function toggleChat() {
        console.log('Toggle chat clicked');
        const chatContainer = document.getElementById('chat-container');
        const toggleBtn = document.getElementById('chat-toggle');
        
        if (!chatContainer || !toggleBtn) {
            console.error('Chat elements not found');
            return;
        }
        
        if (chatOpen) {
            chatContainer.style.display = 'none';
            toggleBtn.innerHTML = '💬 AI Assistant';
            chatOpen = false;
        } else {
            chatContainer.style.display = 'block';
            toggleBtn.innerHTML = '✖️ Close Chat';
            chatOpen = true;
        }
    }
    
    async function sendMessage() {
        const input = document.getElementById('chat-input');
        const messages = document.getElementById('chat-messages');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        const userMsg = document.createElement('div');
        userMsg.className = 'message user';
        userMsg.textContent = message;
        messages.appendChild(userMsg);
        
        input.value = '';
        messages.scrollTop = messages.scrollHeight;
        
        // Send to AI
        try {
            const formData = new FormData();
            formData.append('message', message);
            
            const response = await fetch('/ai-chat', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            // Add bot response
            const botMsg = document.createElement('div');
            botMsg.className = 'message bot';
            botMsg.textContent = result.response || result.error || 'Sorry, something went wrong.';
            messages.appendChild(botMsg);
            
            // Update cart count if provided
            if (result.cart_count !== undefined) {
                const badge = document.querySelector('.cart-badge');
                if (badge) {
                    badge.textContent = result.cart_count;
                }
                // Optionally refresh the page to show updated cart
                setTimeout(() => location.reload(), 1000);
            }
            
        } catch (error) {
            const errorMsg = document.createElement('div');
            errorMsg.className = 'message bot';
            errorMsg.textContent = 'Sorry, I had trouble processing that request.';
            messages.appendChild(errorMsg);
        }
        
        messages.scrollTop = messages.scrollHeight;
    }
    
    // Send message on Enter key
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM loaded, setting up event listeners');
        
        const input = document.getElementById('chat-input');
        if (input) {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        }
        
        // Ensure toggle button works
        const toggleBtn = document.getElementById('chat-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleChat);
        }
    });
    """
    return Response(js_content, media_type="application/javascript")

if __name__ == "__main__":
    serve()  # Default: http://127.0.0.1:5001
