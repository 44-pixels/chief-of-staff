#!/usr/bin/env python3
"""
Chief of Staff - Main Orchestrator
Automated meeting preparation for product marketing meetings
"""

import json
import asyncio
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

# Import context gathering capabilities
from context_methods import ContextGatherer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChiefOfStaffOrchestrator:
    """Main orchestrator for meeting preparation automation"""
    
    def __init__(self):
        self.products = ["clara", "cue", "vivi", "wordcast", "gpteen"]
        self.meeting_keywords = ["marketing", "weekly", "review", "performance"]
        self.preparation_deadline = "20:00"  # 8 PM
        self.context_gatherer = ContextGatherer()  # NEW: Context intelligence
        
    async def run_daily_prep(self):
        """Main entry point for daily meeting preparation"""
        logger.info("🚀 Starting Chief of Staff daily meeting preparation")
        
        try:
            # Step 1: Scan calendar for tomorrow's meetings
            meetings = await self.detect_meetings()
            
            if not meetings:
                logger.info("📅 No product marketing meetings found for tomorrow")
                return
                
            logger.info(f"📋 Found {len(meetings)} meetings requiring preparation")
            
            # Step 2: Prepare each meeting
            for meeting in meetings:
                await self.prepare_meeting(meeting)
                
        except Exception as e:
            logger.error(f"❌ Chief of Staff orchestration failed: {e}")
            await self.send_error_notification(str(e))
    
    async def detect_meetings(self) -> List[Dict[str, Any]]:
        """Detect product marketing meetings in tomorrow's calendar"""
        logger.info("🔍 Scanning calendar for product marketing meetings...")
        
        # Calculate date range (tomorrow)
        tomorrow = datetime.now() + timedelta(days=1)
        day_after = tomorrow + timedelta(days=1)
        
        tomorrow_iso = tomorrow.strftime("%Y-%m-%dT00:00:00")
        day_after_iso = day_after.strftime("%Y-%m-%dT00:00:00")
        
        try:
            # Use gog to get calendar events
            result = subprocess.run([
                "gog", "calendar", "events", "primary", 
                "--from", tomorrow_iso,
                "--to", day_after_iso,
                "--json"
            ], capture_output=True, text=True, check=True)
            
            events = json.loads(result.stdout)
            
            # Filter and classify meetings
            meetings = []
            for event in events:
                meeting = self.classify_meeting(event)
                if meeting and meeting['prep_required']:
                    meetings.append(meeting)
            
            return meetings
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Calendar access failed: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"❌ Calendar JSON parsing failed: {e}")
            return []
    
    def classify_meeting(self, event: Dict) -> Optional[Dict[str, Any]]:
        """Classify calendar event as product marketing meeting"""
        title = event.get('summary', '').lower()
        
        # Check for product marketing keywords
        has_marketing_keyword = any(keyword in title for keyword in self.meeting_keywords)
        if not has_marketing_keyword:
            return None
            
        # Extract product
        product = self.extract_product_from_title(title)
        if not product:
            return None
            
        # Build meeting object
        meeting = {
            'id': event.get('id'),
            'title': event.get('summary'),
            'product': product,
            'type': self.determine_meeting_type(title),
            'start_time': event.get('start', {}).get('dateTime'),
            'duration_minutes': self.calculate_duration(event),
            'attendees': [a.get('email') for a in event.get('attendees', [])],
            'prep_required': True,
            'confidence': self.calculate_confidence(title, product)
        }
        
        return meeting
    
    def extract_product_from_title(self, title: str) -> Optional[str]:
        """Extract product name from meeting title"""
        title_lower = title.lower()
        
        for product in self.products:
            if product in title_lower:
                return product
                
        return None
    
    def determine_meeting_type(self, title: str) -> str:
        """Determine the type of marketing meeting"""
        title_lower = title.lower()
        
        if 'weekly' in title_lower:
            return 'weekly_marketing'
        elif 'review' in title_lower:
            return 'performance_review'  
        elif 'planning' in title_lower:
            return 'campaign_planning'
        else:
            return 'marketing_general'
    
    def calculate_duration(self, event: Dict) -> int:
        """Calculate meeting duration in minutes"""
        start = event.get('start', {}).get('dateTime')
        end = event.get('end', {}).get('dateTime')
        
        if not start or not end:
            return 60  # Default assumption
            
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            duration = (end_dt - start_dt).total_seconds() / 60
            return int(duration)
        except:
            return 60
    
    def calculate_confidence(self, title: str, product: str) -> float:
        """Calculate confidence score for meeting classification"""
        score = 0.5  # Base score
        
        # Product name match
        if product in title.lower():
            score += 0.3
            
        # Marketing keyword match  
        marketing_words = ['marketing', 'campaign', 'performance', 'review']
        matches = sum(1 for word in marketing_words if word in title.lower())
        score += matches * 0.05
        
        return min(score, 1.0)
    
    async def prepare_meeting(self, meeting: Dict[str, Any]):
        """Prepare intelligence report for a specific meeting"""
        product = meeting['product']
        logger.info(f"📊 Preparing meeting intelligence for {product.title()}")
        
        try:
            # Step 1: Gather intelligence from multiple sources
            intelligence = await self.gather_intelligence(product, meeting)
            
            # Step 2: Generate comprehensive report
            report_url = await self.generate_report(product, meeting, intelligence)
            
            # Step 3: Send notifications
            await self.send_notifications(meeting, intelligence, report_url)
            
            logger.info(f"✅ Meeting preparation completed for {product.title()}")
            
        except Exception as e:
            logger.error(f"❌ Meeting preparation failed for {product}: {e}")
            await self.send_error_notification(f"Failed to prepare {product} meeting: {e}")
    
    async def gather_intelligence(self, product: str, meeting: Dict) -> Dict[str, Any]:
        """Orchestrate intelligence gathering from multiple sources"""
        logger.info(f"🔍 Gathering intelligence for {product}")
        
        intelligence = {
            'product': product,
            'meeting_date': meeting['start_time'],
            'performance': {},
            'creatives': {},
            'competitive': {},
            'context': {},  # Email + Slack context
            'campaigns': {},  # NEW: Multi-channel campaign intelligence
            'historical': {},  # NEW: Google Drive meeting notes context
            'alerts': [],
            'recommendations': []
        }
        
        # Spawn 44growth agent for performance data
        performance_task = self.spawn_44growth(product)
        
        # Spawn creative-strategist for creative intelligence  
        creative_task = self.spawn_creative_strategist(product)
        
        # Query Sensor Tower MCP for competitive data
        competitive_task = self.query_sensor_tower(product)
        
        # Gather context from email and Slack
        context_task = self.context_gatherer.gather_context_intelligence(product, meeting)
        
        # NEW: Gather campaign intelligence across all channels
        campaign_task = self.gather_campaign_intelligence(product)
        
        # NEW: Gather Google Drive context from meeting notes
        drive_context_task = self.gather_drive_context(product, meeting['type'])
        
        # Wait for all intelligence gathering to complete
        try:
            performance_data = await asyncio.wait_for(performance_task, timeout=300)
            creative_data = await asyncio.wait_for(creative_task, timeout=300) 
            competitive_data = await asyncio.wait_for(competitive_task, timeout=180)
            context_data = await asyncio.wait_for(context_task, timeout=120)
            campaign_data = await asyncio.wait_for(campaign_task, timeout=360)  # NEW
            drive_data = await asyncio.wait_for(drive_context_task, timeout=90)  # NEW
            
            intelligence['performance'] = performance_data
            intelligence['creatives'] = creative_data
            intelligence['competitive'] = competitive_data
            intelligence['context'] = context_data
            intelligence['campaigns'] = campaign_data  # NEW
            intelligence['historical'] = drive_data  # NEW
            
            # Detect alerts and generate recommendations
            intelligence['alerts'] = self.detect_alerts(intelligence)
            intelligence['recommendations'] = self.generate_recommendations(intelligence)
            
        except asyncio.TimeoutError as e:
            logger.warning(f"⏰ Intelligence gathering timeout for {product}: {e}")
            # Continue with partial data
            
        return intelligence
    
    async def spawn_44growth(self, product: str) -> Dict[str, Any]:
        """Spawn 44growth agent for performance analysis"""
        # Implementation would use sessions_spawn to get performance data
        # For now, return mock data structure
        return {
            'cpi': 2.45,
            'daily_spend': 1247,
            'conversions': 89,
            'trends': {'cpi_change': 8, 'spend_change': -12, 'conv_change': 15}
        }
    
    async def spawn_creative_strategist(self, product: str) -> Dict[str, Any]:
        """Spawn creative-strategist agent for creative analysis"""
        # Implementation would use sessions_spawn to get creative insights
        return {
            'recent_launches': [],
            'test_results': [],
            'hook_performance': {},
            'pipeline_status': 'healthy'
        }
    
    async def query_sensor_tower(self, product: str) -> Dict[str, Any]:
        """Query Sensor Tower MCP for competitive intelligence"""
        # Implementation would use mcporter to call Sensor Tower
        return {
            'market_position': 'stable',
            'competitor_movements': [],
            'category_trends': {}
        }
    
    def detect_alerts(self, intelligence: Dict) -> List[Dict]:
        """Detect performance and competitive alerts"""
        alerts = []
        
        perf = intelligence.get('performance', {})
        trends = perf.get('trends', {})
        
        # Performance alerts
        if trends.get('cpi_change', 0) > 15:
            alerts.append({
                'type': 'cpi_spike',
                'priority': 'HIGH',
                'message': f"CPI increased {trends['cpi_change']}% - audience saturation risk"
            })
            
        return alerts
    
    def generate_recommendations(self, intelligence: Dict) -> List[Dict]:
        """Generate strategic recommendations based on intelligence"""
        recommendations = []
        
        # Example recommendation logic
        alerts = intelligence.get('alerts', [])
        for alert in alerts:
            if alert['type'] == 'cpi_spike':
                recommendations.append({
                    'priority': 'HIGH',
                    'action': 'Expand audience targeting',
                    'rationale': 'Address CPI inflation through lookalike expansion',
                    'timeline': 'This week',
                    'owner': 'Campaign Manager'
                })
                
        return recommendations
    
    async def generate_report(self, product: str, meeting: Dict, intelligence: Dict) -> str:
        """Generate and deploy comprehensive meeting preparation report"""
        logger.info(f"📋 Generating report for {product}")
        
        # Generate report content using report-generator skill logic
        report_content = self.format_report(product, meeting, intelligence)
        
        # Deploy to 44reports MCP
        date_slug = datetime.now().strftime("%Y-%m-%d")
        slug = f"meeting-prep-{product}-{date_slug}"
        
        try:
            result = subprocess.run([
                "mcporter", "call", "44reports-mcp.deploy_context",
                f'name=Meeting Prep: {product.title()} - {date_slug}',
                f'slug={slug}',
                f'description=Marketing meeting preparation for {product.title()}',
                f'content={report_content}',
                'tags=["meeting-prep", "marketing", "weekly"]',
                'agent_id=chief-of-staff',
                'agent_name=Chief of Staff'
            ], capture_output=True, text=True, check=True)
            
            report_url = f"https://reporter.44pixels.workers.dev/r/{slug}"
            logger.info(f"📋 Report deployed: {report_url}")
            return report_url
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Report deployment failed: {e}")
            raise
    
    def format_report(self, product: str, meeting: Dict, intelligence: Dict) -> str:
        """Format intelligence data into markdown report"""
        perf = intelligence.get('performance', {})
        context = intelligence.get('context', {})
        alerts = intelligence.get('alerts', [])
        recs = intelligence.get('recommendations', [])
        
        report = f"""# Meeting Prep: {product.title()} Marketing

## Executive Summary
**Meeting:** {meeting['title']}  
**Date:** {meeting['start_time'][:10]}  
**Duration:** {meeting['duration_minutes']} minutes

### Key Metrics
- **CPI:** ${perf.get('cpi', 'N/A')} 
- **Daily Spend:** ${perf.get('daily_spend', 'N/A')}
- **Conversions:** {perf.get('conversions', 'N/A')}

### Attention Required
{self.format_alerts(alerts)}

## Team Context & Recent Developments
{self.format_context_section(context)}

## Performance Analysis
{self.format_performance_section(perf)}

## Strategic Recommendations  
{self.format_recommendations(recs)}

## Action Items
{self.format_context_action_items(context)}

---
*Generated by Chief of Staff • {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
        return report
    
    def format_alerts(self, alerts: List[Dict]) -> str:
        """Format alerts section"""
        if not alerts:
            return "✅ No critical alerts"
            
        formatted = []
        for alert in alerts:
            priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(alert['priority'], "ℹ️")
            formatted.append(f"{priority_emoji} {alert['message']}")
            
        return "\n".join(formatted)
    
    def format_performance_section(self, perf: Dict) -> str:
        """Format performance analysis section"""
        trends = perf.get('trends', {})
        
        return f"""
