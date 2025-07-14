"""
Business Doctor AI Diagnostic Tool for Microsoft 365
Analyzes current usage and identifies top AI automation opportunities
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class M365DiagnosticTool:
    """
    Automated assessment tool that analyzes Microsoft 365 usage
    and identifies AI transformation opportunities
    """
    
    def __init__(self):
        self.diagnostic_categories = [
            "email_efficiency",
            "document_automation", 
            "meeting_productivity",
            "data_insights",
            "security_posture",
            "collaboration_patterns"
        ]
        
    def analyze_tenant(self, tenant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main diagnostic function that returns prioritized AI opportunities
        """
        results = {
            "diagnostic_date": datetime.now().isoformat(),
            "tenant_id": tenant_data.get("tenant_id"),
            "company_name": tenant_data.get("company_name"),
            "employee_count": tenant_data.get("employee_count"),
            "current_state_analysis": {},
            "ai_opportunities": [],
            "potential_roi": {},
            "implementation_roadmap": []
        }
        
        # Analyze each category
        for category in self.diagnostic_categories:
            analysis = self._analyze_category(category, tenant_data)
            results["current_state_analysis"][category] = analysis
            
        # Identify top 3 AI opportunities
        results["ai_opportunities"] = self._identify_opportunities(results["current_state_analysis"])
        
        # Calculate ROI
        results["potential_roi"] = self._calculate_roi(
            results["ai_opportunities"], 
            tenant_data.get("employee_count", 50)
        )
        
        # Generate roadmap
        results["implementation_roadmap"] = self._generate_roadmap(results["ai_opportunities"])
        
        return results
    
    def _analyze_category(self, category: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze specific category of M365 usage"""
        
        if category == "email_efficiency":
            return {
                "avg_emails_per_day": data.get("email_volume", 0) / data.get("employee_count", 1),
                "response_time_hours": data.get("avg_response_time", 24),
                "inbox_zero_percentage": data.get("inbox_managed_users", 10),
                "manual_filing_hours": data.get("email_filing_time", 5),
                "pain_points": [
                    "High email volume causing delays",
                    "Manual email categorization",
                    "Missed important messages"
                ]
            }
            
        elif category == "document_automation":
            return {
                "documents_created_monthly": data.get("doc_creation_rate", 100),
                "template_usage_rate": data.get("template_usage", 20),
                "manual_data_entry_hours": data.get("data_entry_time", 40),
                "approval_cycle_days": data.get("approval_time", 5),
                "pain_points": [
                    "Repetitive document creation",
                    "Manual data transfer between docs",
                    "Slow approval processes"
                ]
            }
            
        elif category == "meeting_productivity":
            return {
                "meetings_per_week": data.get("meeting_count", 50),
                "avg_meeting_duration": data.get("meeting_duration", 45),
                "no_agenda_percentage": data.get("meetings_without_agenda", 60),
                "no_followup_percentage": data.get("meetings_without_followup", 70),
                "pain_points": [
                    "Meetings without clear outcomes",
                    "Manual note-taking",
                    "Lost action items"
                ]
            }
            
        # Add more categories as needed
        return {}
    
    def _identify_opportunities(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify and prioritize AI automation opportunities"""
        
        opportunities = []
        
        # Email AI Assistant Opportunity
        if analysis["email_efficiency"]["avg_emails_per_day"] > 50:
            opportunities.append({
                "name": "AI Email Assistant",
                "description": "Deploy AI to auto-categorize, prioritize, and draft responses",
                "impact": "high",
                "effort": "medium",
                "time_saved_hours_monthly": analysis["email_efficiency"]["manual_filing_hours"] * 20,
                "tools": ["Power Automate", "Azure OpenAI", "Custom Email Classifier"],
                "priority": 1
            })
        
        # Document Automation Opportunity
        if analysis["document_automation"]["template_usage_rate"] < 50:
            opportunities.append({
                "name": "Intelligent Document Automation",
                "description": "AI-powered document generation and data extraction",
                "impact": "high", 
                "effort": "low",
                "time_saved_hours_monthly": analysis["document_automation"]["manual_data_entry_hours"],
                "tools": ["Power Automate", "AI Builder", "SharePoint Syntex"],
                "priority": 2
            })
        
        # Meeting Intelligence Opportunity
        if analysis["meeting_productivity"]["no_followup_percentage"] > 50:
            opportunities.append({
                "name": "AI Meeting Assistant",
                "description": "Automated transcription, action item extraction, and follow-up",
                "impact": "medium",
                "effort": "low",
                "time_saved_hours_monthly": analysis["meeting_productivity"]["meetings_per_week"] * 2,
                "tools": ["Teams Premium", "Power Automate", "Azure Cognitive Services"],
                "priority": 3
            })
        
        return sorted(opportunities, key=lambda x: x["priority"])[:3]
    
    def _calculate_roi(self, opportunities: List[Dict[str, Any]], employee_count: int) -> Dict[str, Any]:
        """Calculate potential ROI from AI implementations"""
        
        total_hours_saved = sum(opp["time_saved_hours_monthly"] for opp in opportunities)
        hourly_rate = 75  # Average for SMB employees
        
        return {
            "monthly_hours_saved": total_hours_saved,
            "monthly_cost_savings": total_hours_saved * hourly_rate,
            "annual_cost_savings": total_hours_saved * hourly_rate * 12,
            "productivity_gain_percentage": (total_hours_saved / (employee_count * 160)) * 100,
            "implementation_cost": 50000,  # Your transformation fee
            "payback_months": 50000 / (total_hours_saved * hourly_rate) if total_hours_saved > 0 else 12,
            "3_year_roi": ((total_hours_saved * hourly_rate * 36) - 50000) / 50000 * 100
        }
    
    def _generate_roadmap(self, opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate implementation roadmap"""
        
        roadmap = []
        start_date = datetime.now()
        
        for i, opp in enumerate(opportunities):
            phase_start = start_date + timedelta(days=i*30)
            roadmap.append({
                "phase": i + 1,
                "name": opp["name"],
                "start_date": phase_start.isoformat(),
                "duration_days": 30,
                "milestones": [
                    f"Week 1: Design {opp['name']} architecture",
                    f"Week 2: Build and configure using {', '.join(opp['tools'])}",
                    f"Week 3: Test with pilot group",
                    f"Week 4: Full deployment and training"
                ],
                "success_metrics": [
                    f"Time saved: {opp['time_saved_hours_monthly']} hours/month",
                    "User adoption: >80%",
                    "Error rate: <5%"
                ]
            })
            
        return roadmap
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate executive summary report"""
        
        report = f"""
# Business Doctor AI Diagnostic Report
**Company**: {results['company_name']}
**Date**: {results['diagnostic_date']}
**Employees**: {results['employee_count']}

## Executive Summary
Our AI diagnostic has identified {len(results['ai_opportunities'])} high-impact opportunities to transform your Microsoft 365 environment.

## Top AI Automation Opportunities

"""
        for i, opp in enumerate(results['ai_opportunities'], 1):
            report += f"""
### {i}. {opp['name']}
- **Description**: {opp['description']}
- **Monthly Time Savings**: {opp['time_saved_hours_monthly']} hours
- **Implementation Effort**: {opp['effort']}
- **Business Impact**: {opp['impact']}
"""

        report += f"""
## Financial Impact
- **Monthly Savings**: ${results['potential_roi']['monthly_cost_savings']:,.0f}
- **Annual Savings**: ${results['potential_roi']['annual_cost_savings']:,.0f}
- **Productivity Gain**: {results['potential_roi']['productivity_gain_percentage']:.1f}%
- **ROI Payback**: {results['potential_roi']['payback_months']:.1f} months
- **3-Year ROI**: {results['potential_roi']['3_year_roi']:.0f}%

## Recommended Next Steps
1. Review detailed findings with your team
2. Prioritize quick wins for immediate impact
3. Schedule Business Doctor transformation kickoff
4. Begin with Phase 1: {results['ai_opportunities'][0]['name']}

---
*This diagnostic identifies opportunities unique to your organization. Contact Business Doctor to begin your AI transformation journey.*
"""
        return report


# Example usage for demos and sales
if __name__ == "__main__":
    # Sample client data (would come from actual M365 analytics)
    sample_client = {
        "tenant_id": "abc-123",
        "company_name": "Smith & Associates Law Firm",
        "employee_count": 45,
        "email_volume": 3500,  # daily
        "avg_response_time": 18,  # hours
        "inbox_managed_users": 15,  # percentage
        "email_filing_time": 10,  # hours per week
        "doc_creation_rate": 500,  # monthly
        "template_usage": 30,  # percentage
        "data_entry_time": 60,  # hours monthly
        "approval_time": 7,  # days
        "meeting_count": 80,  # weekly
        "meeting_duration": 50,  # minutes average
        "meetings_without_agenda": 70,  # percentage  
        "meetings_without_followup": 80  # percentage
    }
    
    tool = M365DiagnosticTool()
    results = tool.analyze_tenant(sample_client)
    report = tool.generate_report(results)
    
    print(report)
    
    # Save results for CRM
    with open("diagnostic_results.json", "w") as f:
        json.dump(results, f, indent=2)