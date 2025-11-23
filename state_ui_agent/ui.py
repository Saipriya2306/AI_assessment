# ui.py - Enhanced UI Components for Ecommerce AI Assistant
from fasthtml.common import *

def get_cart_quantity(cart, product_id):
    """Get quantity of product in cart"""
    for item in cart:
        if item.id == product_id:
            return item.qty
    return 0

def product_card(product, cart):
    """Enhanced product card with quantity display and improved styling"""
    qty_in_cart = get_cart_quantity(cart, product.id)
    
    # Use emoji icons as placeholders for missing images
    emoji_map = {
        'laptop': '💻',
        'phone': '📱', 
        'headphone': '🎧',
        'tablet': '📱',
        'watch': '⌚',
        'camera': '📷'
    }
    
    # Find appropriate emoji based on product ID or title
    icon = '📦'  # default
    for key, emoji in emoji_map.items():
        if key in product.id.lower() or key in product.title.lower():
            icon = emoji
            break
    
    # Quantity badge (only show if in cart)
    qty_badge = Div(
        f"🛒 {qty_in_cart} in cart",
        cls="quantity-badge",
        style="position: absolute; top: 10px; right: 10px; background: #22c55e; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem;"
    ) if qty_in_cart > 0 else Div()
    
    # Add to cart form
    add_form = Form(
        Input(type="hidden", name="pid", value=product.id),
        Button("+ Add to Cart", type="submit", cls="btn btn-primary", style="flex: 1;"),
        action="/add", method="post",
        style="flex: 1;"
    )
    
    # Remove form (only if item is in cart)
    remove_form = Form(
        Input(type="hidden", name="pid", value=product.id),
        Button("- Remove", type="submit", cls="btn btn-danger", style="width: 80px;"),
        action="/remove", method="post"
    ) if qty_in_cart > 0 else Div()
    
    return Div(
        qty_badge,
        Div(icon, cls="product-image"),
        Div(
            H3(product.title, cls="product-title"),
            Div(f"₹{product.price:,}", cls="product-price"),
            Div(
                add_form,
                remove_form,
                cls="product-actions",
                style="display: flex; gap: 10px; align-items: center;"
            ),
            cls="product-info"
        ),
        cls="product-card",
        style="position: relative;"
    )

def search_bar(current_query=""):
    """Enhanced search bar"""
    return Div(
        Form(
            Input(
                type="text", 
                name="q", 
                value=current_query,
                placeholder="Search laptops, phones, headphones...",
                cls="search-bar"
            ),
            Button("Search", type="submit", cls="btn btn-primary"),
            action="/search", method="get",
            style="display: flex; gap: 10px; margin-bottom: 20px;"
        )
    )

def navigation_bar(cart_count=0):
    """Navigation bar with cart link"""
    return Div(
        Div(
            H1("🛍️ AI Shopping Assistant", style="margin: 0;"),
            Div(
                A("Home", href="/", cls="btn btn-secondary"),
                A(f"🛒 Cart ({cart_count})", href="/cart", cls="btn btn-secondary"),
                style="display: flex; gap: 10px; align-items: center;"
            ),
            style="display: flex; justify-content: space-between; align-items: center;"
        ),
        cls="header"
    )

def floating_ai_button():
    """Floating AI assistant button"""
    return Button(
        "🤖 AI Assistant", 
        id="chat-toggle",
        style="position: fixed; bottom: 20px; right: 20px; z-index: 1001; padding: 18px 24px; border-radius: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4); cursor: pointer; font-size: 1rem; font-weight: 600;"
    )

