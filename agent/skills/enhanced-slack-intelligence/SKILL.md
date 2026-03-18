# Enhanced Slack Intelligence Skill

## Purpose
Deep Slack analysis for comprehensive team context, sentiment, and operational intelligence.

## Enhanced Slack Capabilities

### 1. **Multi-Channel Search Strategy**
```python
# Product-specific channel mapping (enhanced)
PRODUCT_CHANNELS = {
    'vivi': {
        'primary': ['#vivi-marketing', '#app-vivi-product'],
        'creative': ['#creative-feedback', '#C0AM69FUNUC'],  # C0AM69FUNUC = creative feedback
        'dev': ['#vivi-dev', '#development'],
        'general': ['#general', '#product-updates']
    },
    'clara': {
        'primary': ['#clara-team', '#app-clara-product'], 
        'creative': ['#creative-feedback', '#C0AM69FUNUC'],
        'dev': ['#clara-dev', '#development'],
        'general': ['#general', '#product-updates']
    },
    'cue': {
        'primary': ['#app-cue-product'],
        'creative': ['#creative-feedback', '#C0AM69FUNUC'],
        'dev': ['#cue-dev', '#development'], 
        'general': ['#general', '#product-updates']
    },
    'wordcast': {
        'primary': ['#wordcast'],
        'creative': ['#creative-feedback', '#C0AM69FUNUC'],
        'dev': ['#wordcast-dev', '#development'],
        'general': ['#general', '#product-updates']
    },
    'gpteen': {
        'primary': ['#app-gpteen-product'],
        'creative': ['#creative-feedback', '#C0AM69FUNUC'],
        'dev': ['#gpteen-dev', '#development'],
        'general': ['#general', '#product-updates']
    }
}

# Key team members to prioritize
KEY_TEAM_MEMBERS = [
    'noam', 'adam', 'anton',  # Founders
    'vlad.posad',             # Creative lead
    'zander',                 # Design lead
    'denis', 'alex', 'ozge'   # Growth team
]
```

### 2. **Advanced Message Analysis**
```python
async def analyze_slack_intelligence(product: str, days_back: int = 7) -> Dict[str, Any]:
    """Deep Slack analysis across all relevant channels"""
    
    channels = PRODUCT_CHANNELS.get(product, {})
    all_channels = (channels.get('primary', []) + 
                   channels.get('creative', []) + 
                   channels.get('dev', []) + 
                   channels.get('general', []))
    
    intelligence = {
        'team_sentiment': {},
        'key_discussions': [],
        'decision_indicators': [],
        'blocker_mentions': [],
        'performance_discussions': [],
        'creative_feedback': [],
        'velocity_indicators': [],
        'urgency_signals': []
    }
    
    # Search each channel with specific queries
    for channel in all_channels:
        messages = await search_channel_messages(channel, product, days_back)
        intelligence = analyze_channel_messages(messages, intelligence, channel)
    
    # Synthesize cross-channel insights
    intelligence['synthesis'] = synthesize_slack_insights(intelligence)
    
    return intelligence
```

