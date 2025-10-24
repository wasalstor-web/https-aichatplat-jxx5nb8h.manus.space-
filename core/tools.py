"""
Tool implementations for the AI Agent.
Provides capabilities for shell execution, web search, and file operations.
"""

import subprocess
import json
import os
from typing import Dict, Any, Optional
import requests


def run_shell(command: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute a shell command and return the result.
    
    Args:
        command: The shell command to execute
        timeout: Maximum time to wait for command execution (seconds)
        
    Returns:
        Dict containing status, output, and error information
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": f"Command timed out after {timeout} seconds",
            "returncode": -1
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "returncode": -1
        }


def run_web_search(query: str, num_results: int = 5) -> Dict[str, Any]:
    """
    Perform a web search and return results.
    
    Args:
        query: The search query
        num_results: Number of results to return
        
    Returns:
        Dict containing search results and metadata
    """
    # This is a placeholder implementation
    # In production, you would integrate with a real search API
    # (e.g., Google Custom Search, Bing Search API, DuckDuckGo, etc.)
    
    try:
        # Example: Using DuckDuckGo Instant Answer API (free, no API key required)
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        # Add abstract if available
        if data.get("Abstract"):
            results.append({
                "title": data.get("Heading", ""),
                "snippet": data.get("Abstract", ""),
                "url": data.get("AbstractURL", "")
            })
        
        # Add related topics
        for topic in data.get("RelatedTopics", [])[:num_results]:
            if isinstance(topic, dict) and "Text" in topic:
                results.append({
                    "title": topic.get("Text", "").split(" - ")[0] if " - " in topic.get("Text", "") else "",
                    "snippet": topic.get("Text", ""),
                    "url": topic.get("FirstURL", "")
                })
        
        return {
            "success": True,
            "query": query,
            "results": results[:num_results],
            "count": len(results[:num_results])
        }
        
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "results": [],
            "count": 0,
            "error": str(e)
        }


def write_to_file(filepath: str, content: str, mode: str = "w") -> Dict[str, Any]:
    """
    Write content to a file.
    
    Args:
        filepath: Path to the file
        content: Content to write
        mode: Write mode ('w' for write, 'a' for append)
        
    Returns:
        Dict containing operation status and metadata
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(filepath, mode, encoding='utf-8') as f:
            f.write(content)
        
        file_size = os.path.getsize(filepath)
        
        return {
            "success": True,
            "filepath": filepath,
            "mode": mode,
            "bytes_written": len(content),
            "file_size": file_size
        }
        
    except Exception as e:
        return {
            "success": False,
            "filepath": filepath,
            "mode": mode,
            "error": str(e)
        }


# Tool registry for easy access
TOOLS = {
    "run_shell": run_shell,
    "run_web_search": run_web_search,
    "write_to_file": write_to_file
}


def get_tool_description() -> Dict[str, Dict[str, str]]:
    """
    Get descriptions of all available tools.
    
    Returns:
        Dict mapping tool names to their descriptions
    """
    return {
        "run_shell": {
            "name": "run_shell",
            "description": "Execute shell commands and return the output",
            "parameters": "command (str), timeout (int, optional)"
        },
        "run_web_search": {
            "name": "run_web_search",
            "description": "Search the web and return relevant results",
            "parameters": "query (str), num_results (int, optional)"
        },
        "write_to_file": {
            "name": "write_to_file",
            "description": "Write content to a file",
            "parameters": "filepath (str), content (str), mode (str, optional)"
        }
    }
