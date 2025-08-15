"""
Decision Agent - Makes final recommendations based on analysis
"""

from langchain.prompts import ChatPromptTemplate

DECISION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are Decision. Produce a concise, actionable recommendation with a short rationale and 2–3 caveats."),
    ("human", "Question: {question}\nAnalysis: {analysis}")
])

def make_decision(question: str, analysis: str, llm) -> str:
    """Make a decision using the decision agent."""
    messages = DECISION_PROMPT.format_messages(
        question=question,
        analysis=analysis
    )
    
    response = llm.invoke(messages)
    decision = getattr(response, "content", str(response)).strip()
    
    return decision 