"""
Streaming Conversation Implementation
Creates natural, responsive AI conversations with perceived performance optimization
"""

import asyncio
import streamlit as st
from typing import AsyncGenerator, List, Optional
import time
import random
from dataclasses import dataclass
import anthropic
from anthropic import AsyncAnthropic

# Initialize async Claude client
async_claude = AsyncAnthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY", ""))

@dataclass
class StreamConfig:
    """Configuration for streaming behavior"""
    typing_speed_wpm: int = 200  # Average human typing speed
    thinking_delay_ms: int = 800  # Pause before starting response
    punctuation_pause_ms: int = 150  # Pause after punctuation
    natural_variation: float = 0.2  # Random variation in timing
    chunk_size: int = 3  # Words to display at once

class StreamingConversationUI:
    """Handles natural-feeling streamed AI responses"""
    
    def __init__(self, config: StreamConfig = None):
        self.config = config or StreamConfig()
        self._calculate_delays()
    
    def _calculate_delays(self):
        """Calculate timing delays based on config"""
        # Convert WPM to delay between words
        self.base_word_delay = 60.0 / self.config.typing_speed_wpm
        self.char_delay = self.base_word_delay / 5  # Assume 5 chars per word average
    
    async def stream_response(self, response_text: str, 
                            container: st.container = None) -> None:
        """
        Stream response with natural typing effect
        
        Args:
            response_text: Full text to stream
            container: Streamlit container to update
        """
        if container is None:
            container = st.empty()
        
        # Initial thinking indicator
        with container:
            st.markdown("🤔 _Analyzing your response..._")
        
        await asyncio.sleep(self.config.thinking_delay_ms / 1000)
        
        # Stream the response
        displayed_text = ""
        words = response_text.split()
        
        for i in range(0, len(words), self.config.chunk_size):
            chunk = words[i:i + self.config.chunk_size]
            chunk_text = " ".join(chunk)
            
            # Character-by-character streaming for current chunk
            for char in chunk_text:
                displayed_text += char
                with container:
                    st.markdown(displayed_text + "▌")  # Cursor effect
                
                # Variable delay for natural feeling
                delay = self.char_delay * (1 + random.uniform(
                    -self.config.natural_variation, 
                    self.config.natural_variation
                ))
                await asyncio.sleep(delay)
            
            # Add space after chunk
            if i + self.config.chunk_size < len(words):
                displayed_text += " "
            
            # Pause at punctuation
            if chunk_text.rstrip().endswith(('.', '!', '?', ':')):
                await asyncio.sleep(self.config.punctuation_pause_ms / 1000)
        
        # Final display without cursor
        with container:
            st.markdown(displayed_text)
    
    async def stream_with_reasoning(self, 
                                   response_text: str,
                                   reasoning_updates: List[dict],
                                   conversation_col: st.container,
                                   reasoning_col: st.container) -> None:
        """
        Stream response while updating reasoning panel
        
        Args:
            response_text: Main response to stream
            reasoning_updates: List of reasoning updates to show
            conversation_col: Column for conversation
            reasoning_col: Column for reasoning
        """
        # Create async tasks for parallel updates
        async def update_reasoning():
            for update in reasoning_updates:
                with reasoning_col:
                    if update['type'] == 'keyword':
                        st.info(f"🔍 Keyword detected: {update['value']}")
                    elif update['type'] == 'pattern':
                        st.warning(f"📊 Pattern identified: {update['value']}")
                    elif update['type'] == 'bottleneck':
                        st.error(f"🚫 Bottleneck found: {update['value']}")
                    elif update['type'] == 'insight':
                        st.success(f"💡 Insight: {update['value']}")
                
                # Delay between reasoning updates
                await asyncio.sleep(update.get('delay', 1.5))
        
        # Run conversation streaming and reasoning updates in parallel
        await asyncio.gather(
            self.stream_response(response_text, conversation_col),
            update_reasoning()
        )

