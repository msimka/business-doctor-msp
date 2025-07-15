# Business Doctor MSP - Technical Stack Documentation

## Architecture Overview
Modern web application with AI-powered conversation engine, designed for rapid prototyping and seamless transition from human-piloted to fully automated system.

## Core Technology Stack

### Frontend & UI
- **Framework**: Streamlit 1.29.0
  - Rapid prototyping and deployment
  - Built-in chat interfaces
  - Real-time updates and streaming
- **Styling**: Custom CSS with professional theming
  - Glass Box transparency effects
  - Business-grade color scheme (#667eea primary)
  - Responsive layout for desktop/mobile

### AI & Language Models
- **Primary AI**: Google Gemini Pro
  - Model: `gemini-pro`
  - Free tier usage (backup API key)
  - Content generation and conversation
- **API Key**: Backup from mikedisney1901@gmail.com account
  - Preserves main API quota for other projects
  - Key: `AIzaSyC0r-ujNDB0Wrpz4_MDUwP1a0yV7zPWqek`

### Backend & Logic
- **Language**: Python 3.13
- **Async Support**: nest-asyncio for Streamlit compatibility
- **Data Structures**: Dataclasses for type safety
- **Session Management**: Streamlit session state

### Deployment & Infrastructure
- **Hosting**: Streamlit Cloud
  - Automatic GitHub integration
  - Free tier deployment
  - SSL and CDN included
- **Repository**: GitHub (msimka/business-doctor-msp)
- **Branch Strategy**: Main branch for production

## Key Dependencies

### Python Packages
```txt
streamlit==1.29.0
google-generativeai==0.3.2
plotly==5.18.0
python-dateutil==2.8.2
```

### Configuration Files
- `.streamlit/config.toml` - Theme and server settings
- `.streamlit/secrets.toml` - API keys and configuration
- `requirements.txt` - Dependency management

## System Architecture

### Dual Interface Design
```
┌─────────────────┐    ┌─────────────────┐
│   Client View   │    │ Operator View   │
│                 │    │                 │
│ • Glass Box UI  │    │ • AI Controls   │
│ • Chat Interface│◄──►│ • Response Edit │
│ • AI Reasoning  │    │ • Metrics Track │
│ • Process Maps  │    │ • Quick Tools   │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
            ┌─────────▼─────────┐
            │  Session State    │
            │                   │
            │ • Conversation    │
            │ • Insights        │
            │ • Bottlenecks     │
            │ • Process Maps    │
            └───────────────────┘
```

### Data Flow
1. **Client Input** → Session State
2. **Operator Processing** → AI Suggestions + Manual Override
3. **AI Generation** → Gemini API → Response Streaming
4. **Context Management** → Structured Summary Objects
5. **Real-time Updates** → Both Interfaces

## File Structure
```
business-doctor-msp/
├── deployment/
│   ├── streamlit_app.py         # Main application
│   ├── test_app.py             # Debug version
│   ├── requirements.txt        # Dependencies
│   └── .streamlit/
│       ├── config.toml         # App configuration
│       └── secrets.toml        # API keys
├── intake-system/
│   ├── wizard_of_oz_implementation.py  # Dual interface
│   ├── streaming_conversation.py       # Chat system
│   └── structured_summary_objects.py   # Data models
├── legal/
│   └── data_consent_gdpr_framework.md  # Compliance
├── products/
│   └── diagnostic_roadmap_product.md   # $2.5K offering
└── session_continuity/          # Documentation
```

## Security & Compliance

### API Key Management
- **Secrets**: Stored in Streamlit Cloud secrets
- **Environment**: Separate keys for dev/prod
- **Rotation**: Manual key rotation capability

### Data Protection
- **GDPR Compliance**: Built-in consent management
- **CCPA Compliance**: Data subject rights handling
- **Encryption**: HTTPS/TLS for all communications
- **Retention**: 90-day active, 7-year archive policy

### Access Control
- **Operator Mode**: URL parameter protection
- **Client Mode**: Public access (intended)
- **Secrets**: Server-side only (not client-exposed)

## Performance Considerations

### Optimization Strategies
- **Lazy Loading**: Import modules as needed
- **Session Caching**: Streamlit session state
- **API Efficiency**: Structured summaries reduce token usage
- **Streaming**: Progressive response display

### Scalability Limits
- **Concurrent Users**: Streamlit Cloud free tier limits
- **API Rate Limits**: Google Gemini free tier quotas
- **Memory**: Session state per user
- **Storage**: No persistent database (pilot phase)

## Development Workflow

### Local Development
```bash
cd deployment
streamlit run streamlit_app.py
# Opens: http://localhost:8501
# Operator: http://localhost:8501?mode=operator
```

### Deployment Process
1. **Git Push** → GitHub repository
2. **Auto Deploy** → Streamlit Cloud detects changes
3. **Build & Test** → Automatic dependency installation
4. **Live Update** → ~30 seconds deployment time

### Debugging Tools
- **Test App**: Simplified version for troubleshooting
- **Error Logging**: Streamlit Cloud dashboard
- **API Testing**: Built-in status checks

## Integration Points

### External Services
- **Google Gemini**: AI conversation generation
- **Streamlit Cloud**: Hosting and deployment
- **GitHub**: Version control and CI/CD

### Future Integrations (Planned)
- **Microsoft Graph**: M365 diagnostic data
- **Power Platform**: Client environment integration
- **Azure**: Enterprise deployment option

## Monitoring & Analytics

### Current Capabilities
- **Session Tracking**: User interaction logs
- **Error Monitoring**: Streamlit error reporting
- **Performance**: Basic timing metrics

### Planned Enhancements
- **User Analytics**: Conversation completion rates
- **Business Metrics**: Conversion tracking
- **Performance Monitoring**: Response time optimization

---
*Technical Stack Version: 1.0*
*Last Updated: 2025-07-14 21:45 PST*
*Deployment Status: Testing Phase*