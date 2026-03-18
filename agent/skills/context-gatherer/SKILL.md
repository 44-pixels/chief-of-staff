# Context Gatherer Skill

## Purpose
Extract relevant context from email and Slack conversations to enrich meeting preparation.

## Data Sources

### 1. Email Context (via gog)
**Search Strategy:**
```bash
# Recent emails about the product
gog gmail search "from:44pixels.ai OR to:44pixels.ai {product} after:2026-03-11" --format json

# Emails with meeting attendees  
gog gmail search "from:{attendee_email} OR to:{attendee_email} {product} after:2026-03-11" --format json

# Recent decisions and updates
gog gmail search "{product} (decision OR update OR blocked OR launch OR campaign) after:2026-03-11" --format json
```

**Context Extraction:**
- **Decisions Made:** Extract key decisions from email threads
- **Blockers/Issues:** Identify current problems and their status
- **Recent Updates:** Product launches, campaign results, team changes
- **Action Items:** Outstanding tasks and ownership
- **Budget/Approvals:** Financial decisions and approval status

### 2. Slack Context (via message tool)
**Channel Strategy:**
```python
product_channels = {
    "vivi": ["#vivi-marketing", "#creative-feedback"],
    "clara": ["#clara-team", "#app-clara-product"], 
    "cue": ["#app-cue-product"],
    "wordcast": ["#wordcast"],
    "gpteen": ["#app-gpteen-product"]
}
```

**Search Patterns:**
- Recent messages mentioning product name (last 7 days)
- Messages from key team members (Vlad, Adam, Anton, Noam)
- Discussions about performance, creatives, blockers
- Reactions and sentiment indicators

**Context Categories:**
- **Team Sentiment:** Recent wins, frustrations, concerns
- **Tactical Updates:** Campaign changes, creative launches, A/B tests
- **Blockers:** Technical issues, resource constraints, approvals
- **Strategic Shifts:** New directions, pivots, competitive responses

## Context Processing Pipeline

### 1. Multi-Source Search
```python
async def gather_context(product: str, meeting: dict, lookback_days: int = 7):
    # Parallel context gathering
    email_context = await search_email_context(product, meeting, lookback_days)
    slack_context = await search_slack_context(product, meeting, lookback_days)
    
    # Merge and prioritize
    return synthesize_context(email_context, slack_context, meeting)
```

### 2. Email Context Extraction
```python
def extract_email_insights(emails: list, product: str) -> dict:
    insights = {
        'recent_decisions': [],
        'active_blockers': [],
        'budget_updates': [],
        'performance_discussions': [],
        'action_items': [],
        'key_threads': []
    }
    
    for email in emails:
        # Extract structured insights using NLP patterns
        if 'decision' in email['subject'].lower():
            insights['recent_decisions'].append(extract_decision_context(email))
        # ... more extraction logic
    
    return insights
```

### 3. Slack Context Extraction  
```python
def extract_slack_insights(messages: list, product: str) -> dict:
    insights = {
        'team_sentiment': 'neutral',
        'recent_updates': [],
        'active_discussions': [],
        'performance_mentions': [],
        'creative_feedback': []
    }
    
    for message in messages:
        # Sentiment analysis on key team members' messages
        if message['author'] in ['vlad.posad', 'adam', 'noam']:
            sentiment = analyze_sentiment(message['text'])
            # ... processing logic
    
    return insights
```

## Context Integration

### Meeting Report Enhancement
```markdown
## Team Context & Recent Developments

### 📧 Email Insights (Last 7 Days)
- **Key Decisions:** {recent_decisions}
- **Active Blockers:** {blockers_with_status}  
- **Budget Updates:** {financial_context}
- **Action Items:** {outstanding_tasks}

### 💬 Slack Team Pulse
- **Sentiment:** {team_sentiment} ({sentiment_reasoning})
- **Hot Topics:** {active_discussions}
- **Recent Wins:** {positive_mentions}
- **Concerns:** {team_concerns}

### 🎯 Meeting Context
- **Previous Discussion Points:** {related_email_threads}
- **Follow-ups from Last Meeting:** {action_item_status}
- **Stakeholder Input:** {relevant_feedback}
```

