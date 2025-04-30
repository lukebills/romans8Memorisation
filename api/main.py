import pandas as pd
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pytz
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "Romans_8_NIV_ESV.csv")

def load_verses():
    verses_df = pd.read_csv(CSV_PATH).dropna()
    if not {'verse_reference', 'text'}.issubset(verses_df.columns):
        raise ValueError("CSV must have 'verse_reference' and 'text' columns.")
    def verse_number(ref):
        try:
            return int(ref.split(":")[1])
        except Exception:
            return 0
    verses_df = verses_df[verses_df['verse_reference'].str.startswith('Romans 8:')]
    verses_df['verse_num'] = verses_df['verse_reference'].apply(verse_number)
    verses_df = verses_df[verses_df['verse_num'] >= 3].sort_values('verse_num')
    verses_df = verses_df.reset_index(drop=True)
    return verses_df

START_VERSE = 3
TIMEZONE = 'Australia/Perth'
START_DATE = datetime(2025, 5, 1)

app = FastAPI()

@app.get("/verse")
def get_verse(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    verses_df = load_verses()
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
    max_verses = len(verses_df)
    verses_learned = min(verses_learned, max_verses)
    if user_date.strftime('%A') == 'Sunday':
        verses = verses_df.iloc[:verses_learned]
        text = " ".join(verses['text'].tolist())
        reference = f"Romans 8:{verses.iloc[0]['verse_num']}-{verses.iloc[verses_learned-1]['verse_num']}"
        return JSONResponse({
            "date": date,
            "verse_reference": reference,
            "text": text
        })
    else:
        verse = verses_df.iloc[verses_learned-1]
        return JSONResponse({
            "date": date,
            "verse_reference": verse['verse_reference'],
            "text": verse['text']
        }) 