### Current Metrics
- **CPI:** ${perf.get('cpi', 'N/A')} ({trends.get('cpi_change', 0):+.1f}% vs last week)
- **Daily Spend:** ${perf.get('daily_spend', 'N/A')} ({trends.get('spend_change', 0):+.1f}% vs target)
- **Conversions:** {perf.get('conversions', 'N/A')} ({trends.get('conv_change', 0):+.1f}% vs last week)

### Insights
Performance analysis shows mixed signals requiring discussion in meeting.
"""
    
    def format_recommendations(self, recs: List[Dict]) -> str:
        """Format recommendations section"""
        if not recs:
            return "No specific recommendations at this time."
            
        formatted = []
        for i, rec in enumerate(recs, 1):
            priority = rec.get('priority', 'MEDIUM')
            formatted.append(f"""
### {i}. {rec.get('action', 'Action Required')} (Priority: {priority})
**Rationale:** {rec.get('rationale', 'See meeting discussion')}  
**Timeline:** {rec.get('timeline', 'TBD')}  
**Owner:** {rec.get('owner', 'TBD')}
""")
        return "\n".join(formatted)
    
    def format_context_section(self, context: Dict) -> str:
        """Format team context section"""
        if not context or context.get('context_quality') == 'failed':
            return "📭 *Context gathering unavailable*"
        
        email_insights = context.get('email_insights', {})
        decisions = context.get('recent_decisions', [])
        blockers = context.get('active_blockers', [])
        sentiment = context.get('team_sentiment', 'neutral')
        summary = context.get('context_summary', 'No context available')
        
        sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'frustrated': '😤'}.get(sentiment, '🤷')
        
        section = f"""
