"""
Workflow Orchestration - Manages the multi-agent workflow execution
"""

from typing import Dict, Any
from core.memory import Memory, add_message, get_last_user_message
from agents.perception import extract_intent_and_entities
from agents.orchestrator import decide_next_step
from agents.research import gather_research
from agents.analysis import analyze_facts
from agents.decision import make_decision
from config import DEFAULT_DISPLAY_LIMIT

class MultiAgentWorkflow:
    """Orchestrates the execution of the multi-agent cognitive architecture."""
    
    def __init__(self, perception_llm, reasoner_llm, display_limit: int = None):
        self.perception_llm = perception_llm
        self.reasoner_llm = reasoner_llm
        self.display_limit = display_limit or DEFAULT_DISPLAY_LIMIT
    
    def run(self, question: str, verbose: bool = True) -> Dict[str, Any]:
        """Run the complete multi-agent workflow."""
        # Initialize state
        state = Memory(
            messages=[{"role": "user", "content": question}],
            entities=[],
            research_facts=[],
        )
        
        if verbose:
            print(f"\n🤔 Processing: {question}")
            print("=" * 50)
        
        # Step 1: Perception
        if verbose:
            print("\n🔍 Step 1: Perception")
        
        perception_result = extract_intent_and_entities(
            get_last_user_message(state), 
            self.perception_llm
        )
        
        state.update(perception_result)
        add_message(state, "system/perception", str(perception_result))
        
        if verbose:
            print(f"   Intent: {state['intent']}")
            print(f"   Entities: {state['entities']}")
        
        # Step 2: Research
        if verbose:
            print("\n📚 Step 2: Research")
        
        research_facts = gather_research(
            state.get("normalized_question", question),
            state.get("entities", []),
            self.reasoner_llm
        )
        
        state["research_facts"] = research_facts
        add_message(state, "agent/research", str(research_facts))
        
        if verbose:
            print(f"   Found {len(research_facts)} facts:")
            for i, fact in enumerate(research_facts, 1):
                if len(fact) > self.display_limit:
                    print(f"   {i}. {fact[:self.display_limit]}...")
                    print(f"      ... (truncated, full length: {len(fact)} chars)")
                else:
                    print(f"   {i}. {fact}")
        
        # Step 3: Analysis
        if verbose:
            print("\n🧠 Step 3: Analysis")
        
        analysis = analyze_facts(
            state.get("normalized_question", question),
            research_facts,
            self.reasoner_llm
        )
        
        state["analysis"] = analysis
        add_message(state, "agent/analysis", analysis)
        
        if verbose:
            if len(analysis) > self.display_limit:
                print(f"   Analysis (truncated, full length: {len(analysis)} chars):")
                print(f"   {analysis[:self.display_limit]}...")
                print(f"   ... (full analysis available in results)")
            else:
                print(f"   Analysis: {analysis}")
        
        # Step 4: Decision
        if verbose:
            print("\n🎯 Step 4: Decision")
        
        decision = make_decision(
            state.get("normalized_question", question),
            analysis,
            self.reasoner_llm
        )
        
        state["decision"] = decision
        add_message(state, "agent/decision", decision)
        
        if verbose:
            if len(decision) > self.display_limit:
                print(f"   Decision (truncated, full length: {len(decision)} chars):")
                print(f"   {decision[:self.display_limit]}...")
                print(f"   ... (full decision available in results)")
            else:
                print(f"   Decision: {decision}")
        
        # Final output
        if verbose:
            print("\n" + "=" * 50)
            print("🎉 Workflow Complete!")
            print("=" * 50)
        
        return state 