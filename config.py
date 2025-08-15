"""
Configuration settings for the Multi-Agent Cognitive Architecture
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Backend Configuration
BACKEND = os.getenv("BACKEND", "groq").lower()  # Changed default to groq
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# System Configuration
VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"
MAX_RESEARCH_FACTS = int(os.getenv("MAX_RESEARCH_FACTS", "6"))
MAX_ANALYSIS_LENGTH = int(os.getenv("MAX_ANALYSIS_LENGTH", "99999999999"))
MAX_DECISION_LENGTH = int(os.getenv("MAX_DECISION_LENGTH", "99999999999"))

# Display Configuration
DEFAULT_DISPLAY_LIMIT = int(os.getenv("DEFAULT_DISPLAY_LIMIT", "99999999999"))
FULL_OUTPUT_DISPLAY_LIMIT = int(os.getenv("FULL_OUTPUT_DISPLAY_LIMIT", "99999999999"))


# Knowledge Base Configuration
ENABLE_KNOWLEDGE_BASE = os.getenv("ENABLE_KNOWLEDGE_BASE", "true").lower() == "true"
KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "data/knowledge_base.json")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/multi_agent.log") 