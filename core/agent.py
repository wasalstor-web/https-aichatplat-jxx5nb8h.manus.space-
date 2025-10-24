"""
AI Agent with reasoning capabilities.
Integrates with OpenRouter API for language model access.
"""

import os
import json
from typing import Dict, List, Any, Optional
import requests
from core.tools import TOOLS, get_tool_description


class AIAgent:
    """AI Agent with reasoning and tool-using capabilities."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "openai/gpt-3.5-turbo"):
        """
        Initialize the AI Agent.
        
        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            model: Model identifier to use for reasoning
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY must be provided or set in environment")
        
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.conversation_history: List[Dict[str, str]] = []
        self.tools = TOOLS
        
    def _make_api_call(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Make an API call to OpenRouter.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            API response data
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/wasalstor-web",
            "X-Title": "AI Agent with Reasoning"
        }
        
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with tool descriptions."""
        tool_descriptions = get_tool_description()
        tools_text = "\n".join([
            f"- {tool['name']}: {tool['description']} (Parameters: {tool['parameters']})"
            for tool in tool_descriptions.values()
        ])
        
        return f"""You are an AI agent with reasoning capabilities and access to tools.

Available Tools:
{tools_text}

When you need to use a tool, respond with a JSON object in this format:
{{
    "reasoning": "Your reasoning about why you need to use this tool",
    "tool": "tool_name",
    "parameters": {{
        "param1": "value1",
        "param2": "value2"
    }}
}}

When you want to respond normally, just provide your response as text.

You can chain multiple tool uses by first analyzing the results and then deciding on next steps.
Always explain your reasoning before using a tool."""
    
    def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process a user message and potentially execute tools.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Dict containing the agent's response and any tool execution results
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages for API call
        messages = [
            {"role": "system", "content": self._build_system_prompt()}
        ] + self.conversation_history
        
        try:
            # Get response from LLM
            response = self._make_api_call(messages)
            assistant_message = response["choices"][0]["message"]["content"]
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Check if the response is a tool call
            tool_result = None
            if assistant_message.strip().startswith("{"):
                try:
                    tool_call = json.loads(assistant_message)
                    if "tool" in tool_call and "parameters" in tool_call:
                        tool_name = tool_call["tool"]
                        parameters = tool_call["parameters"]
                        reasoning = tool_call.get("reasoning", "")
                        
                        # Execute the tool
                        if tool_name in self.tools:
                            tool_result = self.tools[tool_name](**parameters)
                            
                            # Add tool result to conversation
                            result_message = f"Tool '{tool_name}' executed. Result: {json.dumps(tool_result, indent=2)}"
                            self.conversation_history.append({
                                "role": "user",
                                "content": result_message
                            })
                            
                            # Get follow-up response
                            messages = [
                                {"role": "system", "content": self._build_system_prompt()}
                            ] + self.conversation_history
                            
                            follow_up = self._make_api_call(messages)
                            follow_up_message = follow_up["choices"][0]["message"]["content"]
                            
                            self.conversation_history.append({
                                "role": "assistant",
                                "content": follow_up_message
                            })
                            
                            return {
                                "response": follow_up_message,
                                "tool_used": tool_name,
                                "tool_reasoning": reasoning,
                                "tool_result": tool_result
                            }
                except json.JSONDecodeError:
                    pass  # Not a JSON response, treat as normal text
            
            return {
                "response": assistant_message,
                "tool_used": None,
                "tool_result": None
            }
            
        except Exception as e:
            error_message = f"Error processing message: {str(e)}"
            return {
                "response": error_message,
                "tool_used": None,
                "tool_result": None,
                "error": str(e)
            }
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
