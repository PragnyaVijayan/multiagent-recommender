"""
Multi-Agent Cognitive Architecture - Main Entry Point
"""

import os
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from core.llm_factory import make_llm, make_reasoner
from core.workflow import MultiAgentWorkflow
from config import DEFAULT_DISPLAY_LIMIT, FULL_OUTPUT_DISPLAY_LIMIT

def main():
    """Main entry point for the multi-agent system."""
    parser = argparse.ArgumentParser(description="Multi-Agent Cognitive Architecture")
    parser.add_argument("--question", help="User query to process")
    parser.add_argument("--backend", choices=["groq", "fake"], 
                       default=os.getenv("BACKEND", "groq"),
                       help="LLM backend to use")
    parser.add_argument("--test", action="store_true", 
                       help="Run built-in tests with FakeLLM")
    parser.add_argument("--interactive", action="store_true",
                       help="Run in interactive mode")
    parser.add_argument("--full-output", action="store_true",
                       help="Show full content without truncation")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running tests with FakeLLM backend...")
        run_tests()
        return
    
    if args.interactive:
        run_interactive(args.backend, args.full_output)
        return
    
    if not args.question:
        print("❌ Please provide a question with --question or use --interactive mode")
        parser.print_help()
        return
    
    # Run the workflow
    run_workflow(args.question, args.backend, args.full_output)

def run_workflow(question: str, backend: str, full_output: bool = False):
    """Run the multi-agent workflow for a given question."""
    try:
        print(f"🚀 Starting Multi-Agent Workflow with {backend} backend...")
        
        # Create LLMs
        perception_llm = make_llm(backend)
        reasoner_llm = make_reasoner(backend)
        
        # Create and run workflow with appropriate display limit
        display_limit = FULL_OUTPUT_DISPLAY_LIMIT if full_output else DEFAULT_DISPLAY_LIMIT
        workflow = MultiAgentWorkflow(perception_llm, reasoner_llm, display_limit)
        result = workflow.run(question)
        
        # Display final results
        print("\n" + "=" * 60)
        print("🎯 FINAL RECOMMENDATION")
        print("=" * 60)
        decision = result.get("decision", "No decision produced.")
        if full_output or len(decision) <= FULL_OUTPUT_DISPLAY_LIMIT:
            print(decision)
        else:
            print(f"{decision[:FULL_OUTPUT_DISPLAY_LIMIT]}...")
            print(f"\n... (truncated, full length: {len(decision)} chars)")
            print("Use --full-output to see complete content")
        
        print("\n" + "=" * 60)
        print("📊 WORKFLOW SUMMARY")
        print("=" * 60)
        print(f"Intent: {result.get('intent', 'Unknown')}")
        print(f"Entities: {', '.join(result.get('entities', []))}")
        print(f"Research Facts: {len(result.get('research_facts', []))} gathered")
        print(f"Analysis: {'✓' if result.get('analysis') else '✗'}")
        print(f"Decision: {'✓' if result.get('decision') else '✗'}")
        
        # Show full content if requested
        if full_output:
            print("\n" + "=" * 60)
            print("📋 FULL CONTENT")
            print("=" * 60)
            
            print("\n🔍 PERCEPTION:")
            print(f"Intent: {result.get('intent')}")
            print(f"Entities: {result.get('entities')}")
            print(f"Normalized Question: {result.get('normalized_question')}")
            
            print("\n📚 RESEARCH FACTS:")
            for i, fact in enumerate(result.get('research_facts', []), 1):
                print(f"{i}. {fact}")
            
            print("\n🧠 ANALYSIS:")
            print(result.get('analysis', 'No analysis available'))
            
            print("\n🎯 DECISION:")
            print(result.get('decision', 'No decision available'))
        
    except Exception as e:
        print(f"❌ Error running workflow: {e}")
        print("\n💡 Troubleshooting tips:")
        if backend == "groq":
            print("   - Make sure GROQ_API_KEY is set in .env file")
            print("   - Check your Groq API key is valid")
            print("   - Verify you have sufficient Groq credits")

def run_interactive(backend: str, full_output: bool = False):
    """Run the system in interactive mode."""
    try:
        print(f"🤖 Multi-Agent System Interactive Mode ({backend} backend)")
        print("Type 'quit' or 'exit' to stop")
        if full_output:
            print("📋 Full output mode enabled")
        print("=" * 50)
        
        # Create LLMs once
        perception_llm = make_llm(backend)
        reasoner_llm = make_reasoner(backend)
        display_limit = FULL_OUTPUT_DISPLAY_LIMIT if full_output else DEFAULT_DISPLAY_LIMIT
        workflow = MultiAgentWorkflow(perception_llm, reasoner_llm, display_limit)
        
        while True:
            try:
                question = input("\n🤔 Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not question:
                    continue
                
                # Run workflow
                workflow.run(question)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to start interactive mode: {e}")

def run_tests():
    """Run basic tests to verify the system works."""
    try:
        print("🧪 Creating test workflow...")
        
        # Use fake backend for tests
        perception_llm = make_llm("fake")
        reasoner_llm = make_reasoner("fake")
        workflow = MultiAgentWorkflow(perception_llm, reasoner_llm)
        
        # Test questions
        test_questions = [
            "Compare MacBook Air vs Pro for development",
            "What are the best Python web frameworks?",
            "How should I choose between different programming languages?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n🧪 Test {i}: {question}")
            try:
                result = workflow.run(question, verbose=False)
                
                # Verify outputs
                assert result.get("intent"), "Intent missing"
                assert result.get("research_facts"), "Research facts missing"
                assert result.get("analysis"), "Analysis missing"
                assert result.get("decision"), "Decision missing"
                
                print(f"   ✅ Test {i} passed")
                
            except Exception as e:
                print(f"   ❌ Test {i} failed: {e}")
                return
        
        print("\n🎉 All tests passed! The multi-agent system is working correctly.")
        
    except Exception as e:
        print(f"❌ Tests failed: {e}")

if __name__ == "__main__":
    main() 