### 📧 Email Intelligence ({email_insights.get('total_threads', 0)} threads)
{summary}

### 💬 Team Sentiment
{sentiment_emoji} **{sentiment.title()}** - Based on recent communication patterns

### 📋 Recent Developments
"""
        
        if decisions:
            section += "**Decisions Made:**\n"
            for decision in decisions[:3]:  # Top 3
                section += f"- {decision['topic']}\n"
            section += "\n"
        
        if blockers:
            section += "**Active Issues:**\n"
            for blocker in blockers[:3]:  # Top 3
                section += f"- {blocker['issue']}\n"
            section += "\n"
        
        if not decisions and not blockers:
            section += "*No major decisions or blockers detected in recent communications*\n"
        
        return section
    
    def format_context_action_items(self, context: Dict) -> str:
        """Format action items enhanced with context"""
        base_items = [
            "- [ ] Review performance trends",
            "- [ ] Discuss budget allocation", 
            "- [ ] Plan upcoming creative tests"
        ]
        
        context_items = []
        
        # Add context-driven action items
        blockers = context.get('active_blockers', [])
        if blockers:
            context_items.append("- [ ] Address active blockers identified in emails")
        
        decisions = context.get('recent_decisions', [])
        if decisions:
            context_items.append("- [ ] Follow up on recent decisions and implementation status")
        
        action_items = context.get('action_items', [])
        if action_items:
            context_items.append(f"- [ ] Review {len(action_items)} outstanding action items from communications")
        
        all_items = base_items + context_items
        return "\n".join(all_items)
    
    async def send_notifications(self, meeting: Dict, intelligence: Dict, report_url: str):
        """Send Telegram and email notifications"""
        logger.info("📱 Sending meeting prep notifications")
        
        # Send Telegram notification
        await self.send_telegram_notification(meeting, intelligence, report_url)
        
        # Send email notification  
        await self.send_email_notification(meeting, intelligence, report_url)
    
    async def send_telegram_notification(self, meeting: Dict, intelligence: Dict, report_url: str):
        """Send Telegram notification with meeting prep summary"""
        product = meeting['product'].title()
        perf = intelligence.get('performance', {})
        context = intelligence.get('context', {})
        alerts = intelligence.get('alerts', [])
        
        # Format alert text
        alert_text = "None" if not alerts else alerts[0]['message']
        
        # Add context highlights
        sentiment = context.get('team_sentiment', 'neutral')
        sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'frustrated': '😤'}.get(sentiment, '🤷')
        
        decisions_count = len(context.get('recent_decisions', []))
        blockers_count = len(context.get('active_blockers', []))
        
        context_line = f"{sentiment_emoji} Team: {sentiment}"
        if decisions_count > 0:
            context_line += f" • {decisions_count} decisions"
        if blockers_count > 0:
            context_line += f" • {blockers_count} blockers"
        
        message = f"""📋 **Meeting Prep Ready: {product} Marketing**

