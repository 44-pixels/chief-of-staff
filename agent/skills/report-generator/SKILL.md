# Report Generator Skill

## Purpose
Transform raw intelligence data into polished, actionable meeting preparation reports.

## Report Template Structure

### Executive Summary (Top of Report)
- **Meeting Context:** Product, date, type, duration
- **Key Metrics:** 3-4 critical KPIs with trend indicators  
- **Top Insights:** 2-3 most important findings requiring attention
- **Action Items:** Immediate decisions or discussions needed

### Performance Analysis
- **Campaign Performance:** CPI, spend, conversions with period comparisons
- **Funnel Analysis:** Attribution, conversion rates, drop-off points
- **Budget Status:** Spend vs targets, efficiency metrics, runway
- **Trend Analysis:** 7-day vs 30-day performance with explanations

### Creative Intelligence  
- **Recent Launches:** New creative performance and insights
- **A/B Test Results:** Winners, losers, statistical significance
- **Hook Analysis:** Performance by messaging theme and format
- **Pipeline Status:** Upcoming creative tests and readiness

### Competitive Landscape
- **Market Position:** Rankings, downloads, revenue vs competitors
- **Competitive Movements:** New launches, growth patterns, threats
- **Creative Analysis:** New competitor messaging or format trends  
- **Market Opportunities:** Gaps or shifts to capitalize on

### Strategic Recommendations
- **Performance Optimizations:** Specific actions to improve metrics
- **Creative Strategy:** Messaging, format, or targeting adjustments
- **Competitive Response:** Actions to address competitive threats
- **Resource Allocation:** Budget or effort reallocation recommendations

### Action Items & Next Steps
- **Immediate (Next 24h):** Urgent decisions or approvals needed
- **This Week:** Key actions with owners and deadlines
- **Strategic (This Month):** Longer-term initiatives to plan
- **Follow-up Required:** Items needing additional data or analysis

## Formatting Standards

### Visual Hierarchy
- **H1:** Section headers (Performance Analysis, etc.)
- **H2:** Subsection headers (Campaign Performance, etc.)  
- **H3:** Metric categories or specific insights
- **Bold:** Key metrics, names, important callouts
- **Italic:** Trend indicators, context, explanations

### Data Presentation
```markdown
## Performance Analysis

### Campaign Performance
- **CPI:** $2.45 (↑8% vs last week) - Within target range
- **Daily Spend:** $1,247 (↓12% vs target) - Underspending opportunity  
- **Conversions:** 89 (↑15% vs last week) - Strong conversion improvement
- **Attribution:** 67% first-touch, 33% multi-touch - Healthy mix

### Key Insights
**🔴 Alert:** CPI trending upward due to audience saturation  
**🟡 Watch:** Creative fatigue detected in primary hook (Hook-A decline)
**🟢 Opportunity:** Competitor launched weak creatives, market share available
```

### Recommendation Format
```markdown
## Strategic Recommendations

### 1. Address CPI Inflation (Priority: HIGH)
**Issue:** CPI increased 8% due to audience saturation in primary targets
**Action:** Expand to lookalike audiences 2-4%, test new interest categories
**Owner:** Campaign Manager  
**Timeline:** This week
**Expected Impact:** 15-20% CPI reduction within 7 days

### 2. Creative Refresh Pipeline (Priority: MEDIUM)  
**Issue:** Primary hook showing 12% performance decline over 2 weeks
**Action:** Launch 3 new hook variations from creative-strategist pipeline
**Owner:** Creative Team
**Timeline:** Next week
**Expected Impact:** Restore hook performance to baseline
```

## Report Deployment

### 44reports MCP Integration
```python
# Deploy comprehensive report
mcporter call 44reports-mcp.deploy_context(
    name=f"{product} Meeting Prep - {meeting_date}",
    slug=f"meeting-prep-{product}-{date_slug}",  
    description=f"Marketing meeting preparation for {product} - {meeting_title}",
    content=formatted_report_markdown,
    tags=["meeting-prep", product, "marketing", "weekly"],
    agent_id="chief-of-staff",
    agent_name="Chief of Staff"
)
```

### Report Metadata
- **URL:** `https://reporter.44pixels.workers.dev/r/meeting-prep-{product}-{date}`
- **Access:** Private (44pixels team only)
- **Retention:** 90 days (quarterly cleanup)
- **Format:** Mobile-optimized for Telegram preview

## Quality Assurance

### Content Validation
- [ ] All intelligence sources represented
- [ ] Metrics include trend context and explanations  
- [ ] Recommendations are specific and actionable
- [ ] Action items have owners and timelines
- [ ] Executive summary captures key decisions needed

### Technical Validation  
- [ ] Report deploys successfully to 44reports MCP
- [ ] URL is accessible and renders properly
- [ ] Mobile preview works for Telegram
- [ ] No sensitive data exposed publicly
- [ ] Proper tagging for searchability

### Editorial Review
- [ ] Professional tone appropriate for leadership
- [ ] Data presented clearly without jargon
- [ ] Insights are supported by evidence
- [ ] Recommendations prioritized by impact/effort
- [ ] Action items are realistic and achievable