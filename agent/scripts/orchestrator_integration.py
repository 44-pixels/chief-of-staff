#!/usr/bin/env python3
"""
Integration updates for Chief of Staff orchestrator
Enhanced context intelligence with Slack + Jira
"""

# Additional methods to add to ChiefOfStaffOrchestrator class

def integrate_enhanced_context(self):
    """Integration method to add enhanced context capabilities"""
    
    # Replace the basic context gatherer with enhanced version
    from enhanced_context_methods import EnhancedContextGatherer
    self.enhanced_context_gatherer = EnhancedContextGatherer()

async def gather_enhanced_intelligence(self, product: str, meeting: Dict) -> Dict[str, Any]:
    """Enhanced intelligence gathering with Slack and Jira intelligence"""
    logger.info(f"🔍 Gathering enhanced intelligence for {product}")
    
    intelligence = {
        'product': product,
        'meeting_date': meeting['start_time'],
        'performance': {},
        'creatives': {},
        'competitive': {},
        'context': {},           # Enhanced: Email + Slack + Jira
        'campaigns': {},         # Multi-channel campaigns
        'historical': {},        # Google Drive context
        'operational': {},       # NEW: Operational intelligence
        'alerts': [],
        'recommendations': []
    }
    
    # Spawn existing agents
    performance_task = self.spawn_44growth(product)
    creative_task = self.spawn_creative_strategist(product) 
    competitive_task = self.query_sensor_tower(product)
    
    # Enhanced context gathering (Email + Slack + Jira)
    enhanced_context_task = self.enhanced_context_gatherer.gather_enhanced_context_intelligence(product, meeting)
    
    # Campaign intelligence across all channels
    campaign_task = self.gather_campaign_intelligence(product)
    
    # Google Drive context from meeting notes
    drive_context_task = self.gather_drive_context(product, meeting['type'])
    
    # Wait for comprehensive intelligence
    try:
        performance_data = await asyncio.wait_for(performance_task, timeout=300)
        creative_data = await asyncio.wait_for(creative_task, timeout=300) 
        competitive_data = await asyncio.wait_for(competitive_task, timeout=180)
        enhanced_context_data = await asyncio.wait_for(enhanced_context_task, timeout=150)  # Enhanced
        campaign_data = await asyncio.wait_for(campaign_task, timeout=360)
        drive_data = await asyncio.wait_for(drive_context_task, timeout=90)
        
        intelligence['performance'] = performance_data
        intelligence['creatives'] = creative_data
        intelligence['competitive'] = competitive_data
        intelligence['context'] = enhanced_context_data  # Enhanced
        intelligence['campaigns'] = campaign_data
        intelligence['historical'] = drive_data
        
        # Generate operational intelligence summary
        intelligence['operational'] = self.synthesize_operational_intelligence(
            enhanced_context_data, campaign_data, performance_data
        )
        
        # Enhanced alert detection with operational context
        intelligence['alerts'] = self.detect_enhanced_alerts(intelligence)
        
        # Context-driven recommendations
        intelligence['recommendations'] = self.generate_enhanced_recommendations(intelligence)
        
    except asyncio.TimeoutError as e:
        logger.warning(f"⏰ Enhanced intelligence gathering timeout for {product}: {e}")
        # Continue with partial data
        
    return intelligence

def synthesize_operational_intelligence(self, context_data: Dict, campaign_data: Dict, performance_data: Dict) -> Dict:
    """Synthesize operational intelligence across all data sources"""
    
    operational = {
        'team_health': 'good',
        'development_velocity': 'normal',
        'campaign_performance': 'stable',
        'operational_risks': [],
        'capacity_status': 'adequate',
        'coordination_status': 'good'
    }
    
    # Analyze team health from Slack intelligence
    slack_intel = context_data.get('slack_intelligence', {})
    team_sentiment = context_data.get('overall_team_sentiment', {})
    
    if team_sentiment.get('overall') == 'frustrated':
        operational['team_health'] = 'at_risk'
        operational['operational_risks'].append('Team sentiment indicates frustration')
    
    # Analyze development velocity from Jira
    jira_intel = context_data.get('jira_intelligence', {})
    if jira_intel.get('data_available'):
        sprint_analysis = jira_intel.get('sprint_analysis', {})
        velocity_status = sprint_analysis.get('velocity_status', 'on_track')
        
        if velocity_status == 'behind':
            operational['development_velocity'] = 'slow'
            operational['operational_risks'].append('Sprint velocity behind target')
        elif velocity_status == 'ahead':
            operational['development_velocity'] = 'fast'
    
    # Analyze campaign performance
    cross_channel = campaign_data.get('cross_channel_analysis', {})
    missing_channels = cross_channel.get('missing_channels', [])
    
    if len(missing_channels) > 0:
        operational['operational_risks'].append(f"Campaign visibility gaps: {', '.join(missing_channels)}")
    
    return operational

