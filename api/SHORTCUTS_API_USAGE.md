# Using the Romans 8 Memory Verse API with Apple Shortcuts

This guide explains how to use your deployed API with Apple Shortcuts for easy Bible verse retrieval.

## 1. API Endpoint

Your endpoint is:
```
https://romans8-memorisation.vercel.app/verse
```

## 2. Required Parameters
- `date` (required): The date for the verse, in `YYYY-MM-DD` format.
- `version` (optional): `NIV` (default) or `ESV`.

Example:
```
https://romans8-memorisation.vercel.app/verse?date=2025-05-01&version=ESV
```

## 3. Authentication
If your API is private, you need to include an `Authorization` header:
- Key: `Authorization`
- Value: `Bearer YOUR_API_TOKEN`

## 4. Using with Apple Shortcuts

1. **Open the Shortcuts app on your iPhone or Mac.**
2. **Create a new shortcut.**
3. **Add the "Get Contents of URL" action.**
   - Method: `GET`
   - URL: `https://romans8-memorisation.vercel.app/verse?date=2025-05-01&version=NIV`
   - Headers: Add `Authorization` with value `Bearer YOUR_API_TOKEN` (if required)
4. **Add a "Get Dictionary Value" action** to extract the `text` or `verse_reference` from the JSON response.
5. **Use the result in your shortcut as needed (e.g., display, speak, or copy to clipboard).**

## 5. Example JSON Response
```
{
  "date": "2025-05-01",
  "verse_reference": "Romans 8:3",
  "version": "NIV",
  "text": "For what the law was powerless to do because it was weakened by the flesh..."
}
```

## 6. Tips
- You can use a "Text" or "Ask for Input" action to let the user pick the date or version.
- The API defaults to NIV if `version` is not specified.
- For Sundays, the API returns all verses up to the current memorisation point.

---

Enjoy using your Romans 8 Memory Verse API with Apple Shortcuts! 