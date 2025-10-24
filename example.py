"""
Example usage of the AI Agent.
Demonstrates how to interact with the agent locally.
"""

import os
from core.agent import AIAgent


def main():
    """Run example agent interactions."""
    
    # Check if API key is set
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable not set!")
        print("Please set it before running: export OPENROUTER_API_KEY='your-key-here'")
        return
    
    print("=" * 60)
    print("AI Agent with Reasoning and Tools - Example")
    print("=" * 60)
    print()
    
    # Initialize agent
    try:
        agent = AIAgent(api_key=api_key)
        print("✓ Agent initialized successfully")
        print(f"✓ Model: {agent.model}")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize agent: {e}")
        return
    
    # Example 1: Simple conversation
    print("Example 1: Simple conversation")
    print("-" * 60)
    result = agent.process_message("Hello! What can you help me with?")
    print(f"User: Hello! What can you help me with?")
    print(f"Agent: {result['response']}")
    print()
    
    # Example 2: Using the write_to_file tool
    print("Example 2: Writing to a file")
    print("-" * 60)
    result = agent.process_message(
        "Please create a file called 'test_output.txt' in the current directory "
        "with the content 'Hello from AI Agent!'"
    )
    print(f"User: Please create a file called 'test_output.txt'...")
    if result.get('tool_used'):
        print(f"Tool used: {result['tool_used']}")
        print(f"Reasoning: {result['tool_reasoning']}")
        print(f"Result: {result['tool_result']}")
    print(f"Agent: {result['response']}")
    print()
    
    # Example 3: Web search
    print("Example 3: Web search")
    print("-" * 60)
    result = agent.process_message("Search the web for information about Python programming")
    print(f"User: Search the web for information about Python programming")
    if result.get('tool_used'):
        print(f"Tool used: {result['tool_used']}")
        print(f"Reasoning: {result['tool_reasoning']}")
    print(f"Agent: {result['response']}")
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
