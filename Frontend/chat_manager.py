"""
Chat Manager
Handles chat history and message flow
"""

import streamlit as st
from typing import List, Dict, Optional
from schemas import BotResponse
from datetime import datetime


class ChatManager:
    """Manages chat state and history"""
    
    SESSION_KEY_HISTORY = "chat_history"
    SESSION_KEY_USER_INPUT = "current_user_input"
    
    @staticmethod
    def init_session_state() -> None:
        """Initialize session state for chat"""
        if ChatManager.SESSION_KEY_HISTORY not in st.session_state:
            st.session_state[ChatManager.SESSION_KEY_HISTORY] = []
        if ChatManager.SESSION_KEY_USER_INPUT not in st.session_state:
            st.session_state[ChatManager.SESSION_KEY_USER_INPUT] = ""
    
    @staticmethod
    def add_user_message(text: str) -> None:
        """Add user message to history"""
        ChatManager.init_session_state()
        st.session_state[ChatManager.SESSION_KEY_HISTORY].append({
            "role": "user",
            "content": text,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    def add_bot_message(response: BotResponse) -> None:
        """Add bot response to history"""
        ChatManager.init_session_state()
        st.session_state[ChatManager.SESSION_KEY_HISTORY].append({
            "role": "bot",
            "content": response.to_dict(),
            "timestamp": response.timestamp
        })
    
    @staticmethod
    def get_history() -> List[Dict]:
        """Get full chat history"""
        ChatManager.init_session_state()
        return st.session_state[ChatManager.SESSION_KEY_HISTORY]
    
    @staticmethod
    def clear_history() -> None:
        """Clear chat history"""
        st.session_state[ChatManager.SESSION_KEY_HISTORY] = []
    
    @staticmethod
    def get_last_n_messages(n: int) -> List[Dict]:
        """Get last N messages from history"""
        history = ChatManager.get_history()
        return history[-n:] if n > 0 else history
    
    @staticmethod
    def set_user_input(text: str) -> None:
        """Set current user input"""
        ChatManager.init_session_state()
        st.session_state[ChatManager.SESSION_KEY_USER_INPUT] = text
    
    @staticmethod
    def get_user_input() -> str:
        """Get current user input"""
        ChatManager.init_session_state()
        return st.session_state.get(ChatManager.SESSION_KEY_USER_INPUT, "")


def render_chat_message(message: Dict, is_user: bool = True) -> None:
    """Render a single chat message"""
    if is_user:
        # User message
        with st.chat_message("user", avatar="👨‍🌾"):
            st.markdown(message["content"])
    else:
        # Bot message (has structured content)
        with st.chat_message("assistant", avatar="🤖"):
            bot_response_dict = message["content"]
            
            # Import here to avoid circular imports
            from components import ResponseRenderer
            
            # Reconstruct BotResponse object from dict
            from schemas import BotResponse, ChartData, InsightCard
            
            insights = None
            if bot_response_dict.get("insights"):
                insights = [
                    InsightCard(**insight) 
                    for insight in bot_response_dict["insights"]
                ]
            
            charts = None
            if bot_response_dict.get("charts"):
                charts = [
                    ChartData(**chart) 
                    for chart in bot_response_dict["charts"]
                ]
            
            response = BotResponse(
                message_id=bot_response_dict.get("message_id", ""),
                timestamp=bot_response_dict.get("timestamp", ""),
                message_type=bot_response_dict.get("message_type", "text"),
                text=bot_response_dict.get("text"),
                insights=insights,
                charts=charts,
                recommendations=bot_response_dict.get("recommendations"),
                alert=bot_response_dict.get("alert"),
                metadata=bot_response_dict.get("metadata")
            )
            
            ResponseRenderer.render_full_response(response)


def render_chat_history(history: List[Dict]) -> None:
    """Render all messages from chat history"""
    for message in history:
        is_user = message["role"] == "user"
        render_chat_message(message, is_user=is_user)


def render_sidebar_options() -> None:
    """Render sidebar with options and suggestions"""
    with st.sidebar:
        st.markdown("### 💬 Quick Commands")
        
        quick_commands = {
            "Crop Health": "How's my crop health today?",
            "Weather": "What's the weather forecast?",
            "Soil Analysis": "Analyze my soil conditions",
            "Pest Alert": "Any pest alerts in my area?",
            "Market Prices": "What are the current market prices?",
            "Recommendations": "What should I plant next season?",
            "Equipment": "Check equipment maintenance status",
        }
        
        for label, command in quick_commands.items():
            if st.button(f"📋 {label}", use_container_width=True, key=f"cmd_{label}"):
                st.session_state["quick_command"] = command
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Chat Options")
        
        if st.button("🗑️ Clear History", use_container_width=True):
            ChatManager.clear_history()
            st.rerun()
        
        if st.button("📋 View Raw JSON", use_container_width=True):
            st.session_state["show_json"] = not st.session_state.get("show_json", False)
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown(
            """
            **AgroChat** - Your AI farming assistant
            
            - 🌾 Crop health monitoring
            - 🌤️ Weather forecasts
            - 🧪 Soil analysis
            - 🚨 Pest alerts
            - 💹 Market insights
            - 🤖 AI recommendations
            
            *Built with Streamlit & structured JSON responses*
            """
        )
