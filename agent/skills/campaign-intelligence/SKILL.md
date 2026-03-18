# Campaign Intelligence Skill

## Purpose
Gather comprehensive campaign performance data across all major paid channels for complete marketing picture.

## Intelligence Sources

### 1. Meta Campaigns (MKL Agent) ✅
**Agent:** `mkl` (Meta Killer Lite)
**Capabilities:**
- Campaign performance across all Meta ad accounts
- Creative-level metrics and insights
- Audience performance and optimization recommendations
- Budget utilization and pacing analysis
- Cross-product campaign comparison

**Spawn Parameters:**
```python
{
    "agentId": "mkl",
    "task": f"Generate {product} Meta campaign performance report for meeting prep. Include: campaign metrics, creative performance, audience insights, budget status, optimization recommendations. Focus on last 7 days vs previous period.",
    "mode": "run",
    "timeoutSeconds": 300
}
```

### 2. Google Campaigns (Seekr Agent) 🔄 NEEDS INSTALL
**Agent:** `seekr` (Google Ads specialist)
**Capabilities:**
- Google Ads campaign performance
- Search query analysis and keyword optimization
- Landing page performance correlation
- Audience insights and conversion tracking
- Budget recommendations and bid optimization

**Installation Required:**
```bash
# User will need to provide GitHub repo and installation instructions
# Expected similar to other agents with workspace setup
```

### 3. Apple Search Ads (apple-search Agent) 🔄 NEEDS INSTALL  
**Agent:** `apple-search`
**Capabilities:**
- Apple Search Ads campaign performance
- Keyword bidding and optimization
- App Store search visibility
- Competitor keyword analysis
- iOS-specific conversion tracking

**Installation Required:**
```bash
# User will provide GitHub repo
# Likely requires Apple Search Ads API credentials
```

### 4. Prior Meeting Notes Context (Google Drive)
**Method:** `gog` Google Drive integration
**Search Strategy:**
```bash
# Search for recent meeting notes/docs
gog drive search "{product} meeting notes" --type document --modified-after 2026-03-01

# Search for strategy docs and decisions
gog drive search "{product} (strategy OR roadmap OR decisions)" --type document 

# Search for previous meeting prep or reviews
gog drive search "{product} (weekly review OR performance review)" --type document
```

**Context Extraction:**
- Previous meeting outcomes and decisions
- Strategic initiatives and their progress
- Recurring issues and their resolution status
- Team commitments and deliverables
- Budget decisions and allocation changes

## Enhanced Intelligence Orchestration

### Campaign Performance Synthesis
```python
async def gather_campaign_intelligence(product: str) -> Dict[str, Any]:
    """Gather comprehensive campaign performance across all channels"""
    
    # Parallel campaign data gathering
    meta_task = spawn_mkl_agent(product)
    google_task = spawn_seekr_agent(product)  # Once installed
    apple_task = spawn_apple_search_agent(product)  # Once installed
    
    campaign_intelligence = {
        'meta': await meta_task,
        'google': await google_task,
        'apple_search': await apple_task,
        'channel_comparison': analyze_cross_channel_performance(),
        'optimization_opportunities': identify_channel_optimization(),
        'budget_allocation_insights': analyze_channel_efficiency()
    }
    
    return campaign_intelligence
```

### Cross-Channel Analysis
```python
def analyze_cross_channel_performance(meta_data, google_data, apple_data):
    """Compare performance across paid channels"""
    
    analysis = {
        'cost_efficiency': {
            'meta_cpi': meta_data.get('average_cpi'),
            'google_cpi': google_data.get('average_cpi'), 
            'apple_cpi': apple_data.get('average_cpi'),
            'most_efficient': determine_most_efficient_channel()
        },
        'scale_opportunities': {
            'meta_scale': assess_meta_scale_potential(),
            'google_scale': assess_google_scale_potential(),
            'apple_scale': assess_apple_scale_potential()
        },
        'audience_insights': {
            'meta_audiences': meta_data.get('top_audiences'),
            'google_keywords': google_data.get('top_keywords'),
            'apple_keywords': apple_data.get('top_keywords')
        }
    }
    
    return analysis
```

