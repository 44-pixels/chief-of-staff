# Jira Velocity Intelligence Skill

## Purpose
Track development velocity, sprint progress, and team capacity to provide operational context for product meetings.

## Jira Intelligence Capabilities

### 1. **Sprint Velocity Analysis**
```python
PRODUCT_JIRA_PROJECTS = {
    'vivi': 'VIVI',        # Board 270, simple
    'clara': 'CLAP',       # Clara Product, product discovery 
    'cue': 'VCS',          # Voices, Board 40, scrum
    'wordcast': 'LIS',     # Listen, Board 237, simple  
    'pixi': 'PIXI',        # Board 3, scrum
    'gpteen': 'DES',       # Design (TBD - may need dedicated project)
    'platform': 'BAC'     # Backends for shared infrastructure
}

async def analyze_sprint_velocity(product: str) -> Dict[str, Any]:
    """Analyze current and historical sprint velocity"""
    
    project_key = PRODUCT_JIRA_PROJECTS.get(product, product.upper())
    
    velocity_data = {
        'current_sprint': {},
        'velocity_trend': {},
        'capacity_analysis': {},
        'blockers_impact': {},
        'upcoming_deliveries': {}
    }
    
    # Get current sprint data
    current_sprint = await get_current_sprint(project_key)
    velocity_data['current_sprint'] = analyze_current_sprint(current_sprint)
    
    # Get velocity trend (last 6 sprints)
    sprint_history = await get_sprint_history(project_key, count=6)
    velocity_data['velocity_trend'] = analyze_velocity_trend(sprint_history)
    
    # Analyze team capacity
    velocity_data['capacity_analysis'] = analyze_team_capacity(current_sprint, sprint_history)
    
    return velocity_data
```

### 2. **Development Progress Tracking**
```python
async def track_development_progress(product: str) -> Dict[str, Any]:
    """Track development progress for product initiatives"""
    
    progress_data = {
        'active_epics': [],
        'feature_delivery_status': {},
        'bug_resolution_rate': {},
        'technical_debt_status': {},
        'release_readiness': {}
    }
    
    project_key = PRODUCT_JIRA_PROJECTS.get(product, product.upper())
    
    # Get active epics and their progress
    epics = await get_active_epics(project_key)
    progress_data['active_epics'] = analyze_epic_progress(epics)
    
    # Analyze feature delivery pipeline
    features = await get_feature_pipeline(project_key)
    progress_data['feature_delivery_status'] = analyze_feature_delivery(features)
    
    # Bug and technical debt analysis
    bugs = await get_bug_metrics(project_key)
    progress_data['bug_resolution_rate'] = analyze_bug_trends(bugs)
    
    return progress_data
```

### 3. **Team Capacity Intelligence**
```python
def analyze_team_capacity(current_sprint: Dict, sprint_history: List[Dict]) -> Dict:
    """Analyze team capacity and utilization patterns"""
    
    capacity_analysis = {
        'current_utilization': 0,
        'capacity_trend': 'stable',
        'bottlenecks': [],
        'availability_issues': [],
        'skill_gaps': []
    }
    
    # Calculate current sprint utilization
    planned_points = current_sprint.get('planned_points', 0)
    completed_points = current_sprint.get('completed_points', 0)
    remaining_points = current_sprint.get('remaining_points', 0)
    
    if planned_points > 0:
        capacity_analysis['current_utilization'] = completed_points / planned_points
    
    # Analyze historical capacity trends
    historical_velocities = [sprint.get('completed_points', 0) for sprint in sprint_history]
    if len(historical_velocities) >= 3:
        recent_avg = sum(historical_velocities[:3]) / 3
        older_avg = sum(historical_velocities[3:]) / max(len(historical_velocities[3:]), 1)
        
        if recent_avg > older_avg * 1.1:
            capacity_analysis['capacity_trend'] = 'improving'
        elif recent_avg < older_avg * 0.9:
            capacity_analysis['capacity_trend'] = 'declining'
    
    # Identify bottlenecks
    capacity_analysis['bottlenecks'] = identify_capacity_bottlenecks(current_sprint)
    
    return capacity_analysis

def identify_capacity_bottlenecks(sprint_data: Dict) -> List[Dict]:
    """Identify development bottlenecks from sprint data"""
    
    bottlenecks = []
    
    # Analyze story status distribution
    status_counts = sprint_data.get('status_distribution', {})
    total_stories = sum(status_counts.values())
    
    if total_stories > 0:
        # Too many stories in "In Progress" = bottleneck
        in_progress_pct = status_counts.get('In Progress', 0) / total_stories
        if in_progress_pct > 0.4:
            bottlenecks.append({
                'type': 'workflow_bottleneck',
                'description': f'{in_progress_pct:.0%} of stories stuck in progress',
                'severity': 'medium' if in_progress_pct < 0.6 else 'high'
            })
        
        # Too many stories in "In Review" = review bottleneck  
        review_pct = status_counts.get('In Review', 0) / total_stories
        if review_pct > 0.3:
            bottlenecks.append({
                'type': 'review_bottleneck', 
                'description': f'{review_pct:.0%} of stories waiting for review',
                'severity': 'medium'
            })
    
    return bottlenecks
```