def detect_enhanced_alerts(self, intelligence: Dict) -> List[Dict]:
    """Enhanced alert detection with operational context"""
    
    alerts = []
    
    # Existing performance alerts
    alerts.extend(self.detect_alerts(intelligence))
    
    # Enhanced context-driven alerts
    context_data = intelligence.get('context', {})
    operational = intelligence.get('operational', {})
    
    # Team sentiment alerts
    team_sentiment = context_data.get('overall_team_sentiment', {})
    if team_sentiment.get('overall') == 'frustrated' and team_sentiment.get('confidence', 0) > 0.7:
        alerts.append({
            'type': 'team_sentiment',
            'priority': 'HIGH',
            'message': 'Team sentiment analysis indicates frustration - address in meeting'
        })
    
    # Development velocity alerts
    jira_intel = context_data.get('jira_intelligence', {})
    if jira_intel.get('data_available'):
        sprint_analysis = jira_intel.get('sprint_analysis', {})
        if sprint_analysis.get('velocity_status') == 'behind':
            alerts.append({
                'type': 'velocity_behind',
                'priority': 'MEDIUM', 
                'message': f'Sprint velocity behind target - {sprint_analysis.get("completion_percentage", 0):.0%} complete'
            })
    
    # Operational risk alerts
    for risk in operational.get('operational_risks', []):
        alerts.append({
            'type': 'operational_risk',
            'priority': 'MEDIUM',
            'message': risk
        })
    
    return alerts

def generate_enhanced_recommendations(self, intelligence: Dict) -> List[Dict]:
    """Generate enhanced recommendations with operational context"""
    
    recommendations = []
    
    # Existing recommendations
    recommendations.extend(self.generate_recommendations(intelligence))
    
    # Context-driven recommendations
    context_data = intelligence.get('context', {})
    operational = intelligence.get('operational', {})
    
    # Slack-driven recommendations
    slack_intel = context_data.get('slack_intelligence', {})
    urgency_signals = []
    
    for category_key, insights in slack_intel.items():
        if category_key.endswith('_insights') and isinstance(insights, dict):
            urgency_signals.extend(insights.get('urgency_indicators', []))
    
    if len(urgency_signals) > 3:
        recommendations.append({
            'priority': 'HIGH',
            'type': 'team_coordination',
            'action': f'Address {len(urgency_signals)} urgent items identified in Slack discussions',
            'rationale': 'Multiple urgency signals indicate coordination issues',
            'timeline': 'This meeting',
            'owner': 'Meeting lead'
        })
    
    # Jira-driven recommendations
    jira_intel = context_data.get('jira_intelligence', {})
    if jira_intel.get('data_available'):
        blocker_analysis = jira_intel.get('blocker_analysis', {})
        active_blockers = blocker_analysis.get('active_blockers', 0)
        
        if active_blockers > 2:
            recommendations.append({
                'priority': 'HIGH',
                'type': 'development_blockers',
                'action': f'Review and resolve {active_blockers} active development blockers',
                'rationale': 'Multiple blockers impacting development velocity',
                'timeline': 'This week',
                'owner': 'Technical lead'
            })
    
    return recommendations

# Enhanced report formatting methods

def format_enhanced_context_section(self, context: Dict) -> str:
    """Format enhanced context section with operational intelligence"""
    
    if not context or context.get('context_quality') == 'failed':
        return "📭 *Enhanced context gathering unavailable*"
    
    # Team sentiment with confidence
    team_sentiment = context.get('overall_team_sentiment', {})
    sentiment = team_sentiment.get('overall', 'neutral')
    confidence = team_sentiment.get('confidence', 0)
    sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'frustrated': '😤'}.get(sentiment, '🤷')
    
    # Operational status
    operational = context.get('operational_status', {})
    dev_health = operational.get('development_health', 'healthy')
    team_coord = operational.get('team_coordination', 'good')
    
    # Jira intelligence
    jira_intel = context.get('jira_intelligence', {})
    
    section = f"""
### 💬 Team Intelligence & Operational Status
**Overall Sentiment:** {sentiment_emoji} **{sentiment.title()}** (confidence: {confidence:.0%})  
**Development Health:** {dev_health.title()} | **Team Coordination:** {team_coord.title()}

### 📧 Communication Analysis
{context.get('context_summary', 'Communication analysis unavailable')}

### 🛠️ Development Velocity"""

    if jira_intel.get('data_available'):
        sprint_analysis = jira_intel.get('sprint_analysis', {})
        completion = sprint_analysis.get('completion_percentage', 0)
        velocity_status = sprint_analysis.get('velocity_status', 'unknown')
        
        section += f"""
**Sprint Progress:** {completion:.0%} complete ({velocity_status})  
**Blockers Impact:** {sprint_analysis.get('blockers_impact', 'minimal')}  
**Velocity Trend:** {jira_intel.get('velocity_trends', {}).get('trend', 'stable')}"""
    else:
        section += "\n*Development velocity data unavailable (Jira integration needed)*"
    
    section += f"""

### 🔍 Operational Insights
{self.format_operational_insights(context)}
"""
    
    return section

def format_operational_insights(self, context: Dict) -> str:
    """Format operational insights from enhanced context"""
    
    operational = context.get('operational_status', {})
    critical_issues = context.get('critical_issues', [])
    
    if not operational and not critical_issues:
        return "*No significant operational issues identified*"
    
    insights = []
    
    # Risk level assessment
    risk_level = operational.get('risk_level', 'low')
    if risk_level == 'high':
        insights.append("🔴 **High operational risk** - multiple issues require attention")
    elif risk_level == 'medium':
        insights.append("🟡 **Medium operational risk** - some issues need monitoring")
    else:
        insights.append("🟢 **Low operational risk** - systems operating normally")
    
    # Critical issues
    if critical_issues:
        insights.append(f"⚠️ **{len(critical_issues)} critical issues** identified across communication channels")
    
    return "\n".join(insights) if insights else "*Operational status good*"
