"""
Structured Summary Objects for Efficient Context Management
Reduces token usage while maintaining conversation coherence
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
from enum import Enum

class TopicCategory(Enum):
    """Categories for organizing conversation topics"""
    OPERATIONS = "operations"
    SALES = "sales"
    MARKETING = "marketing"
    FINANCE = "finance"
    TECHNOLOGY = "technology"
    HUMAN_RESOURCES = "hr"
    CUSTOMER_SERVICE = "customer_service"
    STRATEGY = "strategy"

@dataclass
class ProcessStep:
    """Individual step in a business process"""
    name: str
    description: str
    time_minutes: float
    cost_per_instance: float
    frequency_per_week: int
    is_automated: bool = False
    is_bottleneck: bool = False
    improvement_potential: float = 0.0  # 0-1 scale

@dataclass
class BusinessProcess:
    """Complete business process with analysis"""
    name: str
    category: TopicCategory
    steps: List[ProcessStep]
    total_time_weekly: float = 0.0
    total_cost_weekly: float = 0.0
    automation_potential: float = 0.0
    
    def __post_init__(self):
        """Calculate totals after initialization"""
        self.total_time_weekly = sum(
            step.time_minutes * step.frequency_per_week 
            for step in self.steps
        ) / 60  # Convert to hours
        
        self.total_cost_weekly = sum(
            step.cost_per_instance * step.frequency_per_week 
            for step in self.steps
        )
        
        # Calculate automation potential
        automatable_time = sum(
            step.time_minutes * step.frequency_per_week * step.improvement_potential
            for step in self.steps if not step.is_automated
        ) / 60
        
        self.automation_potential = (
            automatable_time / self.total_time_weekly 
            if self.total_time_weekly > 0 else 0
        )

@dataclass
class Bottleneck:
    """Identified bottleneck with impact analysis"""
    name: str
    description: str
    category: TopicCategory
    impact_hours_weekly: float
    impact_cost_weekly: float
    affected_processes: List[str]
    severity: str = "medium"  # low, medium, high, critical
    solution_complexity: str = "medium"  # simple, medium, complex
    ai_solvable: bool = True

@dataclass
class Insight:
    """Business insight derived from conversation"""
    text: str
    category: TopicCategory
    confidence: float  # 0-1
    supporting_evidence: List[str]
    potential_value: float  # Dollar value if implemented
    implementation_effort: str = "medium"  # low, medium, high
    priority_score: float = 0.0
    
    def __post_init__(self):
        """Calculate priority score"""
        effort_multiplier = {"low": 1.5, "medium": 1.0, "high": 0.5}
        self.priority_score = (
            self.potential_value * self.confidence * 
            effort_multiplier.get(self.implementation_effort, 1.0)
        )

@dataclass
class TopicSummary:
    """Summary of a conversation topic"""
    category: TopicCategory
    discussed_at: datetime
    key_points: List[str]
    processes_identified: List[str]
    bottlenecks_found: List[str]
    estimated_impact_hours: float
    estimated_impact_dollars: float
    follow_up_questions: List[str] = field(default_factory=list)
    completion_percentage: float = 0.0

@dataclass
class ConversationSummary:
    """Complete structured summary of conversation"""
    client_id: str
    company_name: str
    industry: str
    employee_count: int
    annual_revenue: float
    conversation_duration_minutes: int
    topics_covered: List[TopicSummary]
    all_processes: List[BusinessProcess]
    all_bottlenecks: List[Bottleneck]
    all_insights: List[Insight]
    total_improvement_potential_hours: float = 0.0
    total_improvement_potential_dollars: float = 0.0
    ai_transformation_readiness: float = 0.0  # 0-1 scale
    recommended_next_steps: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Calculate summary metrics"""
        self.total_improvement_potential_hours = sum(
            bottleneck.impact_hours_weekly 
            for bottleneck in self.all_bottlenecks
        )
        
        self.total_improvement_potential_dollars = sum(
            bottleneck.impact_cost_weekly * 52  # Annualized
            for bottleneck in self.all_bottlenecks
        )
        
        # Calculate AI readiness based on multiple factors
        factors = [
            1.0 if self.employee_count > 20 else 0.5,
            1.0 if self.annual_revenue > 1000000 else 0.5,
            len(self.all_bottlenecks) / 10,  # More bottlenecks = more opportunity
            sum(b.ai_solvable for b in self.all_bottlenecks) / max(len(self.all_bottlenecks), 1),
            min(self.total_improvement_potential_hours / 40, 1.0)  # Cap at 40 hrs/week
        ]
        self.ai_transformation_readiness = sum(factors) / len(factors)

