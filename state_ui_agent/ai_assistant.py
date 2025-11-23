# ai_assistant.py - AI Assistant for Ecommerce
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any
import json

class CartCommand(BaseModel):
    action: str  # "add", "remove", "view", "clear", "search"
    product_id: str = ""
    product_name: str = ""
    quantity: int = 1

# AI Assistant Agent
ecommerce_agent = Agent(
    "google-gla:gemini-2.5-flash",
    system_prompt="""You are an intelligent ecommerce shopping assistant. Help users with:

1. ADDING ITEMS: When users want to add items, extract product details
2. REMOVING ITEMS: When users want to remove items from cart
3. VIEW CART: When users ask about cart contents or totals
4. SEARCH PRODUCTS: When users search for products
5. RECOMMENDATIONS: Suggest products based on user needs

Always respond in a helpful, friendly tone. Parse user requests and provide structured commands for cart operations.

For adding items, try to match user requests to available products:
- laptops (laptop-1: Basic Laptop ₹45000, laptop-2: Gaming Laptop ₹75000, laptop-3: Pro Laptop ₹95000)
- phones (phone-1: Basic Phone ₹15000, phone-2: Pro Phone ₹35000, phone-3: Flagship Phone ₹55000)  
- headphones (headphone-1: Wired ₹2000, headphone-2: Wireless ₹5000, headphone-3: Premium ₹8000)

When users ask to add items, respond with the action and help them complete their request.
"""
)

def parse_user_request(user_input: str, available_products: List[Dict], current_cart: List[Dict]) -> Dict[str, Any]:
    """
    Parse user input and determine what action to take
    """
    user_input = user_input.lower()
    
    # Simple parsing logic (can be enhanced with the AI agent)
    if "add" in user_input or "buy" in user_input:
        # Look for product keywords
        for product in available_products:
            if any(keyword in user_input for keyword in product['title'].lower().split()):
                return {
                    "action": "add",
                    "product_id": product['id'],
                    "message": f"Added {product['title']} to your cart!"
                }
        return {"action": "search", "query": user_input}
    
    elif "remove" in user_input or "delete" in user_input:
        # Check if it's remove all vs remove one
        remove_all = any(word in user_input for word in ['all', 'completely', 'entirely'])
        
        # Try to find which product to remove from cart
        for cart_item in current_cart:
            item_keywords = cart_item['title'].lower().split()
            if any(keyword in user_input for keyword in item_keywords):
                return {
                    "action": "remove_all" if remove_all else "remove",
                    "product_id": cart_item['id'],
                    "message": f"{'Completely removed' if remove_all else 'Removed one'} {cart_item['title']} from your cart!"
                }
        
        # If no specific item found, show cart for user to choose
        if current_cart:
            return {"action": "view_cart", "message": "Here's your cart. Which item would you like to remove?"}
        else:
            return {"action": "view_cart", "message": "Your cart is empty, nothing to remove."}
    
    elif "cart" in user_input or "show" in user_input:
        return {"action": "view_cart", "message": "Here's your current cart:"}
    
    elif "clear" in user_input and "cart" in user_input:
        return {"action": "clear_cart", "message": "Cart cleared successfully!"}
    
    else:
        return {"action": "search", "query": user_input}

async def process_ai_request(user_input: str, state, available_products: List[Dict]) -> Dict[str, Any]:
    """
    Process user request using AI and return appropriate action
    """
    try:
        # Get current cart data
        current_cart = [item.dict() for item in state.cart]
        
        # Use the AI agent to process the request
        result = await ecommerce_agent.run(
            f"User request: {user_input}\n\nAvailable products: {json.dumps(available_products, indent=2)}\n\nCurrent cart: {json.dumps(current_cart, indent=2)}"
        )
        
        # For now, use simple parsing (can be enhanced with structured output from AI)
        parsed = parse_user_request(user_input, available_products, current_cart)
        parsed["ai_response"] = str(result.output)
        
        return parsed
        
    except Exception as e:
        return {
            "action": "error",
            "message": f"Sorry, I couldn't process your request: {str(e)}",
            "ai_response": "I'm having trouble understanding that request. Please try again."
        }