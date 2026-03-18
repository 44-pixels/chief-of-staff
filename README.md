# Chief of Staff Agent 📋

Intelligent meeting preparation automation for 44pixels product marketing meetings.

## Overview

The Chief of Staff agent automatically:

1. **Scans calendar** for product marketing meetings (8pm daily)
2. **Gathers intelligence** from performance, creative, and competitive sources
3. **Generates comprehensive reports** deployed to 44reports MCP
4. **Sends notifications** via Telegram and email with key insights

## Architecture

### Core Components
- **Meeting Detector** - Scans Google Calendar via `gog`, identifies product meetings
- **Intelligence Orchestrator** - Coordinates data from 44growth + Sensor Tower + creative-strategist  
- **Report Generator** - Creates polished meeting prep reports with recommendations
- **Notification Delivery** - Sends Telegram/email alerts with report summaries

### Data Sources
- **Performance:** 44growth agent (CPI, spend, conversions, trends)
- **Creative:** creative-strategist agent (launches, A/B tests, pipeline)
- **Competitive:** Sensor Tower MCP + Apify competitor scanning

### Products Supported
- Clara (AI receptionist)
- Cue (meeting notes) 
- Vivi (viral video clips)
- Wordcast (text-to-speech)
- GPTeen (kids AI)

## Meeting Detection

Automatically identifies meetings with:
- **Keywords:** "marketing", "weekly", "review", "performance"
- **Products:** Clara, Cue, Vivi, Wordcast, GPTeen in title
- **Type:** Weekly product marketing meetings

## Report Structure

### Executive Summary
- Meeting context and key metrics
- Top insights requiring attention  
- Critical action items

### Performance Analysis
- Campaign metrics with trends
- Funnel analysis and attribution
- Budget status and efficiency

### Creative Intelligence
- Recent launches and A/B test results
- Hook performance analysis
- Creative pipeline status

### Competitive Landscape  
- Market position and competitor movements
- New competitor creatives and messaging
- Opportunities and threats

### Strategic Recommendations
- Prioritized actions with rationale
- Owners and timelines
- Expected impact

## Installation

1. **Deploy Agent**
   ```bash
   cp -r agent/ ~/.openclaw/agents/chief-of-staff/
   ```

2. **Add Cron Job**
   ```bash
   cron add --job-file chief-of-staff-cron.json
   ```

3. **Configure Access**
   - Ensure `gog` calendar access configured
   - Verify 44growth and creative-strategist agents accessible
   - Test Sensor Tower MCP connectivity

## Usage

### Automatic (Recommended)
- Runs daily at 8pm London time
- Scans next day's calendar automatically
- Sends notifications when meetings detected

### Manual Testing
```bash
python3 agent/scripts/orchestrator.py
```

## Output

### Report Deployment
- **URL Pattern:** `https://reporter.44pixels.workers.dev/r/meeting-prep-{product}-{date}`
- **Access:** 44pixels team only
- **Retention:** 90 days

### Notifications
- **Telegram:** Main chat with meeting summary + report link
- **Email:** noam@44pixels.ai with formatted HTML summary

## Configuration

### Meeting Keywords
```python
meeting_keywords = ["marketing", "weekly", "review", "performance"]
```

### Products
```python
products = ["clara", "cue", "vivi", "wordcast", "gpteen"]
```

### Timing
- **Scan Time:** 8:00 PM London time daily
- **Scope:** Next 24-48 hours of calendar
- **Delivery:** Immediate after report generation

## Dependencies

- **OpenClaw Tools:** `gog`, `sessions_spawn`, `mcporter`, `message`
- **Agents:** 44growth, creative-strategist
- **MCPs:** Sensor Tower, 44reports
- **External:** Apify (competitor scanning)

## Error Handling

- **Agent Timeouts:** Continue with available data, flag missing intelligence
- **API Failures:** Retry with backoff, use cached data when available  
- **Report Errors:** Send error notifications, log for manual review
- **Delivery Issues:** Ensure at least one notification channel succeeds