### Context-Aware Recommendations
```python
def generate_contextual_recommendations(performance_data, context_data):
    recommendations = []
    
    # Context influences recommendations
    if context_data['team_sentiment'] == 'frustrated':
        recommendations.append({
            'priority': 'HIGH',
            'type': 'team_morale',
            'action': 'Address team concerns first in meeting',
            'context': context_data['team_concerns']
        })
    
    # Email decisions inform next steps
    for decision in context_data['recent_decisions']:
        if decision['requires_follow_up']:
            recommendations.append({
                'priority': 'MEDIUM',
                'type': 'follow_up',
                'action': f"Review status of {decision['topic']}",
                'context': decision['details']
            })
    
    return recommendations
```

## Search Optimization

### Email Search Strategies
```python
def build_email_queries(product: str, attendees: list, meeting_date: str):
    base_queries = [
        f"{product} (performance OR metrics OR campaign)",
        f"{product} (decision OR approved OR blocked)",
        f"{product} (launch OR creative OR test)",
        f"{product} (budget OR spend OR cost)"
    ]
    
    # Add attendee-specific queries
    for attendee in attendees:
        base_queries.append(f"from:{attendee} {product}")
    
    # Add date constraints
    after_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    return [f"{query} after:{after_date}" for query in base_queries]
```

### Slack Search Optimization
```python
def get_relevant_channels(product: str) -> list:
    channel_map = {
        'vivi': ['#vivi-marketing', '#creative-feedback', '#C0AM69FUNUC'],
        'clara': ['#clara-team', '#app-clara-product', '#creative-feedback'],
        'cue': ['#app-cue-product', '#creative-feedback'], 
        'wordcast': ['#wordcast', '#creative-feedback'],
        'gpteen': ['#app-gpteen-product']
    }
    
    # Always include general channels
    base_channels = ['#general', '#marketing', '#product-updates']
    
    return channel_map.get(product, []) + base_channels
```

## Context Quality Control

### Relevance Filtering
- **Time-based:** Prioritize recent context (last 3 days > last week)
- **Participant-based:** Weight input from meeting attendees higher
- **Topic-based:** Focus on performance, strategy, blockers over general discussion
- **Sentiment-based:** Highlight emotional context (frustration, excitement, concern)

### Privacy & Security
- **Email Access:** Respect privacy, focus on business context only
- **Slack Messages:** Public channels only, respect confidential discussions
- **Data Retention:** Context stored only for report generation, then discarded
- **Sensitive Info:** Flag and exclude personal or confidential content

### Context Freshness
- **Real-time Integration:** Pull context at report generation time
- **Cache Strategy:** Cache common searches, refresh for each meeting
- **Staleness Detection:** Flag when context sources are unavailable
- **Fallback:** Continue with performance/competitive data if context fails

## Integration Points

### Orchestrator Integration
```python
# Add to intelligence gathering pipeline
async def gather_intelligence(self, product: str, meeting: Dict) -> Dict[str, Any]:
    # Existing sources
    performance_task = self.spawn_44growth(product)
    creative_task = self.spawn_creative_strategist(product) 
    competitive_task = self.query_sensor_tower(product)
    
    # NEW: Context gathering
    context_task = self.gather_context(product, meeting)
    
    # Wait for all intelligence
    intelligence['context'] = await asyncio.wait_for(context_task, timeout=120)
```

### Report Template Updates
- Add "Team Context" section before performance analysis
- Include context-driven insights in executive summary
- Reference email threads and Slack discussions in recommendations
- Surface action items and follow-ups from previous communications

This contextual intelligence will make meeting prep reports significantly more valuable and actionable! 📧💬📋