def ai_assistant_drawer():
    """AI assistant as a drawer/popover above the button"""
    return Div(
        # Overlay
        Div(
            id="ai-overlay",
            style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.1); z-index: 999; display: none;"
        ),
        
        # AI Assistant drawer
        Div(
            # Header
            Div(
                Div(
                    H4("🤖 AI Shopping Assistant", style="margin: 0; font-size: 1.1rem; font-weight: 600;"),
                    P("I can help you shop, manage cart, and find products!", 
                      style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;"),
                    style="flex: 1;"
                ),
                Button(
                    "×", 
                    id="ai-close-btn",
                    style="background: none; border: none; color: white; font-size: 1.5rem; cursor: pointer; padding: 0; width: 30px; height: 30px;"
                ),
                style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; display: flex; align-items: center; justify-content: space-between; border-radius: 15px 15px 0 0;"
            ),
            
            # Chat messages
            Div(
                Div("👋 Hi! I'm your AI shopping assistant.", style="margin-bottom: 10px; padding: 10px; background: #f0f0f0; border-radius: 8px;"),
                Div("Try saying: 'Add gaming laptop to cart' or 'Show my cart'", style="margin-bottom: 10px; padding: 10px; background: #f0f0f0; border-radius: 8px; font-size: 0.9rem;"),
                id="chat-messages",
                style="flex: 1; padding: 15px; max-height: 300px; overflow-y: auto; border-bottom: 1px solid #e2e8f0;"
            ),
            
            # Chat input
            Div(
                Input(
                    type="text",
                    id="chat-input", 
                    placeholder="Ask me anything about shopping...",
                    style="width: 100%; padding: 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.95rem; box-sizing: border-box;"
                ),
                Button(
                    "Send Message", 
                    id="send-message-btn",
                    style="margin-top: 10px; width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;"
                ),
                style="padding: 15px; background: #f8fafc;"
            ),
            
            id="ai-drawer",
            style="position: fixed; bottom: 80px; right: 20px; width: 380px; max-height: 500px; background: white; border-radius: 15px; box-shadow: 0 15px 40px rgba(0,0,0,0.2); z-index: 1000; border: 1px solid #e2e8f0; display: none; flex-direction: column;"
        )
    )