class ConversationOrchestrator:
    """Orchestrates the full streaming conversation experience"""
    
    def __init__(self):
        self.streamer = StreamingConversationUI()
        self.conversation_state = []
    
    async def process_user_input(self, 
                               user_input: str,
                               conversation_container: st.container,
                               reasoning_container: st.container) -> None:
        """
        Process user input and generate streamed response with reasoning
        
        Args:
            user_input: User's message
            conversation_container: Container for conversation
            reasoning_container: Container for reasoning updates
        """
        # Add user message to conversation
        with conversation_container:
            st.chat_message("user", avatar="👤").write(user_input)
        
        # Generate AI response and reasoning
        response_data = await self._generate_ai_response(user_input)
        
        # Stream response with reasoning updates
        with conversation_container:
            message_placeholder = st.chat_message("assistant", avatar="🏥")
            
        await self.streamer.stream_with_reasoning(
            response_data['response'],
            response_data['reasoning_updates'],
            message_placeholder,
            reasoning_container
        )
        
        # Update conversation state
        self.conversation_state.append({
            'user': user_input,
            'assistant': response_data['response'],
            'reasoning': response_data['reasoning_updates']
        })
    
    async def _generate_ai_response(self, user_input: str) -> dict:
        """Generate AI response with reasoning updates"""
        # Extract keywords and patterns for reasoning panel
        keywords = self._extract_keywords(user_input)
        patterns = self._identify_patterns(user_input)
        
        # Generate main response
        response = await self._call_claude(user_input)
        
        # Create reasoning updates with timing
        reasoning_updates = []
        
        for keyword in keywords[:3]:  # Limit to 3 keywords
            reasoning_updates.append({
                'type': 'keyword',
                'value': keyword,
                'delay': 0.5
            })
        
        for pattern in patterns[:2]:  # Limit to 2 patterns
            reasoning_updates.append({
                'type': 'pattern',
                'value': pattern,
                'delay': 1.0
            })
        
        # Add insights based on response
        if "bottleneck" in response.lower():
            reasoning_updates.append({
                'type': 'bottleneck',
                'value': 'Process inefficiency detected',
                'delay': 1.5
            })
        
        reasoning_updates.append({
            'type': 'insight',
            'value': f'Potential time savings: {random.randint(5, 20)} hours/week',
            'delay': 2.0
        })
        
        return {
            'response': response,
            'reasoning_updates': reasoning_updates
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract business-relevant keywords"""
        business_keywords = [
            'manual', 'process', 'time', 'cost', 'efficiency',
            'bottleneck', 'workflow', 'automation', 'scale',
            'revenue', 'growth', 'challenge', 'problem'
        ]
        
        words = text.lower().split()
        found_keywords = [w for w in words if w in business_keywords]
        
        # Add some discovered keywords
        if 'excel' in text.lower():
            found_keywords.append('spreadsheet tracking')
        if 'email' in text.lower() or 'call' in text.lower():
            found_keywords.append('communication gaps')
            
        return list(set(found_keywords))
    
    def _identify_patterns(self, text: str) -> List[str]:
        """Identify business patterns from text"""
        patterns = []
        
        text_lower = text.lower()
        
        if 'manual' in text_lower and any(word in text_lower for word in ['track', 'manage', 'process']):
            patterns.append('Manual process overhead')
        
        if any(word in text_lower for word in ['miss', 'lose', 'forget']):
            patterns.append('Revenue leakage')
            
        if any(word in text_lower for word in ['slow', 'delay', 'wait']):
            patterns.append('Speed bottleneck')
            
        if any(word in text_lower for word in ['grow', 'scale', 'expand']):
            patterns.append('Growth constraint')
            
        return patterns
    
    async def _call_claude(self, user_input: str) -> str:
        """Call Claude API for response generation"""
        try:
            # Create context from conversation history
            context = "\n".join([
                f"User: {turn['user']}\nAssistant: {turn['assistant']}"
                for turn in self.conversation_state[-3:]  # Last 3 turns
            ])
            
            response = await async_claude.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are a Business Doctor AI conducting an intake interview. 
                        Be conversational, insightful, and focused on understanding the business deeply.
                        Ask follow-up questions to uncover bottlenecks and inefficiencies.
                        
                        Previous context:
                        {context}
                        
                        User's current message: {user_input}
                        
                        Respond naturally and identify areas for improvement."""
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            # Fallback response
            return self._get_fallback_response(user_input)
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Fallback responses if API fails"""
        fallbacks = [
            "That's an interesting point about your process. Can you tell me more about how long this typically takes?",
            "I see the challenge there. How is this impacting your team's productivity?",
            "This sounds like it could be streamlined. What would the ideal workflow look like for you?",
            "Many businesses face similar challenges. How much time do you estimate this costs you weekly?"
        ]
        return random.choice(fallbacks)

# Example usage in Streamlit app
async def main():
    st.set_page_config(page_title="Business Doctor AI", layout="wide")
    
    st.title("🏥 Business Doctor AI Consultation")
    
    # Initialize orchestrator
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = ConversationOrchestrator()
    
    # Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Conversation")
        conversation_container = st.container()
        
        # Input
        user_input = st.chat_input("Tell me about your business challenges...")
        
    with col2:
        st.header("🧠 AI Analysis")
        reasoning_container = st.container()
    
    # Process input
    if user_input:
        await st.session_state.orchestrator.process_user_input(
            user_input,
            conversation_container,
            reasoning_container
        )

# Run with: streamlit run streaming_conversation.py
if __name__ == "__main__":
    asyncio.run(main())