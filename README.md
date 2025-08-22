# Multi-Agent Cognitive Architecture

A sophisticated multi-agent system built with LangChain and LangGraph that implements a cognitive architecture with specialized agents for perception, research, analysis, and decision-making. This can be templatized and used in other agentic ai projects.

## 🏗️ Architecture Overview

The system consists of four specialized agents working in sequence:

1. **🔍 Perception Agent** - Extracts user intent and key entities from input
2. **📚 Research Agent** - Gathers relevant facts and information
3. **🧠 Analysis Agent** - Analyzes facts to provide insights and comparisons
4. **🎯 Decision Agent** - Makes final recommendations with rationale and caveats

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file in the project root:

```bash
# Choose your LLM backend
BACKEND=groq  # or fake for testing

# For Groq (hosted - default)
GROQ_API_KEY=your_groq_api_key_here

# Optional: Customize behavior
TEMPERATURE=0.2
VERBOSE=true
```

### 3. Run the System

#### Single Question Mode
```bash
python main.py --question "Compare MacBook Air vs Pro for development"
```

#### Interactive Mode
```bash
python main.py --interactive
```

#### Test Mode (with FakeLLM)
```bash
python main.py --test
```

## 🔧 Backend Options

### Groq (Hosted - Default)
- **Pros**: Very fast, reliable, good for production
- **Setup**: Get API key from [Groq](https://console.groq.com)
- **Cost**: Free tier available
- **Default**: Set as the primary backend

### FakeLLM (Testing)
- **Pros**: No external dependencies, deterministic responses
- **Use**: Perfect for testing and development

## 📁 Project Structure

```
multi_agentic_research/
├── agents/                 # Specialized agent modules
│   ├── __init__.py
│   ├── perception.py      # Intent and entity extraction
│   ├── orchestrator.py    # Workflow coordination
│   ├── research.py        # Fact gathering
│   ├── analysis.py        # Fact analysis
│   └── decision.py        # Final recommendations
├── core/                  # Core system components
│   ├── __init__.py
│   ├── llm_factory.py    # LLM backend management
│   ├── memory.py         # State and conversation management
│   └── workflow.py       # Main workflow orchestration
├── main.py               # Entry point and CLI
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🧪 Testing

The system includes built-in tests that verify all agents work correctly:

```bash
python main.py --test
```

This runs tests with the FakeLLM backend, so no external LLM is required.

## 🔄 Workflow Example

Here's how the system processes a question:

1. **User Input**: "Compare MacBook Air vs Pro for development"
2. **Perception**: Extracts intent="compare", entities=["MacBook Air", "MacBook Pro"]
3. **Research**: Gathers facts about both laptops from knowledge base
4. **Analysis**: Compares performance, battery, price, and developer needs
5. **Decision**: Recommends MacBook Pro for heavy development, Air for light work

## 🎯 Use Cases

- **Product Comparisons**: Compare different options with structured analysis
- **Research Questions**: Gather facts and synthesize insights
- **Decision Support**: Get recommendations with clear rationale
- **Educational Content**: Break down complex topics into digestible insights

## 🚧 Troubleshooting

### Common Issues

**Groq API key issues:**
```bash
# Ensure .env file exists and contains correct keys
echo "GROQ_API_KEY=your_actual_key_here" > .env

# Verify API key is valid
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check LangChain version compatibility
pip show langchain
```

**API key issues:**
- Ensure `.env` file exists and contains correct keys
- Verify API keys are valid and have sufficient credits
- Check Groq service status at https://status.groq.com

## 🔮 Future Enhancements

- [ ] Web search integration for real-time research
- [ ] Memory persistence across sessions
- [ ] Custom knowledge base management
- [ ] Agent learning and adaptation
- [ ] Multi-language support
- [ ] API endpoints for integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License. 