def ai_chat_javascript():
    """JavaScript component for AI chat functionality"""
    return Script("""
        let aiOpen = false;
        let chatHistory = JSON.parse(localStorage.getItem('aiChatHistory') || '[]');
        
        function saveChatHistory() {
            localStorage.setItem('aiChatHistory', JSON.stringify(chatHistory));
        }
        
        function toggleAIAssistant() {
            console.log('toggleAIAssistant called, aiOpen:', aiOpen);
            
            const aiDrawer = document.getElementById('ai-drawer');
            const aiOverlay = document.getElementById('ai-overlay');
            const toggleBtn = document.getElementById('chat-toggle');
            
            console.log('Elements found:', {aiDrawer: !!aiDrawer, aiOverlay: !!aiOverlay, toggleBtn: !!toggleBtn});
            
            if (!aiDrawer) {
                console.error('AI drawer not found!');
                return;
            }
            
            if (aiOpen) {
                // Close the drawer
                aiDrawer.style.display = 'none';
                if (aiOverlay) aiOverlay.style.display = 'none';
                if (toggleBtn) toggleBtn.innerHTML = '🤖 AI Assistant';
                aiOpen = false;
                console.log('AI Assistant closed');
            } else {
                // Open the drawer
                aiDrawer.style.display = 'flex';
                if (aiOverlay) aiOverlay.style.display = 'block';
                if (toggleBtn) toggleBtn.innerHTML = '🤖 Close Assistant';
                aiOpen = true;
                console.log('AI Assistant opened');
                
                // Focus input
                setTimeout(() => {
                    const input = document.getElementById('chat-input');
                    if (input) input.focus();
                }, 100);
            }
        }
        
        function loadChatHistory() {
            const messages = document.getElementById('chat-messages');
            if (!messages) return;
            
            // Add stored history
            chatHistory.forEach(item => {
                const msgDiv = document.createElement('div');
                msgDiv.className = `message ${item.isUser ? 'user' : 'bot'}`;
                msgDiv.textContent = item.message;
                messages.appendChild(msgDiv);
            });
            
            messages.scrollTop = messages.scrollHeight;
        }
        
        function addMessageToChat(message, isUser = true) {
            const messages = document.getElementById('chat-messages');
            if (!messages) return;
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            messageDiv.textContent = message;
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
            
            // Save to history (limit to last 20 messages)
            chatHistory.push({ message, isUser, timestamp: Date.now() });
            if (chatHistory.length > 20) {
                chatHistory = chatHistory.slice(-20);
            }
            saveChatHistory();
        }
        
        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input?.value?.trim();
            
            if (!message) return;
            
            // Add user message
            addMessageToChat(message, true);
            input.value = '';
            
            // Show typing indicator
            const messages = document.getElementById('chat-messages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot';
            typingDiv.innerHTML = '🤔 Thinking...';
            typingDiv.id = 'typing-indicator';
            messages.appendChild(typingDiv);
            messages.scrollTop = messages.scrollHeight;
            
            try {
                const formData = new FormData();
                formData.append('message', message);
                
                const response = await fetch('/ai-chat', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                // Remove typing indicator
                document.getElementById('typing-indicator')?.remove();
                
                // Add bot response
                const botMessage = result.response || result.error || 'Sorry, something went wrong.';
                addMessageToChat(botMessage, false);
                
                // Reload page after successful cart operations
                if (result.response && (result.response.includes('Added') || result.response.includes('Removed'))) {
                    setTimeout(() => location.reload(), 1500);
                }
                
            } catch (error) {
                document.getElementById('typing-indicator')?.remove();
                addMessageToChat('Sorry, I had trouble processing that request.', false);
            }
        }
        
        // Set up event listeners - using both DOMContentLoaded and immediate setup
        function setupEventListeners() {
            console.log('Setting up AI Assistant event listeners');
            
            const toggleBtn = document.getElementById('chat-toggle');
            const closeBtn = document.getElementById('ai-close-btn');
            const sendBtn = document.getElementById('send-message-btn');
            const input = document.getElementById('chat-input');
            const overlay = document.getElementById('ai-overlay');
            
            console.log('Found elements:', {toggleBtn: !!toggleBtn, closeBtn: !!closeBtn, sendBtn: !!sendBtn, input: !!input, overlay: !!overlay});
            
            if (toggleBtn) {
                // Remove any existing listeners
                toggleBtn.removeEventListener('click', toggleAIAssistant);
                toggleBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    console.log('Toggle button clicked');
                    toggleAIAssistant();
                });
                console.log('Toggle button listener added');
            } else {
                console.error('Toggle button not found!');
            }
            
            if (closeBtn) {
                closeBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    toggleAIAssistant();
                });
            }
            
            if (sendBtn) {
                sendBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    sendMessage();
                });
            }
            
            if (input) {
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage();
                    }
                });
            }
            
            if (overlay) {
                overlay.addEventListener('click', function() {
                    if (aiOpen) {
                        toggleAIAssistant();
                    }
                });
            }
        }
        
        // Set up immediately and on DOM ready
        setupEventListeners();
        document.addEventListener('DOMContentLoaded', setupEventListeners);
        
        // Also try after a short delay
        setTimeout(setupEventListeners, 500);
    """)

