"""
Chatbot API routes.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from services.chatbot_service import ChatbotService

chat_bp = Blueprint("chat", __name__)

chatbot = ChatbotService()


@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Receive a user message and return the AI response.
    """

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "success": False,
                    "message": "Invalid request."
                }
            ), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify(
                {
                    "success": False,
                    "message": "Message cannot be empty."
                }
            ), 400

        ai_response = chatbot.get_response(user_message)

        return jsonify(
            {
                "success": True,
                "response": ai_response
            }
        )

    except Exception as e:

        print(e)

        return jsonify(
            {
                "success": False,
                "message": "Internal Server Error."
            }
        ), 500
