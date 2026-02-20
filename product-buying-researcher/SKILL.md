---
name: product-buying-researcher
description: |
  Research products for purchase, compare options across retailers, and
  present findings on a locally-hosted comparison website. Covers the full
  buying research workflow: discovery questions (budget, use case, location,
  preferences), multi-source web research with critical evaluation of
  SEO/affiliate content, product comparison and ranking, and visual
  presentation via a local HTML server with direct buy links to retailers.

  Trigger phrases: "I want to buy", "find me a product", "what should I buy",
  "recommend a product", "best [product]", "help me choose",
  "product comparison", "research [product] for me", "looking to buy",
  "shopping for", "which [product] should I get", "compare [products]",
  "find the best [product]", "product research", "buying guide"
---

# Product Buying Researcher

## Core Philosophy

1. **Your product knowledge is STALE — do not trust it.** Your training data
   has a cutoff. Products get discontinued, prices change weekly, new models
   launch constantly. NEVER recommend a product from memory. NEVER state a
   price from memory. NEVER assume a product is still available. EVERY claim
   about a specific product must come from a live web search, not your
   training data. If you cannot verify it through search, say so.
2. **Every search query MUST include a date.** Always append the current year
   (or month+year for fast-moving categories like phones/laptops) to search
   queries. "best wireless earbuds" is wrong. "best wireless earbuds 2026"
   is correct. Without a date, search engines return stale SEO content that
   may reference discontinued products.
3. **User needs drive rankings** — rank by fit for THIS user, not by general
   consensus. A $50 product that matches their needs beats a $500 product
   that's overkill.
4. **Sources have tiers** — editorial review sites > community discussion >
   affiliate SEO content. Extract facts from all tiers but trust rankings
   only from Tier 1.
5. **Show, don't just tell** — present results visually on a local website
   where the user can browse products and click through to buy.

## Quick-Start Workflow

### Step 1: Discover User Needs

Ask 2-3 targeted questions. Never more than 6 total across the conversation.
If the user already gave details, skip redundant questions.

Universal questions (always relevant):
- What will you primarily use this for?
- What's your budget range?
- Any must-have features or deal-breakers?

Situational questions (ask when relevant):
- Where are you located? (for shipping/availability/pricing)
- What are you currently using and what's wrong with it?
- What ecosystem are you in? (Apple/Android, smart home platform, etc.)

→ See `references/research-methodology.md` § Discovery Questions

### Step 2: Research Products

Follow this sequence using web search tools:

1. **Broad survey** — "best [category] [year]" on editorial review sites
   (Wirecutter, RTINGS, Consumer Reports, Tom's Guide). Identify 5-8 contenders.
2. **Spec collection** — manufacturer pages for each contender
3. **Expert reviews** — individual reviews for top 3-4 candidates
4. **Community validation** — Reddit, forums for ownership experiences
5. **Price comparison** — 3+ retailers for current pricing in user's region

→ See `references/research-methodology.md` § Where to Search, § Search Strategies

### Step 3: Evaluate Sources Critically

- **Affiliate "best of" blogs**: extract spec tables, ignore rankings
- **"X vs Y" articles**: use for side-by-side specs, not conclusions
- **Reddit**: real experiences but biased toward complaints
- **YouTube**: check for sponsorship disclosures in descriptions

→ See `references/research-methodology.md` § Evaluating Affiliate Content

### Step 4: Rank and Recommend

Rank 3-5 products by user fit. Include pros, cons, and buy links for each.

| Factor | Weight |
|--------|--------|
| Matches primary use case | Highest |
| Within budget | Hard requirement |
| Meets must-have features | Hard requirement |
| Expert consensus | High |
| Community satisfaction | Medium |
| Value for money | Medium |

### Step 5: Present on Local Website

1. Create directory: `mkdir -p /tmp/product-research`
2. Write product data JSON to `/tmp/product-research/data.json`
   → See `references/data-format.md` for schema and field guide
3. Start the server:
   ```
   python3 {this_skill_directory}/scripts/serve.py /tmp/product-research/data.json
   ```
4. Browser opens automatically with the comparison page
5. Tell user they can click buy links to visit retailers directly

### Step 6: Iterate

After presenting results, ask if the user wants to adjust:
- Different price range or priorities
- More products or deeper research on a specific one
- Different retailers or regions

If they request changes, update `data.json` and restart the server.

## Decision Trees

### How Many Questions to Ask

| User Input | Action |
|-----------|--------|
| Category only: "I need headphones" | Ask use case + budget |
| Category + use case: "headphones for running" | Ask budget + deal-breakers |
| Full context: "noise-cancelling headphones under $200 for commuting" | Start research immediately |
| Gift: "present for my dad" | Ask recipient interests + budget |

### Research Source Selection by Category

| Category | Go-To Sources | Watch For |
|----------|--------------|-----------|
| Electronics | RTINGS, Wirecutter, YouTube | Release dates, battery life claims |
| Home & Kitchen | Wirecutter, r/BuyItForLife | Warranty terms, durability |
| Software | G2, Capterra, free trials | Pricing changes, vendor lock-in |
| Fitness & Health | Certified testing, medical sources | Unverified health claims |
| Fashion | User reviews, YouTube try-ons | Sizing variance, return policies |

### Confidence Communication

| Confidence | Condition | What to Tell User |
|-----------|-----------|-------------------|
| High | 3+ expert sources agree | Recommend confidently |
| Medium | Mixed reviews or limited data | Recommend but note uncertainty |
| Low | Niche product, few reviews | State it's based on specs only, suggest waiting |

## Reference Files

| File | Contents |
|------|----------|
| `references/research-methodology.md` | Question frameworks, source tier system (Tier 1-3), critical evaluation of affiliate/SEO content with red flags table, search query patterns, location-aware retailer selection, ranking criteria, category-specific tips |
| `references/data-format.md` | Product data JSON schema, field requirements and guidelines, serve script usage, example data, troubleshooting |
