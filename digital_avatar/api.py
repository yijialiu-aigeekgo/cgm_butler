"""
Flask API for Digital Avatar

This module provides REST API endpoints for the digital avatar functionality.
Can be integrated into the main dashboard or run as a separate service.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from digital_avatar import ConversationManager, AvatarConfig
from digital_avatar.gpt_chat import GPTChatManager

# Create Blueprint
avatar_bp = Blueprint('avatar', __name__, url_prefix='/api/avatar')

# Initialize managers
conversation_manager = None
gpt_chat_manager = None


def init_avatar_api(tavus_api_key: str = None, persona_id: str = None, openai_api_key: str = None):
    """
    Initialize the avatar API.
    
    Args:
        tavus_api_key: Tavus API key
        persona_id: Persona ID
        openai_api_key: OpenAI API key
    """
    global conversation_manager, gpt_chat_manager
    
    # Tavus conversation manager (for video avatar)
    conversation_manager = ConversationManager(
        tavus_api_key=tavus_api_key,
        persona_id=persona_id or AvatarConfig.TAVUS_PERSONA_ID
    )
    
    # GPT chat manager (for text chat)
    gpt_chat_manager = GPTChatManager(api_key=openai_api_key)


@avatar_bp.route('/start', methods=['POST'])
def start_conversation():
    """
    Start a new conversation with the digital avatar.
    
    Request body:
        {
            "user_id": "user_001",
            "config": {  // optional
                "language": "en"
            }
        }
    
    Returns:
        {
            "success": true,
            "conversation_id": "conv_123",
            "user_id": "user_001",
            "message": "Conversation started successfully"
        }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        config = data.get('config')
        
        if not user_id:
            return jsonify({
                "success": False,
                "message": "user_id is required"
            }), 400
        
        result = conversation_manager.start_conversation(user_id, config)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/message', methods=['POST'])
def send_message():
    """
    Send a message in a conversation.
    
    Request body:
        {
            "conversation_id": "conv_123",
            "message": "What's my current glucose level?"
        }
    
    Returns:
        {
            "success": true,
            "conversation_id": "conv_123",
            "user_message": "What's my current glucose level?",
            "avatar_response": "Your current glucose is 120 mg/dL (Normal) ✅",
            "timestamp": "2025-10-27T10:30:00"
        }
    """
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        message = data.get('message')
        
        if not conversation_id or not message:
            return jsonify({
                "success": False,
                "message": "conversation_id and message are required"
            }), 400
        
        result = conversation_manager.send_message(conversation_id, message)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/history/<conversation_id>', methods=['GET'])
def get_history(conversation_id: str):
    """
    Get conversation history.
    
    Returns:
        {
            "success": true,
            "conversation_id": "conv_123",
            "history": [...]
        }
    """
    try:
        result = conversation_manager.get_conversation_history(conversation_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/end/<conversation_id>', methods=['POST'])
def end_conversation(conversation_id: str):
    """
    End a conversation.
    
    Returns:
        {
            "success": true,
            "conversation_id": "conv_123",
            "message": "Conversation ended successfully"
        }
    """
    try:
        result = conversation_manager.end_conversation(conversation_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/active', methods=['GET'])
def get_active_conversations():
    """
    Get list of active conversations.
    
    Returns:
        {
            "success": true,
            "conversations": [
                {
                    "conversation_id": "conv_123",
                    "user_id": "user_001"
                }
            ]
        }
    """
    try:
        conversations = conversation_manager.get_active_conversations()
        return jsonify({
            "success": True,
            "conversations": conversations
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        {
            "status": "ok",
            "module": "digital_avatar",
            "version": "1.0.0"
        }
    """
    return jsonify({
        "status": "ok",
        "module": "digital_avatar",
        "version": "1.0.0",
        "conversation_manager_initialized": conversation_manager is not None,
        "gpt_chat_manager_initialized": gpt_chat_manager is not None
    })


# GPT Chat Endpoints
@avatar_bp.route('/gpt/chat', methods=['POST'])
def gpt_chat():
    """
    GPT-4o聊天端点
    
    Request body:
        {
            "user_id": "user_001",
            "message": "我的血糖是多少？"
        }
    
    Returns:
        {
            "success": true,
            "response": "您的当前血糖是...",
            "function_called": "get_latest_glucose"  // 可选
        }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        message = data.get('message')
        
        if not user_id or not message:
            return jsonify({
                "success": False,
                "message": "user_id and message are required"
            }), 400
        
        result = gpt_chat_manager.chat(user_id, message)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/gpt/start', methods=['POST'])
def gpt_start():
    """
    开始GPT对话
    
    Request body:
        {
            "user_id": "user_001"
        }
    
    Returns:
        {
            "success": true,
            "user_id": "user_001",
            "message": "对话已开始"
        }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                "success": False,
                "message": "user_id is required"
            }), 400
        
        result = gpt_chat_manager.start_conversation(user_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/gpt/end', methods=['POST'])
def gpt_end():
    """
    结束GPT对话并保存到数据库
    
    Request body:
        {
            "user_id": "user_001"
        }
    
    Returns:
        {
            "success": true,
            "conversation_id": "uuid",
            "message": "对话已保存",
            "duration_seconds": 300
        }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                "success": False,
                "message": "user_id is required"
            }), 400
        
        result = gpt_chat_manager.end_conversation(user_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/gpt/history/<user_id>', methods=['GET'])
def gpt_history(user_id: str):
    """
    获取用户的对话历史
    
    Query params:
        - limit: 返回对话数量 (默认 10)
        - days: 天数范围 (默认 7)
    
    Returns:
        {
            "success": true,
            "user_id": "user_001",
            "conversations": [...],
            "stats": {
                "total_conversations": 5,
                "by_type": {"gpt_chat": 3, "tavus_video": 2},
                "follow_up_needed": 1
            }
        }
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        days = request.args.get('days', 7, type=int)
        
        # 获取对话列表
        from database.conversation_manager import ConversationManager
        db = ConversationManager()
        
        conversations = db.get_user_conversations(
            user_id=user_id,
            limit=limit,
            conversation_type='gpt_chat'
        )
        
        # 获取统计信息
        stats = db.get_conversation_stats(user_id, days=days)
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "conversations": conversations,
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@avatar_bp.route('/gpt/clear/<user_id>', methods=['POST'])
def gpt_clear(user_id: str):
    """
    清除GPT对话历史
    
    Returns:
        {
            "success": true,
            "message": "对话历史已清除"
        }
    """
    try:
        gpt_chat_manager.clear_conversation(user_id)
        return jsonify({
            "success": True,
            "message": "对话历史已清除"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# Standalone Flask app for testing
if __name__ == '__main__':
    from flask import Flask
    
    app = Flask(__name__)
    
    # Initialize avatar API
    init_avatar_api()
    
    # Register blueprint
    app.register_blueprint(avatar_bp)
    
    print("\n" + "="*60)
    print("🤖 Digital Avatar API Server")
    print("="*60)
    print("🌐 Running on: http://localhost:5001")
    print("📚 API Endpoints:")
    print("  POST /api/avatar/start - Start conversation")
    print("  POST /api/avatar/message - Send message")
    print("  GET  /api/avatar/history/<id> - Get history")
    print("  POST /api/avatar/end/<id> - End conversation")
    print("  GET  /api/avatar/active - List active conversations")
    print("  GET  /api/avatar/health - Health check")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

