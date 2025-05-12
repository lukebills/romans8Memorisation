import pandas as pd  # (can be removed if not used elsewhere)
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import pytz

# In-memory data for Romans 8:3 and 8:4 as a template
ROMANS_8_VERSES = [
  {
    "verse_num": 1,
    "Verse": "Romans 8:1",
    "NIV": "Therefore, there is now no condemnation for those who are in Christ Jesus,",
    "ESV": "There is therefore now no condemnation for those who are in Christ Jesus."
  },
  {
    "verse_num": 2,
    "Verse": "Romans 8:2",
    "NIV": "because through Christ Jesus the law of the Spirit who gives life has set you free from the law of sin and death.",
    "ESV": "For the law of the Spirit of life has set you free in Christ Jesus from the law of sin and death."
  },
  {
    "verse_num": 3,
    "Verse": "Romans 8:3",
    "NIV": "For what the law was powerless to do because it was weakened by the flesh, God did by sending his own Son in the likeness of sinful flesh to be a sin offering. And so he condemned sin in the flesh,",
    "ESV": "For God has done what the law, weakened by the flesh, could not do. By sending his own Son in the likeness of sinful flesh and for sin, he condemned sin in the flesh,"
  },
  {
    "verse_num": 4,
    "Verse": "Romans 8:4",
    "NIV": "in order that the righteous requirement of the law might be fully met in us, who do not live according to the flesh but according to the Spirit.",
    "ESV": "in order that the righteous requirement of the law might be fulfilled in us, who walk not according to the flesh but according to the Spirit."
  },
  {
    "verse_num": 5,
    "Verse": "Romans 8:5",
    "NIV": "Those who live according to the flesh have their minds set on what the flesh desires; but those who live in accordance with the Spirit have their minds set on what the Spirit desires.",
    "ESV": "For those who live according to the flesh set their minds on the things of the flesh, but those who live according to the Spirit set their minds on the things of the Spirit."
  },
  {
    "verse_num": 6,
    "Verse": "Romans 8:6",
    "NIV": "The mind governed by the flesh is death, but the mind governed by the Spirit is life and peace.",
    "ESV": "For to set the mind on the flesh is death, but to set the mind on the Spirit is life and peace."
  },
  {
    "verse_num": 7,
    "Verse": "Romans 8:7",
    "NIV": "The mind governed by the flesh is hostile to God; it does not submit to God's law, nor can it do so.",
    "ESV": "For the mind that is set on the flesh is hostile to God, for it does not submit to God's law; indeed, it cannot."
  },
  {
    "verse_num": 8,
    "Verse": "Romans 8:8",
    "NIV": "Those who are in the realm of the flesh cannot please God.",
    "ESV": "Those who are in the flesh cannot please God."
  },
  {
    "verse_num": 9,
    "Verse": "Romans 8:9",
    "NIV": "You, however, are not in the realm of the flesh but are in the realm of the Spirit, if indeed the Spirit of God lives in you. And if anyone does not have the Spirit of Christ, they do not belong to Christ.",
    "ESV": "You, however, are not in the flesh but in the Spirit, if in fact the Spirit of God dwells in you. Anyone who does not have the Spirit of Christ does not belong to him."
  },
  {
    "verse_num": 10,
    "Verse": "Romans 8:10",
    "NIV": "But if Christ is in you, then even though your body is subject to death because of sin, the Spirit gives life because of righteousness.",
    "ESV": "But if Christ is in you, although the body is dead because of sin, the Spirit is life because of righteousness."
  },
  {
    "verse_num": 11,
    "Verse": "Romans 8:11",
    "NIV": "And if the Spirit of him who raised Jesus from the dead is living in you, he who raised Christ from the dead will also give life to your mortal bodies because of his Spirit who lives in you.",
    "ESV": "If the Spirit of him who raised Jesus from the dead dwells in you, he who raised Christ Jesus from the dead will also give life to your mortal bodies through his Spirit who dwells in you."
  },
  {
    "verse_num": 12,
    "Verse": "Romans 8:12",
    "NIV": "Therefore, brothers and sisters, we have an obligation—but it is not to the flesh, to live according to it.",
    "ESV": "So then, brothers, we are debtors, not to the flesh, to live according to the flesh."
  },
  {
    "verse_num": 13,
    "Verse": "Romans 8:13",
    "NIV": "For if you live according to the flesh, you will die; but if by the Spirit you put to death the misdeeds of the body, you will live.",
    "ESV": "For if you live according to the flesh you will die, but if by the Spirit you put to death the deeds of the body, you will live."
  },
  {
    "verse_num": 14,
    "Verse": "Romans 8:14",
    "NIV": "For those who are led by the Spirit of God are the children of God.",
    "ESV": "For all who are led by the Spirit of God are sons of God."
  },
  {
    "verse_num": 15,
    "Verse": "Romans 8:15",
    "NIV": "The Spirit you received does not make you slaves, so that you live in fear again; rather, the Spirit you received brought about your adoption to sonship. And by him we cry, 'Abba, Father.'",
    "ESV": "For you did not receive the spirit of slavery to fall back into fear, but you have received the Spirit of adoption as sons, by whom we cry, 'Abba! Father!'"
  },
  {
    "verse_num": 16,
    "Verse": "Romans 8:16",
    "NIV": "The Spirit himself testifies with our spirit that we are God's children.",
    "ESV": "The Spirit himself bears witness with our spirit that we are children of God,"
  },
  {
    "verse_num": 17,
    "Verse": "Romans 8:17",
    "NIV": "Now if we are children, then we are heirs—heirs of God and co-heirs with Christ, if indeed we share in his sufferings in order that we may also share in his glory.",
    "ESV": "and if children, then heirs—heirs of God and fellow heirs with Christ, provided we suffer with him in order that we may also be glorified with him."
  },
  {
    "verse_num": 18,
    "Verse": "Romans 8:18",
    "NIV": "I consider that our present sufferings are not worth comparing with the glory that will be revealed in us.",
    "ESV": "For I consider that the sufferings of this present time are not worth comparing with the glory that is to be revealed to us."
  },
  {
    "verse_num": 19,
    "Verse": "Romans 8:19",
    "NIV": "For the creation waits in eager expectation for the children of God to be revealed.",
    "ESV": "For the creation waits with eager longing for the revealing of the sons of God."
  },
  {
    "verse_num": 20,
    "Verse": "Romans 8:20",
    "NIV": "For the creation was subjected to frustration, not by its own choice, but by the will of the one who subjected it, in hope",
    "ESV": "For the creation was subjected to futility, not willingly, but because of him who subjected it, in hope"
  },
  {
    "verse_num": 21,
    "Verse": "Romans 8:21",
    "NIV": "that the creation itself will be liberated from its bondage to decay and brought into the freedom and glory of the children of God.",
    "ESV": "that the creation itself will be set free from its bondage to corruption and obtain the freedom of the glory of the children of God."
  },
  {
    "verse_num": 22,
    "Verse": "Romans 8:22",
    "NIV": "We know that the whole creation has been groaning as in the pains of childbirth right up to the present time.",
    "ESV": "For we know that the whole creation has been groaning together in the pains of childbirth until now."
  },
  {
    "verse_num": 23,
    "Verse": "Romans 8:23",
    "NIV": "Not only so, but we ourselves, who have the firstfruits of the Spirit, groan inwardly as we wait eagerly for our adoption to sonship, the redemption of our bodies.",
    "ESV": "And not only the creation, but we ourselves, who have the firstfruits of the Spirit, groan inwardly as we wait eagerly for adoption as sons, the redemption of our bodies."
  },
  {
    "verse_num": 24,
    "Verse": "Romans 8:24",
    "NIV": "For in this hope we were saved. But hope that is seen is no hope at all. Who hopes for what they already have?",
    "ESV": "For in this hope we were saved. Now hope that is seen is not hope. For who hopes for what he sees?"
  },
  {
    "verse_num": 25,
    "Verse": "Romans 8:25",
    "NIV": "But if we hope for what we do not yet have, we wait for it patiently.",
    "ESV": "But if we hope for what we do not see, we wait for it with patience."
  },
]

