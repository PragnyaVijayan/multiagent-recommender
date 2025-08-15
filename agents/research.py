"""
Research Agent - Gathers facts and information relevant to the user's query
"""

import json
from typing import List
from langchain.prompts import ChatPromptTemplate

RESEARCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are Research. Use tools + reasoning to gather 3–6 concise, factual bullets relevant to the question.\n"
               "Prefer concrete, verifiable facts. Output as a JSON array of strings."),
    ("human", "Question: {question}\nEntities: {entities}\n\nHere is a tiny local KB you may use: {kb}")
])

# Knowledge base for research
KNOWLEDGE_BASE = {
    "macbook comparison": [
        "MacBook Air (M3) has fanless design; quieter but can throttle under sustained loads.",
        "MacBook Pro (M3 Pro) offers more performance cores and active cooling; better for long compiles.",
        "Both have excellent battery; Air tends to last longer under light workloads.",
        "Developer workflows with Docker/containers tend to prefer more RAM/cores (Pro advantage).",
        "Price: Air is cheaper; value depends on workload intensity.",
    ],
    "python web frameworks": [
        "FastAPI excels at async I/O and typing; great DX.",
        "Django is batteries-included, ORM, admin, robust ecosystem.",
        "Flask is minimal and flexible; pick extensions as needed.",
    ],
    "general": [
        "Research involves gathering factual information from reliable sources.",
        "Analysis requires examining facts to identify patterns and insights.",
        "Decision-making involves weighing options based on analysis and constraints.",
    ]
}

def gather_research(question: str, entities: List[str], llm) -> List[str]:
    """Gather research facts using the research agent."""
    # Determine relevant knowledge base
    kb_key = "macbook comparison" if "macbook" in question.lower() else (
        "python web frameworks" if "python" in question.lower() and "framework" in question.lower() else "general"
    )
    kb_items = KNOWLEDGE_BASE.get(kb_key, KNOWLEDGE_BASE["general"])
    
    messages = RESEARCH_PROMPT.format_messages(
        question=question, 
        entities=entities, 
        kb=kb_items
    )
    
    raw = llm.invoke(messages)
    content = getattr(raw, "content", str(raw))
    
    try:
        facts = json.loads(content)
        if not isinstance(facts, list):
            raise ValueError("Expected list of facts")
        return facts
    except Exception:
        # Fallback: extract facts from text
        lines = content.split("\n")
        facts = []
        for line in lines:
            line = line.strip()
            if line and line.startswith(("-", "•", "*")):
                facts.append(line.lstrip("- • *").strip())
            elif line and len(line) > 20:  # Reasonable fact length
                facts.append(line)
        
        return facts[:6]  # Limit to 6 facts 