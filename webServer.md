# Romans 8 Memory Verse API

## Purpose

This API provides daily Bible verses from Romans 8 for memorisation. Starting from verse 3, it progresses by one verse every second day. On Sundays, it returns all verses memorised so far in a single text block.

## Memorisation Logic

- **Start Verse**: Romans 8:3
- **Progression**: +1 verse every 2 days
- **Sunday**: Return all verses up to the current memorisation point
- **Bible Version**: NIV (default)
- **Time Zone**: Australia/Perth

## API Specification

### `GET /verse?date=YYYY-MM-DD`

**Parameters**
- `date` (required): ISO format (e.g. `2025-05-01`)

**Response Structure**

#### Weekday Example
```json
{
  "date": "2025-05-01",
  "verse_reference": "Romans 8:3",
  "text": "For what the law was powerless to do because it was weakened by the flesh..."
}