def home_page(products, cart_count=0, cart=None):
    """Enhanced home page with products and AI assistant drawer"""
    if cart is None:
        cart = []
        
    return Html(
        Head(
            Title("AI Shopping Assistant"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1")
        ),
        Body(
            navigation_bar(cart_count),
            Div(
                H2("Welcome to AI Shopping! 🛍️", style="text-align: center; color: #333; margin-bottom: 10px;"),
                P("Browse our products below or use the AI assistant to help you shop!", 
                  style="text-align: center; color: #666; margin-bottom: 30px;"),
                
                search_bar(),
                
                Div(
                    *[product_card(product, cart) for product in products],
                    cls="product-grid"
                ),
                
                cls="container"
            ),
            
            # Floating AI button
            floating_ai_button(),
            
            # AI assistant drawer
            ai_assistant_drawer(),
            
            # JavaScript for AI functionality
            ai_chat_javascript()
        )
    )

def search_page(products, query, cart, cart_count=0):
    """Search results page with AI assistant drawer"""
    if cart is None:
        cart = []
    
    return Html(
        Head(
            Title(f"Search: {query} - AI Shopping Assistant"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1")
        ),
        Body(
            navigation_bar(cart_count),
            Div(
                H2(f"Search Results for '{query}'" if query else "All Products"),
                
                search_bar(query),
                
                P(f"Found {len(products)} products") if products else P("No products found. Try a different search."),
                
                Div(
                    *[product_card(product, cart) for product in products],
                    cls="product-grid"
                ) if products else Div(),
                
                cls="container"
            ),
            
            # Floating AI button
            floating_ai_button(),
            
            # AI assistant drawer
            ai_assistant_drawer(),
            
            # JavaScript for AI functionality
            ai_chat_javascript()
        )
    )

def cart_page(cart_items, subtotal, cart_count=0):
    """Enhanced cart page"""
    if not cart_items:
        return Html(
            Head(Title("Cart - AI Shopping Assistant")),
            Body(
                navigation_bar(cart_count),
                Div(
                    H2("Your Shopping Cart"),
                    Div(
                        H3("🛒 Cart is empty"),
                        P("Start shopping to add items to your cart!"),
                        A("Continue Shopping", href="/", cls="btn btn-primary"),
                        style="text-align: center; padding: 40px; background: white; border-radius: 12px; margin: 20px 0;"
                    ),
                    cls="container"
                ),
                
                # Floating AI button
                floating_ai_button(),
                
                # AI assistant drawer
                ai_assistant_drawer(),
                
                # JavaScript for AI functionality
                ai_chat_javascript()
            )
        )
    
    cart_rows = []
    for item in cart_items:
        cart_rows.append(
            Div(
                Div(
                    H4(item.title),
                    P(f"₹{item.price:,} each"),
                    style="flex: 1;"
                ),
                Div(
                    Span(f"Quantity: {item.qty}", cls="quantity-display"),
                    P(f"Subtotal: ₹{item.price * item.qty:,}", style="font-weight: bold; margin: 5px 0;"),
                    Form(
                        Input(type="hidden", name="pid", value=item.id),
                        Button("Remove One", type="submit", cls="btn btn-danger"),
                        action="/remove", method="post"
                    ),
                    style="text-align: right;"
                ),
                style="display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid #eee; background: white; border-radius: 8px; margin-bottom: 10px;"
            )
        )
    
    return Html(
        Head(Title("Cart - AI Shopping Assistant")),
        Body(
            navigation_bar(cart_count),
            Div(
                H2("Your Shopping Cart"),
                
                Div(*cart_rows),
                
                Div(
                    H3(f"Total: ₹{subtotal:,}", style="text-align: right; color: #667eea;"),
                    Div(
                        A("Continue Shopping", href="/", cls="btn btn-secondary"),
                        Form(
                            Button("Checkout", type="submit", cls="btn btn-primary"),
                            action="/checkout", method="post",
                            style="display: inline-block; margin-left: 10px;"
                        ),
                        A("Clear Cart", href="/clear-cart", cls="btn btn-danger", style="margin-left: 10px;"),
                        style="text-align: right; margin-top: 20px;"
                    ),
                    style="background: white; padding: 20px; border-radius: 12px; margin-top: 20px;"
                ),
                
                cls="container"
            ),
            
            # Floating AI button
            floating_ai_button(),
            
            # AI assistant drawer
            ai_assistant_drawer(),
            
            # JavaScript for AI functionality
            ai_chat_javascript()
        )
    )

def checkout_page(total):
    """Checkout success page"""
    return Html(
        Head(Title("Checkout Complete - AI Shopping Assistant")),
        Body(
            navigation_bar(0),
            Div(
                Div(
                    H2("🎉 Order Complete!"),
                    P(f"Thank you for your purchase!"),
                    H3(f"Total Paid: ₹{total:,}"),
                    P("Your order will be delivered within 3-5 business days."),
                    A("Continue Shopping", href="/", cls="btn btn-primary"),
                    style="text-align: center; padding: 40px; background: white; border-radius: 12px; margin: 40px 0;"
                ),
                cls="container"
            ),
            
            # Floating AI button
            floating_ai_button(),
            
            # AI assistant drawer
            ai_assistant_drawer(),
            
            # JavaScript for AI functionality
            ai_chat_javascript()
        )
    )