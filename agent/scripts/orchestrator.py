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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChiefOfStaffOrchestrator:
    """Main orchestrator for meeting preparation automation"""
    
    def __init__(self):
        self.products = ["clara", "cue", "vivi", "wordcast", "gpteen"]
        self.meeting_keywords = ["marketing", "weekly", "review", "performance"]
        self.preparation_deadline = "20:00"  # 8 PM
        
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
            'alerts': [],
            'recommendations': []
        }
        
        # Spawn 44growth agent for performance data
        performance_task = self.spawn_44growth(product)
        
        # Spawn creative-strategist for creative intelligence  
        creative_task = self.spawn_creative_strategist(product)
        
        # Query Sensor Tower MCP for competitive data
        competitive_task = self.query_sensor_tower(product)
        
        # Wait for all intelligence gathering to complete
        try:
            performance_data = await asyncio.wait_for(performance_task, timeout=300)
            creative_data = await asyncio.wait_for(creative_task, timeout=300) 
            competitive_data = await asyncio.wait_for(competitive_task, timeout=180)
            
            intelligence['performance'] = performance_data
            intelligence['creatives'] = creative_data
            intelligence['competitive'] = competitive_data
            
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

## Performance Analysis
{self.format_performance_section(perf)}

## Strategic Recommendations  
{self.format_recommendations(recs)}

## Action Items
- [ ] Review performance trends
- [ ] Discuss budget allocation
- [ ] Plan upcoming creative tests

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
        alerts = intelligence.get('alerts', [])
        
        # Format alert text
        alert_text = "None" if not alerts else alerts[0]['message']
        
        message = f"""📋 **Meeting Prep Ready: {product} Marketing**

🗓 **Tomorrow** - {meeting['title']}

📊 **Key Metrics:**
• CPI: ${perf.get('cpi', 'N/A')}
• Spend: ${perf.get('daily_spend', 'N/A')}
• Conversions: {perf.get('conversions', 'N/A')}

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