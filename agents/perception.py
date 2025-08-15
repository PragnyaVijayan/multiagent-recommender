"""
Perception Agent - Extracts user intent and key entities from input
"""

import json
from typing import Dict, List, Any
from langchain.prompts import ChatPromptTemplate

PERCEPTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are Perception. Extract user intent and key entities.\n"
               "Return compact JSON with keys: intent, entities (array), normalized_question.\n"
               "Be concise and do not include any extra commentary."),
    ("human", "{question}")
])

def extract_intent_and_entities(question: str, llm) -> Dict[str, Any]:
    """Extract intent and entities from user question using the perception agent."""
    messages = PERCEPTION_PROMPT.format_messages(question=question)
    raw = llm.invoke(messages)
    content = getattr(raw, "content", str(raw))
    
    try:
        data = json.loads(content)
        return {
            "intent": data.get("intent", "general_query"),
            "entities": data.get("entities", []),
            "normalized_question": data.get("normalized_question", question)
        }
    except Exception:
        # Fallback if JSON parsing fails
        return {
            "intent": "general_query",
            "entities": [],
            "normalized_question": question
        } 