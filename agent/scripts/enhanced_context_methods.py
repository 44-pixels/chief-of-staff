#!/usr/bin/env python3
"""
Enhanced context gathering methods for Chief of Staff
Slack + Jira intelligence integration
"""

import subprocess
import json
import asyncio
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class EnhancedContextGatherer:
    """Enhanced context gathering with deep Slack and Jira intelligence"""
    
    def __init__(self):
        # Enhanced Slack channel mapping
        self.product_channels = {
            'vivi': {
                'primary': ['#vivi-marketing', '#app-vivi-product'],
                'creative': ['#creative-feedback', '#C0AM69FUNUC'],
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
        
        # Key team members for sentiment analysis
        self.key_team_members = [
            'noam', 'adam', 'anton',      # Founders
            'vlad.posad',                 # Creative lead
            'zander',                     # Design lead  
            'denis', 'alex', 'ozge'       # Growth team
        ]
        
        # Jira project mapping
        self.jira_projects = {
            'vivi': 'VIVI',
            'clara': 'CLARA', 
            'cue': 'CUE',
            'wordcast': 'WC',
            'gpteen': 'GPTEEN',
            'platform': 'PLAT'
        }
    
    async def gather_enhanced_context_intelligence(self, product: str, meeting: Dict, lookback_days: int = 7) -> Dict[str, Any]:
        """Gather comprehensive context with enhanced Slack and Jira intelligence"""
        logger.info(f"🔍 Gathering enhanced context intelligence for {product}")
        
        context = {
            'email_insights': {},
            'slack_intelligence': {},  # Enhanced
            'jira_intelligence': {},   # New
            'team_sentiment': 'neutral',
            'operational_status': {},  # New
            'context_quality': 'partial'
        }
        
        try:
            # Parallel enhanced context gathering
            email_task = self.gather_email_context(product, meeting, lookback_days)
            slack_task = self.gather_enhanced_slack_intelligence(product, lookback_days)
            jira_task = self.gather_jira_intelligence(product)
            
            # Wait for all context sources
            email_context = await asyncio.wait_for(email_task, timeout=60)
            slack_intelligence = await asyncio.wait_for(slack_task, timeout=90)
            jira_intelligence = await asyncio.wait_for(jira_task, timeout=60)
            
            context['email_insights'] = email_context
            context['slack_intelligence'] = slack_intelligence
            context['jira_intelligence'] = jira_intelligence
            context['context_quality'] = 'comprehensive'
            
            # Enhanced synthesis with operational intelligence
            context.update(self.synthesize_enhanced_context(
                email_context, slack_intelligence, jira_intelligence
            ))
            
        except asyncio.TimeoutError:
            logger.warning(f"⏰ Enhanced context gathering timeout for {product}")
            context['context_quality'] = 'limited'
        except Exception as e:
            logger.error(f"❌ Enhanced context gathering failed for {product}: {e}")
            context['context_quality'] = 'failed'
            
        return context
    
    async def gather_enhanced_slack_intelligence(self, product: str, lookback_days: int) -> Dict[str, Any]:
        """Gather deep Slack intelligence across all relevant channels"""
        logger.info(f"💬 Gathering enhanced Slack intelligence for {product}")
        
        channels = self.product_channels.get(product, {})
        all_channels = []
        for category, channel_list in channels.items():
            all_channels.extend([(ch, category) for ch in channel_list])
        
        slack_intelligence = {
            'channels_analyzed': len(all_channels),
            'team_sentiment_analysis': {},
            'decision_indicators': [],
            'blocker_mentions': [],
            'creative_feedback_analysis': {},
            'urgency_signals': [],
            'velocity_indicators': [],
            'cross_channel_insights': {}
        }
        
        # Analyze each channel category
        for channel, category in all_channels:
            try:
                messages = await self.search_channel_enhanced(channel, product, lookback_days)
                channel_analysis = self.analyze_channel_intelligence(messages, category, product)
                
                # Aggregate insights by category
                slack_intelligence[f'{category}_insights'] = channel_analysis
                
            except Exception as e:
                logger.warning(f"⚠️ Slack channel {channel} analysis failed: {e}")
                continue
        
        # Synthesize cross-channel insights
        slack_intelligence['synthesis'] = self.synthesize_slack_intelligence(slack_intelligence)
        
        return slack_intelligence
    
    async def search_channel_enhanced(self, channel: str, product: str, days_back: int) -> List[Dict]:
        """Enhanced Slack channel search with multiple query patterns"""
        
        # Multiple search patterns for comprehensive coverage
        search_patterns = [
            f"{product}",
            f"{product} performance",
            f"{product} creative",
            "blocked OR issue OR problem",
            "decision OR approved OR launch",
            "urgent OR critical OR priority"
        ]
        
        all_messages = []
        
        for pattern in search_patterns:
            try:
                # Simulated message tool call - would be actual implementation
                # message_response = await message_tool_call({
                #     'action': 'read',
                #     'channel': channel,
                #     'query': pattern,
                #     'limit': 20,
                #     'after': calculate_date_filter(days_back)
                # })
                
                # For now, return mock data structure
                messages = self.get_mock_slack_messages(channel, pattern, product)
                all_messages.extend(messages)
                
            except Exception as e:
                logger.warning(f"⚠️ Slack search failed for {channel} / {pattern}: {e}")
                continue
        
        # Deduplicate messages by timestamp and content
        unique_messages = self.deduplicate_messages(all_messages)
        
        return unique_messages
    
    def analyze_channel_intelligence(self, messages: List[Dict], category: str, product: str) -> Dict[str, Any]:
        """Analyze Slack messages for intelligence insights"""
        
        analysis = {
            'message_count': len(messages),
            'sentiment_indicators': [],
            'key_themes': [],
            'decision_mentions': [],
            'blocker_mentions': [],
            'urgency_indicators': [],
            'team_participation': {}
        }
        
        # Sentiment analysis patterns
        positive_patterns = [
            r'(great|good|excellent|success|win|approved|love|excited)',
            r'(working well|looks good|shipped|launched)'
        ]
        
        negative_patterns = [
            r'(blocked|stuck|problem|issue|bug|failed|broken)',
            r'(frustrated|concerned|not working|delayed)'
        ]
        
        urgency_patterns = [
            r'(urgent|asap|critical|emergency|priority)',
            r'(need this|deadline|due|fire)'
        ]
        
        for message in messages:
            text = message.get('text', '').lower()
            author = message.get('author', '').lower()
            
            # Sentiment analysis
            positive_score = sum(1 for pattern in positive_patterns if re.search(pattern, text))
            negative_score = sum(1 for pattern in negative_patterns if re.search(pattern, text))
            urgency_score = sum(1 for pattern in urgency_patterns if re.search(pattern, text))
            
            if positive_score > 0:
                analysis['sentiment_indicators'].append({
                    'type': 'positive',
                    'author': author,
                    'text': text[:100],
                    'score': positive_score
                })
            
            if negative_score > 0:
                analysis['sentiment_indicators'].append({
                    'type': 'negative', 
                    'author': author,
                    'text': text[:100],
                    'score': negative_score
                })
            
            if urgency_score > 0:
                analysis['urgency_indicators'].append({
                    'author': author,
                    'text': text[:100],
                    'urgency': urgency_score
                })
            
            # Track team participation
            if any(member in author for member in self.key_team_members):
                analysis['team_participation'][author] = analysis['team_participation'].get(author, 0) + 1
        
        return analysis
    
    async def gather_jira_intelligence(self, product: str) -> Dict[str, Any]:
        """Gather development velocity and progress intelligence from Jira"""
        logger.info(f"🛠️ Gathering Jira intelligence for {product}")
        
        project_key = self.jira_projects.get(product, product.upper())
        
        jira_intelligence = {
            'project_key': project_key,
            'sprint_analysis': {},
            'velocity_trends': {},
            'blocker_analysis': {},
            'release_readiness': {},
            'team_capacity': {},
            'data_available': False
        }
        
        try:
            # Check if Jira is accessible
            if not self.is_jira_accessible():
                jira_intelligence['error'] = 'Jira API not configured'
                return jira_intelligence
            
            # Gather sprint data
            current_sprint = await self.get_current_sprint_data(project_key)
            jira_intelligence['sprint_analysis'] = self.analyze_sprint_data(current_sprint)
            
            # Gather velocity trends
            sprint_history = await self.get_sprint_history(project_key, count=6)
            jira_intelligence['velocity_trends'] = self.analyze_velocity_trends(sprint_history)
            
            # Analyze blockers impact
            jira_intelligence['blocker_analysis'] = self.analyze_development_blockers(current_sprint)
            
            # Release readiness assessment
            upcoming_releases = await self.get_upcoming_releases(project_key)
            jira_intelligence['release_readiness'] = self.analyze_release_readiness(upcoming_releases)
            
            jira_intelligence['data_available'] = True
            
        except Exception as e:
            logger.warning(f"⚠️ Jira intelligence gathering failed for {product}: {e}")
            jira_intelligence['error'] = str(e)
        
        return jira_intelligence
    
    def is_jira_accessible(self) -> bool:
        """Check if Jira API is configured and accessible"""
        jira_token = os.getenv('JIRA_API_TOKEN')
        return bool(jira_token)
    
    async def get_current_sprint_data(self, project_key: str) -> Dict:
        """Get current sprint data for project (mock implementation)"""
        # In real implementation, would call Jira API
        return {
            'name': f'{project_key} Sprint 23',
            'planned_points': 45,
            'completed_points': 28,
            'remaining_points': 17,
            'status_distribution': {
                'To Do': 3,
                'In Progress': 8,
                'In Review': 2,
                'Done': 12
            },
            'blocked_issues': [
                {'key': f'{project_key}-123', 'summary': 'Blocked by external dependency', 'points': 5}
            ],
            'days_remaining': 3
        }
    
    def analyze_sprint_data(self, sprint_data: Dict) -> Dict:
        """Analyze current sprint performance"""
        
        analysis = {
            'completion_percentage': 0,
            'velocity_status': 'on_track',
            'burndown_trend': 'normal',
            'capacity_utilization': 0,
            'blockers_impact': 'minimal'
        }
        
        planned = sprint_data.get('planned_points', 0)
        completed = sprint_data.get('completed_points', 0)
        remaining = sprint_data.get('remaining_points', 0)
        
        if planned > 0:
            analysis['completion_percentage'] = completed / planned
            
            # Assess velocity status
            if analysis['completion_percentage'] > 0.8:
                analysis['velocity_status'] = 'ahead'
            elif analysis['completion_percentage'] < 0.5:
                analysis['velocity_status'] = 'behind'
        
        # Analyze blocker impact
        blocked_points = sum(issue.get('points', 0) for issue in sprint_data.get('blocked_issues', []))
        if planned > 0 and blocked_points / planned > 0.2:
            analysis['blockers_impact'] = 'significant'
        elif blocked_points > 0:
            analysis['blockers_impact'] = 'moderate'
        
        return analysis
    
    def synthesize_enhanced_context(self, email_context: Dict, slack_intelligence: Dict, jira_intelligence: Dict) -> Dict[str, Any]:
        """Synthesize all context sources into operational insights"""
        
        synthesis = {
            'overall_team_sentiment': self.determine_overall_sentiment(email_context, slack_intelligence),
            'operational_status': self.assess_operational_status(slack_intelligence, jira_intelligence),
            'critical_issues': self.identify_critical_issues(email_context, slack_intelligence, jira_intelligence),
            'development_velocity': self.assess_development_velocity(jira_intelligence),
            'team_capacity_status': self.assess_team_capacity(slack_intelligence, jira_intelligence),
            'context_driven_recommendations': self.generate_context_recommendations(
                email_context, slack_intelligence, jira_intelligence
            )
        }
        
        return synthesis
    
    def determine_overall_sentiment(self, email_context: Dict, slack_intelligence: Dict) -> Dict:
        """Determine overall team sentiment from multiple sources"""
        
        sentiment_data = {
            'overall': 'neutral',
            'confidence': 0.5,
            'sources': [],
            'key_indicators': []
        }
        
        # Email sentiment indicators
        email_blockers = len(email_context.get('blocker_keywords', []))
        email_decisions = len(email_context.get('decision_keywords', []))
        
        # Slack sentiment indicators  
        slack_positive = 0
        slack_negative = 0
        
        for category_key, insights in slack_intelligence.items():
            if category_key.endswith('_insights') and isinstance(insights, dict):
                sentiment_indicators = insights.get('sentiment_indicators', [])
                slack_positive += len([s for s in sentiment_indicators if s.get('type') == 'positive'])
                slack_negative += len([s for s in sentiment_indicators if s.get('type') == 'negative'])
        
        # Combine sentiment signals
        total_positive = email_decisions + slack_positive
        total_negative = email_blockers + slack_negative
        
        if total_positive > total_negative * 1.5:
            sentiment_data['overall'] = 'positive'
            sentiment_data['confidence'] = min((total_positive + total_negative) / 10, 1.0)
        elif total_negative > total_positive * 1.5:
            sentiment_data['overall'] = 'frustrated'
            sentiment_data['confidence'] = min((total_positive + total_negative) / 10, 1.0)
        
        return sentiment_data
    
    def assess_operational_status(self, slack_intelligence: Dict, jira_intelligence: Dict) -> Dict:
        """Assess overall operational status from Slack and Jira data"""
        
        status = {
            'development_health': 'healthy',
            'team_coordination': 'good',
            'delivery_confidence': 'medium',
            'risk_level': 'low'
        }
        
        # Assess development health from Jira
        if jira_intelligence.get('data_available'):
            sprint_analysis = jira_intelligence.get('sprint_analysis', {})
            velocity_status = sprint_analysis.get('velocity_status', 'on_track')
            
            if velocity_status == 'behind':
                status['development_health'] = 'at_risk'
                status['risk_level'] = 'medium'
            elif velocity_status == 'ahead':
                status['development_health'] = 'excellent'
        
        # Assess team coordination from Slack
        urgency_count = 0
        for category_key, insights in slack_intelligence.items():
            if category_key.endswith('_insights') and isinstance(insights, dict):
                urgency_count += len(insights.get('urgency_indicators', []))
        
        if urgency_count > 5:
            status['team_coordination'] = 'strained'
            status['risk_level'] = 'high'
        elif urgency_count > 2:
            status['team_coordination'] = 'busy'
            status['risk_level'] = 'medium'
        
        return status
    
    # Mock methods for testing (would be replaced with real implementations)
    
    def get_mock_slack_messages(self, channel: str, pattern: str, product: str) -> List[Dict]:
        """Generate mock Slack messages for testing"""
        return [
            {
                'text': f'{product} performance looking good this week',
                'author': 'noam',
                'timestamp': '2026-03-17T10:00:00Z',
                'channel': channel
            },
            {
                'text': f'blocked on {product} integration with external API',
                'author': 'developer',
                'timestamp': '2026-03-17T14:30:00Z', 
                'channel': channel
            }
        ]
    
    def deduplicate_messages(self, messages: List[Dict]) -> List[Dict]:
        """Remove duplicate messages based on timestamp and content"""
        seen = set()
        unique = []
        
        for msg in messages:
            key = (msg.get('timestamp', ''), msg.get('text', '')[:50])
            if key not in seen:
                seen.add(key)
                unique.append(msg)
        
        return unique
    
    # Placeholder methods for Jira API calls
    
    async def get_sprint_history(self, project_key: str, count: int) -> List[Dict]:
        """Get sprint history (mock implementation)"""
        return []
    
    def analyze_velocity_trends(self, sprint_history: List[Dict]) -> Dict:
        """Analyze velocity trends (mock implementation)"""
        return {'trend': 'stable', 'average_velocity': 40}
    
    def analyze_development_blockers(self, sprint_data: Dict) -> Dict:
        """Analyze development blockers (mock implementation)"""
        return {'active_blockers': 1, 'impact_level': 'low'}
    
    async def get_upcoming_releases(self, project_key: str) -> List[Dict]:
        """Get upcoming releases (mock implementation)"""
        return []
    
    def analyze_release_readiness(self, releases: List[Dict]) -> Dict:
        """Analyze release readiness (mock implementation)"""
        return {'next_release': None, 'confidence': 'medium'}
    
    def identify_critical_issues(self, email_context: Dict, slack_intelligence: Dict, jira_intelligence: Dict) -> List[Dict]:
        """Identify critical issues across all context sources"""
        return []
    
    def assess_development_velocity(self, jira_intelligence: Dict) -> Dict:
        """Assess development velocity"""
        return {'status': 'normal', 'trend': 'stable'}
    
    def assess_team_capacity(self, slack_intelligence: Dict, jira_intelligence: Dict) -> Dict:
        """Assess team capacity"""
        return {'utilization': 'good', 'bottlenecks': []}
    
    def generate_context_recommendations(self, email_context: Dict, slack_intelligence: Dict, jira_intelligence: Dict) -> List[Dict]:
        """Generate context-driven recommendations"""
        return []
    
    # Inherit email gathering from base class
    async def gather_email_context(self, product: str, meeting: Dict, lookback_days: int) -> Dict[str, Any]:
        """Gather email context (inherited from base ContextGatherer)"""
        # This would call the original email context gathering method
        return {
            'total_threads': 0,
            'decision_keywords': [],
            'blocker_keywords': [],
            'performance_mentions': []
        }
    
    def synthesize_slack_intelligence(self, slack_intelligence: Dict) -> Dict:
        """Synthesize Slack intelligence across channels"""
        return {
            'overall_activity': 'normal',
            'sentiment_summary': 'neutral',
            'key_themes': []
        }