TIMEZONE = 'Australia/Perth'
VALID_VERSIONS = {"NIV", "ESV"}

tz = pytz.timezone(TIMEZONE)

app = FastAPI(title="Romans 8 Memory Verse API")

@app.get("/verse")
def get_verse(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    version: str = Query("NIV", description="Bible version: NIV or ESV"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    start_verse: int = Query(1, description="Starting verse number (1-25)")
):
    try:
        version = version.upper()
        if version not in VALID_VERSIONS:
            raise HTTPException(status_code=400, detail="Version must be 'NIV' or 'ESV'.")
        
        if not 1 <= start_verse <= 25:
            raise HTTPException(status_code=400, detail="Start verse must be between 1 and 25.")
        
        try:
            user_dt = tz.localize(datetime.strptime(date, "%Y-%m-%d"))
            start_dt = tz.localize(datetime.strptime(start_date, "%Y-%m-%d"))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        
        monday_start = start_dt - timedelta(days=start_dt.weekday())
        
        if user_dt.date() < monday_start.date():
            raise HTTPException(status_code=400, detail="Date is before memorisation start.")

        # Work out how many Mondays have passed
        weeks_since_start = (user_dt.date() - monday_start.date()).days // 7
        current_verse_num = start_verse + weeks_since_start

        # Cap at the length of ROMANS_8_VERSES
        max_verse = ROMANS_8_VERSES[-1]["verse_num"]
        current_verse_num = min(current_verse_num, max_verse)

        # Build the response
        if user_dt.weekday() == 6:  # Sunday
            # Include verses from start_verse to current
            verses = [v for v in ROMANS_8_VERSES if start_verse <= v["verse_num"] <= current_verse_num]
            reference = f"Romans 8:{start_verse}-{current_verse_num}"
            text = " ".join(v[version] for v in verses)
        else:
            verse = next(v for v in ROMANS_8_VERSES if v["verse_num"] == current_verse_num)
            reference = f"Romans 8:{current_verse_num}"
            text = verse[version]

        return JSONResponse({
            "date": date,
            "start_date": start_date,
            "start_verse": start_verse,
            "verse_reference": reference,
            "version": version,
            "text": text
        })
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) 