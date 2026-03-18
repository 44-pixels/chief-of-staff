# Chief of Staff Agent - Operations Guide

## Daily Workflow

### 8:00 PM - Meeting Prep Automation

1. **Calendar Scan**
   ```bash
   gog calendar events primary --from tomorrow --to day-after-tomorrow
   ```

2. **Meeting Classification**
   - Keywords: "marketing", "weekly", "review", "performance"
   - Products: Clara, Cue, Vivi, Wordcast, GPTeen
   - Skip: 1:1s, internal ops, non-product meetings

3. **Intelligence Gathering**
   - Spawn 44growth for performance data
   - Query Sensor Tower MCP for competitive intel
   - Consult creative-strategist for creative insights
   - Run Apify competitor ad scans if alerts detected

4. **Report Generation**
   - Executive summary with key metrics
   - Performance analysis with trends
   - Creative performance and pipeline
   - Competitive landscape updates
   - Strategic recommendations

5. **Delivery**
   - Deploy to 44reports MCP
   - Send Telegram notification
   - Send email summary
   - Log completion

## Agent Coordination

### 44growth (Performance Data)
```python
sessions_spawn(
    agentId="44growth", 
    task=f"Generate {product} performance report for meeting prep - CPI, spend, conversions, trends last 7 days"
)
```

### creative-strategist (Creative Intelligence)  
```python
sessions_spawn(
    agentId="creative-strategist",
    task=f"Analyze {product} creative performance and pipeline for marketing meeting"
)
```

### Sensor Tower MCP
```python
mcporter call sensortower.get_app_metadata app_ids=[product_app_ids]
mcporter call sensortower.get_rankings app_id=product_app_id
```

### Apify Competitor Scanning
```python
# Triggered only if competitor growth detected
run_competitor_scan(competitor_pages, product_category)
```

## Memory & Context

### Meeting History
- Track past meetings and outcomes
- Reference previous reports and actions taken
- Identify recurring issues and themes

### Product Context
- Current campaigns and tests
- Strategic initiatives
- Budget constraints and targets
- Known issues and blockers

### Market Context
- Seasonal trends
- Competitive landscape changes
- Platform updates and policies
- Industry benchmarks

## Quality Standards

### Report Completeness
- [ ] Performance metrics with context
- [ ] Creative analysis with insights  
- [ ] Competitive intelligence
- [ ] Strategic recommendations
- [ ] Next steps with owners

### Timeliness
- [ ] Deployed by 8:00 PM day before
- [ ] Notifications sent within 5 minutes
- [ ] All data sources consulted
- [ ] Report accessible and formatted

### Actionability  
- [ ] Clear recommendations with rationale
- [ ] Prioritized next steps
- [ ] Owner assignments where relevant
- [ ] Timeline for actions
- [ ] Success metrics defined

## Error Handling

### Missing Data
- Note gaps in report
- Provide partial analysis
- Flag for manual review
- Continue with available data

### Agent Failures
- Retry with timeout
- Fall back to direct API calls
- Include error note in report
- Log for post-meeting follow-up

### Calendar Issues
- Handle recurring meetings
- Parse complex titles
- Ask for clarification when uncertain
- Default to inclusive rather than miss meetings