# AI Assessment Projects

This repository contains two AI-powered projects built with Python, demonstrating different AI capabilities and frameworks.

## 🚀 Projects Overview

### 1. Research Agent (`research_agent/`)
An intelligent research assistant that uses DuckDuckGo's Instant Answer API to provide factual information on various topics.

**Key Features:**
- 🔍 Real-time web search capabilities
- 🤖 Google Gemini 2.5 Flash AI model integration
- 📊 FastAPI web interface
- 🛡️ Error handling and fallback mechanisms
- 📝 Comprehensive logging with Logfire

### 2. Ecommerce AI Assistant (`state_ui_agent/`)
A complete ecommerce platform with an intelligent AI shopping assistant that helps users manage their cart through natural language.

**Key Features:**
- 🛒 Full shopping cart functionality
- 💬 AI chat assistant for product recommendations
- 🎨 Modern, responsive UI with FastHTML
- 💾 Persistent chat history
- 🔍 Product search and filtering
- 📱 Mobile-friendly design

## 🛠️ Technical Stack

| Component | Research Agent | Ecommerce Agent |
|-----------|---------------|----------------|
| **AI Model** | Google Gemini 2.5 Flash | Google Gemini 2.5 Flash |
| **Framework** | pydantic-ai | pydantic-ai |
| **Web Framework** | FastAPI | FastHTML |
| **External APIs** | DuckDuckGo Instant Answer | - |
| **Frontend** | HTML/CSS/JavaScript | FastHTML Components |
| **Logging** | Logfire | Logfire |

## 📋 Prerequisites

- **Python 3.11+** (Recommended: Python 3.13)
- **Google AI API Key** (Gemini 2.5 Flash)
- **Git** (for cloning)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Saipriya2306/AI_assessment.git
cd AI_assessment
```

### 2. Set Up Environment Variables

Create `.env` files in both project directories:

**For Research Agent (`research_agent/.env`):**
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
LOGFIRE_TOKEN=your_logfire_token_here
```

**For Ecommerce Agent (`state_ui_agent/.env`):**
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
LOGFIRE_TOKEN=your_logfire_token_here
```

### 3. Install Dependencies

**For Research Agent:**
```bash
cd research_agent
pip install -r requirements.txt
```

**For Ecommerce Agent:**
```bash
cd ../state_ui_agent
pip install -r requirements.txt
```

## 🚀 Running the Applications

### Research Agent
```bash
cd research_agent
python main.py
```
- **Access at:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Ecommerce AI Assistant
```bash
cd state_ui_agent
python main.py
```
- **Access at:** http://localhost:5001
- **Features:** Browse products, use AI chat assistant

## 📖 Usage Examples

### Research Agent
Ask questions like:
- "What is artificial intelligence?"
- "Tell me about climate change"
- "Explain quantum computing"

### Ecommerce AI Assistant
Try these commands in the AI chat:
- "Add a gaming laptop to my cart"
- "Show me all smartphones"
- "Remove the tablet from my cart"
- "What's in my cart?"

## 🏗️ Project Structure

```
AI_assessment/
├── README.md
├── research_agent/
│   ├── .env                 # Environment variables
│   ├── .gitignore          # Git ignore rules
│   ├── agent.py            # Research agent logic
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── sample_logs.txt     # Example log outputs
│   └── tools.py            # DuckDuckGo API integration
└── state_ui_agent/
    ├── .env                # Environment variables
    ├── .gitignore         # Git ignore rules
    ├── agent.py           # Product catalog & cart management
    ├── ai_assistant.py    # AI chat processing
    ├── main.py            # FastHTML application
    ├── requirements.txt   # Python dependencies
    └── ui.py              # UI components & styling
```

## 🔑 API Keys Setup

### Google AI (Gemini) API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Add to your `.env` files

### Logfire Token (Optional)
1. Visit [Logfire](https://logfire.pydantic.dev/)
2. Create account and get token
3. Add to your `.env` files

## 🎨 Features Showcase

### Research Agent Features
- ✅ Natural language query processing
- ✅ Real-time web search integration
- ✅ Structured response formatting
- ✅ Error handling and fallbacks
- ✅ API documentation with FastAPI

### Ecommerce Agent Features
- ✅ 14 diverse product catalog
- ✅ Shopping cart with persistence
- ✅ AI-powered natural language interface
- ✅ Chat history preservation
- ✅ Responsive design with modern UI
- ✅ Real-time cart updates
- ✅ Product search functionality

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure you're in the correct directory and virtual environment
pip install -r requirements.txt
```

**2. API Key Issues**
```bash
# Check your .env file exists and has correct format
cat .env  # On Windows: type .env
```

**3. Port Already in Use**
```bash
# Kill existing processes
# Windows: netstat -ano | findstr :8000
# Kill process: taskkill /PID <PID> /F
```

### Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📊 Performance & Monitoring

Both applications include:
- **Structured logging** with Logfire integration
- **Error tracking** and debugging capabilities
- **Performance monitoring** for API calls
- **Request/response logging** for analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Author

**Saipriya Vaishnavam**
- GitHub: [@Saipriya2306](https://github.com/Saipriya2306)
- Email: saipriyavaishnavam@gmail.com

## 🙏 Acknowledgments

- **Pydantic AI** - For the excellent AI framework
- **Google AI** - For Gemini 2.5 Flash model
- **FastAPI & FastHTML** - For web framework capabilities
- **DuckDuckGo** - For search API integration

---

⭐ **If you find this project useful, please consider giving it a star!** ⭐