class StructuredSummaryManager:
    """Manages creation and updates of structured summaries during conversation"""
    
    def __init__(self):
        self.current_summary = None
        self.topic_in_progress = None
    
    def start_new_conversation(self, client_info: Dict[str, Any]) -> ConversationSummary:
        """Initialize new conversation summary"""
        self.current_summary = ConversationSummary(
            client_id=client_info.get('client_id', ''),
            company_name=client_info.get('company_name', ''),
            industry=client_info.get('industry', ''),
            employee_count=client_info.get('employee_count', 0),
            annual_revenue=client_info.get('annual_revenue', 0),
            conversation_duration_minutes=0,
            topics_covered=[],
            all_processes=[],
            all_bottlenecks=[],
            all_insights=[]
        )
        return self.current_summary
    
    def start_new_topic(self, category: TopicCategory) -> TopicSummary:
        """Begin discussing a new topic"""
        self.topic_in_progress = TopicSummary(
            category=category,
            discussed_at=datetime.now(),
            key_points=[],
            processes_identified=[],
            bottlenecks_found=[],
            estimated_impact_hours=0,
            estimated_impact_dollars=0
        )
        return self.topic_in_progress
    
    def add_process(self, process: BusinessProcess) -> None:
        """Add identified process to summary"""
        if self.current_summary:
            self.current_summary.all_processes.append(process)
            if self.topic_in_progress:
                self.topic_in_progress.processes_identified.append(process.name)
                self.topic_in_progress.estimated_impact_hours += process.total_time_weekly
                self.topic_in_progress.estimated_impact_dollars += process.total_cost_weekly
    
    def add_bottleneck(self, bottleneck: Bottleneck) -> None:
        """Add identified bottleneck to summary"""
        if self.current_summary:
            self.current_summary.all_bottlenecks.append(bottleneck)
            if self.topic_in_progress:
                self.topic_in_progress.bottlenecks_found.append(bottleneck.name)
    
    def add_insight(self, insight: Insight) -> None:
        """Add business insight to summary"""
        if self.current_summary:
            self.current_summary.all_insights.append(insight)
    
    def complete_topic(self, completion_percentage: float = 100.0) -> None:
        """Mark current topic as complete and add to summary"""
        if self.topic_in_progress and self.current_summary:
            self.topic_in_progress.completion_percentage = completion_percentage
            self.current_summary.topics_covered.append(self.topic_in_progress)
            self.topic_in_progress = None
    
    def get_context_for_ai(self, include_full_processes: bool = False) -> Dict[str, Any]:
        """
        Get optimized context for AI to continue conversation
        This is much more token-efficient than passing full transcript
        """
        if not self.current_summary:
            return {}
        
        context = {
            "company_info": {
                "name": self.current_summary.company_name,
                "industry": self.current_summary.industry,
                "size": self.current_summary.employee_count,
                "revenue": self.current_summary.annual_revenue
            },
            "topics_discussed": [
                {
                    "category": topic.category.value,
                    "key_points": topic.key_points[:3],  # Limit to top 3
                    "impact_hours": topic.estimated_impact_hours
                }
                for topic in self.current_summary.topics_covered
            ],
            "top_bottlenecks": [
                {
                    "name": b.name,
                    "impact": b.impact_hours_weekly,
                    "severity": b.severity
                }
                for b in sorted(
                    self.current_summary.all_bottlenecks, 
                    key=lambda x: x.impact_hours_weekly, 
                    reverse=True
                )[:5]  # Top 5 bottlenecks
            ],
            "improvement_potential": {
                "hours_weekly": self.current_summary.total_improvement_potential_hours,
                "dollars_annually": self.current_summary.total_improvement_potential_dollars
            },
            "ai_readiness": self.current_summary.ai_transformation_readiness
        }
        
        if include_full_processes:
            context["processes"] = [
                {
                    "name": p.name,
                    "time_weekly": p.total_time_weekly,
                    "automation_potential": p.automation_potential
                }
                for p in self.current_summary.all_processes
            ]
        
        return context
    
    def export_summary(self, format: str = "json") -> str:
        """Export summary in requested format"""
        if not self.current_summary:
            return ""
        
        if format == "json":
            return json.dumps(asdict(self.current_summary), default=str, indent=2)
        
        elif format == "markdown":
            return self._generate_markdown_summary()
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_markdown_summary(self) -> str:
        """Generate human-readable markdown summary"""
        s = self.current_summary
        
        md = f"""# Business Analysis Summary - {s.company_name}

## Company Overview
- **Industry**: {s.industry}
- **Employees**: {s.employee_count}
- **Annual Revenue**: ${s.annual_revenue:,.0f}
- **AI Readiness Score**: {s.ai_transformation_readiness:.1%}

## Topics Analyzed
"""
        
        for topic in s.topics_covered:
            md += f"\n### {topic.category.value.replace('_', ' ').title()}\n"
            md += f"- **Completion**: {topic.completion_percentage:.0f}%\n"
            md += f"- **Impact**: {topic.estimated_impact_hours:.1f} hours/week "
            md += f"(${topic.estimated_impact_dollars:,.0f}/week)\n"
            
            if topic.key_points:
                md += "- **Key Points**:\n"
                for point in topic.key_points:
                    md += f"  - {point}\n"
        
        md += f"\n## Identified Bottlenecks ({len(s.all_bottlenecks)} total)\n"
        
        for b in sorted(s.all_bottlenecks, key=lambda x: x.impact_hours_weekly, reverse=True)[:5]:
            md += f"\n### {b.name}\n"
            md += f"- **Impact**: {b.impact_hours_weekly:.1f} hours/week "
            md += f"(${b.impact_cost_weekly:,.0f}/week)\n"
            md += f"- **Severity**: {b.severity}\n"
            md += f"- **AI Solvable**: {'Yes' if b.ai_solvable else 'No'}\n"
        
        md += f"\n## Top Insights\n"
        
        for insight in sorted(s.all_insights, key=lambda x: x.priority_score, reverse=True)[:5]:
            md += f"\n- **{insight.text}**\n"
            md += f"  - Potential Value: ${insight.potential_value:,.0f}\n"
            md += f"  - Confidence: {insight.confidence:.0%}\n"
            md += f"  - Implementation Effort: {insight.implementation_effort}\n"
        
        md += f"""
## Total Improvement Potential
- **Time Savings**: {s.total_improvement_potential_hours:.1f} hours/week
- **Cost Savings**: ${s.total_improvement_potential_dollars:,.0f}/year
- **ROI on $50k Investment**: {(s.total_improvement_potential_dollars / 50000 * 100):.0f}%

## Recommended Next Steps
"""
        
        for i, step in enumerate(s.recommended_next_steps[:5], 1):
            md += f"{i}. {step}\n"
        
        return md

