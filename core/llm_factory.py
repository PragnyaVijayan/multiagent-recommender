"""
LLM Factory - Creates and manages different LLM backends
"""

import os
from typing import Optional

# LLM backends (optional — not required when using FakeLLM)
try:
    from langchain_groq import ChatGroq
except Exception:
    ChatGroq = None

# Configuration
BACKEND = os.getenv("BACKEND", "groq").lower()  # Changed default to groq
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

class FakeLLM:
    """A tiny deterministic LLM for offline tests."""
    def __init__(self, name: str = "fake", temperature: float = 0.0):
        self.name = name
        self.temperature = temperature

    def invoke(self, messages):
        # Simple mock responses for testing
        return type('MockResponse', (), {'content': f"Mock response from {self.name}"})()

def make_llm(backend: str = None):
    """Create an LLM instance based on the specified backend."""
    if backend is None:
        backend = BACKEND
    
    backend = backend.lower()
    
    if backend == "fake":
        return FakeLLM("fake", TEMPERATURE)
    
    if backend == "groq":
        if ChatGroq is None:
            raise RuntimeError("langchain-groq not installed. pip install langchain-groq")
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise RuntimeError("GROQ_API_KEY not set in environment or .env file.")
        return ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, api_key=groq_api_key)
    
    # Default fallback to groq
    if ChatGroq is None:
        raise RuntimeError("langchain-groq not installed. pip install langchain-groq")
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY not set in environment or .env file.")
    return ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, api_key=groq_api_key)

def make_reasoner(backend: str = None):
    """Create a reasoner LLM instance (can be different from the main LLM)."""
    if backend is None:
        backend = BACKEND
    
    backend = backend.lower()
    
    if backend == "fake":
        return FakeLLM("fake-reasoner", TEMPERATURE)
    
    if backend == "groq":
        if ChatGroq is None:
            raise RuntimeError("langchain-groq not installed. pip install langchain-groq")
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise RuntimeError("GROQ_API_KEY not set in environment or .env file.")
        return ChatGroq(model=os.getenv("GROQ_REASONER_MODEL", GROQ_MODEL), temperature=TEMPERATURE, api_key=groq_api_key)
    
    # Default fallback to groq
    if ChatGroq is None:
        raise RuntimeError("langchain-groq not installed. pip install langchain-groq")
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY not set in environment or .env file.")
    return ChatGroq(model=os.getenv("GROQ_REASONER_MODEL", GROQ_MODEL), temperature=TEMPERATURE, api_key=groq_api_key) 