"""
Business Doctor Core Engine
Handles all business logic, data processing, and AI interactions
Terminal-based, no GUI dependencies
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
import google.generativeai as genai
from enum import Enum

class ConversationStage(Enum):
    """Stages of the business intake conversation"""
    OPENING = "opening"
    COMPANY_OVERVIEW = "company_overview"
    PAIN_POINTS = "pain_points"
    PROCESS_DISCOVERY = "process_discovery"
    BOTTLENECK_ANALYSIS = "bottleneck_analysis"
    FINANCIAL_IMPACT = "financial_impact"
    SOLUTION_EXPLORATION = "solution_exploration"
    CLOSING = "closing"

@dataclass
class BusinessMetrics:
    """Core business metrics collected during intake"""
    company_name: str = ""
    industry: str = ""
    employee_count: int = 0
    annual_revenue: float = 0.0
    main_services: List[str] = field(default_factory=list)
    technology_stack: List[str] = field(default_factory=list)
    current_challenges: List[str] = field(default_factory=list)

@dataclass
class ProcessBottleneck:
    """Identified process bottleneck with impact analysis"""
    name: str
    description: str
    department: str
    frequency: str  # daily, weekly, monthly
    time_impact_hours: float
    cost_impact: float
    automation_potential: float  # 0-1 scale
    priority: str  # low, medium, high, critical
    
    def calculate_annual_impact(self) -> Tuple[float, float]:
        """Calculate annualized time and cost impact"""
        frequency_multiplier = {
            "daily": 250,  # business days
            "weekly": 52,
            "monthly": 12,
            "quarterly": 4
        }
        multiplier = frequency_multiplier.get(self.frequency.lower(), 12)
        
        annual_hours = self.time_impact_hours * multiplier
        annual_cost = self.cost_impact * multiplier
        
        return annual_hours, annual_cost

@dataclass
class AIInsight:
    """AI-generated insight about the business"""
    category: str
    insight: str
    confidence: float
    supporting_data: List[str]
    potential_value: float
    implementation_effort: str  # low, medium, high

class BusinessDoctorEngine:
    """Core engine for Business Doctor consultations"""
    
    def __init__(self, api_key: str):
        """Initialize with Google Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.metrics = BusinessMetrics()
        self.bottlenecks: List[ProcessBottleneck] = []
        self.insights: List[AIInsight] = []
        self.conversation_history: List[Dict] = []
        self.current_stage = ConversationStage.OPENING
        
    def process_input(self, user_input: str) -> Dict:
        """Process user input and return structured response"""
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Extract information based on current stage
        extracted_data = self._extract_information(user_input)
        
        # Update metrics and findings
        self._update_business_data(extracted_data)
        
        # Generate AI response
        ai_response = self._generate_contextual_response(user_input)
        
        # Add AI response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Determine next stage
        self._advance_conversation_stage()
        
        return {
            "response": ai_response,
            "extracted_data": extracted_data,
            "current_stage": self.current_stage.value,
            "metrics_updated": self._get_metrics_summary(),
            "bottlenecks_found": len(self.bottlenecks),
            "insights_generated": len(self.insights)
        }
    
    def _extract_information(self, user_input: str) -> Dict:
        """Extract structured information from user input"""
        prompt = f"""
        Analyze this business owner's response and extract structured information:
        
        User Input: "{user_input}"
        Current Conversation Stage: {self.current_stage.value}
        
        Extract the following if mentioned:
        1. Company details (name, size, industry)
        2. Financial metrics (revenue, costs)
        3. Process descriptions
        4. Time/efficiency issues
        5. Pain points or challenges
        6. Current tools/technology
        
        Return as JSON with these keys:
        - company_info: dict
        - financial_data: dict
        - processes: list
        - challenges: list
        - metrics: dict
        
        Only include data explicitly mentioned.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Parse JSON from response
            json_str = response.text.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:-3]
            return json.loads(json_str)
        except:
            # Fallback to basic extraction
            return self._basic_extraction(user_input)
    
    def _basic_extraction(self, user_input: str) -> Dict:
        """Basic keyword-based extraction as fallback"""
        extracted = {
            "company_info": {},
            "financial_data": {},
            "processes": [],
            "challenges": [],
            "metrics": {}
        }
        
        # Look for numbers (potential metrics)
        import re
        numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', user_input)
        if numbers:
            extracted["metrics"]["numbers_mentioned"] = numbers
        
        # Look for time indicators
        time_words = ["hours", "minutes", "days", "weeks", "monthly", "daily"]
        for word in time_words:
            if word in user_input.lower():
                extracted["metrics"]["time_mentioned"] = True
                break
        
        # Look for process keywords
        process_keywords = ["process", "workflow", "procedure", "system", "manual", "automate"]
        for keyword in process_keywords:
            if keyword in user_input.lower():
                extracted["processes"].append(f"Mentioned: {keyword}")
        
        return extracted
    
    def _update_business_data(self, extracted_data: Dict):
        """Update business metrics and identify bottlenecks"""
        # Update company info
        if company_info := extracted_data.get("company_info"):
            if "name" in company_info:
                self.metrics.company_name = company_info["name"]
            if "employee_count" in company_info:
                self.metrics.employee_count = company_info["employee_count"]
            if "industry" in company_info:
                self.metrics.industry = company_info["industry"]
        
        # Update financial data
        if financial_data := extracted_data.get("financial_data"):
            if "revenue" in financial_data:
                self.metrics.annual_revenue = financial_data["revenue"]
        
        # Process challenges into bottlenecks
        if challenges := extracted_data.get("challenges"):
            for challenge in challenges:
                if isinstance(challenge, str) and len(challenge) > 10:
                    # Create bottleneck from challenge
                    bottleneck = ProcessBottleneck(
                        name=f"Challenge: {challenge[:50]}",
                        description=challenge,
                        department="TBD",
                        frequency="daily",
                        time_impact_hours=5,  # Default estimate
                        cost_impact=375,  # 5 hours * $75/hour
                        automation_potential=0.7,
                        priority="medium"
                    )
                    self.bottlenecks.append(bottleneck)
    
    def _generate_contextual_response(self, user_input: str) -> str:
        """Generate appropriate response based on conversation stage"""
        stage_prompts = {
            ConversationStage.OPENING: """
                You are a Business Doctor conducting an intake consultation.
                Warmly greet the business owner and ask about their company.
                Be professional but conversational. Ask for company name, size, and industry.
            """,
            ConversationStage.COMPANY_OVERVIEW: """
                You're learning about their business. Ask follow-up questions about:
                - What services/products they offer
                - Their typical customers
                - Team structure
                Keep it conversational and show genuine interest.
            """,
            ConversationStage.PAIN_POINTS: """
                Transition to understanding their challenges. Ask:
                - What tasks take the most time?
                - Where do bottlenecks occur?
                - What frustrates them most about current processes?
                Be empathetic and probe deeper into pain points.
            """,
            ConversationStage.PROCESS_DISCOVERY: """
                Dive deep into specific processes they mentioned. Ask:
                - How exactly does this process work today?
                - How many people are involved?
                - How long does each step take?
                - What tools do they currently use?
            """,
            ConversationStage.BOTTLENECK_ANALYSIS: """
                Analyze the bottlenecks identified. For each one:
                - Quantify time impact
                - Estimate cost impact
                - Assess automation potential
                - Prioritize by business impact
            """,
            ConversationStage.FINANCIAL_IMPACT: """
                Help them understand the financial impact:
                - Calculate total hours lost to inefficiencies
                - Translate to dollar impact
                - Project potential savings with automation
                - Show ROI of addressing these issues
            """,
            ConversationStage.SOLUTION_EXPLORATION: """
                Explore how AI and automation could help:
                - Suggest specific solutions for their bottlenecks
                - Explain implementation approach
                - Discuss timeline and investment
                - Address concerns or questions
            """,
            ConversationStage.CLOSING: """
                Wrap up the consultation:
                - Summarize key findings
                - Highlight top 3 opportunities
                - Explain next steps
                - Offer to prepare detailed proposal
            """
        }
        
        context = f"""
        Current stage: {self.current_stage.value}
        User said: "{user_input}"
        
        Company info known: {self.metrics.company_name or 'Not yet'}, 
        {self.metrics.employee_count or '?'} employees, 
        Industry: {self.metrics.industry or 'Unknown'}
        
        Bottlenecks identified: {len(self.bottlenecks)}
        
        Instructions: {stage_prompts.get(self.current_stage, "Continue the conversation naturally.")}
        
        Respond as a helpful business consultant. Be specific and actionable.
        """
        
        try:
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> str:
        """Fallback responses if AI fails"""
        fallbacks = {
            ConversationStage.OPENING: "Hello! I'm your Business Doctor. I'm here to help diagnose inefficiencies in your business processes and prescribe AI-powered solutions. Could you start by telling me about your company?",
            ConversationStage.COMPANY_OVERVIEW: "That's interesting. Could you tell me more about your day-to-day operations and what your team typically works on?",
            ConversationStage.PAIN_POINTS: "I see. What would you say are the biggest time-wasters or frustrations in your current processes?",
            ConversationStage.PROCESS_DISCOVERY: "Let's dig deeper into that process. Can you walk me through exactly how it works today, step by step?",
            ConversationStage.BOTTLENECK_ANALYSIS: "Based on what you've told me, I can see several areas where automation could save significant time. Let me analyze the impact of each.",
            ConversationStage.FINANCIAL_IMPACT: "Let's look at what this means financially. If we could automate these processes, here's the potential impact on your bottom line.",
            ConversationStage.SOLUTION_EXPLORATION: "I have some specific recommendations for how AI and automation could address these challenges. Would you like me to explain how we could tackle your top priority?",
            ConversationStage.CLOSING: "This has been very insightful. I'd like to prepare a detailed proposal showing exactly how we can transform these processes. What questions do you have for me?"
        }
        return fallbacks.get(self.current_stage, "Could you tell me more about that?")
    
    def _advance_conversation_stage(self):
        """Move to next conversation stage based on progress"""
        # Simple progression for now - can be made smarter
        stage_order = list(ConversationStage)
        current_index = stage_order.index(self.current_stage)
        
        # Advance based on information collected
        if self.current_stage == ConversationStage.OPENING and self.metrics.company_name:
            self.current_stage = ConversationStage.COMPANY_OVERVIEW
        elif self.current_stage == ConversationStage.COMPANY_OVERVIEW and self.metrics.employee_count > 0:
            self.current_stage = ConversationStage.PAIN_POINTS
        elif self.current_stage == ConversationStage.PAIN_POINTS and len(self.bottlenecks) > 0:
            self.current_stage = ConversationStage.PROCESS_DISCOVERY
        elif len(self.conversation_history) > 20:  # After sufficient conversation
            if current_index < len(stage_order) - 1:
                self.current_stage = stage_order[current_index + 1]
    
    def _get_metrics_summary(self) -> Dict:
        """Get current metrics summary"""
        return {
            "company_name": self.metrics.company_name,
            "employee_count": self.metrics.employee_count,
            "industry": self.metrics.industry,
            "revenue": self.metrics.annual_revenue,
            "challenges_identified": len(self.metrics.current_challenges),
            "bottlenecks_found": len(self.bottlenecks)
        }
    
    def generate_diagnostic_report(self) -> Dict:
        """Generate comprehensive diagnostic report"""
        total_hours_impact = sum(b.time_impact_hours * 52 for b in self.bottlenecks if b.frequency == "weekly")
        total_cost_impact = sum(b.cost_impact * 52 for b in self.bottlenecks if b.frequency == "weekly")
        
        report = {
            "company_overview": asdict(self.metrics),
            "bottlenecks_identified": [
                {
                    "name": b.name,
                    "description": b.description,
                    "annual_hours_impact": b.calculate_annual_impact()[0],
                    "annual_cost_impact": b.calculate_annual_impact()[1],
                    "automation_potential": b.automation_potential,
                    "priority": b.priority
                }
                for b in self.bottlenecks
            ],
            "total_impact": {
                "annual_hours_wasted": total_hours_impact,
                "annual_cost_impact": total_cost_impact,
                "potential_roi": total_cost_impact * 0.7  # 70% efficiency gain
            },
            "recommendations": self._generate_recommendations(),
            "implementation_roadmap": self._generate_roadmap(),
            "conversation_duration": len(self.conversation_history),
            "report_generated": datetime.now().isoformat()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[Dict]:
        """Generate prioritized recommendations"""
        recommendations = []
        
        # Sort bottlenecks by impact
        sorted_bottlenecks = sorted(
            self.bottlenecks, 
            key=lambda b: b.calculate_annual_impact()[1], 
            reverse=True
        )
        
        for i, bottleneck in enumerate(sorted_bottlenecks[:5]):  # Top 5
            recommendations.append({
                "priority": i + 1,
                "bottleneck": bottleneck.name,
                "solution": f"Implement AI-powered automation for {bottleneck.name}",
                "expected_time_savings": f"{bottleneck.calculate_annual_impact()[0]:.0f} hours/year",
                "expected_cost_savings": f"${bottleneck.calculate_annual_impact()[1]:,.0f}/year",
                "implementation_effort": bottleneck.automation_potential
            })
        
        return recommendations
    
    def _generate_roadmap(self) -> List[Dict]:
        """Generate 90-day implementation roadmap"""
        return [
            {
                "phase": 1,
                "days": "1-30",
                "title": "Quick Wins",
                "activities": [
                    "Implement automated email responses",
                    "Set up basic workflow automation",
                    "Deploy initial AI assistants"
                ]
            },
            {
                "phase": 2,
                "days": "31-60",
                "title": "Core Systems",
                "activities": [
                    "Integrate AI with existing tools",
                    "Automate primary bottlenecks",
                    "Train team on new systems"
                ]
            },
            {
                "phase": 3,
                "days": "61-90",
                "title": "Scale & Optimize",
                "activities": [
                    "Expand automation across departments",
                    "Measure and optimize performance",
                    "Plan next phase of transformation"
                ]
            }
        ]
    
    def export_conversation(self) -> str:
        """Export conversation history as JSON"""
        return json.dumps({
            "conversation": self.conversation_history,
            "metrics": asdict(self.metrics),
            "bottlenecks": [asdict(b) for b in self.bottlenecks],
            "insights": [asdict(i) for i in self.insights]
        }, indent=2)

# Terminal interface functions for testing
def run_terminal_consultation(api_key: str):
    """Run a consultation in terminal mode"""
    engine = BusinessDoctorEngine(api_key)
    
    print("\n" + "="*60)
    print("BUSINESS DOCTOR AI CONSULTATION")
    print("="*60)
    print("\nType 'exit' to end consultation")
    print("Type 'report' to generate diagnostic report")
    print("Type 'export' to save conversation\n")
    
    while True:
        # Show current stage
        print(f"\n[Stage: {engine.current_stage.value}]")
        
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'report':
            report = engine.generate_diagnostic_report()
            print("\n" + "="*60)
            print("DIAGNOSTIC REPORT")
            print("="*60)
            print(json.dumps(report, indent=2))
            continue
        elif user_input.lower() == 'export':
            export_data = engine.export_conversation()
            filename = f"consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                f.write(export_data)
            print(f"\nConversation exported to {filename}")
            continue
        
        # Process input
        result = engine.process_input(user_input)
        
        # Show AI response
        print(f"\nBusiness Doctor: {result['response']}")
        
        # Show metrics update (for debugging)
        if result['bottlenecks_found'] > 0:
            print(f"\n[System: {result['bottlenecks_found']} bottlenecks identified]")
    
    print("\nThank you for your time. Generating final report...")
    report = engine.generate_diagnostic_report()
    print(f"\nTotal Annual Impact Identified: ${report['total_impact']['annual_cost_impact']:,.0f}")
    print(f"Potential ROI: ${report['total_impact']['potential_roi']:,.0f}")

if __name__ == "__main__":
    # Test with sample API key
    API_KEY = "your-gemini-api-key"
    run_terminal_consultation(API_KEY)