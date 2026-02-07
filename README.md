# 🤖 Claude Code - AI Coding Assistant

[![CodeCrafters](https://img.shields.io/badge/CodeCrafters-Challenge-blue)](https://codecrafters.io/challenges/claude-code)
[![Python](https://img.shields.io/badge/Python-3.14-green)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Compatible-orange)](https://openai.com/)

A powerful AI coding assistant built from scratch using Large Language Models (LLMs) and tool calling. This project demonstrates how to build an intelligent agent that can read files, write code, execute commands, and perform multi-step tasks autonomously.

## 🌟 Features

- **🔄 Agent Loop**: Intelligent multi-step task execution with conversation memory
- **📖 File Reading**: Read and analyze file contents
- **✍️ File Writing**: Create and modify files programmatically
- **⚡ Shell Execution**: Run bash commands and capture output
- **🧠 Context Awareness**: Maintains conversation history for complex tasks
- **🛡️ Error Handling**: Graceful error recovery and reporting

## 🚀 Quick Start

### Prerequisites

- Python 3.14+
- `uv` package manager
- OpenRouter API key (or compatible OpenAI API)

### Setup

1. **Set your API credentials**:

   ```bash
   export OPENROUTER_API_KEY="your-api-key-here"
   export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"  # Optional
   ```

2. **Run the assistant**:
   ```bash
   ./your_program.sh -p "your prompt here"
   ```

## 💡 Usage Examples

### Simple File Reading

```bash
./your_program.sh -p "What's in README.md?"
```

### Multi-Step Task

```bash
./your_program.sh -p "Read config.json, extract the version number, and create a VERSION file with that number"
```

### Code Analysis

```bash
./your_program.sh -p "Read app/main.py and summarize what it does"
```

### File Operations

```bash
./your_program.sh -p "Create a new Python file called hello.py that prints 'Hello, World!'"
```

### Shell Commands

```bash
./your_program.sh -p "List all Python files in the current directory and count them"
```

## 🛠️ Available Tools

The AI assistant has access to three powerful tools:

| Tool         | Description            | Example Use Case                            |
| ------------ | ---------------------- | ------------------------------------------- |
| `read_file`  | Read file contents     | Analyzing code, reading configs             |
| `write_file` | Write/create files     | Generating code, creating documentation     |
| `Bash`       | Execute shell commands | Running tests, file operations, system info |

## 🏗️ Architecture

```
┌─────────────────┐
│  User Prompt    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent Loop     │◄──────┐
│  (main.py)      │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  LLM API Call   │       │
│  (Claude/GPT)   │       │
└────────┬────────┘       │
         │                │
         ▼                │
    ┌────────┐            │
    │Tool    │            │
    │Call?   │────No──────┤
    └───┬────┘            │
        │Yes              │
        ▼                 │
┌─────────────────┐       │
│ Execute Tools   │       │
│ - read_file     │       │
│ - write_file    │       │
│ - Bash          │       │
└────────┬────────┘       │
         │                │
         └────────────────┘
```

## 📚 How It Works

1. **Initialization**: The user provides a prompt via the `-p` flag
2. **Agent Loop**: The system enters a continuous loop:
   - Sends the conversation history to the LLM
   - Receives a response (possibly with tool calls)
   - Executes any requested tools
   - Appends results to conversation history
   - Repeats until the LLM provides a final answer
3. **Output**: The final response is printed to stdout

## 🧪 Development

### Running Tests

```bash
codecrafters submit
```

### Local Development

```bash
# Install dependencies
uv sync

# Run the assistant
./your_program.sh -p "your test prompt"
```

## 🎓 Learning Objectives

This project teaches:

- ✅ HTTP RESTful API integration
- ✅ OpenAI-compatible tool calling
- ✅ Agent loop implementation
- ✅ Multi-tool integration
- ✅ Conversation state management
- ✅ Error handling and recovery

## 📝 Technical Details

- **Language**: Python 3.14
- **LLM Provider**: OpenRouter (OpenAI-compatible)
- **Default Model**: Anthropic Claude Haiku 4.5
- **Architecture Pattern**: Agent Loop with Tool Calling
- **Message Format**: OpenAI Chat Completion API

## 🤝 Contributing

This is a CodeCrafters challenge project. Feel free to fork and experiment!

## 📄 License

This project is part of the CodeCrafters "Build Your Own Claude Code" challenge.

## 🔗 Resources

- [CodeCrafters Challenge](https://codecrafters.io/challenges/claude-code)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [OpenRouter Documentation](https://openrouter.ai/docs)

---

**Built with ❤️ as part of the CodeCrafters coding challenge**
