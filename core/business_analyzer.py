"""
Business Analyzer - ROI Calculations and Business Intelligence
Analyzes business data and generates actionable insights
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
from datetime import datetime
import statistics

@dataclass
class ROICalculation:
    """ROI calculation for a specific improvement"""
    description: str
    current_cost: float
    improved_cost: float
    implementation_cost: float
    time_to_implement_days: int
    annual_savings: float
    roi_percentage: float
    payback_period_months: float
    confidence_level: float

class BusinessAnalyzer:
    """Analyzes business data and calculates ROI"""
    
    # Industry benchmarks (can be expanded)
    INDUSTRY_BENCHMARKS = {
        "legal": {
            "revenue_per_employee": 200000,
            "billable_hours_percentage": 0.65,
            "admin_overhead_percentage": 0.35,
            "typical_hourly_rate": 300
        },
        "accounting": {
            "revenue_per_employee": 150000,
            "billable_hours_percentage": 0.70,
            "admin_overhead_percentage": 0.30,
            "typical_hourly_rate": 200
        },
        "consulting": {
            "revenue_per_employee": 175000,
            "billable_hours_percentage": 0.75,
            "admin_overhead_percentage": 0.25,
            "typical_hourly_rate": 250
        },
        "msp": {
            "revenue_per_employee": 125000,
            "billable_hours_percentage": 0.60,
            "admin_overhead_percentage": 0.40,
            "typical_hourly_rate": 150
        },
        "default": {
            "revenue_per_employee": 100000,
            "billable_hours_percentage": 0.50,
            "admin_overhead_percentage": 0.50,
            "typical_hourly_rate": 75
        }
    }
    
    def __init__(self):
        self.calculations: List[ROICalculation] = []
    
    def analyze_business_metrics(self, metrics: Dict) -> Dict:
        """Analyze business metrics and identify opportunities"""
        analysis = {
            "company_size_category": self._categorize_company_size(metrics.get("employee_count", 0)),
            "revenue_per_employee": self._calculate_revenue_per_employee(metrics),
            "industry_comparison": self._compare_to_industry(metrics),
            "automation_readiness": self._assess_automation_readiness(metrics),
            "growth_potential": self._assess_growth_potential(metrics)
        }
        
        return analysis
    
    def calculate_bottleneck_roi(self, bottleneck: Dict, company_metrics: Dict) -> ROICalculation:
        """Calculate ROI for addressing a specific bottleneck"""
        # Get hourly cost
        hourly_cost = self._get_hourly_cost(company_metrics)
        
        # Current state costs
        annual_hours = bottleneck.get("annual_hours_impact", 0)
        current_cost = annual_hours * hourly_cost
        
        # Improved state (based on automation potential)
        automation_potential = bottleneck.get("automation_potential", 0.7)
        improved_cost = current_cost * (1 - automation_potential)
        annual_savings = current_cost - improved_cost
        
        # Implementation cost estimate
        complexity_multiplier = {
            "low": 10000,
            "medium": 25000,
            "high": 50000
        }
        solution_complexity = bottleneck.get("solution_complexity", "medium")
        implementation_cost = complexity_multiplier.get(solution_complexity, 25000)
        
        # Time to implement
        time_multiplier = {
            "low": 30,
            "medium": 60,
            "high": 90
        }
        time_to_implement = time_multiplier.get(solution_complexity, 60)
        
        # ROI calculations
        if annual_savings > 0:
            roi_percentage = ((annual_savings - implementation_cost) / implementation_cost) * 100
            payback_period_months = (implementation_cost / annual_savings) * 12
        else:
            roi_percentage = 0
            payback_period_months = float('inf')
        
        # Confidence based on data quality
        confidence = self._calculate_confidence(bottleneck, company_metrics)
        
        roi_calc = ROICalculation(
            description=f"Automate {bottleneck.get('name', 'process')}",
            current_cost=current_cost,
            improved_cost=improved_cost,
            implementation_cost=implementation_cost,
            time_to_implement_days=time_to_implement,
            annual_savings=annual_savings,
            roi_percentage=roi_percentage,
            payback_period_months=payback_period_months,
            confidence_level=confidence
        )
        
        self.calculations.append(roi_calc)
        return roi_calc
    
    def calculate_portfolio_roi(self, bottlenecks: List[Dict], company_metrics: Dict) -> Dict:
        """Calculate ROI for entire portfolio of improvements"""
        portfolio_calculations = []
        
        for bottleneck in bottlenecks:
            roi_calc = self.calculate_bottleneck_roi(bottleneck, company_metrics)
            portfolio_calculations.append(roi_calc)
        
        # Sort by ROI
        portfolio_calculations.sort(key=lambda x: x.roi_percentage, reverse=True)
        
        # Calculate portfolio metrics
        total_current_cost = sum(calc.current_cost for calc in portfolio_calculations)
        total_improved_cost = sum(calc.improved_cost for calc in portfolio_calculations)
        total_implementation_cost = sum(calc.implementation_cost for calc in portfolio_calculations)
        total_annual_savings = sum(calc.annual_savings for calc in portfolio_calculations)
        
        # Portfolio ROI
        if total_implementation_cost > 0:
            portfolio_roi = ((total_annual_savings - total_implementation_cost) / total_implementation_cost) * 100
            portfolio_payback = (total_implementation_cost / total_annual_savings) * 12
        else:
            portfolio_roi = 0
            portfolio_payback = 0
        
        return {
            "individual_projects": [
                {
                    "description": calc.description,
                    "annual_savings": calc.annual_savings,
                    "roi_percentage": calc.roi_percentage,
                    "payback_months": calc.payback_period_months,
                    "confidence": calc.confidence_level
                }
                for calc in portfolio_calculations[:10]  # Top 10
            ],
            "portfolio_summary": {
                "total_current_cost": total_current_cost,
                "total_improved_cost": total_improved_cost,
                "total_implementation_cost": total_implementation_cost,
                "total_annual_savings": total_annual_savings,
                "portfolio_roi_percentage": portfolio_roi,
                "portfolio_payback_months": portfolio_payback,
                "number_of_improvements": len(portfolio_calculations)
            },
            "recommendations": self._generate_recommendations(portfolio_calculations),
            "implementation_phases": self._create_implementation_phases(portfolio_calculations)
        }
    
    def benchmark_against_industry(self, company_metrics: Dict) -> Dict:
        """Benchmark company against industry standards"""
        industry = company_metrics.get("industry", "default").lower()
        benchmarks = self.INDUSTRY_BENCHMARKS.get(industry, self.INDUSTRY_BENCHMARKS["default"])
        
        # Calculate company metrics
        employees = company_metrics.get("employee_count", 1)
        revenue = company_metrics.get("annual_revenue", 0)
        revenue_per_employee = revenue / employees if employees > 0 else 0
        
        # Compare to benchmarks
        comparison = {
            "revenue_per_employee": {
                "company": revenue_per_employee,
                "industry_average": benchmarks["revenue_per_employee"],
                "difference_percentage": ((revenue_per_employee - benchmarks["revenue_per_employee"]) / benchmarks["revenue_per_employee"] * 100) if benchmarks["revenue_per_employee"] > 0 else 0
            },
            "estimated_billable_percentage": benchmarks["billable_hours_percentage"],
            "estimated_overhead_percentage": benchmarks["admin_overhead_percentage"],
            "industry_hourly_rate": benchmarks["typical_hourly_rate"]
        }
        
        # Performance rating
        if comparison["revenue_per_employee"]["difference_percentage"] > 20:
            performance = "Above Average"
        elif comparison["revenue_per_employee"]["difference_percentage"] > -20:
            performance = "Average"
        else:
            performance = "Below Average"
        
        comparison["performance_rating"] = performance
        
        # Improvement potential
        if performance == "Below Average":
            gap = benchmarks["revenue_per_employee"] - revenue_per_employee
            comparison["improvement_potential"] = gap * employees
            comparison["improvement_message"] = f"Reaching industry average could add ${gap * employees:,.0f} in annual revenue"
        else:
            comparison["improvement_potential"] = 0
            comparison["improvement_message"] = "Already performing at or above industry average"
        
        return comparison
    
    def generate_executive_summary(self, company_metrics: Dict, bottlenecks: List[Dict]) -> Dict:
        """Generate executive summary of findings"""
        # Calculate portfolio ROI
        portfolio = self.calculate_portfolio_roi(bottlenecks, company_metrics)
        
        # Industry benchmark
        benchmark = self.benchmark_against_industry(company_metrics)
        
        # Key metrics
        total_hours_wasted = sum(b.get("annual_hours_impact", 0) for b in bottlenecks)
        total_cost_impact = sum(b.get("annual_cost_impact", 0) for b in bottlenecks)
        
        # Create summary
        summary = {
            "company_snapshot": {
                "name": company_metrics.get("company_name", "Company"),
                "employees": company_metrics.get("employee_count", 0),
                "annual_revenue": company_metrics.get("annual_revenue", 0),
                "industry": company_metrics.get("industry", "Unknown")
            },
            "key_findings": {
                "total_inefficiency_hours_annual": total_hours_wasted,
                "total_inefficiency_cost_annual": total_cost_impact,
                "number_of_bottlenecks": len(bottlenecks),
                "automation_opportunity": portfolio["portfolio_summary"]["total_annual_savings"]
            },
            "roi_highlights": {
                "total_investment_required": portfolio["portfolio_summary"]["total_implementation_cost"],
                "annual_savings_potential": portfolio["portfolio_summary"]["total_annual_savings"],
                "roi_percentage": portfolio["portfolio_summary"]["portfolio_roi_percentage"],
                "payback_period_months": portfolio["portfolio_summary"]["portfolio_payback_months"]
            },
            "industry_comparison": benchmark,
            "top_3_opportunities": portfolio["individual_projects"][:3],
            "executive_recommendation": self._generate_executive_recommendation(
                portfolio, benchmark, company_metrics
            )
        }
        
        return summary
    
    def _categorize_company_size(self, employee_count: int) -> str:
        """Categorize company by size"""
        if employee_count < 20:
            return "Micro"
        elif employee_count < 50:
            return "Small"
        elif employee_count < 250:
            return "Medium"
        elif employee_count < 500:
            return "Mid-Market"
        else:
            return "Enterprise"
    
    def _calculate_revenue_per_employee(self, metrics: Dict) -> float:
        """Calculate revenue per employee"""
        revenue = metrics.get("annual_revenue", 0)
        employees = metrics.get("employee_count", 1)
        return revenue / employees if employees > 0 else 0
    
    def _compare_to_industry(self, metrics: Dict) -> str:
        """Compare to industry benchmarks"""
        industry = metrics.get("industry", "default").lower()
        benchmarks = self.INDUSTRY_BENCHMARKS.get(industry, self.INDUSTRY_BENCHMARKS["default"])
        
        revenue_per_employee = self._calculate_revenue_per_employee(metrics)
        benchmark_revenue = benchmarks["revenue_per_employee"]
        
        if revenue_per_employee > benchmark_revenue * 1.2:
            return "Outperforming industry"
        elif revenue_per_employee > benchmark_revenue * 0.8:
            return "Industry average"
        else:
            return "Below industry average"
    
    def _assess_automation_readiness(self, metrics: Dict) -> str:
        """Assess readiness for automation"""
        score = 0
        
        # Size factor
        employees = metrics.get("employee_count", 0)
        if employees >= 20:
            score += 2
        elif employees >= 10:
            score += 1
        
        # Revenue factor
        revenue = metrics.get("annual_revenue", 0)
        if revenue >= 5000000:
            score += 2
        elif revenue >= 1000000:
            score += 1
        
        # Technology factor
        tech_stack = metrics.get("technology_stack", [])
        if len(tech_stack) >= 3:
            score += 2
        elif len(tech_stack) >= 1:
            score += 1
        
        # Readiness levels
        if score >= 5:
            return "High - Ready for comprehensive automation"
        elif score >= 3:
            return "Medium - Ready for targeted automation"
        else:
            return "Low - Start with basic automation"
    
    def _assess_growth_potential(self, metrics: Dict) -> str:
        """Assess growth potential with automation"""
        employees = metrics.get("employee_count", 0)
        
        if employees < 50:
            return "High - Can scale 2-3x with same headcount"
        elif employees < 200:
            return "Medium - Can scale 1.5-2x with same headcount"
        else:
            return "Moderate - Can improve efficiency 20-50%"
    
    def _get_hourly_cost(self, company_metrics: Dict) -> float:
        """Get hourly cost for calculations"""
        # Use provided rate or calculate from revenue
        if "average_hourly_cost" in company_metrics:
            return company_metrics["average_hourly_cost"]
        
        # Calculate from revenue and employees
        revenue = company_metrics.get("annual_revenue", 0)
        employees = company_metrics.get("employee_count", 1)
        
        if revenue > 0 and employees > 0:
            # Assume 2000 working hours per year, 60% labor cost
            annual_labor_cost = revenue * 0.6
            total_hours = employees * 2000
            return annual_labor_cost / total_hours if total_hours > 0 else 75
        
        # Default by industry
        industry = company_metrics.get("industry", "default").lower()
        benchmarks = self.INDUSTRY_BENCHMARKS.get(industry, self.INDUSTRY_BENCHMARKS["default"])
        return benchmarks["typical_hourly_rate"]
    
    def _calculate_confidence(self, bottleneck: Dict, company_metrics: Dict) -> float:
        """Calculate confidence level in ROI calculation"""
        confidence = 0.5  # Base confidence
        
        # Data completeness factors
        if bottleneck.get("time_impact_hours"):
            confidence += 0.1
        if bottleneck.get("cost_impact"):
            confidence += 0.1
        if bottleneck.get("frequency"):
            confidence += 0.1
        if company_metrics.get("annual_revenue"):
            confidence += 0.1
        if company_metrics.get("employee_count"):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _generate_recommendations(self, calculations: List[ROICalculation]) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Quick wins (high ROI, fast implementation)
        quick_wins = [calc for calc in calculations 
                     if calc.roi_percentage > 100 and calc.time_to_implement_days <= 30]
        if quick_wins:
            recommendations.append(
                f"Start with {len(quick_wins)} quick wins that can deliver "
                f"${sum(c.annual_savings for c in quick_wins):,.0f} in annual savings within 30 days"
            )
        
        # High impact projects
        high_impact = [calc for calc in calculations if calc.annual_savings > 50000]
        if high_impact:
            recommendations.append(
                f"Focus on {len(high_impact)} high-impact projects with combined "
                f"savings of ${sum(c.annual_savings for c in high_impact):,.0f} annually"
            )
        
        # Phased approach
        if len(calculations) > 5:
            recommendations.append(
                "Implement improvements in phases to manage change and demonstrate value incrementally"
            )
        
        return recommendations
    
    def _create_implementation_phases(self, calculations: List[ROICalculation]) -> List[Dict]:
        """Create phased implementation plan"""
        # Sort by ROI and implementation time
        sorted_calcs = sorted(calculations, 
                            key=lambda x: (x.roi_percentage / max(x.time_to_implement_days, 1)), 
                            reverse=True)
        
        phases = []
        
        # Phase 1: Quick wins (0-30 days)
        phase1 = [calc for calc in sorted_calcs 
                 if calc.time_to_implement_days <= 30 and calc.roi_percentage > 50][:3]
        if phase1:
            phases.append({
                "phase": 1,
                "name": "Quick Wins",
                "duration": "0-30 days",
                "projects": [calc.description for calc in phase1],
                "investment": sum(calc.implementation_cost for calc in phase1),
                "expected_savings": sum(calc.annual_savings for calc in phase1)
            })
        
        # Phase 2: Core improvements (31-90 days)
        phase2 = [calc for calc in sorted_calcs 
                 if calc not in phase1 and calc.time_to_implement_days <= 90][:3]
        if phase2:
            phases.append({
                "phase": 2,
                "name": "Core Improvements",
                "duration": "31-90 days",
                "projects": [calc.description for calc in phase2],
                "investment": sum(calc.implementation_cost for calc in phase2),
                "expected_savings": sum(calc.annual_savings for calc in phase2)
            })
        
        # Phase 3: Transformation (91+ days)
        phase3 = [calc for calc in sorted_calcs 
                 if calc not in phase1 + phase2][:3]
        if phase3:
            phases.append({
                "phase": 3,
                "name": "Full Transformation",
                "duration": "91-180 days",
                "projects": [calc.description for calc in phase3],
                "investment": sum(calc.implementation_cost for calc in phase3),
                "expected_savings": sum(calc.annual_savings for calc in phase3)
            })
        
        return phases
    
    def _generate_executive_recommendation(self, portfolio: Dict, benchmark: Dict, 
                                         company_metrics: Dict) -> str:
        """Generate executive recommendation"""
        roi = portfolio["portfolio_summary"]["portfolio_roi_percentage"]
        payback = portfolio["portfolio_summary"]["portfolio_payback_months"]
        performance = benchmark["performance_rating"]
        
        if roi > 200 and payback < 6:
            recommendation = "STRONGLY RECOMMENDED: This AI transformation presents an exceptional opportunity "
            recommendation += f"with {roi:.0f}% ROI and {payback:.1f} month payback. "
        elif roi > 100 and payback < 12:
            recommendation = "RECOMMENDED: This initiative offers strong returns "
            recommendation += f"with {roi:.0f}% ROI and {payback:.1f} month payback. "
        else:
            recommendation = "WORTH CONSIDERING: While returns are moderate, "
            recommendation += "the strategic benefits of automation are significant. "
        
        if performance == "Below Average":
            recommendation += "Additionally, reaching industry benchmarks could add "
            recommendation += f"${benchmark['improvement_potential']:,.0f} in annual revenue."
        
        return recommendation

# Test the analyzer
if __name__ == "__main__":
    analyzer = BusinessAnalyzer()
    
    # Sample company metrics
    company_metrics = {
        "company_name": "Smith Law Firm",
        "employee_count": 45,
        "annual_revenue": 8500000,
        "industry": "legal"
    }
    
    # Sample bottlenecks
    bottlenecks = [
        {
            "name": "Manual client intake",
            "annual_hours_impact": 1040,  # 20 hrs/week
            "annual_cost_impact": 156000,
            "automation_potential": 0.8,
            "solution_complexity": "medium"
        },
        {
            "name": "Document management",
            "annual_hours_impact": 520,  # 10 hrs/week
            "annual_cost_impact": 78000,
            "automation_potential": 0.7,
            "solution_complexity": "low"
        }
    ]
    
    # Generate executive summary
    summary = analyzer.generate_executive_summary(company_metrics, bottlenecks)
    print(json.dumps(summary, indent=2))