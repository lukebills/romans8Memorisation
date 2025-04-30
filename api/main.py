from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pytz

# In-memory data for Romans 8:3 and 8:4 as a template
ROMANS_8_VERSES = [
    {"verse_num": 3, "Verse": "Romans 8:3", "NIV": "For what the law was powerless to do... (NIV)", "ESV": "For God has done what the law... (ESV)"},
    {"verse_num": 4, "Verse": "Romans 8:4", "NIV": "in order that the righteous... (NIV)", "ESV": "in order that the righteous... (ESV)"},
    # Add more verses as needed
]

START_VERSE = 3
TIMEZONE = 'Australia/Perth'
START_DATE = datetime(2025, 4, 30)

app = FastAPI()

@app.get("/verse")
def get_verse(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    version: str = Query("NIV", description="Bible version: NIV or ESV")
):
    try:
        version = version.upper()
        if version not in ["NIV", "ESV"]:
            raise HTTPException(status_code=400, detail="Version must be 'NIV' or 'ESV'.")
        try:
            user_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        tz = pytz.timezone(TIMEZONE)
        user_date = tz.localize(user_date)
        days_since_start = (user_date.date() - START_DATE.date()).days
        if days_since_start < 0:
            raise HTTPException(status_code=400, detail="Date is before memorisation start.")
        verses_learned = days_since_start // 2 + 1
        max_verses = len(ROMANS_8_VERSES)
        verses_learned = min(verses_learned, max_verses)
        if user_date.strftime('%A') == 'Sunday':
            verses = ROMANS_8_VERSES[:verses_learned]
            text = " ".join([v[version] for v in verses])
            reference = f"Romans 8:{verses[0]['verse_num']}-{verses[verses_learned-1]['verse_num']}"
            return JSONResponse({
                "date": date,
                "verse_reference": reference,
                "version": version,
                "text": text
            })
        else:
            verse = ROMANS_8_VERSES[verses_learned-1]
            return JSONResponse({
                "date": date,
                "verse_reference": verse['Verse'],
                "version": version,
                "text": verse[version]
            })
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) 