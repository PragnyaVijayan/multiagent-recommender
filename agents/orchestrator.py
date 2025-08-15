"""
Orchestrator Agent - Coordinates the workflow between different specialist agents
"""

from langchain.prompts import ChatPromptTemplate

ORCHESTRATOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are the Orchestrator. Given perception (intent, entities) and STM, choose next step.\n"
               "Options: research, analysis, decision, done.\n"
               "Rules:\n"
               "- If facts are missing for a comparative or factual query → research.\n"
               "- If research_facts exist but no analysis → analysis.\n"
               "- If analysis exists but no decision → decision.\n"
               "- Otherwise: done.\n"
               "Output ONLY one word: research|analysis|decision|done."),
    ("human", "intent={intent}\nentities={entities}\nresearch_facts={research_facts}\nanalysis={analysis}\ndecision={decision}")
])

def decide_next_step(state: dict, llm) -> str:
    """Decide which agent should run next based on current state."""
    messages = ORCHESTRATOR_PROMPT.format_messages(
        intent=state.get("intent"),
        entities=state.get("entities"),
        research_facts=state.get("research_facts", []),
        analysis=state.get("analysis"),
        decision=state.get("decision"),
    )
    
    step = llm.invoke(messages).content.strip().lower()
    
    # Validate and fallback logic
    if step not in {"research", "analysis", "decision", "done"}:
        if not state.get("research_facts"):
            step = "research"
        elif not state.get("analysis"):
            step = "analysis"
        elif not state.get("decision"):
            step = "decision"
        else:
            step = "done"
    
    return step 