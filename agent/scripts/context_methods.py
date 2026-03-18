#!/usr/bin/env python3
"""
Context gathering methods for Chief of Staff
Email and Slack intelligence integration
"""

import subprocess
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ContextGatherer:
    """Gather context from email and Slack for meeting preparation"""
    
    def __init__(self):
        self.product_channels = {
            'vivi': ['#vivi-marketing', '#creative-feedback'], 
            'clara': ['#clara-team', '#app-clara-product', '#creative-feedback'],
            'cue': ['#app-cue-product', '#creative-feedback'],
            'wordcast': ['#wordcast', '#creative-feedback'],
            'gpteen': ['#app-gpteen-product', '#creative-feedback']
        }
        self.base_channels = ['#general', '#marketing', '#product-updates']
    
    async def gather_context_intelligence(self, product: str, meeting: Dict, lookback_days: int = 7) -> Dict[str, Any]:
        """Gather context from email and Slack for enhanced meeting prep"""
        logger.info(f"📧 Gathering email and Slack context for {product}")
        
        context = {
            'email_insights': {},
            'slack_insights': {},
            'team_sentiment': 'neutral',
            'recent_decisions': [],
            'active_blockers': [],
            'action_items': [],
            'context_quality': 'partial'
        }
        
        try:
            # Parallel context gathering
            email_task = self.gather_email_context(product, meeting, lookback_days)
            slack_task = self.gather_slack_context(product, meeting, lookback_days)
            
            # Wait for both with timeouts
            email_context = await asyncio.wait_for(email_task, timeout=60)
            slack_context = await asyncio.wait_for(slack_task, timeout=60)
            
            context['email_insights'] = email_context
            context['slack_insights'] = slack_context
            context['context_quality'] = 'comprehensive'
            
            # Synthesize insights
            context.update(self.synthesize_context(email_context, slack_context))
            
        except asyncio.TimeoutError:
            logger.warning(f"⏰ Context gathering timeout for {product}")
            context['context_quality'] = 'limited'
        except Exception as e:
            logger.error(f"❌ Context gathering failed for {product}: {e}")
            context['context_quality'] = 'failed'
            
        return context
    
    async def gather_email_context(self, product: str, meeting: Dict, lookback_days: int) -> Dict[str, Any]:
        """Gather relevant email context using gog Gmail search"""
        logger.info(f"📧 Searching emails for {product} context")
        
        # Calculate date range
        after_date = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        
        # Build search queries
        queries = [
            f"{product} (performance OR metrics OR campaign OR results) after:{after_date}",
            f"{product} (decision OR approved OR blocked OR launch) after:{after_date}",
            f"{product} (budget OR spend OR cost OR ROI) after:{after_date}",
            f"{product} (creative OR test OR hook OR messaging) after:{after_date}"
        ]
        
        # Add attendee-specific searches
        attendees = [a for a in meeting.get('attendees', []) if '@44pixels.ai' in a]
        for attendee in attendees[:3]:  # Limit to prevent too many queries
            queries.append(f"from:{attendee} {product} after:{after_date}")
        
        email_insights = {
            'recent_threads': [],
            'decisions_mentioned': [],
            'performance_discussions': [],
            'budget_context': [],
            'action_items': []
        }
        
        # Execute searches
        for query in queries[:5]:  # Limit total queries
            try:
                result = subprocess.run([
                    "gog", "gmail", "search", query, 
                    "--format", "json", "--max-results", "5"
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and result.stdout.strip():
                    emails = json.loads(result.stdout)
                    email_insights['recent_threads'].extend(emails[:3])  # Top 3 per query
                    
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as e:
                logger.warning(f"⚠️ Email search failed for query '{query[:50]}...': {e}")
                continue
        
        # Process and extract insights
        email_insights = self.process_email_insights(email_insights, product)
        
        return email_insights
    
    def process_email_insights(self, email_insights: Dict, product: str) -> Dict[str, Any]:
        """Process raw email data into actionable insights"""
        processed = {
            'total_threads': len(email_insights['recent_threads']),
            'decision_keywords': [],
            'blocker_keywords': [], 
            'performance_mentions': [],
            'recent_subjects': [],
            'key_participants': set()
        }
        
        # Extract patterns from email subjects and snippets
        for email in email_insights['recent_threads']:
            subject = email.get('subject', '').lower()
            snippet = email.get('snippet', '').lower()
            
            processed['recent_subjects'].append(email.get('subject', ''))
            
            # Extract key participants
            if 'from' in email:
                processed['key_participants'].add(email['from'].get('name', 'Unknown'))
            
            # Look for decision indicators
            decision_words = ['decision', 'approved', 'go ahead', 'launch', 'stop', 'pause']
            if any(word in subject or word in snippet for word in decision_words):
                processed['decision_keywords'].append(subject)
            
            # Look for blocker indicators
            blocker_words = ['blocked', 'issue', 'problem', 'stuck', 'waiting', 'delayed']
            if any(word in subject or word in snippet for word in blocker_words):
                processed['blocker_keywords'].append(subject)
            
            # Look for performance mentions
            perf_words = ['performance', 'metrics', 'cpi', 'roas', 'conversion', 'results']
            if any(word in subject or word in snippet for word in perf_words):
                processed['performance_mentions'].append(subject)
        
        processed['key_participants'] = list(processed['key_participants'])
        
        return processed
    
    async def gather_slack_context(self, product: str, meeting: Dict, lookback_days: int) -> Dict[str, Any]:
        """Gather relevant Slack context using message tool"""
        logger.info(f"💬 Searching Slack for {product} context")
        
        # Get relevant channels for product
        channels = self.product_channels.get(product, []) + self.base_channels
        
        slack_insights = {
            'channels_searched': channels,
            'recent_mentions': [],
            'team_discussions': [],
            'sentiment_indicators': [],
            'key_messages': []
        }
        
        # Search each channel (simplified approach - would need actual Slack search implementation)
        # This is a placeholder for the actual Slack search logic
        # In reality, would use message tool to search channels
        
        # For now, return structure with placeholder data
        slack_insights['context_available'] = False
        slack_insights['note'] = "Slack search implementation needed"
        
        return slack_insights
    
    def synthesize_context(self, email_context: Dict, slack_context: Dict) -> Dict[str, Any]:
        """Synthesize email and Slack context into actionable insights"""
        synthesis = {
            'team_sentiment': self.determine_team_sentiment(email_context, slack_context),
            'recent_decisions': self.extract_recent_decisions(email_context),
            'active_blockers': self.extract_active_blockers(email_context),
            'action_items': self.extract_action_items(email_context, slack_context),
            'context_summary': self.generate_context_summary(email_context, slack_context)
        }
        
        return synthesis
    
    def determine_team_sentiment(self, email_context: Dict, slack_context: Dict) -> str:
        """Determine overall team sentiment from communication patterns"""
        # Analyze email subjects and content for sentiment indicators
        decision_count = len(email_context.get('decision_keywords', []))
        blocker_count = len(email_context.get('blocker_keywords', []))
        
        if blocker_count > decision_count * 2:
            return 'frustrated'
        elif decision_count > 0 and blocker_count == 0:
            return 'positive'
        else:
            return 'neutral'
    
    def extract_recent_decisions(self, email_context: Dict) -> List[Dict]:
        """Extract recent decisions from email context"""
        decisions = []
        
        for subject in email_context.get('decision_keywords', []):
            decisions.append({
                'topic': subject,
                'source': 'email',
                'confidence': 'medium',
                'requires_follow_up': 'decision' in subject.lower()
            })
        
        return decisions
    
    def extract_active_blockers(self, email_context: Dict) -> List[Dict]:
        """Extract active blockers from email context"""
        blockers = []
        
        for subject in email_context.get('blocker_keywords', []):
            blockers.append({
                'issue': subject,
                'source': 'email',
                'status': 'unknown',
                'priority': 'medium'
            })
        
        return blockers
    
    def extract_action_items(self, email_context: Dict, slack_context: Dict) -> List[Dict]:
        """Extract outstanding action items from context"""
        action_items = []
        
        # Extract from email subjects that indicate action needed
        for subject in email_context.get('recent_subjects', []):
            if any(word in subject.lower() for word in ['action', 'todo', 'follow up', 'next steps']):
                action_items.append({
                    'item': subject,
                    'source': 'email',
                    'status': 'pending',
                    'owner': 'unknown'
                })
        
        return action_items
    
    def generate_context_summary(self, email_context: Dict, slack_context: Dict) -> str:
        """Generate human-readable context summary"""
        email_threads = email_context.get('total_threads', 0)
        decisions = len(email_context.get('decision_keywords', []))
        blockers = len(email_context.get('blocker_keywords', []))
        performance_mentions = len(email_context.get('performance_mentions', []))
        
        summary = f"Found {email_threads} recent email threads"
        
        if decisions > 0:
            summary += f", {decisions} decisions mentioned"
        
        if blockers > 0:
            summary += f", {blockers} potential blockers"
        
        if performance_mentions > 0:
            summary += f", {performance_mentions} performance discussions"
        
        summary += f". Team sentiment appears {self.determine_team_sentiment(email_context, slack_context)}."
        
        return summary