# Meeting Detector Skill

## Purpose
Scan Noam's calendar and identify product marketing meetings requiring preparation.

## Trigger Keywords
- "marketing" (Clara Marketing, Vivi Marketing)
- "weekly" (Clara Weekly, Product Weekly)  
- "review" (Performance Review, Campaign Review)
- "performance" (Vivi Performance, Growth Review)
- Product names: Clara, Cue, Vivi, Wordcast, GPTeen

## Calendar Access
```bash
# Scan next 24-48 hours
gog calendar events primary --from tomorrow --to day-after-tomorrow --json
```

## Meeting Classification Logic

### Include Meetings:
- Title contains product name + marketing keyword
- Weekly recurring product meetings
- Performance review meetings  
- Campaign planning sessions

### Exclude Meetings:
- 1:1 meetings (unless product-specific)
- Internal operations meetings
- Client/external meetings without product context
- Cancelled or tentative meetings

## Product Extraction

### Pattern Matching:
- "Vivi Marketing Weekly" → Product: Vivi, Type: Marketing Weekly
- "Clara Performance Review" → Product: Clara, Type: Performance Review  
- "Weekly Marketing - Cue" → Product: Cue, Type: Weekly Marketing

### Fallback Logic:
- If ambiguous, extract most likely product from context
- If still uncertain, ask Noam for clarification
- Default to "multi-product" for general marketing meetings

## Output Format
```json
{
  "meetings": [
    {
      "id": "calendar_event_id",
      "title": "Vivi Marketing Weekly",  
      "product": "vivi",
      "type": "marketing_weekly",
      "start_time": "2026-03-19T09:00:00Z",
      "duration_minutes": 60,
      "attendees": ["noam@44pixels.ai", "vlad@44pixels.ai"],
      "prep_required": true,
      "confidence": 0.95
    }
  ],
  "total_meetings": 1,
  "prep_deadline": "2026-03-18T20:00:00Z"
}
```

## Integration Points
- Called by main chief-of-staff orchestrator
- Output feeds into intelligence gathering pipeline
- Results logged for meeting history tracking
- Confidence scores help prioritize prep effort