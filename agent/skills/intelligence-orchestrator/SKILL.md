# Intelligence Orchestrator Skill

## Purpose
Coordinate data gathering across multiple agents and systems for comprehensive meeting preparation.

## Data Sources

### 1. Performance Intelligence (44growth Agent)
**Spawn Parameters:**
```python
{
    "agentId": "44growth",
    "task": f"Generate comprehensive {product} marketing performance report for meeting prep. Include: CPI trends, spend efficiency, conversion funnels, attribution data, campaign ROI, budget utilization. Focus on last 7 days vs previous period. Identify key insights and recommendations.",
    "mode": "run",
    "timeoutSeconds": 300
}
```

**Expected Output:** Performance metrics, trends, alerts, recommendations

### 2. Creative Intelligence (creative-strategist Agent)
**Spawn Parameters:**
```python
{
    "agentId": "creative-strategist", 
    "task": f"Analyze {product} creative performance for marketing meeting prep. Include: recent creative launches, A/B test results, hook performance analysis, messaging insights, creative pipeline status, upcoming tests. Provide strategic creative recommendations.",
    "mode": "run", 
    "timeoutSeconds": 300
}
```

**Expected Output:** Creative performance analysis, test results, pipeline status

### 3. Competitive Intelligence (Sensor Tower MCP)
**API Calls:**
```python
# App performance data
mcporter call sensortower.get_app_metadata app_ids=[product_app_ids]
mcporter call sensortower.get_rankings app_id=product_app_id country=US

# Competitive landscape  
mcporter call sensortower.find_related_apps app_id=product_app_id
mcporter call sensortower.get_category_apps category_id=product_category
```

**Expected Output:** Market position, competitor movements, category trends

### 4. Creative Monitoring (Apify)
**Triggered When:** Sensor Tower shows competitor growth >20% or new app launches
**API Calls:**
```python
# Scan competitor Facebook pages for new creatives
apify_scan_competitors(competitor_pages_for_product, max_ads=5)
```

**Expected Output:** New competitor creatives, messaging shifts, creative insights

## Orchestration Logic

### Parallel Execution
1. **Launch All Agents Simultaneously** (performance + creative analysis)
2. **Execute API Calls** (Sensor Tower + conditional Apify)  
3. **Wait for Completion** (max 5 minutes total)
4. **Aggregate Results** into unified intelligence report

### Data Synthesis
```python
intelligence_report = {
    "product": product_name,
    "meeting_date": meeting_date,
    "performance": performance_data,
    "creatives": creative_data, 
    "competitive": competitive_data,
    "alerts": identified_alerts,
    "recommendations": strategic_recommendations,
    "next_steps": actionable_items
}
```

### Alert Detection
- **Performance Alerts:** CPI increase >15%, spend efficiency drop >10%
- **Creative Alerts:** Hook performance decline, test failures  
- **Competitive Alerts:** New competitor launches, creative pattern changes
- **Market Alerts:** Category ranking shifts, seasonal trends

## Error Handling

### Agent Timeouts
- Continue with available data
- Note missing intelligence in report
- Flag for manual follow-up
- Provide partial recommendations

### API Failures
- Retry with exponential backoff
- Use cached data if recent (<24h)
- Include data quality notes
- Proceed with available sources

### Data Quality Issues
- Validate data ranges and formats
- Flag anomalies for review
- Cross-reference between sources
- Include confidence scores

## Output Integration
- Feed aggregated intelligence to report generator
- Store raw data for historical analysis
- Log performance for system optimization
- Update meeting context for future reference