"""
Test script to validate tools functionality.
Tests each tool independently without requiring API key.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.tools import run_shell, run_web_search, write_to_file, get_tool_description


def test_run_shell():
    """Test the run_shell tool."""
    print("\n" + "=" * 60)
    print("Testing run_shell tool")
    print("=" * 60)
    
    # Test a simple command
    result = run_shell("echo 'Hello from shell!'")
    print(f"Command: echo 'Hello from shell!'")
    print(f"Success: {result['success']}")
    print(f"Output: {result['output'].strip()}")
    print(f"Return code: {result['returncode']}")
    
    assert result['success'] == True, "Shell command should succeed"
    assert "Hello from shell!" in result['output'], "Output should contain expected text"
    
    print("✓ run_shell test passed!")


def test_write_to_file():
    """Test the write_to_file tool."""
    print("\n" + "=" * 60)
    print("Testing write_to_file tool")
    print("=" * 60)
    
    # Test writing to a file
    test_file = "/tmp/test_agent_file.txt"
    test_content = "This is a test file created by the AI Agent!"
    
    result = write_to_file(test_file, test_content)
    print(f"File: {test_file}")
    print(f"Success: {result['success']}")
    print(f"Bytes written: {result.get('bytes_written', 0)}")
    
    # Verify file was created
    assert result['success'] == True, "Write operation should succeed"
    assert os.path.exists(test_file), "File should exist"
    
    with open(test_file, 'r') as f:
        content = f.read()
        assert content == test_content, "File content should match"
    
    # Clean up
    os.remove(test_file)
    
    print("✓ write_to_file test passed!")


def test_web_search():
    """Test the run_web_search tool."""
    print("\n" + "=" * 60)
    print("Testing run_web_search tool")
    print("=" * 60)
    
    # Test a simple search
    result = run_web_search("Python programming language", num_results=3)
    print(f"Query: Python programming language")
    print(f"Success: {result['success']}")
    print(f"Results count: {result.get('count', 0)}")
    
    if result['success'] and result.get('results'):
        print("\nFirst result:")
        first = result['results'][0]
        print(f"  Title: {first.get('title', 'N/A')}")
        print(f"  Snippet: {first.get('snippet', 'N/A')[:100]}...")
        print(f"  URL: {first.get('url', 'N/A')}")
    
    # Note: Web search might fail due to network issues, so we just check format
    assert 'success' in result, "Result should have success field"
    assert 'results' in result, "Result should have results field"
    
    print("✓ run_web_search test passed!")


def test_tool_descriptions():
    """Test tool description retrieval."""
    print("\n" + "=" * 60)
    print("Testing tool descriptions")
    print("=" * 60)
    
    descriptions = get_tool_description()
    
    print(f"Number of tools: {len(descriptions)}")
    
    expected_tools = ["run_shell", "run_web_search", "write_to_file"]
    for tool_name in expected_tools:
        assert tool_name in descriptions, f"Tool {tool_name} should be in descriptions"
        print(f"\n{tool_name}:")
        print(f"  Description: {descriptions[tool_name]['description']}")
        print(f"  Parameters: {descriptions[tool_name]['parameters']}")
    
    print("\n✓ Tool descriptions test passed!")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AI Agent Tools Test Suite")
    print("=" * 60)
    
    try:
        test_run_shell()
        test_write_to_file()
        test_web_search()
        test_tool_descriptions()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60 + "\n")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