### 4. **Release & Delivery Intelligence**
```python
async def analyze_delivery_pipeline(product: str) -> Dict[str, Any]:
    """Analyze upcoming deliveries and release readiness"""
    
    project_key = PRODUCT_JIRA_PROJECTS.get(product, product.upper())
    
    delivery_analysis = {
        'upcoming_releases': [],
        'feature_readiness': {},
        'risk_assessment': {},
        'timeline_confidence': 0
    }
    
    # Get upcoming versions/releases
    versions = await get_upcoming_versions(project_key)
    delivery_analysis['upcoming_releases'] = analyze_release_readiness(versions)
    
    # Assess delivery risks
    risks = await assess_delivery_risks(project_key)
    delivery_analysis['risk_assessment'] = risks
    
    return delivery_analysis

def analyze_release_readiness(versions: List[Dict]) -> List[Dict]:
    """Analyze readiness of upcoming releases"""
    
    release_analysis = []
    
    for version in versions:
        version_data = {
            'name': version.get('name'),
            'target_date': version.get('releaseDate'),
            'completion_pct': 0,
            'readiness_status': 'on_track',
            'blockers': [],
            'confidence': 'medium'
        }
        
        # Calculate completion percentage
        total_issues = version.get('issuesCount', 0)
        resolved_issues = version.get('resolvedIssuesCount', 0)
        
        if total_issues > 0:
            version_data['completion_pct'] = resolved_issues / total_issues
            
            # Assess readiness status
            if version_data['completion_pct'] > 0.9:
                version_data['readiness_status'] = 'ready'
                version_data['confidence'] = 'high'
            elif version_data['completion_pct'] > 0.7:
                version_data['readiness_status'] = 'on_track'
            else:
                version_data['readiness_status'] = 'at_risk'
                version_data['confidence'] = 'low'
        
        release_analysis.append(version_data)
    
    return release_analysis
```

### 5. **Blocker Impact Analysis**
```python
def analyze_blocker_impact(project_key: str, sprint_data: Dict) -> Dict:
    """Analyze how blockers are impacting development velocity"""
    
    blocker_analysis = {
        'active_blockers': [],
        'velocity_impact': 'minimal',
        'blocker_trends': {},
        'resolution_time': {}
    }
    
    # Get blocked issues
    blocked_issues = sprint_data.get('blocked_issues', [])
    
    for issue in blocked_issues:
        blocker_info = {
            'key': issue.get('key'),
            'summary': issue.get('summary'),
            'blocked_since': issue.get('blocked_date'),
            'blocker_type': classify_blocker_type(issue),
            'impact_level': assess_blocker_impact(issue)
        }
        blocker_analysis['active_blockers'].append(blocker_info)
    
    # Assess overall velocity impact
    total_blocked_points = sum(issue.get('storyPoints', 0) for issue in blocked_issues)
    total_sprint_points = sprint_data.get('planned_points', 0)
    
    if total_sprint_points > 0:
        blocked_pct = total_blocked_points / total_sprint_points
        if blocked_pct > 0.3:
            blocker_analysis['velocity_impact'] = 'significant'
        elif blocked_pct > 0.15:
            blocker_analysis['velocity_impact'] = 'moderate'
    
    return blocker_analysis
```

## Jira API Integration

### 1. **Jira REST API Wrapper**
```python
class JiraIntelligence:
    """Jira API wrapper for development intelligence"""
    
    def __init__(self):
        self.base_url = "https://44pixels.atlassian.net"
        self.auth_token = self.get_auth_token()
    
    def get_auth_token(self) -> str:
        """Get Jira API token from environment or config"""
        # Implementation would get token from secure storage
        return os.getenv('JIRA_API_TOKEN', '')
    
    async def get_current_sprint(self, project_key: str) -> Dict:
        """Get current active sprint for project"""
        
        # JQL query for current sprint
        jql = f"project = {project_key} AND sprint in openSprints()"
        
        response = await self.jira_api_call(
            endpoint="/rest/api/3/search",
            params={
                'jql': jql,
                'fields': 'summary,status,assignee,storyPoints,created,updated',
                'maxResults': 100
            }
        )
        
        return self.process_sprint_data(response)
    
    async def get_sprint_history(self, project_key: str, count: int = 6) -> List[Dict]:
        """Get historical sprint data for velocity analysis"""
        
        # Get completed sprints
        board_id = await self.get_board_id(project_key)
        
        response = await self.jira_api_call(
            endpoint=f"/rest/agile/1.0/board/{board_id}/sprint",
            params={
                'state': 'closed',
                'maxResults': count
            }
        )
        
        return self.process_sprint_history(response)
```