## Monitoring

- **Success Rate:** Track report generation and delivery
- **Data Quality:** Monitor intelligence source availability
- **User Engagement:** Track report access and feedback
- **Performance:** Optimize execution time and resource usage

## Development

### Adding New Products
1. Add to `products` list in orchestrator
2. Configure Sensor Tower app mapping
3. Test meeting detection patterns

### Adding Intelligence Sources
1. Create skill in `agent/skills/`
2. Add to orchestration logic
3. Update report template

### Customizing Reports
1. Modify `format_report()` in orchestrator
2. Update templates in report-generator skill
3. Test with sample data

## Support

For issues or enhancements, contact the 44pixels development team.

## Deployment Status ✅

**Repository:** https://github.com/44-pixels/chief-of-staff  
**Cron Job ID:** `19a9fa99-cef1-4e63-ba62-aaebb5ecfebd`  
**Schedule:** Daily at 8:00 PM London time  
**Next Run:** Automatic based on calendar scanning  

### Testing Results
- ✅ Meeting detection working (85-90% confidence)
- ✅ Product extraction from titles (Clara, Cue, Vivi, Wordcast, GPTeen)
- ✅ Meeting type classification (weekly_marketing, performance_review)
- ✅ Duration calculation and attendee parsing
- ✅ Cron job active and scheduled

### Integration Status
- 🔄 **Pending:** First run will occur at next 8pm London time
- 🔄 **Testing:** Real calendar integration via `gog`
- 🔄 **Validation:** Agent spawning (44growth, creative-strategist)
- 🔄 **Verification:** Report deployment to 44reports MCP

## Context Intelligence Enhancement ✅

### NEW: Email & Slack Integration
The Chief of Staff now gathers context from communication channels:

**📧 Email Context (via gog):**
- Recent decisions and approvals
- Active blockers and issues  
- Performance discussions
- Budget and campaign updates
- Action items and follow-ups

**💬 Slack Context (via message tool):**
- Team sentiment analysis
- Recent product discussions
- Creative feedback and insights
- Real-time team pulse

### Enhanced Report Sections

**Team Context & Recent Developments:**
```markdown
### 📧 Email Intelligence (12 threads)
Found 12 recent email threads, 3 decisions mentioned, 1 potential blocker, 
4 performance discussions. Team sentiment appears positive.

### 💬 Team Sentiment  
😊 **Positive** - Based on recent communication patterns

### 📋 Recent Developments
**Decisions Made:**
- Approved new creative tests for Q2
- Increased budget allocation for winning hooks
- Launched competitor analysis initiative

**Active Issues:**
- Creative approval workflow delayed
```

### Context-Driven Action Items
```markdown
## Action Items
- [ ] Review performance trends
- [ ] Discuss budget allocation
- [ ] Plan upcoming creative tests
- [ ] Address active blockers identified in emails
- [ ] Follow up on recent decisions and implementation status  
- [ ] Review 3 outstanding action items from communications
```

### Intelligence Sources Overview
1. **Performance Data** (44growth agent)
2. **Creative Insights** (creative-strategist agent)  
3. **Competitive Intelligence** (Sensor Tower MCP + Apify)
4. **📧 Email Context** (gog Gmail search) ← NEW
5. **💬 Slack Context** (message tool search) ← NEW

### Context Search Patterns

**Email Queries:**
- `{product} (performance OR metrics OR campaign) after:{date}`
- `{product} (decision OR approved OR blocked) after:{date}`
- `{product} (budget OR spend OR cost) after:{date}`
- `from:{attendee} {product} after:{date}`

**Slack Channels by Product:**
- **Vivi:** #vivi-marketing, #creative-feedback
- **Clara:** #clara-team, #app-clara-product, #creative-feedback
- **Cue:** #app-cue-product, #creative-feedback  
- **Wordcast:** #wordcast, #creative-feedback
- **GPTeen:** #app-gpteen-product, #creative-feedback

This context intelligence makes meeting prep reports significantly more valuable and actionable! 📧💬📋
