# Business Doctor Core Engine

## Overview
This is the core business logic and data pipeline for the Business Doctor AI system. It's designed as a terminal-based application (MS-DOS style) that handles all the business intelligence, data processing, and AI interactions without any GUI dependencies.

## Architecture

### Core Components

1. **Business Doctor Engine** (`business_doctor_engine.py`)
   - Main conversation engine using Google Gemini AI
   - Handles conversation flow through 8 stages
   - Extracts business metrics and identifies bottlenecks
   - Generates contextual responses based on conversation stage

2. **Data Pipeline** (`data_pipeline.py`)
   - SQLite-based data persistence
   - Handles all data flow and transformations
   - Stores consultations, bottlenecks, insights, and reports
   - Provides data validation and processing

3. **Business Analyzer** (`business_analyzer.py`)
   - ROI calculations and financial analysis
   - Industry benchmarking
   - Portfolio optimization
   - Executive summary generation

4. **Terminal Application** (`terminal_app.py`)
   - MS-DOS style interface
   - Manages user interaction
   - Orchestrates all components
   - Generates reports

## Data Flow

```
User Input → Business Doctor Engine → Extract Information
                    ↓
              Identify Bottlenecks
                    ↓
              Data Pipeline → Store in SQLite
                    ↓
            Business Analyzer → Calculate ROI
                    ↓
              Generate Report → Export Results
```

## Key Features

### Conversation Management
- 8-stage structured conversation flow
- Intelligent stage progression
- Context-aware responses
- Fallback responses for reliability

### Data Extraction
- Automated extraction of business metrics
- Process identification
- Bottleneck detection
- Time and cost impact analysis

### Business Intelligence
- ROI calculations for each bottleneck
- Portfolio-level analysis
- Industry benchmarking
- Phased implementation planning

### Data Persistence
- SQLite database for all data
- Structured data model
- Full conversation history
- Report generation and storage

## Usage

### Running the Terminal App
```bash
# Set your API key
export GOOGLE_API_KEY='your-gemini-api-key'

# Run the application
./run_business_doctor.sh
```

### Direct Python Usage
```python
from core.business_doctor_engine import BusinessDoctorEngine
from core.data_pipeline import create_pipeline
from core.business_analyzer import BusinessAnalyzer

# Initialize components
engine = BusinessDoctorEngine(api_key)
pipeline = create_pipeline()
analyzer = BusinessAnalyzer()

# Process user input
result = engine.process_input("We have 50 employees and struggle with manual invoicing")

# Store bottlenecks
for bottleneck in engine.bottlenecks:
    # Process through pipeline
    pass

# Generate analysis
summary = analyzer.generate_executive_summary(
    engine.metrics.__dict__, 
    engine.bottlenecks
)
```

## Database Schema

### Consultations Table
- `id`: Unique consultation ID
- `client_id`: Client email
- `company_name`: Company name
- `start_time`: Consultation start
- `end_time`: Consultation end
- `status`: in_progress/completed
- `conversation_data`: Full conversation JSON
- `metrics_data`: Company metrics JSON

### Bottlenecks Table
- `id`: Unique bottleneck ID
- `consultation_id`: Parent consultation
- `name`: Bottleneck name
- `description`: Detailed description
- `time_impact_hours`: Weekly time impact
- `cost_impact`: Weekly cost impact
- `automation_potential`: 0-1 scale
- `priority`: low/medium/high/critical

### Insights Table
- `id`: Unique insight ID
- `consultation_id`: Parent consultation
- `category`: Insight category
- `insight`: Insight text
- `confidence`: 0-1 confidence level
- `potential_value`: Dollar value
- `implementation_effort`: low/medium/high

### Reports Table
- `id`: Unique report ID
- `consultation_id`: Parent consultation
- `report_type`: diagnostic/proposal/executive
- `report_data`: Full report JSON

## Business Metrics

### Company Metrics Tracked
- Company name and industry
- Employee count
- Annual revenue
- Technology stack
- Current challenges

### Bottleneck Analysis
- Time impact (hours/week)
- Cost impact (dollars/week)
- Automation potential (0-1)
- Annual projections
- Priority ranking

### ROI Calculations
- Current state costs
- Improved state projections
- Implementation investment
- Annual savings
- Payback period
- ROI percentage

## Industry Benchmarks

Pre-loaded benchmarks for:
- Legal firms
- Accounting firms
- Consulting firms
- MSPs (Managed Service Providers)
- Default/General business

Each benchmark includes:
- Revenue per employee
- Billable hours percentage
- Admin overhead percentage
- Typical hourly rates

## Report Generation

The system generates comprehensive reports including:
- Executive summary
- Company snapshot
- Key findings
- ROI analysis
- Top opportunities
- Implementation roadmap
- Industry comparison
- Strategic recommendations

## Terminal Interface

The MS-DOS style interface provides:
- Clear navigation menus
- Status tracking
- Color-coded output
- Progress indicators
- Command shortcuts
- Report generation
- Data export options

## Future Enhancements

1. **Additional AI Models**
   - Support for Claude, GPT-4
   - Model selection based on task

2. **Advanced Analytics**
   - Machine learning for pattern detection
   - Predictive analytics
   - Comparative analysis

3. **Integration APIs**
   - REST API for external access
   - Webhook support
   - Third-party integrations

4. **Enhanced Reporting**
   - PDF generation
   - Email delivery
   - Custom templates