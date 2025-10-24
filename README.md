# AI Agent with Reasoning and Tools

A powerful AI agent service that combines advanced language models with practical tool-calling capabilities. This agent can reason about tasks, make decisions, and execute actions using built-in tools for shell commands, web searches, and file operations.

## 🌟 Introduction

This project implements an intelligent AI agent that goes beyond simple chat interactions. By integrating with OpenRouter's API, the agent gains access to state-of-the-art language models while being equipped with practical tools that enable it to:

- **Reason** about complex problems and break them down into actionable steps
- **Execute** shell commands to interact with the system
- **Search** the web for up-to-date information
- **Manipulate** files and directories

The agent uses a reasoning-first approach, where it thinks through problems before taking action, making it reliable and transparent in its decision-making process.

## ✨ Key Features

### 🛠️ Built-in Tools

The agent comes with three powerful tools out of the box:

1. **`run_shell`** - Execute shell commands and capture their output
   - Run system commands safely with timeout controls
   - Capture both stdout and stderr
   - Handle errors gracefully
   - Perfect for automation tasks, system monitoring, and DevOps operations

2. **`run_web_search`** - Search the web for information
   - Query web search APIs to get current information
   - Retrieve multiple results with snippets and URLs
   - Useful for research, fact-checking, and staying up-to-date
   - Integrated with DuckDuckGo's free API (no API key required)

3. **`write_to_file`** - Create and modify files
   - Write content to files with automatic directory creation
   - Support for both write and append modes
   - Track file operations with detailed feedback
   - Essential for data persistence and report generation

### 🧠 Advanced Capabilities