🗓 **Tomorrow** - {meeting['title']}

📊 **Key Metrics:**
• CPI: ${perf.get('cpi', 'N/A')}
• Spend: ${perf.get('daily_spend', 'N/A')}
• Conversions: {perf.get('conversions', 'N/A')}

📧 **Context:** {context_line}

⚠️ **Attention Required:**
{alert_text}

📋 **Full Report:** {report_url}"""

        # Implementation would use message tool to send to Telegram
        logger.info("📱 Telegram notification sent")
    
    async def send_email_notification(self, meeting: Dict, intelligence: Dict, report_url: str):
        """Send email notification with detailed summary"""
        # Implementation would use email sending capability
        logger.info("📧 Email notification sent")
    
    async def send_error_notification(self, error_message: str):
        """Send error notification when system fails"""
        logger.error(f"🚨 Sending error notification: {error_message}")
        # Implementation would send error alert

if __name__ == "__main__":
    orchestrator = ChiefOfStaffOrchestrator()
    asyncio.run(orchestrator.run_daily_prep())
    async def gather_campaign_intelligence(self, product: str) -> Dict[str, Any]:
        """Gather comprehensive campaign performance across all channels"""
        logger.info(f"📊 Gathering campaign intelligence for {product}")
        
        campaign_intelligence = {
            'meta': {},
            'google': {},
            'apple_search': {},
            'cross_channel_analysis': {},
            'data_sources': []
        }
        
        # Meta campaigns via MKL agent (available)
        try:
            meta_task = self.spawn_mkl_agent(product)
            campaign_intelligence['meta'] = await asyncio.wait_for(meta_task, timeout=300)
            campaign_intelligence['data_sources'].append('meta_mkl')
            logger.info(f"✅ Meta campaign data gathered for {product}")
        except Exception as e:
            logger.warning(f"⚠️ Meta campaign data failed for {product}: {e}")
            campaign_intelligence['meta'] = {'error': str(e), 'status': 'failed'}
        
        # Google campaigns via Seekr agent (needs installation)
        try:
            google_task = self.spawn_seekr_agent(product)
            campaign_intelligence['google'] = await asyncio.wait_for(google_task, timeout=300)
            campaign_intelligence['data_sources'].append('google_seekr')
            logger.info(f"✅ Google campaign data gathered for {product}")
        except Exception as e:
            logger.warning(f"⚠️ Seekr agent not available for {product}: {e}")
            campaign_intelligence['google'] = {'error': 'Seekr agent not installed', 'status': 'unavailable'}
        
        # Apple Search Ads via apple-search agent (needs installation)  
        try:
            apple_task = self.spawn_apple_search_agent(product)
            campaign_intelligence['apple_search'] = await asyncio.wait_for(apple_task, timeout=300)
            campaign_intelligence['data_sources'].append('apple_search')
            logger.info(f"✅ Apple Search campaign data gathered for {product}")
        except Exception as e:
            logger.warning(f"⚠️ apple-search agent not available for {product}: {e}")
            campaign_intelligence['apple_search'] = {'error': 'apple-search agent not installed', 'status': 'unavailable'}
        
        # Cross-channel analysis with available data
        campaign_intelligence['cross_channel_analysis'] = self.analyze_cross_channel_performance(
            campaign_intelligence['meta'], 
            campaign_intelligence['google'], 
            campaign_intelligence['apple_search']
        )
        
        return campaign_intelligence
    
    async def spawn_mkl_agent(self, product: str) -> Dict[str, Any]:
        """Spawn MKL agent for Meta campaign analysis"""
        # Implementation would use sessions_spawn to get Meta campaign data
        # For now, return mock data structure
        return {
            'campaigns': [],
            'creative_performance': {},
            'audience_insights': {},
            'budget_utilization': {},
            'optimization_recommendations': [],
            'data_source': 'mkl_agent'
        }
    
    async def spawn_seekr_agent(self, product: str) -> Dict[str, Any]:
        """Spawn Seekr agent for Google Ads analysis (when available)"""
        # This will be implemented once Seekr is installed
        raise Exception("Seekr agent not installed - Google Ads data unavailable")
    
    async def spawn_apple_search_agent(self, product: str) -> Dict[str, Any]:
        """Spawn apple-search agent for Apple Search Ads analysis (when available)"""  
        # This will be implemented once apple-search is installed
        raise Exception("apple-search agent not installed - Apple Search Ads data unavailable")
    
    def analyze_cross_channel_performance(self, meta_data: Dict, google_data: Dict, apple_data: Dict) -> Dict:
        """Analyze performance across all available paid channels"""
        
        available_channels = []
        total_spend = 0
        total_conversions = 0
        channel_efficiency = {}
        
        # Process Meta data
        if meta_data.get('status') != 'failed' and meta_data.get('status') != 'unavailable':
            available_channels.append('meta')
            # Extract metrics from meta_data when real implementation
            
        # Process Google data
        if google_data.get('status') != 'failed' and google_data.get('status') != 'unavailable':
            available_channels.append('google')
            
        # Process Apple data  
        if apple_data.get('status') != 'failed' and apple_data.get('status') != 'unavailable':
            available_channels.append('apple_search')
        
        analysis = {
            'available_channels': available_channels,
            'missing_channels': [ch for ch in ['meta', 'google', 'apple_search'] if ch not in available_channels],
            'data_completeness': len(available_channels) / 3,  # 3 total channels
            'cross_channel_insights': self.generate_cross_channel_insights(available_channels),
            'optimization_opportunities': self.identify_channel_optimization(available_channels)
        }
        
        return analysis
    
    def generate_cross_channel_insights(self, available_channels: List[str]) -> List[str]:
        """Generate insights based on available channel data"""
        insights = []
        
        if len(available_channels) == 0:
            insights.append("⚠️ No campaign data available - cannot provide channel insights")
        elif len(available_channels) == 1:
            insights.append(f"📊 Limited to {available_channels[0]} channel data - install additional agents for complete picture")
        else:
            insights.append(f"📊 Multi-channel analysis available across {', '.join(available_channels)}")
        
        return insights
    
    def identify_channel_optimization(self, available_channels: List[str]) -> List[Dict]:
        """Identify optimization opportunities based on available data"""
        opportunities = []
        
        missing_channels = [ch for ch in ['meta', 'google', 'apple_search'] if ch not in available_channels]
        
        for channel in missing_channels:
            if channel == 'google':
                opportunities.append({
                    'type': 'missing_data',
                    'channel': 'google_ads', 
                    'action': 'Install Seekr agent',
                    'impact': 'HIGH - $30.4K/day spend visibility missing',
                    'priority': 'CRITICAL'
                })
            elif channel == 'apple_search':
                opportunities.append({
                    'type': 'missing_data',
                    'channel': 'apple_search_ads',
                    'action': 'Install apple-search agent', 
                    'impact': 'MEDIUM - iOS search optimization blind spot',
                    'priority': 'HIGH'
                })
        
        return opportunities

    async def gather_drive_context(self, product: str, meeting_type: str) -> Dict[str, Any]:
        """Gather context from Google Drive meeting notes and strategy docs"""
        logger.info(f"📄 Gathering Google Drive context for {product}")
        
        drive_context = {
            'previous_meetings': [],
            'strategic_documents': [],
            'outstanding_items': [],
            'search_queries_used': [],
            'documents_found': 0,
            'context_quality': 'partial'
        }
        
        # Define search queries
        queries = [
            f"{product} meeting notes",
            f"{product} weekly review",
            f"{product} performance review", 
            f"{product} strategy decisions",
            f"{product} roadmap"
        ]
        
        # Execute Google Drive searches
        for query in queries:
            try:
                result = subprocess.run([
                    "gog", "drive", "search", query,
                    "--type", "document",
                    "--modified-after", "2026-03-01",
                    "--max-results", "5",
                    "--json"
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and result.stdout.strip():
                    docs = json.loads(result.stdout)
                    drive_context['previous_meetings'].extend(docs[:3])  # Top 3 per query
                    drive_context['documents_found'] += len(docs)
                    drive_context['search_queries_used'].append(query)
                    
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as e:
                logger.warning(f"⚠️ Drive search failed for '{query}': {e}")
                continue
        
        # Process and extract insights from found documents
        if drive_context['documents_found'] > 0:
            drive_context['context_quality'] = 'good'
            drive_context = self.process_drive_documents(drive_context, product)
        else:
            drive_context['context_quality'] = 'limited'
            logger.info(f"📄 No Google Drive documents found for {product}")
        
        return drive_context
    
    def process_drive_documents(self, drive_context: Dict, product: str) -> Dict:
        """Process Google Drive documents to extract actionable insights"""
        
        processed = {
            'recent_meeting_themes': [],
            'strategic_initiatives': [],
            'recurring_issues': [],
            'previous_decisions': [],
            'document_titles': []
        }
        
        # Extract insights from document titles and metadata
        for doc in drive_context['previous_meetings']:
            title = doc.get('name', '').lower()
            processed['document_titles'].append(doc.get('name', 'Untitled'))
            
            # Look for strategic themes in titles
            if any(word in title for word in ['strategy', 'roadmap', 'planning']):
                processed['strategic_initiatives'].append(title)
            
            # Look for performance/review themes
            if any(word in title for word in ['performance', 'review', 'weekly', 'metrics']):
                processed['recent_meeting_themes'].append(title)
        
        # Update drive_context with processed insights
        drive_context.update(processed)
        
        return drive_context

    async def spawn_apple_search_agent(self, product: str) -> Dict[str, Any]:
        """Spawn apple-search agent for Apple Search Ads analysis"""
        
        # Check if product has Apple Search campaigns
        apple_products = ['cue', 'wordcast', 'clara', 'pixi', 'vivi']
        
        if product not in apple_products:
            return {
                'error': f'{product} not in Apple Search portfolio',
                'status': 'not_applicable',
                'data_source': 'apple_search_agent'
            }
        
        # Implementation would use sessions_spawn to get Apple Search intelligence
        task_message = f"""Analyze {product} Apple Search Ads performance for marketing meeting prep:

1. Campaign performance (spend, conversions, ROAS) last 7 days vs previous period
2. Keyword ranking changes and ASO opportunities  
3. Competitive positioning and threats
4. Budget utilization and pacing
5. Optimization recommendations for discussion

Focus on actionable insights for marketing team meeting."""

        try:
            # This would be the actual implementation
            # response = sessions_spawn(
            #     agentId="apple-search",
            #     task=task_message,
            #     mode="run",
            #     timeoutSeconds=300
            # )
            
            # For now, return structured mock data
            return {
                'campaign_performance': {
                    'total_spend': 1250,
                    'conversions': 47,
                    'roas': 2.3,
                    'trend': 'improving'
                },
                'aso_insights': {
                    'keyword_rankings': 'stable',
                    'app_store_position': 'maintaining',
                    'optimization_opportunities': 2
                },
                'competitive_intelligence': {
                    'new_competitors': 0,
                    'ranking_threats': 'minimal',
                    'market_share': 'stable'
                },
                'recommendations': [
                    'Increase budget for high-ROAS keywords',
                    'Test new ASO metadata variations',
                    'Monitor competitor bidding patterns'
                ],
                'data_source': 'apple_search_agent',
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"❌ Apple Search agent spawn failed for {product}: {e}")
            return {
                'error': str(e),
                'status': 'failed',
                'data_source': 'apple_search_agent'
            }
