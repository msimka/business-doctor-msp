"""
Wizard of Oz Implementation for Business Doctor Intake System
Phase 1: Human-piloted AI for first 10 clients
"""

import streamlit as st
import asyncio
from datetime import datetime
import json
from typing import Dict, List, Optional
import pandas as pd
import plotly.graph_objects as go
from dataclasses import dataclass, asdict
import google.generativeai as genai

# Initialize Gemini client
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
gemini = genai.GenerativeModel('gemini-pro')

@dataclass
class ConversationState:
    """Track conversation progress and insights"""
    client_name: str
    industry: str
    stage: str = "opening"
    topics_covered: List[str] = None
    bottlenecks: List[Dict] = None
    insights: List[Dict] = None
    process_map: Dict = None
    roi_calculations: Dict = None
    confidence_scores: Dict = None
    duration_minutes: int = 0
    
    def __post_init__(self):
        if self.topics_covered is None:
            self.topics_covered = []
        if self.bottlenecks is None:
            self.bottlenecks = []
        if self.insights is None:
            self.insights = []

class WizardOfOzInterface:
    """Dual interface for operator and client during pilot phase"""
    
    def __init__(self):
        if 'conversation_state' not in st.session_state:
            st.session_state.conversation_state = ConversationState(
                client_name="",
                industry=""
            )
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'operator_notes' not in st.session_state:
            st.session_state.operator_notes = []
            
    def render(self):
        """Render appropriate interface based on URL parameter"""
        query_params = st.query_params
        
        if query_params.get("mode") == "operator":
            self.render_operator_view()
        else:
            self.render_client_view()
    
    def render_client_view(self):
        """Client-facing Glass Box interface"""
        st.set_page_config(
            page_title="Business Doctor AI Consultation",
            page_icon="🏥",
            layout="wide"
        )
        
        # Header
        st.title("🏥 Business Doctor AI Consultation")
        st.caption("I'm here to help diagnose and transform your business operations")
        
        # Three-column layout
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            self._render_conversation_area()
            
        with col2:
            self._render_ai_reasoning_panel()
            
        with col3:
            self._render_impact_metrics()
            
        # Bottom area for process visualization
        if st.session_state.conversation_state.process_map:
            st.header("📊 Your Business Process Map")
            self._render_process_map()
            
        # Progress bar
        progress = len(st.session_state.conversation_state.topics_covered) / 8
        st.progress(progress)
        st.caption(f"Progress: {progress:.0%} complete ({st.session_state.conversation_state.duration_minutes} minutes)")
    
    def _render_conversation_area(self):
        """Chat interface for client"""
        st.header("💬 Our Conversation")
        
        # Display message history
        message_container = st.container(height=400)
        with message_container:
            for msg in st.session_state.messages:
                if msg["role"] == "assistant":
                    st.chat_message("assistant", avatar="🏥").write(msg["content"])
                else:
                    st.chat_message("user", avatar="👤").write(msg["content"])
        
        # Input area
        if prompt := st.chat_input("Type your response here..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Show typing indicator
            with st.spinner("Business Doctor is analyzing..."):
                # In pilot phase, wait for operator response
                asyncio.run(self._wait_for_operator_response())
    
    def _render_ai_reasoning_panel(self):
        """Show AI's thinking process"""
        st.header("🧠 AI Analysis")
        
        state = st.session_state.conversation_state
        
        # Current insights
        if state.insights:
            st.subheader("Key Insights")
            for insight in state.insights[-3:]:  # Show last 3
                st.info(f"💡 {insight['text']}")
                st.caption(f"Confidence: {insight['confidence']:.0%}")
        
        # Identified bottlenecks
        if state.bottlenecks:
            st.subheader("Bottlenecks Identified")
            for bottleneck in state.bottlenecks:
                col1, col2 = st.columns(2)
                with col1:
                    st.error(f"🚫 {bottleneck['name']}")
                with col2:
                    st.metric("Impact", f"{bottleneck['hours_weekly']} hrs/week")
        
        # Current analysis focus
        st.subheader("Currently Analyzing")
        st.write(f"📍 {state.stage.replace('_', ' ').title()}")
    
    def _render_impact_metrics(self):
        """Show running ROI calculations"""
        st.header("💰 Impact")
        
        roi = st.session_state.conversation_state.roi_calculations or {}
        
        st.metric(
            "Time Savings",
            f"{roi.get('hours_saved_weekly', 0)} hrs/week",
            f"{roi.get('hours_saved_yearly', 0)} hrs/year"
        )
        
        st.metric(
            "Cost Savings",
            f"${roi.get('cost_savings_monthly', 0):,.0f}/mo",
            f"${roi.get('cost_savings_yearly', 0):,.0f}/year"
        )
        
        if roi.get('roi_percentage'):
            st.metric(
                "Projected ROI",
                f"{roi.get('roi_percentage', 0):.0f}%",
                "First Year"
            )
    
    def render_operator_view(self):
        """Hidden operator interface for pilot phase"""
        st.set_page_config(
            page_title="Operator Console - Business Doctor",
            page_icon="🎛️",
            layout="wide"
        )
        
        st.title("🎛️ Wizard of Oz Operator Console")
        
        # Sidebar controls
        with st.sidebar:
            st.header("Quick Actions")
            
            # Conversation stage selector
            stage = st.selectbox(
                "Conversation Stage",
                ["opening", "discovery", "deep_dive", "synthesis"],
                index=["opening", "discovery", "deep_dive", "synthesis"].index(
                    st.session_state.conversation_state.stage
                )
            )
            st.session_state.conversation_state.stage = stage
            
            # Quick metrics update
            st.subheader("Update Metrics")
            hours_saved = st.number_input("Hours Saved/Week", 0, 100, 10)
            cost_savings = hours_saved * 75 * 4  # $75/hr * 4 weeks
            
            if st.button("Update ROI"):
                st.session_state.conversation_state.roi_calculations = {
                    "hours_saved_weekly": hours_saved,
                    "hours_saved_yearly": hours_saved * 52,
                    "cost_savings_monthly": cost_savings,
                    "cost_savings_yearly": cost_savings * 12,
                    "roi_percentage": (cost_savings * 12 / 50000) * 100
                }
        
        # Main area - dual view
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("🤖 AI Suggestions")
            self._render_ai_suggestions()
            
        with col2:
            st.header("📝 Response Composer")
            self._render_response_composer()
        
        # Bottom area - insights and process mapping
        col3, col4 = st.columns([1, 1])
        
        with col3:
            st.header("💡 Insight Builder")
            self._render_insight_builder()
            
        with col4:
            st.header("🗺️ Process Mapper")
            self._render_process_mapper()
    
    def _render_ai_suggestions(self):
        """Show AI-generated response options"""
        if st.session_state.messages:
            last_user_message = next(
                (msg for msg in reversed(st.session_state.messages) 
                 if msg["role"] == "user"), 
                None
            )
            
            if last_user_message and st.button("🤖 Generate AI Suggestions"):
                suggestions = self._generate_ai_suggestions(last_user_message["content"])
                
                for i, suggestion in enumerate(suggestions):
                    if st.button(f"Use Suggestion {i+1}", key=f"sugg_{i}"):
                        st.session_state.operator_response = suggestion
                    
                    with st.expander(f"Suggestion {i+1}"):
                        st.write(suggestion)
    
    def _render_response_composer(self):
        """Compose and send responses to client"""
        response = st.text_area(
            "Compose Response",
            value=st.session_state.get('operator_response', ''),
            height=200,
            key="response_composer"
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎯 Send to Client", type="primary"):
                if response:
                    # Add to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    # Clear composer
                    st.session_state.operator_response = ""
                    st.rerun()
        
        with col2:
            if st.button("💾 Save as Template"):
                self._save_template(response)
        
        with col3:
            confidence = st.slider("Confidence", 0, 100, 85)
            st.session_state.current_confidence = confidence / 100
    
    def _render_insight_builder(self):
        """Build insights to show in reasoning panel"""
        insight_text = st.text_input("New Insight")
        insight_confidence = st.slider("Insight Confidence", 0, 100, 80, key="insight_conf")
        
        if st.button("➕ Add Insight"):
            if insight_text:
                st.session_state.conversation_state.insights.append({
                    "text": insight_text,
                    "confidence": insight_confidence / 100,
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()
        
        # Bottleneck builder
        st.subheader("Bottleneck Identifier")
        bottleneck_name = st.text_input("Bottleneck Name")
        bottleneck_hours = st.number_input("Hours/Week Impact", 0, 50, 5)
        
        if st.button("🚫 Add Bottleneck"):
            if bottleneck_name:
                st.session_state.conversation_state.bottlenecks.append({
                    "name": bottleneck_name,
                    "hours_weekly": bottleneck_hours,
                    "cost_impact": bottleneck_hours * 75 * 4
                })
                st.rerun()
    
    def _render_process_mapper(self):
        """Quick process mapping tool"""
        if st.button("🗺️ Generate Sample Process Map"):
            # Create sample process map
            st.session_state.conversation_state.process_map = {
                "steps": [
                    {"name": "Lead Capture", "x": 0, "y": 1, "is_bottleneck": False},
                    {"name": "Manual Entry", "x": 1, "y": 1, "is_bottleneck": True},
                    {"name": "Follow-up", "x": 2, "y": 1, "is_bottleneck": True},
                    {"name": "Qualification", "x": 3, "y": 1, "is_bottleneck": False},
                    {"name": "Close", "x": 4, "y": 1, "is_bottleneck": False}
                ],
                "connections": [
                    {"x_coords": [0, 1], "y_coords": [1, 1]},
                    {"x_coords": [1, 2], "y_coords": [1, 1]},
                    {"x_coords": [2, 3], "y_coords": [1, 1]},
                    {"x_coords": [3, 4], "y_coords": [1, 1]}
                ]
            }
            st.success("Process map generated!")
    
    def _generate_ai_suggestions(self, user_message: str) -> List[str]:
        """Generate response suggestions using AI"""
        try:
            prompt = f"""As a Business Doctor AI conducting intake, suggest 3 different responses to this client message. 
            Make them conversational, insightful, and focused on understanding their business deeply.
            
            Client message: {user_message}
            
            Current stage: {st.session_state.conversation_state.stage}
            Topics covered: {st.session_state.conversation_state.topics_covered}
            
            Provide 3 different response options, separated by ---"""
            
            response = gemini.generate_content(prompt)
            
            suggestions = response.text.split("---")
            return [s.strip() for s in suggestions if s.strip()][:3]
            
        except Exception as e:
            st.error(f"Error generating suggestions: {e}")
            return ["I understand. Let me dig deeper into that...", 
                    "That's interesting. Can you tell me more about...",
                    "I see the challenge there. How does this impact..."]
    
    def _render_process_map(self):
        """Render interactive process visualization"""
        process_data = st.session_state.conversation_state.process_map
        
        fig = go.Figure()
        
        # Add nodes
        for step in process_data['steps']:
            fig.add_trace(go.Scatter(
                x=[step['x']], 
                y=[step['y']],
                mode='markers+text',
                marker=dict(
                    size=60,
                    color='red' if step['is_bottleneck'] else 'lightblue',
                    line=dict(width=2, color='DarkSlateGrey')
                ),
                text=step['name'],
                textposition="bottom center",
                name=step['name']
            ))
        
        # Add connections
        for connection in process_data['connections']:
            fig.add_trace(go.Scatter(
                x=connection['x_coords'],
                y=connection['y_coords'],
                mode='lines',
                line=dict(width=3, color='gray'),
                showlegend=False
            ))
        
        fig.update_layout(
            showlegend=False,
            height=300,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    async def _wait_for_operator_response(self):
        """Wait for operator to compose response"""
        # In real implementation, this would poll for updates
        await asyncio.sleep(1)
    
    def _save_template(self, response: str):
        """Save response as template for future use"""
        if 'response_templates' not in st.session_state:
            st.session_state.response_templates = []
        
        st.session_state.response_templates.append({
            "text": response,
            "stage": st.session_state.conversation_state.stage,
            "timestamp": datetime.now().isoformat()
        })
        st.success("Template saved!")

# Main execution
if __name__ == "__main__":
    woz = WizardOfOzInterface()
    woz.render()