- **Reasoning Engine**: The agent explains its thinking before using tools
- **Conversation Memory**: Maintains context across multiple interactions
- **Session Management**: Support for multiple concurrent conversations
- **RESTful API**: Clean HTTP interface for easy integration
- **Error Handling**: Robust error management and informative feedback

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (comes with Python)
- **Git** - For cloning the repository
- **OpenRouter API Key** - Sign up at [OpenRouter.ai](https://openrouter.ai/)

## 🚀 Local Setup Guide

Follow these steps to run the AI agent on your local machine:

### Step 1: Clone the Repository

```bash
git clone https://github.com/wasalstor-web/https-aichatplat-jxx5nb8h.manus.space-.git
cd https-aichatplat-jxx5nb8h.manus.space-
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file or export the API key:

```bash
# Option 1: Export directly (Linux/Mac)
export OPENROUTER_API_KEY='your-api-key-here'

# Option 1: Export directly (Windows)
set OPENROUTER_API_KEY=your-api-key-here

# Option 2: Create a .env file
echo "OPENROUTER_API_KEY=your-api-key-here" > .env
```

To get your API key:
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Navigate to the API Keys section
4. Create a new API key
5. Copy and use it in your environment

### Step 5: Run the API Server

```bash
python api/server.py
```

The server will start on `http://localhost:5000` by default.

### Step 6: Test the Agent

You can test the agent using curl, Postman, or the included example script:

**Using the example script:**
```bash
python example.py
```

**Using curl:**
```bash
# Health check
curl http://localhost:5000/

# Send a chat message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! What can you do?"}'

# List available tools
curl http://localhost:5000/tools
```

**Example API Response:**
```json
{
  "response": "Hello! I'm an AI agent with reasoning capabilities...",
  "tool_used": null,
  "tool_result": null
}
```

## 🌐 Deploy to Render.com

Render.com provides easy, free hosting for web services. Follow this comprehensive guide to deploy your AI agent.

### What is render.yaml?

The `render.yaml` file is Render's infrastructure-as-code configuration. It defines:

- **Service type**: Web service (API)
- **Runtime environment**: Python
- **Build command**: How to install dependencies (`pip install -r requirements.txt`)
- **Start command**: How to run the application (`python api/server.py`)
- **Environment variables**: Required configuration like API keys
- **Port configuration**: Network settings for the service

This file allows Render to automatically set up and deploy your service with the correct configuration.

### Step-by-Step Deployment Guide

#### Step 1: Prepare Your Repository

Ensure all files are committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

#### Step 2: Create a Render Account

1. Go to [Render.com](https://render.com/)
2. Click "Get Started" or "Sign Up"
3. Sign up using your GitHub account (recommended for easy integration)

#### Step 3: Create a New Web Service

1. From your Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub account if you haven't already
4. Find and select your repository: `wasalstor-web/https-aichatplat-jxx5nb8h.manus.space-`

#### Step 4: Configure the Service

Render will automatically detect the `render.yaml` file. Verify the settings:

- **Name**: `ai-agent-service` (or customize)
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python api/server.py`
- **Plan**: Free (or select your preferred plan)

#### Step 5: Add the OPENROUTER_API_KEY Secret

**This is the most critical step!** The agent cannot function without this API key.

1. In the service configuration page, find **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Enter:
   - **Key**: `OPENROUTER_API_KEY`
   - **Value**: Your OpenRouter API key (get it from [OpenRouter.ai](https://openrouter.ai/keys))
4. **Important**: Make sure to keep this value secret - never commit it to your repository!

#### Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies
   - Start your service
   - Provide you with a public URL (e.g., `https://ai-agent-service.onrender.com`)

The initial deployment may take 2-5 minutes.

#### Step 7: Verify Deployment

Once deployed, test your service:

```bash
# Health check (replace with your Render URL)
curl https://your-service-name.onrender.com/

# Test chat endpoint
curl -X POST https://your-service-name.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### Understanding OPENROUTER_API_KEY

**What is it?**
- The OPENROUTER_API_KEY is your authentication token for accessing OpenRouter's AI models
- OpenRouter acts as a gateway to multiple AI providers (OpenAI, Anthropic, etc.)

**Why is it required?**
- Without this key, the agent cannot make API calls to language models
- It authenticates your requests and tracks your usage
- It's how OpenRouter bills for API usage

**Security Best Practices:**
- ✅ Store it as an environment variable (never in code)
- ✅ Use Render's secret management (encrypted storage)
- ✅ Rotate keys periodically
- ❌ Never commit API keys to Git
- ❌ Don't share keys publicly
- ❌ Don't hardcode keys in your application

**Getting Your Key:**
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Go to API Keys section
4. Click "Create API Key"
5. Give it a name (e.g., "Render Production")
6. Copy the key immediately (it won't be shown again)
7. Add it to Render's environment variables

### Render.com Free Plan Limitations

Be aware of the free tier limitations:
- Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- 750 hours/month of runtime
- Shared resources

For production use, consider upgrading to a paid plan.

## 📁 Project Structure

```
.
├── core/
│   ├── __init__.py       # Core module initialization
│   ├── agent.py          # AI Agent with reasoning engine
│   └── tools.py          # Tool implementations (run_shell, run_web_search, write_to_file)
├── api/
│   ├── __init__.py       # API module initialization
│   └── server.py         # Flask REST API server
├── docs/
│   └── README.md         # Additional documentation
├── example.py            # Example usage script
├── requirements.txt      # Python dependencies
├── render.yaml           # Render.com deployment configuration
├── README.md             # This file
├── LICENSE               # MIT License
└── .gitignore            # Git ignore rules
```

## 🔌 API Endpoints

### `GET /`
Health check endpoint
```bash
curl http://localhost:5000/
```

### `POST /chat`
Send a message to the agent
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Your message here",
    "session_id": "optional-session-id"
  }'
```

### `POST /reset`
Reset conversation history
```bash
curl -X POST http://localhost:5000/reset \
  -H "Content-Type: application/json" \
  -d '{"session_id": "optional-session-id"}'
```

### `GET /tools`
List available tools
```bash
curl http://localhost:5000/tools
```

### `GET /history`
Get conversation history
```bash
curl http://localhost:5000/history?session_id=optional-session-id
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenRouter.ai for providing access to multiple AI models
- Flask framework for the API server
- DuckDuckGo for the free search API

## 📞 Support

For questions, issues, or suggestions:
- Open an issue in the GitHub repository
- Check the [documentation](docs/README.md)
- Review existing issues and discussions

---

**Built with ❤️ for the AI community**