### 3. **Sentiment Analysis Enhancement**
```python
def analyze_team_sentiment(messages: List[Dict], key_members: List[str]) -> Dict:
    """Advanced sentiment analysis focusing on key team members"""
    
    sentiment_data = {
        'overall': 'neutral',
        'by_person': {},
        'trend': 'stable',
        'confidence': 0.5,
        'indicators': []
    }
    
    # Sentiment indicators by message patterns
    positive_indicators = [
        'great results', 'looking good', 'winning', 'success', 
        'approved', 'launched', 'excited', 'love this'
    ]
    
    negative_indicators = [
        'blocked', 'stuck', 'problem', 'issue', 'frustrated',
        'not working', 'failed', 'concerned', 'delayed'
    ]
    
    neutral_indicators = [
        'update', 'status', 'meeting', 'review', 'planning'
    ]
    
    # Analyze messages from key team members
    for message in messages:
        author = message.get('author', '').lower()
        text = message.get('text', '').lower()
        
        if any(member in author for member in key_members):
            # Weight key members' sentiment higher
            sentiment_score = calculate_message_sentiment(text, positive_indicators, negative_indicators)
            sentiment_data['by_person'][author] = sentiment_score
            sentiment_data['indicators'].append({
                'author': author,
                'text': text[:100],
                'sentiment': sentiment_score,
                'timestamp': message.get('timestamp')
            })
    
    # Calculate overall sentiment
    if sentiment_data['by_person']:
        avg_sentiment = sum(sentiment_data['by_person'].values()) / len(sentiment_data['by_person'])
        if avg_sentiment > 0.3:
            sentiment_data['overall'] = 'positive'
        elif avg_sentiment < -0.3:
            sentiment_data['overall'] = 'frustrated'
        else:
            sentiment_data['overall'] = 'neutral'
        
        sentiment_data['confidence'] = min(len(sentiment_data['by_person']) / 5, 1.0)  # Max confidence at 5+ people
    
    return sentiment_data
```

### 4. **Decision & Blocker Detection**
```python
def extract_decisions_and_blockers(messages: List[Dict]) -> Dict:
    """Extract actionable decisions and blockers from Slack discussions"""
    
    # Decision indicators
    decision_patterns = [
        r'(approved|go ahead|decision|launch|ship|deploy)',
        r'(let\'s do|we\'ll|going with|decided)',
        r'(signed off|green light|thumbs up)'
    ]
    
    # Blocker indicators  
    blocker_patterns = [
        r'(blocked by|waiting for|stuck on|can\'t proceed)',
        r'(issue with|problem with|broken|not working)',
        r'(delayed|postponed|on hold|paused)'
    ]
    
    # Urgency indicators
    urgency_patterns = [
        r'(urgent|asap|critical|important|priority)',
        r'(need this|deadline|due|tomorrow)',
        r'(fire|emergency|broken)'
    ]
    
    extraction = {
        'recent_decisions': [],
        'active_blockers': [],
        'urgent_items': [],
        'action_items': []
    }
    
    for message in messages:
        text = message.get('text', '').lower()
        author = message.get('author', '')
        timestamp = message.get('timestamp', '')
        
        # Check for decisions
        for pattern in decision_patterns:
            if re.search(pattern, text):
                extraction['recent_decisions'].append({
                    'text': message.get('text', '')[:200],
                    'author': author,
                    'timestamp': timestamp,
                    'confidence': 'medium'
                })
        
        # Check for blockers
        for pattern in blocker_patterns:
            if re.search(pattern, text):
                extraction['active_blockers'].append({
                    'text': message.get('text', '')[:200],
                    'author': author, 
                    'timestamp': timestamp,
                    'severity': determine_blocker_severity(text)
                })
        
        # Check for urgency
        for pattern in urgency_patterns:
            if re.search(pattern, text):
                extraction['urgent_items'].append({
                    'text': message.get('text', '')[:200],
                    'author': author,
                    'timestamp': timestamp,
                    'urgency': 'high'
                })
    
    return extraction
```

### 5. **Creative Feedback Intelligence**
```python
def analyze_creative_feedback(messages: List[Dict], product: str) -> Dict:
    """Analyze creative feedback patterns from #creative-feedback channel"""
    
    feedback_intelligence = {
        'recent_creative_posts': [],
        'feedback_sentiment': 'neutral',
        'common_themes': [],
        'performance_mentions': [],
        'iteration_requests': []
    }
    
    # Look for creative posts and feedback patterns
    creative_keywords = ['creative', 'hook', 'ad', 'video', 'image', 'copy', 'messaging']
    feedback_keywords = ['feedback', 'thoughts', 'review', 'score', 'rating']
    
    for message in messages:
        text = message.get('text', '').lower()
        
        # Identify creative posts
        if any(keyword in text for keyword in creative_keywords):
            if product.lower() in text:
                feedback_intelligence['recent_creative_posts'].append({
                    'text': message.get('text', '')[:150],
                    'author': message.get('author', ''),
                    'timestamp': message.get('timestamp', ''),
                    'has_feedback': any(keyword in text for keyword in feedback_keywords)
                })
    
    return feedback_intelligence
```