### Meeting Notes Context Integration
```python
async def gather_drive_context(product: str, meeting_type: str) -> Dict[str, Any]:
    """Extract context from Google Drive meeting notes and docs"""
    
    # Search for relevant documents
    queries = [
        f"{product} meeting notes",
        f"{product} weekly review", 
        f"{product} performance review",
        f"{product} strategy decisions"
    ]
    
    drive_context = {
        'previous_meetings': [],
        'strategic_context': [],
        'outstanding_items': [],
        'recurring_themes': []
    }
    
    for query in queries:
        docs = await search_google_drive(query, days_back=30)
        drive_context = await extract_document_insights(docs, drive_context)
    
    return drive_context
```

## Report Integration

### Enhanced Campaign Performance Section
```markdown
## Campaign Performance Analysis

### 📊 Multi-Channel Overview
| Channel | Spend | CPI | Conversions | Efficiency |
|---------|-------|-----|-------------|------------|
| Meta | ${meta_spend} | ${meta_cpi} | {meta_conv} | {meta_eff} |
| Google | ${google_spend} | ${google_cpi} | {google_conv} | {google_eff} |
| Apple | ${apple_spend} | ${apple_cpi} | {apple_conv} | {apple_eff} |

### 🎯 Channel Optimization Opportunities
**Meta:** {meta_optimization_rec}
**Google:** {google_optimization_rec}  
**Apple Search:** {apple_optimization_rec}

### 💰 Budget Allocation Insights
**Most Efficient:** {best_channel} (${best_cpi} CPI)
**Scale Opportunity:** {scale_channel} ({scale_rationale})
**Reallocation Rec:** {budget_shift_recommendation}
```

### Enhanced Meeting Context
```markdown
## Meeting Context & Historical Perspective

### 📄 Previous Meeting Outcomes
- **Last Review:** {last_meeting_date} - {key_decisions}
- **Outstanding Items:** {pending_action_items}
- **Progress Updates:** {completed_initiatives}

### 📈 Strategic Context
- **Current Initiatives:** {active_strategy_items}
- **Roadmap Progress:** {roadmap_status}
- **Resource Allocation:** {team_focus_areas}

### 🔄 Recurring Themes
{recurring_issues_and_patterns}
```

## Integration Points

### Orchestrator Enhancement
```python
# Add to intelligence gathering pipeline
async def gather_intelligence(self, product: str, meeting: Dict) -> Dict[str, Any]:
    
    # Existing intelligence sources
    performance_task = self.spawn_44growth(product)
    creative_task = self.spawn_creative_strategist(product) 
    competitive_task = self.query_sensor_tower(product)
    context_task = self.context_gatherer.gather_context_intelligence(product, meeting)
    
    # NEW: Campaign intelligence across all channels
    campaign_task = self.gather_campaign_intelligence(product)
    
    # NEW: Meeting notes context from Google Drive  
    drive_context_task = self.gather_drive_context(product, meeting['type'])
    
    # Wait for comprehensive intelligence
    intelligence = {
        'performance': await performance_task,
        'creatives': await creative_task,
        'competitive': await competitive_task,
        'context': await context_task,
        'campaigns': await campaign_task,  # NEW
        'historical': await drive_context_task  # NEW
    }
    
    return intelligence
```

### Agent Dependencies
- **✅ Available:** mkl (Meta campaigns)
- **🔄 Needs Install:** seekr (Google campaigns)  
- **🔄 Needs Install:** apple-search (Apple Search Ads)
- **✅ Available:** gog (Google Drive integration)

### Error Handling
- **Missing Agents:** Continue with available campaign data, note gaps
- **API Failures:** Use cached data where available, flag data freshness
- **Drive Access:** Graceful degradation if Drive search fails
- **Cross-Channel Analysis:** Adapt to available data sources

This comprehensive campaign intelligence will give Chifi complete visibility across all paid acquisition channels! 🚀📊