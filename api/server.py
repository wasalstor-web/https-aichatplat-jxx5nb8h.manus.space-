"""
Flask API server for the AI Agent.
Provides REST endpoints for interacting with the agent.
"""

import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from core.agent import AIAgent
from core.tools import get_tool_description

app = Flask(__name__)
CORS(app)

# Global agent instance (in production, use session management)
agents = {}


def get_or_create_agent(session_id: str = "default") -> AIAgent:
    """Get or create an agent for a session."""
    if session_id not in agents:
        agents[session_id] = AIAgent()
    return agents[session_id]


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint."""
    return jsonify({
        "status": "running",
        "service": "AI Agent with Reasoning and Tools",
        "version": "1.0.0"
    })


@app.route('/chat', methods=['POST'])
def chat():
    """
    Process a chat message.
    
    Expected JSON payload:
    {
        "message": "User message",
        "session_id": "optional-session-id"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' in request body"
            }), 400
        
        message = data['message']
        session_id = data.get('session_id', 'default')
        
        agent = get_or_create_agent(session_id)
        result = agent.process_message(message)
        
        # Sanitize result to prevent stack trace exposure
        if 'error' in result:
            # Log the detailed error for debugging
            app.logger.error(f"Agent error for session {session_id}: {result.get('error')}")
            # Return sanitized error to client
            return jsonify({
                "response": "An error occurred while processing your message. Please try again.",
                "tool_used": None,
                "tool_result": None
            }), 500
        
        return jsonify(result)
        
    except ValueError as e:
        # Log the error for debugging (in production, use proper logging)
        app.logger.error(f"ValueError in chat endpoint: {str(e)}")
        return jsonify({
            "error": "Invalid input provided"
        }), 400
    except Exception as e:
        # Log the full error for debugging (in production, use proper logging)
        app.logger.error(f"Exception in chat endpoint: {str(e)}")
        return jsonify({
            "error": "An internal error occurred while processing your request"
        }), 500


@app.route('/reset', methods=['POST'])
def reset_conversation():
    """
    Reset the conversation for a session.
    
    Expected JSON payload:
    {
        "session_id": "optional-session-id"
    }
    """
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        
        if session_id in agents:
            agents[session_id].reset_conversation()
            return jsonify({
                "status": "success",
                "message": f"Conversation reset for session: {session_id}"
            })
        else:
            return jsonify({
                "status": "success",
                "message": "No active session to reset"
            })
            
    except Exception as e:
        app.logger.error(f"Exception in reset endpoint: {str(e)}")
        return jsonify({
            "error": "An internal error occurred while resetting the conversation"
        }), 500


@app.route('/tools', methods=['GET'])
def list_tools():
    """List all available tools and their descriptions."""
    try:
        tools = get_tool_description()
        return jsonify({
            "tools": list(tools.values())
        })
    except Exception as e:
        app.logger.error(f"Exception in tools endpoint: {str(e)}")
        return jsonify({
            "error": "An internal error occurred while listing tools"
        }), 500


@app.route('/history', methods=['GET'])
def get_history():
    """
    Get conversation history for a session.
    
    Query parameters:
    - session_id: optional session identifier
    """
    try:
        session_id = request.args.get('session_id', 'default')
        
        if session_id in agents:
            history = agents[session_id].get_conversation_history()
            return jsonify({
                "session_id": session_id,
                "history": history
            })
        else:
            return jsonify({
                "session_id": session_id,
                "history": []
            })
            
    except Exception as e:
        app.logger.error(f"Exception in history endpoint: {str(e)}")
        return jsonify({
            "error": "An internal error occurred while retrieving conversation history"
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