## Integration with Message Tool

### 1. **Channel Search Implementation**
```python
async def search_channel_messages(channel: str, product: str, days_back: int) -> List[Dict]:
    """Search specific Slack channel for product-related messages"""
    
    # Use message tool with enhanced search
    search_results = await message_tool_search({
        'action': 'read',
        'channel': channel,
        'query': f"{product} OR performance OR creative OR blocked OR decision",
        'limit': 50,
        'after': calculate_date_filter(days_back)
    })
    
    return search_results.get('messages', [])

async def message_tool_search(params: Dict) -> Dict:
    """Enhanced message tool usage for Slack search"""
    
    # Implementation would use the message tool
    # This is a placeholder for the actual implementation
    return {
        'messages': [],
        'channel': params.get('channel'),
        'total_found': 0
    }
```

### 2. **Multi-Channel Orchestration**
```python
async def orchestrate_slack_intelligence(product: str) -> Dict[str, Any]:
    """Orchestrate intelligence gathering across all relevant Slack channels"""
    
    channels = PRODUCT_CHANNELS.get(product, {})
    
    # Parallel channel searches
    tasks = []
    for category, channel_list in channels.items():
        for channel in channel_list:
            task = search_channel_messages(channel, product, 7)
            tasks.append((channel, category, task))
    
    # Wait for all searches
    results = {}
    for channel, category, task in tasks:
        try:
            messages = await asyncio.wait_for(task, timeout=30)
            results[channel] = {
                'category': category,
                'messages': messages,
                'message_count': len(messages)
            }
        except asyncio.TimeoutError:
            results[channel] = {
                'category': category,
                'error': 'timeout',
                'message_count': 0
            }
    
    return results
```

## Report Integration

### Enhanced Slack Context Section
```markdown
## 💬 Slack Team Intelligence

### Team Sentiment Analysis
**Overall:** {sentiment_emoji} **{overall_sentiment}** (confidence: {confidence_pct}%)  
**Key Contributors:** {key_member_sentiments}

### Recent Decisions (Last 7 Days)
{decision_list}

### Active Blockers  
{blocker_list}

### Creative Feedback Pulse
**Recent Posts:** {creative_posts_count} creative items shared  
**Feedback Activity:** {feedback_activity_level}  
**Common Themes:** {creative_themes}

### Velocity Indicators
**Development Mentions:** {dev_progress_indicators}  
**Urgency Signals:** {urgent_items_count} high-priority items  
**Team Capacity:** {capacity_indicators}
```

### Actionable Insights
```python
def generate_slack_insights(slack_data: Dict) -> List[str]:
    """Generate actionable insights from Slack intelligence"""
    
    insights = []
    
    # Sentiment-based insights
    if slack_data['team_sentiment']['overall'] == 'frustrated':
        insights.append("🔴 Team sentiment appears frustrated - prioritize addressing blockers in meeting")
    
    # Decision follow-up insights
    decisions = slack_data.get('recent_decisions', [])
    if len(decisions) > 0:
        insights.append(f"📋 {len(decisions)} recent decisions identified - verify implementation status")
    
    # Blocker insights
    blockers = slack_data.get('active_blockers', [])
    if len(blockers) > 0:
        insights.append(f"⚠️ {len(blockers)} active blockers detected - review resolution plans")
    
    # Creative feedback insights
    creative_posts = slack_data.get('creative_feedback', {}).get('recent_creative_posts', [])
    if len(creative_posts) > 3:
        insights.append(f"🎨 High creative activity ({len(creative_posts)} items) - review feedback patterns")
    
    return insights
```

This enhanced Slack intelligence will give Chifi much deeper team operational awareness and context! Next, let's add Jira integration for velocity and progress tracking. 🚀💬