### 2. **Sprint Data Processing**
```python
def process_sprint_data(self, api_response: Dict) -> Dict:
    """Process Jira API response into sprint intelligence"""
    
    issues = api_response.get('issues', [])
    
    sprint_data = {
        'total_issues': len(issues),
        'planned_points': 0,
        'completed_points': 0,
        'remaining_points': 0,
        'status_distribution': {},
        'blocked_issues': [],
        'assignee_distribution': {}
    }
    
    for issue in issues:
        # Extract story points
        story_points = issue.get('fields', {}).get('customfield_10016', 0) or 0
        sprint_data['planned_points'] += story_points
        
        # Status analysis
        status = issue.get('fields', {}).get('status', {}).get('name', 'Unknown')
        sprint_data['status_distribution'][status] = sprint_data['status_distribution'].get(status, 0) + 1
        
        if status in ['Done', 'Closed']:
            sprint_data['completed_points'] += story_points
        else:
            sprint_data['remaining_points'] += story_points
        
        # Check for blocked issues
        if 'blocked' in issue.get('fields', {}).get('summary', '').lower():
            sprint_data['blocked_issues'].append({
                'key': issue.get('key'),
                'summary': issue.get('fields', {}).get('summary'),
                'storyPoints': story_points
            })
        
        # Assignee distribution
        assignee = issue.get('fields', {}).get('assignee', {})
        if assignee:
            assignee_name = assignee.get('displayName', 'Unassigned')
            sprint_data['assignee_distribution'][assignee_name] = sprint_data['assignee_distribution'].get(assignee_name, 0) + 1
    
    return sprint_data
```

## Report Integration

### Enhanced Development Intelligence Section
```markdown
## 🛠️ Development Velocity & Progress

### Sprint Status (Current)
**Completion:** {completion_pct}% ({completed_points}/{planned_points} points)  
**Velocity Trend:** {velocity_trend} ({trend_indicator})  
**Team Utilization:** {utilization_pct}%

### Active Development
**Epics In Progress:** {active_epics_count}  
**Features in Pipeline:** {feature_count} ({ready_count} ready)  
**Blockers:** {active_blockers_count} ({blocker_impact} velocity impact)

### Release Readiness
**Next Release:** {next_release_name} - {release_date} ({release_confidence})  
**Completion:** {release_completion_pct}%  
**Risk Level:** {release_risk_level}

### Capacity Insights
**Bottlenecks:** {identified_bottlenecks}  
**Team Availability:** {availability_status}  
**Skill Gaps:** {skill_gap_indicators}
```

### Development-Driven Meeting Recommendations
```python
def generate_dev_recommendations(jira_data: Dict, product: str) -> List[Dict]:
    """Generate meeting recommendations based on development intelligence"""
    
    recommendations = []
    
    # Velocity-based recommendations
    velocity_trend = jira_data.get('velocity_trend', {}).get('trend', 'stable')
    if velocity_trend == 'declining':
        recommendations.append({
            'priority': 'HIGH',
            'type': 'velocity_concern',
            'action': 'Discuss velocity decline and identify contributing factors',
            'context': f"Team velocity has declined - review capacity and blockers"
        })
    
    # Blocker-based recommendations
    active_blockers = jira_data.get('blockers_impact', {}).get('active_blockers', [])
    if len(active_blockers) > 3:
        recommendations.append({
            'priority': 'MEDIUM',
            'type': 'blocker_resolution',
            'action': f'Address {len(active_blockers)} active development blockers',
            'context': 'Multiple blockers impacting development progress'
        })
    
    # Release readiness recommendations
    releases = jira_data.get('upcoming_deliveries', {}).get('upcoming_releases', [])
    at_risk_releases = [r for r in releases if r.get('readiness_status') == 'at_risk']
    if at_risk_releases:
        recommendations.append({
            'priority': 'HIGH',
            'type': 'release_risk',
            'action': f'Review at-risk releases: {[r["name"] for r in at_risk_releases]}',
            'context': 'Release timeline confidence is low'
        })
    
    return recommendations
```

This Jira intelligence will give Chifi complete operational awareness of development capacity and delivery timelines! 🛠️📊