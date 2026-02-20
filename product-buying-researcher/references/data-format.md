# Product Data Format and Presentation

Sources: Web application data patterns, product comparison site
conventions, JSON schema design.

Specification for the product data JSON file that powers the comparison
website. Covers the schema, field descriptions, presentation workflow,
and the serve script.

---

## 1. Data File Location

Write the product data as a JSON file to a working directory. Convention:

```
/tmp/product-research/data.json
```

The serve script reads this file and combines it with the HTML template.

---

## 2. JSON Schema

```json
{
  "metadata": {
    "query": "string — the product category or search query",
    "date": "string — research date, e.g. 2025-01-15",
    "location": "string | null — user's location if provided",
    "budget": "string | null — budget range, e.g. $100-200",
    "priorities": ["string array — user's stated priorities"],
    "notes": "string | null — additional context from the conversation"
  },
  "recommendation": "string — 1-3 sentence summary recommending the top pick and why",
  "products": [
    {
      "rank": "number — position (1 = best match for user)",
      "name": "string — full product name with model number",
      "image": "string | null — URL to product image",
      "price": "string — representative price, e.g. $249",
      "priceRange": "string | null — price range across retailers, e.g. $228-$348",
      "rating": "number | null — average rating out of 5, e.g. 4.7",
      "ratingSource": "string | null — where the rating comes from, e.g. Amazon (15K reviews)",
      "highlights": "string — 1-2 sentence summary of what makes this product notable",
      "bestFor": "string | null — who this product is ideal for",
      "pros": ["string array — 3-5 key advantages"],
      "cons": ["string array — 2-4 honest drawbacks"],
      "buyLinks": [
        {
          "store": "string — retailer name",
          "url": "string — direct link to product page",
          "price": "string | null — price at this retailer"
        }
      ]
    }
  ]
}
```

---

## 3. Field Guidelines

### metadata

| Field | Required | Notes |
|-------|----------|-------|
| query | Yes | Use the user's words or a cleaned-up version. This becomes the page title |
| date | Yes | ISO date of when research was conducted |
| location | No | Only if user provided it. Affects retailer selection |
| budget | No | Include if user stated a budget. Helps contextualize the recommendation |
| priorities | No | List features the user emphasized. Shown as tags on the page |
| notes | No | Any extra context: "replacing a broken unit", "for my daughter" |

### products

Include 3-5 products. Fewer than 3 feels incomplete. More than 7 creates
decision fatigue.

| Field | Required | Notes |
|-------|----------|-------|
| rank | Yes | Sequential, 1 = best match. Rank by user fit, not "objectively best" |
| name | Yes | Full name including brand and model: "Sony WH-1000XM5" not "Sony headphones" |
| image | No | Use manufacturer or retailer product image URL. Template handles missing images gracefully |
| price | Yes | The most common or representative price |
| priceRange | No | Show if prices vary significantly across retailers |
| rating | No | Aggregate rating if available. Prefer sources with high review counts |
| ratingSource | No | Always cite where the rating comes from |
| highlights | Yes | What makes this product stand out. Focus on user-relevant strengths |
| bestFor | No | One-line descriptor of ideal buyer. Helps user self-identify |
| pros | Yes | 3-5 items. Be specific: "30-hour battery" not "good battery" |
| cons | Yes | 2-4 items. Be honest. Every product has real drawbacks |
| buyLinks | Yes | 2-4 retailers with direct links and prices. More links = more helpful |

### buyLinks

- Always include at least 2 retailers when possible
- Use direct product page URLs, not search result pages
- Include price at each retailer — users compare across stores
- If user provided location, prioritize retailers available in their region
- Order by price (lowest first) or by retailer reliability

---

## 4. Serving the Website

### File Preparation

1. Create the working directory:
   ```
   mkdir -p /tmp/product-research
   ```

2. Write the data file:
   ```
   Write product data JSON to /tmp/product-research/data.json
   ```

3. Start the server using the skill's serve script:
   ```
   python3 {skill_directory}/scripts/serve.py /tmp/product-research/data.json
   ```

The script automatically:
- Finds an available port (starting at 8432)
- Combines the HTML template with the product data
- Opens the browser
- Prints the URL to the console

### After Serving

Tell the user:
- The URL where results are available (printed by the script)
- That they can click any "buy" link to go directly to the retailer
- That they can press Ctrl+C in the terminal to stop the server
- Offer to refine the research if they want changes

---

## 5. Example Data

Minimal working example:

```json
{
  "metadata": {
    "query": "Best Wireless Earbuds for Running",
    "date": "2025-06-15",
    "budget": "$50-150",
    "priorities": ["sweat resistance", "secure fit", "battery life"]
  },
  "recommendation": "The Jabra Elite 8 Active offers the best combination of secure fit, durability, and sound quality for runners in your budget.",
  "products": [
    {
      "rank": 1,
      "name": "Jabra Elite 8 Active",
      "price": "$129",
      "rating": 4.5,
      "ratingSource": "Amazon (3,200 reviews)",
      "highlights": "IP68 rated with a wing-tip design that stays put during intense workouts.",
      "bestFor": "Serious runners who need earbuds that won't fall out",
      "pros": [
        "IP68 dust and water resistance",
        "Secure wing-tip fit",
        "8-hour battery (32 with case)",
        "Strong ANC for outdoor noise"
      ],
      "cons": [
        "Bass can be overpowering on default EQ",
        "Touch controls take practice",
        "Case is bulky"
      ],
      "buyLinks": [
        {"store": "Amazon", "url": "https://amazon.com/dp/example", "price": "$129"},
        {"store": "Best Buy", "url": "https://bestbuy.com/example", "price": "$129"}
      ]
    }
  ]
}
```

---

## 6. Common Issues

| Problem | Fix |
|---------|-----|
| Images not loading | Image URLs must be full HTTPS URLs. Check they're not behind auth |
| Missing product data | Ensure required fields (name, rank, price, pros, cons, buyLinks) are present |
| Server won't start | Check if another process is using the port. Script tries 50 ports |
| Page shows "No products found" | Verify data.json is valid JSON and has a non-empty products array |
| Buy links go to wrong page | Use direct product page URLs, not retailer homepage or search pages |
