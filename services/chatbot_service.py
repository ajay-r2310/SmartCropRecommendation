"""
AI Chatbot Service using Groq API.
"""

from __future__ import annotations

from groq import Groq

from config import Config


class ChatbotService:
    """Handles AI chatbot responses."""

    def __init__(self):

        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in .env")

        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

        self.system_prompt = """
You are Agro AI.

You are an expert agriculture assistant.

Only answer agriculture-related questions.

You can help with:

• Crop recommendation
• Fertilizers
• Soil health
• Irrigation
• Weather advice
• Pest control
• Plant diseases
• Harvesting
• Organic farming
• Modern agriculture

Rules:

1. Keep answers simple.
2. Use bullet points.
3. Explain in easy English.
4. Maximum 200 words.
5. If the question is unrelated to agriculture,
politely say:

'I am Agro AI. I can only answer agriculture-related questions.'
"""

    def get_response(self, message: str) -> str:

        try:

            chat = self.client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],

                temperature=0.5,

                max_tokens=500

            )

            return chat.choices[0].message.content

        except Exception as e:

            print(e)

            return "Sorry! Agro AI is currently unavailable."
