# -*- coding: utf-8 -*-
"""
AgroChat - Main Streamlit Application
Frontend chat interface with mock bot responses
Demonstrates structured JSON responses with rich visualizations
"""

import streamlit as st
from typing import Dict, Any, List
from datetime import datetime
import random

# Import custom components
import requests
from components.bot_reply_renderer import BotReplyRenderer
from components.visual_dispatcher import VisualizationDispatcher


# ============================================================================
# CHAT MANAGER - Session State Management
# ============================================================================

class ChatManager:
    """Manages chat session state and history"""
    
    SESSION_KEY_HISTORY = "chat_history"
    SESSION_KEY_USER_INPUT = "user_input"
    
    @staticmethod
    def init_session_state() -> None:
        """Initialize session state if not already done"""
        if ChatManager.SESSION_KEY_HISTORY not in st.session_state:
            st.session_state[ChatManager.SESSION_KEY_HISTORY] = []
        if ChatManager.SESSION_KEY_USER_INPUT not in st.session_state:
            st.session_state[ChatManager.SESSION_KEY_USER_INPUT] = ""
    
    @staticmethod
    def add_user_message(text: str) -> None:
        """Add user message to history"""
        ChatManager.init_session_state()
        message = {
            "role": "user",
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        st.session_state[ChatManager.SESSION_KEY_HISTORY].append(message)
    
    @staticmethod
    def add_bot_message(response: Dict[str, Any]) -> None:
        """Add bot response to history"""
        ChatManager.init_session_state()
        message = {
            "role": "bot",
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        st.session_state[ChatManager.SESSION_KEY_HISTORY].append(message)
    
    @staticmethod
    def get_history() -> List[Dict[str, Any]]:
        """Get full chat history"""
        ChatManager.init_session_state()
        return st.session_state[ChatManager.SESSION_KEY_HISTORY]
    
    @staticmethod
    def clear_history() -> None:
        """Clear chat history"""
        st.session_state[ChatManager.SESSION_KEY_HISTORY] = []


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="ArgoChat - AI Assistant",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional chat UI
st.markdown(
    """
    <style>
    /* Root variables - Dark theme (default) */
    :root {
        --primary: #0F172A;
        --secondary: #1E293B;
        --tertiary: #334155;
        --accent: #3B82F6;
        --accent-light: #60A5FA;
        --text-primary: #F1F5F9;
        --text-secondary: #CBD5E1;
        --border: #475569;
        --surface: #1E293B;
        --surface-light: #334155;
        --radius: 6px;
        --transition: all 0.2s ease;
    }
    
    /* Layout adjustments for ChatGPT-like appearance */
    .block-container {
        max-width: 850px !important;
        margin: 0 auto !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* Light mode theme variables */
    @media (prefers-color-scheme: light) {
        :root {
            --primary: #FFFFFF;
            --secondary: #F8FAFC;
            --tertiary: #F1F5F9;
            --accent: #3B82F6;
            --accent-light: #2563EB;
            --text-primary: #0F172A;
            --text-secondary: #334155;
            --border: #E2E8F0;
            --surface: #F1F5F9;
            --surface-light: #E2E8F0;
        }
    }
    
    /* Chat message wrapper for proper alignment */
    .chat-message-user {
        display: flex;
        justify-content: flex-end;
        margin: 12px 0;
        animation: slideInRight 0.3s ease-out;
        padding: 0 0;
        width: 100%;
    }
    
    .chat-message-bot {
        display: flex;
        justify-content: flex-start;
        margin: 12px 0;
        animation: slideInLeft 0.3s ease-out;
        padding: 0 0;
        width: 100%;
    }
    
    /* Slide-in animations */
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-12px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(12px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Chat container - Centered like ChatGPT */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 0;
        padding: 16px 40px;
        max-width: 800px;
        margin: 0 auto;
        width: 100%;
    }
    
    /* User message - Clean rectangle */
    .user-bubble {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: #FFFFFF;
        padding: 12px 18px;
        border-radius: 16px;
        border-bottom-right-radius: 4px;
        max-width: 85%;
        word-break: normal;
        overflow-wrap: anywhere;
        white-space: pre-wrap;
        font-size: 16px;
        line-height: 1.5;
        font-weight: 400;
        letter-spacing: 0;
        box-shadow: 0 1px 2px rgba(59, 130, 246, 0.12);
        margin-left: auto;
        margin-right: 0;
        transition: var(--transition);
        backdrop-filter: blur(2px);
        display: inline-block;
        min-width: 120px;
        width: fit-content;
        box-sizing: border-box;
    }
    
    .user-bubble:hover {
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.18);
        transform: translateY(-1px);
    }
    
    /* Bot message - Soft background */
    .bot-bubble {
        background: color-mix(in srgb, currentColor 5%, transparent);
        color: inherit;
        padding: 12px 18px;
        border-radius: 16px;
        border-bottom-left-radius: 4px;
        max-width: 85%;
        word-break: normal;
        overflow-wrap: anywhere;
        white-space: pre-wrap;
        font-size: 16px;
        line-height: 1.5;
        font-weight: 400;
        letter-spacing: 0;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
        border: 1px solid color-mix(in srgb, currentColor 12%, transparent);
        margin-left: 0;
        margin-right: auto;
        transition: var(--transition);
        display: inline-block;
        min-width: 120px;
        width: fit-content;
        box-sizing: border-box;
    }
    
    .bot-bubble:hover {
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
        background: color-mix(in srgb, currentColor 8%, transparent);
    }
    
    /* Message timestamp styling */
    .message-time {
        font-size: 11px;
        color: var(--text-secondary);
        margin-top: 6px;
        opacity: 0.7;
        letter-spacing: 0.3px;
    }
    
    .user-time {
        text-align: right;
        padding-right: 2px;
    }
    
    .bot-time {
        text-align: left;
        padding-left: 2px;
    }
    
    /* Typography improvements */
    .chat-container h1 {
        font-size: 28px;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin-bottom: 16px;
        color: var(--text-primary);
    }
    
    .chat-container h2 {
        font-size: 20px;
        font-weight: 600;
        letter-spacing: -0.3px;
        margin-top: 20px;
        margin-bottom: 12px;
        color: var(--text-primary);
    }
    
    .chat-container h3 {
        font-size: 16px;
        font-weight: 500;
        margin-top: 16px;
        margin-bottom: 10px;
        color: var(--text-secondary);
    }
    
    /* Section headers - Clean dividers */
    .section-header {
        color: var(--accent-light);
        font-weight: 500;
        border-bottom: 1px solid var(--border);
        padding-bottom: 12px;
        margin: 18px 0 12px 0;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    @media (prefers-color-scheme: light) {
        .section-header {
            color: var(--accent);
        }
    }
    
    /* Dividers - Subtle */
    hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 16px 0;
    }
    
    /* Text emphasis */
    strong {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    em {
        color: var(--text-secondary);
        font-style: italic;
    }
    
    /* Code blocks - Readable */
    code {
        background: rgba(255, 255, 255, 0.04);
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 13px;
        color: #A8E6CF;
        font-family: 'Menlo', 'Monaco', monospace;
    }
    
    pre {
        background: rgba(15, 23, 42, 0.8);
        padding: 12px;
        border-radius: var(--radius);
        border: 1px solid rgba(255, 255, 255, 0.05);
        overflow-x: auto;
    }
    
    /* Link styling - Minimal */
    a {
        color: var(--accent);
        text-decoration: none;
        border-bottom: 1px solid transparent;
        transition: var(--transition);
    }
    
    a:hover {
        border-bottom-color: var(--accent);
    }
    
    /* List styling - Clean */
    ul, ol {
        margin: 8px 0;
        padding-left: 20px;
    }
    
    li {
        margin: 6px 0;
        color: var(--text-primary);
    }
    
    /* Blockquote - Soft emphasis */
    blockquote {
        border-left: 3px solid var(--accent);
        padding-left: 12px;
        margin: 12px 0;
        color: var(--text-secondary);
        font-style: italic;
    }
    
    /* ========================================================================
       SIDEBAR STYLING - Clean & Lightweight with Mode Support
       ======================================================================== */
    
    /* Sidebar container - Refined spacing */
    [data-testid="stSidebar"] {
        background: var(--primary);
        transition: background 0.3s ease;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }
    }
    
    [data-testid="stSidebar"] > div {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Sidebar header - Brand section */
    [data-testid="stSidebar"] h1 {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0 !important;
        padding-top: 0px !important;
        display: inline-block;
        color: var(--text-primary);
        line-height: 1.2;
    }
    
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
        padding-bottom: 0px !important;
    }

    /* Target the container directly around the h1 and subheader */
    [data-testid="stSidebar"] > div > div:first-child > div:first-child em {
        font-size: 18px;
        opacity: 0.7;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        font-weight: 500;
        margin-top: 4px;
        display: block;
    }
    
    /* Section dividers - Subtle */
    [data-testid="stSidebar"] hr {
        margin: 18px 0;
        opacity: 0.4;
    }
    
    /* Sidebar section headers */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 20px;
        font-weight: 600;
        letter-spacing: 0.4px;
        text-transform: uppercase;
        margin: 18px 0 12px 0;
        color: var(--text-secondary);
        opacity: 0.9;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--text-primary);
            opacity: 1;
        }
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 16px;
        margin: 16px 0 10px 0;
    }
    
    /* Make collapse button always visible */
    [data-testid="stSidebarCollapseButton"] svg {
        opacity: 1 !important;
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebarCollapseButton"] {
        opacity: 1 !important;
        background-color: transparent !important;
    }
    [data-testid="stSidebarCollapseButton"]:hover {
        background-color: rgba(128, 128, 128, 0.1) !important;
    }
    
    /* Buttons - Lightweight & clean with subtle interactions */
    [data-testid="stSidebar"] button {
        background: transparent !important;
        color: inherit !important;
        border: none !important;
        border-radius: var(--radius) !important;
        font-size: 16px;
        font-weight: 500;
        padding: 6px 12px !important;
        margin: 0 !important;
        transition: background 0.12s ease, color 0.12s ease !important;
        letter-spacing: 0.2px;
        box-shadow: none !important;
        cursor: pointer;
        text-align: left !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Target the inner container of sidebar buttons to ensure text left alignment */
    [data-testid="stSidebar"] button > div > p {
        text-align: left !important;
        width: 100%;
        margin: 0 !important;
    }
    
    /* Remove vertical spacing placed BY STREAMLIT around the button containers */
    [data-testid="stSidebar"] div.stButton {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] div.stButton > button {
        margin: 0 !important;
    }
    
    /* Eliminate gap added by element containers */
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        gap: 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stSidebar"] button {
            background: transparent !important;
            border: none !important;
            color: inherit !important;
        }
        
        [data-testid="stSidebar"] button:hover {
            background: rgba(0, 0, 0, 0.05) !important;
            box-shadow: none !important;
        }
        
        [data-testid="stSidebar"] button:active {
            background: rgba(0, 0, 0, 0.1) !important;
            box-shadow: none !important;
        }
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: var(--text-primary) !important;
        box-shadow: none !important;
    }
    
    [data-testid="stSidebar"] button:focus {
        outline: none !important;
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1) !important;
    }
    
    [data-testid="stSidebar"] button:active {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: var(--accent) !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Button text alignment - Icon + text */
    [data-testid="stSidebar"] button span {
        letter-spacing: 0.2px;
    }
    
    /* Checkboxes - Align properly */
    [data-testid="stCheckbox"] {
        display: flex !important;
        align-items: center !important;
    }
    
    [data-testid="stCheckbox"] label {
        display: flex !important;
        align-items: center !important;
        margin: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Ensure the checkbox box is perfectly centered with text */
    [data-testid="stCheckbox"] div[role="checkbox"] {
        margin-right: 8px !important;
        margin-top: 2px !important; /* Small tweak for ideal visual alignment */
    }

    [data-testid="stSidebar"] [role="checkbox"] {
        cursor: pointer;
        transition: opacity 0.12s ease;
    }
    
    [data-testid="stSidebar"] label {
        font-size: 16px !important;
        font-weight: 400;
        color: var(--text-primary);
        cursor: pointer;
        opacity: 0.9;
        transition: opacity 0.12s ease, color 0.12s ease;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stSidebar"] label {
            opacity: 1;
        }
    }
    
    [data-testid="stSidebar"] label:hover {
        opacity: 1;
        color: var(--text-primary);
    }
    
    [data-testid="stSidebar"] label:focus-within {
        opacity: 1;
    }
    
    /* Move sidebar collapse button logic */
    [data-testid="stSidebarHeader"] {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        padding-top: 0.5rem !important;
    }
    
    [data-testid="stSidebarCollapseButton"] {
        position: relative !important;
        right: 0px !important;
    }
    
    /* Light mode Streamlit Dropdown Menu Fix */
    @media (prefers-color-scheme: light) {
        /* Fix dropdown menu text visibility */
        [data-testid="stToolbar"] ul, 
        [data-testid="stToolbar"] li, 
        [data-testid="stToolbar"] span {
            color: #0F172A !important;
        }
        .st-emotion-cache-16idsys p {
            color: #0F172A !important;
        }
    }
    
    /* Selectbox - Lightweight with subtle interactions */
    [data-testid="stSidebar"] [role="listbox"],
    [data-testid="stSidebar"] [role="combobox"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius) !important;
        transition: border-color 0.12s ease, background 0.12s ease, box-shadow 0.12s ease !important;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stSidebar"] [role="listbox"],
        [data-testid="stSidebar"] [role="combobox"] {
            background: rgba(0, 0, 0, 0.02) !important;
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
        }
        
        [data-testid="stSidebar"] [role="listbox"]:hover,
        [data-testid="stSidebar"] [role="combobox"]:hover {
            border-color: rgba(0, 0, 0, 0.12) !important;
            background: rgba(0, 0, 0, 0.04) !important;
        }
    }
    
    [data-testid="stSidebar"] [role="listbox"]:hover,
    [data-testid="stSidebar"] [role="combobox"]:hover {
        border-color: rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }
    
    [data-testid="stSidebar"] [role="listbox"]:focus,
    [data-testid="stSidebar"] [role="combobox"]:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Expander - Minimal with subtle interactions */
    [data-testid="stSidebar"] .streamlit-expander {
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: var(--radius) !important;
        margin: 8px 0 !important;
        transition: border-color 0.12s ease, background 0.12s ease !important;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stSidebar"] .streamlit-expander {
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
        }
        
        [data-testid="stSidebar"] .streamlit-expander:hover {
            border-color: rgba(0, 0, 0, 0.12) !important;
            background: rgba(0, 0, 0, 0.02) !important;
        }
    }
    
    [data-testid="stSidebar"] .streamlit-expander:hover {
        border-color: rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.02) !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expander:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.08) !important;
    }
    
    /* Expander header - Clean with subtle interactions */
    [data-testid="stSidebar"] [data-testid="stExpanderToggleIcon"] {
        opacity: 0.5;
        transition: opacity 0.12s ease;
    }
    
    [data-testid="stSidebar"] .streamlit-expander:hover [data-testid="stExpanderToggleIcon"] {
        opacity: 0.8;
    }
    
    /* Expander content - Better spacing */
    [data-testid="stSidebar"] [role="region"] > div {
        padding: 12px 0 !important;
    }
    
    /* Text in sidebar - Optimize readability */
    [data-testid="stSidebar"] p {
        font-size: 16px;
        line-height: 1.6;
        color: var(--text-primary);
        margin: 8px 0;
    }
    
    [data-testid="stSidebar"] small {
        font-size: 14px;
        color: var(--text-secondary);
        opacity: 0.8;
    }
    
    /* Info boxes - Subtle */
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: var(--radius) !important;
        padding: 10px 12px !important;
        margin: 8px 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stAlert"] > div {
        font-size: 12px;
        color: var(--text-secondary) !important;
    }
    
    /* Lists in sidebar - Clean */
    [data-testid="stSidebar"] ul {
        list-style: none;
        padding-left: 0;
    }
    
    [data-testid="stSidebar"] li {
        padding-left: 0;
        margin: 6px 0;
        font-size: 14px;
        color: var(--text-primary);
    }
    
    [data-testid="stSidebar"] li::before {
        content: "• ";
        color: var(--accent);
        margin-right: 6px;
        opacity: 0.6;
    }
    
    /* Links in sidebar with subtle interactions */
    [data-testid="stSidebar"] a {
        color: var(--accent);
        text-decoration: none;
        opacity: 0.85;
        transition: opacity 0.12s ease, color 0.12s ease, border-bottom-color 0.12s ease;
        border-bottom: 1px solid transparent;
    }
    
    [data-testid="stSidebar"] a:hover {
        opacity: 1;
        border-bottom-color: var(--accent);
    }
    
    [data-testid="stSidebar"] a:focus {
        outline: 2px solid var(--accent);
        outline-offset: 2px;
        border-radius: 2px;
    }
    
    /* ========================================================================
       KEY METRICS CARDS - Data-Focused & Serious
       ======================================================================== */
    
    /* Card container - Clean & calm */
    [data-testid="stMetricRow"] {
        margin-bottom: 8px !important;
    }
    
    /* Metric card wrapper with subtle interactions */
    [data-testid="stMetricRow"] > div > div {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 6px !important;
        padding: 20px !important;
        transition: background 0.12s ease, border-color 0.12s ease, box-shadow 0.12s ease !important;
        cursor: default;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stMetricRow"] > div > div {
            background: rgba(0, 0, 0, 0.02) !important;
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
        }
        
        [data-testid="stMetricRow"] > div > div:hover {
            background: rgba(0, 0, 0, 0.04) !important;
            border-color: rgba(0, 0, 0, 0.12) !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
        }
    }
    
    [data-testid="stMetricRow"] > div > div:hover {
        background: rgba(255, 255, 255, 0.06) !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }
    
    [data-testid="stMetricRow"] > div > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.08) !important;
    }
    
    /* Metric number - Large and dominant */
    [data-testid="stMetricRow"] [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        letter-spacing: -0.7px !important;
        line-height: 1.1 !important;
        margin-bottom: 8px !important;
    }
    
    [data-testid="stMetricRow"] [data-testid="stMetricValue"] > div {
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    
    /* Metric label - Small and serious */
    [data-testid="stMetricRow"] [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        color: var(--text-secondary) !important;
        opacity: 0.85 !important;
        margin: 0 !important;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stMetricRow"] [data-testid="stMetricLabel"] {
            color: var(--text-primary) !important;
            opacity: 1 !important;
        }
    }
    
    /* Metric delta (trend) - Subtle */
    [data-testid="stMetricRow"] [data-testid="stMetricDelta"] {
        font-size: 11px !important;
        font-weight: 500 !important;
        opacity: 0.8 !important;
        margin-top: 8px !important;
    }
    
    /* Custom HTML metric cards from components with subtle interactions */
    div > div > div[style*="padding: 20px"] {
        transition: all 0.12s ease !important;
    }
    
    @media (prefers-color-scheme: light) {
        div > div > div[style*="padding: 20px"]:hover {
            border-color: rgba(0, 0, 0, 0.12) !important;
            background: rgba(0, 0, 0, 0.04) !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
        }
    }
    
    div > div > div[style*="padding: 20px"]:hover {
        border-color: rgba(255, 255, 255, 0.12) !important;
        background: rgba(255, 255, 255, 0.06) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }
    
    div > div > div[style*="padding: 20px"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.08) !important;
    }
    
    /* Metric value inside custom cards */
    div[style*="font-size: 28px"][style*="font-weight: 700"] {
        line-height: 1.1 !important;
        margin-bottom: 6px !important;
    }
    
    /* Metric label inside custom cards */
    div[style*="text-transform: uppercase"][style*="letter-spacing: 0.5px"] {
        opacity: 0.8 !important;
        margin-bottom: 8px !important;
    }
    
    @media (prefers-color-scheme: light) {
        div[style*="text-transform: uppercase"][style*="letter-spacing: 0.5px"] {
            opacity: 1 !important;
        }
    }
    
    /* Trend indicator inside cards */
    div[style*="font-size: 11px"][style*="font-weight: 500"][style*="opacity: 0.85"] {
        margin-top: 8px !important;
        opacity: 0.8 !important;
    }
    
    /* General text improvements for light mode */
    @media (prefers-color-scheme: light) {
        /* Input fields and text areas */
        input[type="text"],
        input[type="number"],
        textarea,
        [role="textbox"] {
            color: var(--text-primary) !important;
        }
        
        /* Placeholder text - lighter in light mode */
        input::placeholder,
        textarea::placeholder {
            color: rgba(15, 23, 42, 0.5) !important;
            opacity: 1 !important;
        }
        
        /* General text visibility */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] small {
            color: var(--text-primary) !important;
            opacity: 1 !important;
        }
        
        /* Links in sidebar */
        [data-testid="stSidebar"] a {
            opacity: 1 !important;
        }
    }
    
    /* Chat input box styling */
    [data-testid="stChatInput"] {
        border-color: var(--accent) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    /* Align chat input bar to exactly match .block-container width */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] > div > div {
        max-width: 850px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        left: 0 !important;
        right: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_api_response(user_text: str) -> Dict[str, Any]:
    """Call the FastAPI backend to get the RAG response."""
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": user_text},
            timeout=120  # generous timeout for local LLM
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "text": f"Backend Error: {response.text}",
                "message_type": "text",
                "alert": {"type": "error", "message": f"Server returned {response.status_code}"}
            }
    except requests.exceptions.RequestException as e:
        return {
            "text": "Failed to connect to the backend server. Is it running on port 8000?",
            "message_type": "text",
            "alert": {"type": "error", "message": str(e)}
        }



# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar() -> None:
    """Render sidebar with information and controls"""
    with st.sidebar:
        st.markdown("## 🌊 ARGOCHAT")
        
        st.markdown("---")
        
        # Response type filter
        st.markdown("### Response Types")
        response_types = {
            "All": None,
            "Charts": "chart",
            "Metrics": "insights",
            "Recommendations": "recommendation",
            "Alerts": "alert",
            "Complex": "composite"
        }
        
        selected_type = st.selectbox(
            "Filter by type:",
            options=list(response_types.keys()),
            key="response_type_filter",
            label_visibility="collapsed"
        )
        
        st.session_state["selected_response_type"] = response_types[selected_type]
        
        st.markdown("---")
        
        # Settings
        st.markdown("### Settings")
        
        st.checkbox(
            "Show response metadata",
            value=True,
            key="show_metadata"
        )
        
        st.checkbox(
            "Show raw JSON",
            value=False,
            key="show_raw_json"
        )
        
        st.markdown("---")
        
        # Chat controls
        st.markdown("### Chat Controls")
        
        if st.button("Clear History", key="clear_history", use_container_width=True):
            ChatManager.clear_history()
            st.success("Chat history cleared!")
            st.rerun()
        
        st.markdown("---")
        
        # Footer info
        st.markdown(
            """
            <div style='text-align: center; color: #95A5A6; font-size: 12px;'>
                <p>ArgoChat v1.0</p>
                <p>Frontend Demo</p>
                <p>Built with Streamlit</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================================
# CHAT RENDERING
# ============================================================================

def render_user_message(text: str, timestamp: str = "") -> None:
    """Render user message with clean styling"""
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            time_str = dt.strftime("%H:%M")
        except:
            time_str = "now"
    else:
        time_str = "now"
    
    st.markdown(
        f"""<div class='chat-message-user'><div style='display: flex; flex-direction: column; align-items: flex-end;'><div class='user-bubble'>{text.strip()}</div><div class='message-time user-time'>{time_str}</div></div></div>""",
        unsafe_allow_html=True
    )


def render_bot_message(response: Dict[str, Any]) -> None:
    """Render bot message with full response"""
    if not response:
        st.warning("No response data")
        return
    
    # Render the complete bot response using the renderer
    # The renderer itself will handle standard chat styling using HTML
    BotReplyRenderer.render(response)
    
    # Optional: Show raw JSON
    if st.session_state.get("show_raw_json", False):
        with st.expander("View Raw JSON", expanded=False):
            st.json(response)


def render_chat_history() -> None:
    """Render all messages in chat history"""
    history = ChatManager.get_history()
    
    if not history:
        st.markdown(
            """
            <div style='text-align: center; padding: 40px 20px; color: #95A5A6;'>
                <h2>Welcome to ArgoChat</h2>
                <p>Ask me about the ocean!</p>
                <p style='font-size: 12px; margin-top: 20px;'>
                    Tip: Type your question about oceanographic data below.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        for message in history:
            if message["role"] == "user":
                render_user_message(
                    message.get("text", ""),
                    message.get("timestamp", "")
                )
            else:
                render_bot_message(message.get("response", {}))


# ============================================================================
# INPUT HANDLING
# ============================================================================

def handle_user_input(user_text: str) -> None:
    """Handle user input and signal main loop to generate bot response"""
    if not user_text.strip():
        st.warning("Please enter a message")
        return
    
    # Add user message to history
    ChatManager.add_user_message(user_text)
    
    # Signal the main loop to fetch the AI response on the next render
    st.session_state["pending_user_message"] = user_text
    
    # Rerun immediately so the user's message appears instantly
    st.rerun()


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application function"""
    
    # Initialize session state
    ChatManager.init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main title
    st.markdown("# Chat")
    st.markdown("AI Oceanography Assistant – Get instant insights on ocean data, marine life, currents, and more")
    
    st.markdown("---")
    
    # Handle pending AI response if we just got a user message
    if st.session_state.get("pending_user_message"):
        # First render the chat history including the new user message
        render_chat_history()
        
        pending_msg = st.session_state["pending_user_message"]
        st.session_state["pending_user_message"] = None
        
        # Show spinner and fetch API response
        with st.spinner("AI is thinking..."):
            bot_response = get_api_response(pending_msg)
            ChatManager.add_bot_message(bot_response)
        
        st.rerun()
    else:
        # Chat history
        render_chat_history()
    
    st.markdown("---")
    
    # Input section - Chat input with Enter key support
    # Use chat_input which supports Enter key submission
    user_input = st.chat_input(
        "Type your message and press Enter...",
        key="user_input_field"
    )
    
    # Handle submission (Enter key or programmatic)
    if user_input:
        handle_user_input(user_input)


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
