"""
Memory Management - Handles agent state and conversation history
"""

from typing import TypedDict, List, Optional, Dict, Any

class Memory(TypedDict, total=False):
    """Short-term memory for the multi-agent system."""
    # Core messages (running transcript for traceability)
    messages: List[Dict[str, Any]]
    # Perception layer outputs
    intent: Optional[str]
    entities: List[str]
    normalized_question: Optional[str]
    # Specialist outputs
    research_facts: List[str]
    analysis: Optional[str]
    decision: Optional[str]
    # Control flags
    step: Optional[str]  # orchestrator: research|analysis|decision|done

def add_message(state: Memory, role: str, content: str) -> None:
    """Add a message to the conversation history."""
    state.setdefault("messages", []).append({"role": role, "content": content})

def get_last_user_message(state: Memory) -> str:
    """Get the last user message from the conversation history."""
    msgs = state.get("messages", [])
    for m in reversed(msgs):
        if m.get("role") == "user":
            return str(m.get("content", ""))
    return ""

def create_initial_state(question: str) -> Memory:
    """Create initial memory state with user question."""
    return {
        "messages": [{"role": "user", "content": question}],
        "entities": [],
        "research_facts": [],
    } 