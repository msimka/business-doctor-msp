# Business Doctor Azure Infrastructure Setup Guide

## Overview
Setting up Azure infrastructure for Business Doctor MSP operations, focusing on multi-tenant architecture and AI services.

## Step 1: Create Azure Account and Tenant

### 1.1 Sign Up
- Go to https://azure.microsoft.com/en-us/free/
- Use business email (mike@businessdoctor.ai)
- Choose "Start free" for $200 credit + 12 months free services

### 1.2 Create Business Doctor Tenant
```bash
# Tenant naming convention
Tenant Name: businessdoctor.onmicrosoft.com
Primary Domain: businessdoctor.ai (add later)
Region: West US 2 (lowest latency for CA)
```

## Step 2: Essential Services Setup

### 2.1 Resource Groups
Create logical groupings for resources:
```
- rg-businessdoctor-core (shared infrastructure)
- rg-businessdoctor-dev (development/testing)
- rg-businessdoctor-clients (client deployments)
- rg-businessdoctor-ai (AI services)
```

### 2.2 Core Services to Enable

#### Azure Active Directory
- Set up MFA for all admin accounts
- Create service principals for automation
- Configure B2B for client access

#### Azure OpenAI Service
1. Apply for access: https://aka.ms/oai/access
2. Deploy models:
   - GPT-4 for complex reasoning
   - GPT-3.5-Turbo for high-volume
   - Text-embedding-ada-002 for search

#### Storage Account
```bash
Name: stbusinessdoctor001
Type: StorageV2
Replication: LRS (locally redundant)
Access tier: Hot
```

#### Key Vault
```bash
Name: kv-businessdoctor-prod
Purpose: Store all secrets, keys, certificates
Access: RBAC-based
```

## Step 3: Development Environment

### 3.1 Azure DevOps Setup
- Create organization: dev.azure.com/businessdoctor
- Set up CI/CD pipelines
- Configure artifact feeds

### 3.2 Development Resources
```yaml
# Azure Functions for custom automation
- Function App: func-bd-automation
- Runtime: Python 3.9
- Plan: Consumption (serverless)

# Logic Apps for Power Automate overflow
- Logic App: logic-bd-workflows
- Region: Same as tenant
```

## Step 4: Client Infrastructure Pattern

### 4.1 Multi-Tenant Architecture
```
Business Doctor Azure Subscription
├── Shared Resources
│   ├── Azure OpenAI (shared, tagged per client)
│   ├── Key Vault (shared secrets)
│   └── Monitor/Log Analytics
└── Per-Client Resources
    ├── Resource Group: rg-client-[name]
    ├── Storage: st[clientname]001
    └── Automation Account (if needed)
```

### 4.2 Client Onboarding Automation
```powershell
# PowerShell script to provision client resources
param(
    [string]$ClientName,
    [string]$ClientId,
    [string]$Tier  # Foundation/Automation/Transformation
)

# Create resource group
New-AzResourceGroup -Name "rg-client-$ClientName" -Location "WestUS2"

# Create storage account
New-AzStorageAccount -ResourceGroupName "rg-client-$ClientName" `
    -Name "st$($ClientName)001" `
    -SkuName Standard_LRS `
    -Location "WestUS2"

# Tag for billing
Set-AzResourceGroup -Name "rg-client-$ClientName" `
    -Tag @{Client=$ClientId; Tier=$Tier; ManagedBy="BusinessDoctor"}
```

## Step 5: Security Configuration

### 5.1 Network Security
- Enable Azure Firewall for egress control
- Configure NSGs for all subnets
- Enable DDoS Protection Basic

### 5.2 Identity Protection
- Enable Conditional Access policies
- Configure PIM for privileged roles
- Set up Azure AD Identity Protection

### 5.3 Compliance
- Enable Azure Policy for governance
- Configure diagnostic settings
- Set up Azure Monitor alerts

## Step 6: Cost Management

### 6.1 Budget Alerts
```json
{
  "name": "Monthly-Azure-Budget",
  "amount": 2000,
  "timeGrain": "Monthly",
  "notifications": {
    "80_percent": {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 80,
      "contactEmails": ["mike@businessdoctor.ai"]
    }
  }
}
```

### 6.2 Cost Optimization
- Use Reserved Instances for predictable workloads
- Enable auto-shutdown for dev resources
- Use spot instances for batch processing

## Step 7: Monitoring Setup

### 7.1 Application Insights
- Track custom automation performance
- Monitor API calls to OpenAI
- Set up alerts for failures

### 7.2 Log Analytics Workspace
```bash
Name: log-businessdoctor-prod
Retention: 30 days (free tier)
Data sources:
- Azure Activity Logs
- Azure AD Sign-ins
- Custom application logs
```

## Step 8: Backup and DR

### 8.1 Backup Strategy
- Azure Backup for VMs (if any)
- Soft delete for storage accounts
- Geo-redundant storage for critical data

### 8.2 Disaster Recovery
- Document RTO/RPO requirements
- Use Azure Site Recovery if needed
- Regular DR testing schedule

## Step 9: Automation Scripts

### 9.1 Client Deployment Script
Save as `deploy-client.ps1`:
```powershell
# Full client deployment automation
# Includes resource creation, permissions, and initial config
# [Full script available in /scripts folder]
```

### 9.2 Monitoring Script
Save as `monitor-clients.ps1`:
```powershell
# Check all client resource health
# Generate usage reports
# Alert on anomalies
```

## Step 10: Partner Benefits Integration

### 10.1 Link Partner ID
- In Azure Portal → Cost Management
- Add Partner ID from Partner Center
- Ensures credit for Azure consumption

### 10.2 Use Partner Credits
- Apply monthly Azure credits
- Track usage in Partner Center
- Plan usage to maximize benefits

## Quick Commands Reference

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "Business Doctor"

# Create resource group
az group create --name rg-businessdoctor-core --location westus2

# List all resources
az resource list --output table

# Check spending
az consumption usage list --start-date 2025-01-01 --end-date 2025-01-31
```

## Next Steps
1. Complete Azure OpenAI access request
2. Set up first client resource group
3. Deploy diagnostic tool as Azure Function
4. Configure monitoring dashboards
5. Document client onboarding process