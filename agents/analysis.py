"""
Analysis Agent - Analyzes research facts to provide insights and comparisons
"""

from langchain.prompts import ChatPromptTemplate

ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are Analysis. Using ReAct, reason step-by-step but return only the final analysis.\n"
               "Compare tradeoffs, address constraints, and be specific."),
    ("human", "Question: {question}\nFacts: {facts}")
])

def analyze_facts(question: str, facts: list, llm) -> str:
    """Analyze research facts using the analysis agent."""
    messages = ANALYSIS_PROMPT.format_messages(
        question=question,
        facts=facts
    )
    
    response = llm.invoke(messages)
    analysis = getattr(response, "content", str(response)).strip()
    
    return analysis 