# Example usage
if __name__ == "__main__":
    # Initialize manager
    manager = StructuredSummaryManager()
    
    # Start conversation
    summary = manager.start_new_conversation({
        'client_id': 'CL001',
        'company_name': 'Smith & Associates Law Firm',
        'industry': 'Legal',
        'employee_count': 45,
        'annual_revenue': 8500000
    })
    
    # Discuss sales topic
    manager.start_new_topic(TopicCategory.SALES)
    
    # Add discovered process
    sales_process = BusinessProcess(
        name="Client Intake Process",
        category=TopicCategory.SALES,
        steps=[
            ProcessStep(
                name="Initial Call Handling",
                description="Receptionist answers and logs call",
                time_minutes=15,
                cost_per_instance=6.25,
                frequency_per_week=50,
                is_automated=False,
                is_bottleneck=True,
                improvement_potential=0.8
            ),
            ProcessStep(
                name="Conflict Check",
                description="Manual search through case database",
                time_minutes=45,
                cost_per_instance=37.50,
                frequency_per_week=50,
                is_automated=False,
                is_bottleneck=True,
                improvement_potential=0.9
            )
        ]
    )
    manager.add_process(sales_process)
    
    # Add bottleneck
    intake_bottleneck = Bottleneck(
        name="Manual Client Intake",
        description="Phone calls often missed, manual data entry",
        category=TopicCategory.SALES,
        impact_hours_weekly=20,
        impact_cost_weekly=1500,
        affected_processes=["Client Intake Process"],
        severity="high",
        solution_complexity="medium",
        ai_solvable=True
    )
    manager.add_bottleneck(intake_bottleneck)
    
    # Complete topic
    manager.complete_topic(90.0)
    
    # Get optimized context for AI
    ai_context = manager.get_context_for_ai()
    print("AI Context:", json.dumps(ai_context, indent=2))
    
    # Export summary
    print("\n" + manager.export_summary(format="markdown"))