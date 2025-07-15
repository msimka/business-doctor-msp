#!/usr/bin/env python3
"""
Business Doctor Terminal Application
MS-DOS style interface for business consultations
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.business_doctor_engine import BusinessDoctorEngine, ProcessBottleneck
from core.data_pipeline import create_pipeline, DataRecord
from core.business_analyzer import BusinessAnalyzer

class TerminalColors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class BusinessDoctorTerminal:
    """Terminal interface for Business Doctor consultations"""
    
    def __init__(self, api_key: str):
        self.engine = BusinessDoctorEngine(api_key)
        self.pipeline = create_pipeline()
        self.analyzer = BusinessAnalyzer()
        self.consultation_id = None
        self.session_start = datetime.now()
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        self.clear_screen()
        print(f"{TerminalColors.CYAN}{'='*80}{TerminalColors.ENDC}")
        print(f"{TerminalColors.BOLD}{TerminalColors.CYAN}")
        print("  ╔══════════════════════════════════════════════════════════════════╗")
        print("  ║                   BUSINESS DOCTOR AI SYSTEM                      ║")
        print("  ║              Intelligent Business Process Analysis               ║")
        print("  ║                    Version 1.0 - Terminal                        ║")
        print("  ╚══════════════════════════════════════════════════════════════════╝")
        print(f"{TerminalColors.ENDC}")
        print(f"{TerminalColors.CYAN}{'='*80}{TerminalColors.ENDC}\n")
    
    def print_menu(self):
        """Print main menu"""
        print(f"{TerminalColors.BOLD}MAIN MENU{TerminalColors.ENDC}")
        print("1. Start New Consultation")
        print("2. Load Previous Consultation")
        print("3. View Reports")
        print("4. Industry Benchmarks")
        print("5. Help")
        print("6. Exit")
        print()
    
    def print_status(self):
        """Print current session status"""
        duration = (datetime.now() - self.session_start).seconds // 60
        stage = self.engine.current_stage.value.replace('_', ' ').title()
        
        print(f"\n{TerminalColors.BLUE}{'─'*80}{TerminalColors.ENDC}")
        print(f"Stage: {TerminalColors.BOLD}{stage}{TerminalColors.ENDC} | ", end="")
        print(f"Duration: {duration} min | ", end="")
        print(f"Bottlenecks: {len(self.engine.bottlenecks)} | ", end="")
        print(f"Messages: {len(self.engine.conversation_history)}")
        print(f"{TerminalColors.BLUE}{'─'*80}{TerminalColors.ENDC}\n")
    
    def start_consultation(self):
        """Start a new consultation"""
        self.print_header()
        print(f"{TerminalColors.BOLD}NEW CONSULTATION{TerminalColors.ENDC}\n")
        
        # Get basic info
        print("Let's start with some basic information:")
        client_id = input("Your email: ").strip()
        
        # Create consultation record
        consultation = DataRecord(
            id="",
            timestamp=datetime.now(),
            record_type="consultation",
            data={
                "client_id": client_id,
                "start_time": datetime.now().isoformat(),
                "status": "in_progress"
            }
        )
        
        # Process through pipeline
        processed = self.pipeline.process(consultation)
        self.consultation_id = processed.id
        
        print(f"\n{TerminalColors.GREEN}✓ Consultation started (ID: {self.consultation_id}){TerminalColors.ENDC}\n")
        
        # Start conversation
        self.run_conversation()
    
    def run_conversation(self):
        """Run the consultation conversation"""
        print(f"{TerminalColors.BOLD}CONSULTATION SESSION{TerminalColors.ENDC}")
        print("Type 'help' for commands, 'exit' to end consultation\n")
        
        # Initial greeting
        result = self.engine.process_input("")
        self.print_ai_response(result["response"])
        
        while True:
            self.print_status()
            
            # Get user input
            user_input = input(f"{TerminalColors.GREEN}You: {TerminalColors.ENDC}").strip()
            
            # Handle commands
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'help':
                self.show_help()
                continue
            elif user_input.lower() == 'status':
                self.show_detailed_status()
                continue
            elif user_input.lower() == 'report':
                self.generate_report()
                continue
            
            # Process input
            print(f"\n{TerminalColors.CYAN}[Processing...]{TerminalColors.ENDC}")
            result = self.engine.process_input(user_input)
            
            # Store bottlenecks in pipeline
            self.store_bottlenecks()
            
            # Show AI response
            self.print_ai_response(result["response"])
            
            # Show insights if any
            if result["bottlenecks_found"] > len(self.engine.bottlenecks) - 1:
                print(f"\n{TerminalColors.WARNING}⚡ New bottleneck identified!{TerminalColors.ENDC}")
        
        # End consultation
        self.end_consultation()
    
    def print_ai_response(self, response: str):
        """Print AI response with formatting"""
        print(f"\n{TerminalColors.BOLD}Business Doctor:{TerminalColors.ENDC}")
        
        # Wrap text for better readability
        words = response.split()
        line = ""
        for word in words:
            if len(line) + len(word) > 75:
                print(line)
                line = word
            else:
                line += (" " + word) if line else word
        if line:
            print(line)
        print()
    
    def show_help(self):
        """Show help information"""
        print(f"\n{TerminalColors.BOLD}AVAILABLE COMMANDS:{TerminalColors.ENDC}")
        print("  help    - Show this help menu")
        print("  status  - Show detailed consultation status")
        print("  report  - Generate current findings report")
        print("  exit    - End consultation and generate final report")
        print()
    
    def show_detailed_status(self):
        """Show detailed consultation status"""
        print(f"\n{TerminalColors.BOLD}CONSULTATION STATUS{TerminalColors.ENDC}")
        
        # Company info
        metrics = self.engine.metrics
        print(f"\nCompany: {metrics.company_name or 'Not specified'}")
        print(f"Industry: {metrics.industry or 'Not specified'}")
        print(f"Employees: {metrics.employee_count or 'Not specified'}")
        print(f"Revenue: ${metrics.annual_revenue:,.0f}" if metrics.annual_revenue else "Revenue: Not specified")
        
        # Bottlenecks
        print(f"\n{TerminalColors.BOLD}Bottlenecks Identified:{TerminalColors.ENDC}")
        if self.engine.bottlenecks:
            for i, bottleneck in enumerate(self.engine.bottlenecks, 1):
                hours, cost = bottleneck.calculate_annual_impact()
                print(f"{i}. {bottleneck.name}")
                print(f"   Impact: {hours:.0f} hours/year (${cost:,.0f})")
                print(f"   Automation Potential: {bottleneck.automation_potential:.0%}")
        else:
            print("No bottlenecks identified yet")
        
        print()
    
    def store_bottlenecks(self):
        """Store identified bottlenecks in pipeline"""
        for bottleneck in self.engine.bottlenecks:
            # Check if already stored
            existing = self.pipeline.get_bottlenecks(self.consultation_id)
            if any(b['name'] == bottleneck.name for b in existing):
                continue
            
            # Store new bottleneck
            record = DataRecord(
                id="",
                timestamp=datetime.now(),
                record_type="bottleneck",
                data={
                    "consultation_id": self.consultation_id,
                    "name": bottleneck.name,
                    "description": bottleneck.description,
                    "department": bottleneck.department,
                    "frequency": bottleneck.frequency,
                    "time_impact_hours": bottleneck.time_impact_hours,
                    "cost_impact": bottleneck.cost_impact,
                    "automation_potential": bottleneck.automation_potential,
                    "priority": bottleneck.priority
                }
            )
            self.pipeline.process(record)
    
    def generate_report(self):
        """Generate and display report"""
        print(f"\n{TerminalColors.BOLD}GENERATING REPORT...{TerminalColors.ENDC}")
        
        # Get data
        consultation = self.pipeline.get_consultation(self.consultation_id)
        bottlenecks = self.pipeline.get_bottlenecks(self.consultation_id)
        
        # Generate analysis
        company_metrics = {
            "company_name": self.engine.metrics.company_name,
            "employee_count": self.engine.metrics.employee_count,
            "annual_revenue": self.engine.metrics.annual_revenue,
            "industry": self.engine.metrics.industry
        }
        
        summary = self.analyzer.generate_executive_summary(company_metrics, bottlenecks)
        
        # Display report
        self.clear_screen()
        print(f"{TerminalColors.CYAN}{'='*80}{TerminalColors.ENDC}")
        print(f"{TerminalColors.BOLD}BUSINESS DIAGNOSTIC REPORT{TerminalColors.ENDC}")
        print(f"{TerminalColors.CYAN}{'='*80}{TerminalColors.ENDC}\n")
        
        # Company snapshot
        snapshot = summary["company_snapshot"]
        print(f"{TerminalColors.BOLD}Company:{TerminalColors.ENDC} {snapshot['name']}")
        print(f"{TerminalColors.BOLD}Industry:{TerminalColors.ENDC} {snapshot['industry']}")
        print(f"{TerminalColors.BOLD}Employees:{TerminalColors.ENDC} {snapshot['employees']}")
        print(f"{TerminalColors.BOLD}Revenue:{TerminalColors.ENDC} ${snapshot['annual_revenue']:,.0f}")
        
        # Key findings
        findings = summary["key_findings"]
        print(f"\n{TerminalColors.BOLD}KEY FINDINGS:{TerminalColors.ENDC}")
        print(f"• Total inefficiency: {findings['total_inefficiency_hours_annual']:,.0f} hours/year")
        print(f"• Cost impact: ${findings['total_inefficiency_cost_annual']:,.0f}/year")
        print(f"• Bottlenecks found: {findings['number_of_bottlenecks']}")
        print(f"• Automation opportunity: ${findings['automation_opportunity']:,.0f}/year")
        
        # ROI highlights
        roi = summary["roi_highlights"]
        print(f"\n{TerminalColors.BOLD}ROI ANALYSIS:{TerminalColors.ENDC}")
        print(f"• Investment required: ${roi['total_investment_required']:,.0f}")
        print(f"• Annual savings: ${roi['annual_savings_potential']:,.0f}")
        print(f"• ROI: {roi['roi_percentage']:.0f}%")
        print(f"• Payback period: {roi['payback_period_months']:.1f} months")
        
        # Top opportunities
        print(f"\n{TerminalColors.BOLD}TOP 3 OPPORTUNITIES:{TerminalColors.ENDC}")
        for i, opp in enumerate(summary["top_3_opportunities"], 1):
            print(f"{i}. {opp['description']}")
            print(f"   Savings: ${opp['annual_savings']:,.0f}/year")
            print(f"   ROI: {opp['roi_percentage']:.0f}%")
        
        # Recommendation
        print(f"\n{TerminalColors.BOLD}RECOMMENDATION:{TerminalColors.ENDC}")
        print(summary["executive_recommendation"])
        
        print(f"\n{TerminalColors.CYAN}{'='*80}{TerminalColors.ENDC}")
        
        # Save report
        self.save_report(summary)
        
        input("\nPress Enter to continue...")
    
    def save_report(self, summary: Dict):
        """Save report to file and pipeline"""
        # Save to pipeline
        record = DataRecord(
            id="",
            timestamp=datetime.now(),
            record_type="report",
            data={
                "consultation_id": self.consultation_id,
                "report_type": "diagnostic",
                "report_data": summary
            }
        )
        self.pipeline.process(record)
        
        # Save to file
        filename = f"report_{self.consultation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n{TerminalColors.GREEN}✓ Report saved to {filename}{TerminalColors.ENDC}")
    
    def end_consultation(self):
        """End consultation and generate final report"""
        print(f"\n{TerminalColors.BOLD}ENDING CONSULTATION...{TerminalColors.ENDC}")
        
        # Update consultation status
        consultation = self.pipeline.get_consultation(self.consultation_id)
        if consultation:
            consultation['end_time'] = datetime.now().isoformat()
            consultation['status'] = 'completed'
            
            # Store updated conversation
            record = DataRecord(
                id=self.consultation_id,
                timestamp=datetime.now(),
                record_type="consultation",
                data={
                    **consultation,
                    "conversation_data": self.engine.conversation_history,
                    "metrics_data": {
                        "company_name": self.engine.metrics.company_name,
                        "employee_count": self.engine.metrics.employee_count,
                        "annual_revenue": self.engine.metrics.annual_revenue,
                        "industry": self.engine.metrics.industry
                    }
                }
            )
            self.pipeline.process(record)
        
        # Generate final report
        self.generate_report()
        
        print(f"\n{TerminalColors.GREEN}✓ Consultation completed successfully!{TerminalColors.ENDC}")
        print(f"Duration: {(datetime.now() - self.session_start).seconds // 60} minutes")
        print(f"Bottlenecks identified: {len(self.engine.bottlenecks)}")
    
    def load_consultation(self):
        """Load a previous consultation"""
        print(f"\n{TerminalColors.BOLD}LOAD CONSULTATION{TerminalColors.ENDC}\n")
        
        consultation_id = input("Enter consultation ID: ").strip()
        
        consultation = self.pipeline.get_consultation(consultation_id)
        if not consultation:
            print(f"{TerminalColors.FAIL}✗ Consultation not found{TerminalColors.ENDC}")
            return
        
        # Load data
        self.consultation_id = consultation_id
        bottlenecks = self.pipeline.get_bottlenecks(consultation_id)
        
        print(f"\n{TerminalColors.GREEN}✓ Loaded consultation{TerminalColors.ENDC}")
        print(f"Company: {consultation.get('company_name', 'Unknown')}")
        print(f"Status: {consultation.get('status', 'Unknown')}")
        print(f"Bottlenecks: {len(bottlenecks)}")
        
        input("\nPress Enter to continue...")
    
    def show_benchmarks(self):
        """Show industry benchmarks"""
        self.clear_screen()
        print(f"{TerminalColors.BOLD}INDUSTRY BENCHMARKS{TerminalColors.ENDC}\n")
        
        for industry, data in BusinessAnalyzer.INDUSTRY_BENCHMARKS.items():
            print(f"{TerminalColors.BOLD}{industry.upper()}{TerminalColors.ENDC}")
            print(f"  Revenue per employee: ${data['revenue_per_employee']:,}")
            print(f"  Billable hours: {data['billable_hours_percentage']:.0%}")
            print(f"  Admin overhead: {data['admin_overhead_percentage']:.0%}")
            print(f"  Typical hourly rate: ${data['typical_hourly_rate']}")
            print()
        
        input("Press Enter to continue...")
    
    def run(self):
        """Run the terminal application"""
        while True:
            self.print_header()
            self.print_menu()
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.start_consultation()
            elif choice == '2':
                self.load_consultation()
            elif choice == '3':
                self.generate_report() if self.consultation_id else print("No active consultation")
            elif choice == '4':
                self.show_benchmarks()
            elif choice == '5':
                self.show_help()
            elif choice == '6':
                print(f"\n{TerminalColors.GREEN}Thank you for using Business Doctor AI!{TerminalColors.ENDC}")
                break
            else:
                print(f"{TerminalColors.FAIL}Invalid option. Please try again.{TerminalColors.ENDC}")
                time.sleep(1)

def main():
    """Main entry point"""
    # Get API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Please set GOOGLE_API_KEY environment variable")
        print("export GOOGLE_API_KEY='your-api-key'")
        return
    
    # Run application
    app = BusinessDoctorTerminal(api_key)
    app.run()

if __name__ == "__main__":
    main()