# Writesonic Affiliate — 30-Day Task Board

> Parsed from: `playbook.md`
> Strategy: Reddit organic + TikTok short-form → Writesonic affiliate signups (30% lifetime recurring)
> Sprint length: 7 days | Total sprints: 4

**Status legend:** `[ ]` To Do · `[~]` In Progress · `[x]` Done · `[!]` Blocked

---

## Sprint 1 — Foundation (Days 1–7)

> **Sprint goal:** Infrastructure live, first research pass complete, first TikTok video published.
> **Acceptance criteria:** Affiliate dashboard active with UTM links, tracking spreadsheet set up, reddit thread list in hand, Hook #3 posted to TikTok.

---

### WS-001 · Sign up for Writesonic affiliate program
- **Owner:** Human (account action)
- **Day:** 1
- **Status:** `[ ]`
- **Details:**
  - Go to writesonic.com → Affiliate Program
  - Confirm commission: 30% lifetime recurring (no 12-month cap)
  - Save dashboard login credentials
- **Blocker if skipped:** All downstream tracking tasks are blocked until affiliate account exists.

---

### WS-002 · Create UTM-tagged tracking links
- **Owner:** Human
- **Day:** 1
- **Status:** `[ ]`
- **Depends on:** WS-001
- **UTM naming convention:**

  | Parameter | Answers | Rule |
  |---|---|---|
  | `utm_source` | *Where* is traffic from? | Platform name (`reddit`, `tiktok`, `hub`) |
  | `utm_medium` | *How* was the link surfaced? | Mechanism (`comment`, `bio-link`, `cta-button`) |
  | `utm_campaign` | *Which campaign?* | Always `jasper-alternative` — identical across all channels for cross-channel roll-up |
  | `utm_content` | *Which specific piece?* | Subreddit name, hook slug, or hub section |

- **Details:** Create one unique affiliate link per traffic source using UTM parameters:

  **Reddit**

  | Link alias | UTM string |
  |---|---|
  | reddit-sidehustle | `utm_source=reddit&utm_medium=comment&utm_campaign=jasper-alternative&utm_content=sidehustle` |
  | reddit-blogging | `utm_source=reddit&utm_medium=comment&utm_campaign=jasper-alternative&utm_content=blogging` |
  | reddit-entrepreneur | `utm_source=reddit&utm_medium=comment&utm_campaign=jasper-alternative&utm_content=entrepreneur` |
  | reddit-seo | `utm_source=reddit&utm_medium=comment&utm_campaign=jasper-alternative&utm_content=seo` |
  | reddit-digitalmarketing | `utm_source=reddit&utm_medium=comment&utm_campaign=jasper-alternative&utm_content=digitalmarketing` |

  **TikTok** — hook identity moves to `utm_content`; `utm_campaign` stays consistent so all TikTok rolls up alongside Reddit.

  | Link alias | UTM string |
  |---|---|
  | tiktok-hook1 | `utm_source=tiktok&utm_medium=bio-link&utm_campaign=jasper-alternative&utm_content=hook1-income-loss` |
  | tiktok-hook2 | `utm_source=tiktok&utm_medium=bio-link&utm_campaign=jasper-alternative&utm_content=hook2-pattern-interrupt` |
  | tiktok-hook3 | `utm_source=tiktok&utm_medium=bio-link&utm_campaign=jasper-alternative&utm_content=hook3-personal-narrative` |
  | tiktok-hook4 | `utm_source=tiktok&utm_medium=bio-link&utm_campaign=jasper-alternative&utm_content=hook4-educational` |
  | tiktok-hook5 | `utm_source=tiktok&utm_medium=bio-link&utm_campaign=jasper-alternative&utm_content=hook5-comparison` |

  **Hub page (writeaudit.com)** — place on each CTA button so you can see which section converts.

  | Link alias | UTM string |
  |---|---|
  | hub-hero-cta | `utm_source=hub&utm_medium=cta-button&utm_campaign=jasper-alternative&utm_content=hero` |
  | hub-comparison-table | `utm_source=hub&utm_medium=cta-button&utm_campaign=jasper-alternative&utm_content=comparison-table` |
  | hub-bottom-cta | `utm_source=hub&utm_medium=cta-button&utm_campaign=jasper-alternative&utm_content=bottom` |

- **Output:** Save all links in a password manager or Notion doc. Never post raw affiliate URLs in Reddit comments — always route through writeaudit.com. Hub page links are the exception — those live on the hub itself.

---

### WS-003 · Build comparison/review hub page
- **Owner:** Human + @content-creator (assist)
- **Day:** 1–2
- **Status:** `[ ]`
- **Depends on:** WS-002
- **Details:**
  - Create a dedicated page on your blog or a public Notion page
  - This page is the only place affiliate links live — Reddit comments and TikTok bio all point here
  - Minimum content for launch: headline, 3 bullet points on Writesonic vs. Jasper, affiliate link button, FTC disclosure (use Option A from `playbook.md` Section 9)
  - Full comparison post gets added in Sprint 2 (WS-010)
- **@content-creator prompt (optional, to generate initial copy):**
  ```
  Write a 300-word intro section for a comparison page:
  "Writesonic vs. Jasper AI in 2025 — My Honest Take After Switching"
  Tone: honest, not hypey. Acknowledge Jasper closed its affiliate program Jan 2025.
  End with a CTA button placeholder: [Try Writesonic — 30% recurring affiliate commission]
  Include FTC disclosure: "I earn a commission if you sign up through my link."
  ```
- **Output:** https://writeaudit.com — hub page is live. Update TikTok bio with this URL.

---

### WS-004 · Set up tracking spreadsheet
- **Owner:** Human
- **Day:** 2
- **Status:** `[ ]`
- **Details:** Create a Google Sheet or Notion table with the following columns:

  ```
  Date | Platform | Thread/Video title | Subreddit/Handle | UTM tag used |
  Clicks (weekly pull) | Signups (weekly pull) | Karma earned | Mod removed? | Notes
  ```

- **Cadence:** Update every Sunday by pulling affiliate dashboard + Reddit karma history.

---

### WS-005 · Keyword research pass
- **Owner:** @trend-researcher
- **Day:** 3
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Research current search trends for the following keywords:
  1. "jasper alternative 2025"
  2. "writesonic review 2025"
  3. "best AI writing affiliate program 2025"
  4. "writesonic vs jasper"
  5. Any emerging comparison or alternative-seeking keywords in the AI writing tool space

  For each keyword provide:
  - Estimated monthly search volume
  - Trend direction (rising / stable / falling)
  - Ranking difficulty (low / medium / high)
  - Top 3 currently ranking URLs
  - Content gap opportunity (what the top results are missing)

  Priority output: ranked list of which keyword to target first with the comparison blog post.
  ```
- **Expected output:** Keyword priority list → feeds directly into WS-010 (comparison post brief).
- **Output destination:** Paste results as a comment in this ticket or save to `research/keywords.md`.

---

### WS-006 · Reddit thread discovery — initial pass
- **Owner:** @reddit-community-builder
- **Day:** 3–4
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Find currently active Reddit threads where users are discussing:
  1. The Jasper AI affiliate program closure (closed January 26, 2025)
  2. Alternatives to Jasper AI for affiliate income
  3. Writesonic as an affiliate program or writing tool

  Target subreddits: r/entrepreneur, r/SEO, r/sidehustle, r/blogging,
  r/artificial, r/digital_marketing

  Use these search operators to find live threads:
    site:reddit.com "jasper" "affiliate" "closed" after:2025-01-01
    site:reddit.com "writesonic" OR "write sonic" "jasper" affiliate 2025
    site:reddit.com r/sidehustle "AI affiliate" 2025
    site:reddit.com r/blogging "jasper" "alternative" 2025
    site:reddit.com r/entrepreneur "jasper affiliate"
    site:reddit.com r/SEO "jasper" "affiliate" OR "alternative"
    site:reddit.com r/digital_marketing "jasper" 2025

  For each thread found, provide:
  - Thread title and URL
  - Subreddit
  - Approximate comment count
  - Activity level (hot / warm / dormant)
  - Best engagement opportunity
  - Which response template to use (Template 1, 2, or 3 from playbook.md Section 7)
  - Audience receptivity score (1–10)

  Sort results by receptivity score descending.
  ```
- **Expected output:** Prioritized list of ≥5 live threads with engagement recommendations.
- **Output destination:** Paste into `research/reddit-threads.md` (create if needed).

---

### WS-007 · Reddit account karma warm-up — begin
- **Owner:** Human
- **Day:** 4–7
- **Status:** `[ ]`
- **Depends on:** WS-006 (to know which subreddits to warm up in)
- **Details:**
  - Post 2–3 genuine, non-affiliate replies per day in r/blogging and r/sidehustle on non-Writesonic topics
  - Goal: reach ≥50 karma in each target subreddit before Sprint 3 posting begins
  - Do NOT mention Writesonic, affiliate programs, or Jasper during warm-up
- **Why this matters:** Reddit spam filters and mods scrutinize accounts with low karma heavily. Warm-up dramatically reduces removal risk in Sprint 3.

---

### WS-008 · TikTok Hook #3 — Personal Narrative (record + publish)
- **Owner:** Human + @tiktok-strategist
- **Day:** 5–7
- **Status:** `[ ]`
- **Agent prompt (pre-production):**
  ```
  Finalize and expand the following TikTok script for Hook #3 (Personal Narrative):

  Current draft:
  "I got ghosted by Jasper. Three years of content, gone. So I spent two months
  testing every AI writing tool with a real affiliate program. Here's the one I
  actually kept."

  Expand to a full 45–60 second script with:
  - Beat-by-beat pacing notes
  - On-screen text overlays for each beat
  - B-roll or visual suggestions
  - Verbal FTC disclosure placement (should feel natural, not tacked on)
  - Closing CTA directing to bio link
  - Posting time recommendation (day of week + hour)
  - First-48-hour engagement strategy (how to respond to early comments)
  ```
- **Script (from playbook.md):**
  > *[No text overlay — direct to camera, casual tone]*
  > "I got ghosted by Jasper. Three years of content, gone. So I spent two months testing every AI writing tool with a real affiliate program. Here's the one I actually kept."
  > **Psychology:** Authenticity signal. "Two months of testing" implies rigor, not impulse.
  > **Hashtags:** `#writesonic #aiwriting #affiliatemarketing #sidehustle #contentcreator`
- **Publish checklist:**
  - [ ] Bio link updated to https://writeaudit.com (from WS-003)
  - [ ] UTM link used: `tiktok-hook3`
  - [ ] FTC disclosure included verbally and as `#ad` in caption
  - [ ] Posted at recommended time
- **Output:** TikTok URL. Log in tracking spreadsheet (WS-004).

---

### Sprint 1 Exit Criteria

| Criteria | Owner | Done? |
|---|---|---|
| Affiliate account active, dashboard accessible | Human | `[ ]` |
| All 10 UTM links created | Human | `[ ]` |
| Hub page live with FTC disclosure | Human | `[ ]` |
| Tracking spreadsheet set up | Human | `[ ]` |
| Keyword research complete | @trend-researcher | `[ ]` |
| Reddit thread list ≥5 threads | @reddit-community-builder | `[ ]` |
| Karma warm-up started | Human | `[ ]` |
| Hook #3 TikTok published | Human | `[ ]` |

---

## Sprint 2 — Content Production (Days 8–14)

> **Sprint goal:** Two blog posts published, three TikTok videos live, Reddit lurk phase complete.
> **Acceptance criteria:** Money page (comparison post) indexed by Google, 3 TikToks published with engagement data starting to accumulate, 5 target Reddit threads identified and ready for Sprint 3 replies.

---

### WS-009 · Brief and draft comparison post
- **Owner:** @content-creator
- **Day:** 8–9
- **Status:** `[ ]`
- **Depends on:** WS-005 (keyword priority from @trend-researcher)
- **Agent prompt:**
  ```
  Write a long-form SEO blog post targeting the keyword "jasper alternative 2025".

  Title: "Writesonic vs. Jasper AI in 2025 — Which Is Worth It Now That Jasper
  Dropped Their Affiliate Program?"

  Target audience: Affiliate marketers and content creators who were earning from
  Jasper and are actively searching for a replacement.

  Tone: Honest, direct, not hypey. Acknowledge Writesonic's weaknesses.
  Length: 1,800–2,400 words.

  Required sections:
  1. What happened to Jasper's affiliate program (factual, 150 words)
  2. Writesonic product overview (strengths + weaknesses, 300 words)
  3. Feature comparison table: Writesonic vs. Jasper (SEO tools, long-form,
     templates, brand voice, integrations)
  4. Affiliate program comparison table: commission %, structure, payout timeline,
     stability indicators
  5. Who Writesonic is best for
  6. Who Writesonic is NOT for (be honest — this builds trust)
  7. Verdict + CTA with affiliate disclosure

  Writesonic facts to include:
  - Strengths: SEO content, GEO (AI-search optimization for ChatGPT/Perplexity),
    Chatsonic, brand voice tools, 30% lifetime recurring affiliate commission
  - Weaknesses: long-form creative/narrative writing not strongest; no native
    Surfer SEO integration depth

  Jasper facts:
  - Closed affiliate program January 26, 2025; final payout April 15, 2025
  - Replaced with enterprise-only "Solutions Partner" program
  - History: 30% lifetime → 25% for 12 months → closed entirely

  FTC disclosure (include at top AND near CTA):
  "I earn a commission if you sign up through my link. All opinions are my own."
  ```
- **Output:** Full draft → human edits → publish. Save URL and submit to Google Search Console.

---

### WS-010 · SEO audit of comparison post
- **Owner:** @seo-specialist
- **Day:** 10
- **Status:** `[ ]`
- **Depends on:** WS-009 (published post URL)
- **Agent prompt:**
  ```
  Audit the following blog post for on-page SEO targeting "jasper alternative 2025":
  [paste post URL]

  Review and provide specific recommendations for:
  - Title tag and meta description
  - H1/H2/H3 structure
  - Keyword placement (primary + secondary)
  - Internal linking opportunities
  - Image alt text
  - Schema markup (Article or Review schema)
  - Mobile readability
  - Page speed flags (images, render-blocking scripts)

  Also identify 3 secondary keywords this page should co-target, based on
  current SERP landscape for AI writing tool comparison searches.
  ```
- **Output:** Implement fixes before the end of Day 10. Log secondary keywords into tracking sheet.

---

### WS-011 · Brief and draft "Best AI Writing Affiliate Programs 2025" post
- **Owner:** @content-creator
- **Day:** 10–11
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Write a long-form SEO blog post targeting "best AI writing affiliate program 2025".

  Title: "Best AI Writing Affiliate Programs in 2025 (Post-Jasper Edition)"

  Audience: Affiliate marketers evaluating which AI writing tool to promote after
  Jasper closed its individual affiliate program in January 2025.

  Tone: Honest comparison. Writesonic ranked #1 with clear reasoning.
  Acknowledge other options honestly — this signals credibility.
  Length: 1,500–2,000 words.

  Required sections:
  1. What changed in 2025 (Jasper context, market shift, 150 words)
  2. What to look for in a stable AI affiliate program (evaluation framework)
  3. Ranked list of top programs (Writesonic #1, then Copy.ai, Rytr — honest
     1-paragraph assessment of each including weaknesses)
  4. Writesonic deep-dive: why it ranks #1 (commission structure, product quality,
     company stability signals)
  5. Programs to avoid / watch with caution (enterprise-pivot warning signs)
  6. Final recommendation + CTA

  FTC disclosure at top: "Some links in this post are affiliate links. I earn
  a commission if you sign up — at no cost to you."
  ```
- **Output:** Full draft → publish. Submit URL to Google Search Console.

---

### WS-012 · TikTok Hook #1 — Income Loss Story (record + publish)
- **Owner:** Human + @tiktok-strategist
- **Day:** 10
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Finalize Hook #1 (Income Loss Story) as a full 45–60 second TikTok script.

  Current draft hook:
  On screen: "$800/month → $0 in 30 days"
  "Jasper AI just deleted their affiliate program with 30 days notice. Here's what
  I'm replacing it with and why — and what to check before you promote any AI tool again."

  Expand with:
  - Full beat-by-beat script
  - On-screen text for each beat
  - Visual/B-roll suggestions (dashboard screenshot, income graph, etc.)
  - Natural FTC disclosure
  - CTA to bio link
  - Hashtag set: #jasperal #aiaffiliate #affiliatemarketing #writesonic #passiveincome
  - Posting time recommendation
  ```
- **UTM link to use:** `tiktok-hook1`
- **Publish checklist:**
  - [ ] FTC disclosure verbal + `#ad` in caption
  - [ ] Bio link = https://writeaudit.com

---

### WS-013 · TikTok Hook #4 — Educational (record + publish)
- **Owner:** Human + @tiktok-strategist
- **Day:** 14
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Finalize Hook #4 (Educational / Framework) as a full 45–60 second TikTok script.

  Current draft hook:
  On screen: "3 questions before promoting any AI affiliate"
  "After Jasper, I made a checklist. Question 1: Is the company still selling to
  individuals, or pivoting to enterprise? Question 2: Can the commission structure
  survive their unit economics? Question 3: Would I pay for this myself?
  Writesonic passes all three — here's why."

  Expand with full script, overlays, B-roll notes, FTC disclosure, CTA.
  Hashtags: #affiliatetips #aitools #writesonic #makemoneyonline #blogging
  ```
- **UTM link to use:** `tiktok-hook4`
- **Note:** This hook targets saves and shares (educational content). Track saves metric specifically — high saves = strong signal to scale this angle.

---

### WS-014 · TikTok comment engagement — Hooks #3 and #1
- **Owner:** Human (+ @tiktok-strategist for guidance)
- **Day:** 8–14 (ongoing after each publish)
- **Status:** `[ ]`
- **Details:**
  - Reply to every comment within 24 hours of posting
  - Pin the comment that asks the most genuine product question
  - Never reply with a direct affiliate link — always say "link in bio"
  - If asked "is this sponsored?": *"I'm an affiliate — I earn a commission if you sign up. Happy to answer product questions honestly."*
- **@tiktok-strategist prompt (if engagement stalls):**
  ```
  TikTok Hook #[X] has [N] views but low comment engagement after 48 hours.
  Current caption: [paste caption]
  Hashtags used: [paste hashtags]
  Suggest: 3 comment-prompt strategies, 1 caption revision, and whether to
  boost with a Duet or Stitch response video.
  ```

---

### WS-015 · Reddit lurk phase — identify top 5 target threads
- **Owner:** Human (using output from WS-006)
- **Day:** 8–14
- **Status:** `[ ]`
- **Depends on:** WS-006
- **Details:**
  - Using the thread list from @reddit-community-builder, select the top 5 threads to engage in Sprint 3
  - Lurk each thread: read all comments, note what tone gets upvoted, note mod behavior
  - Do NOT post any affiliate-related replies yet
  - Note: which template (1, 2, or 3) fits each thread
- **Output:** Fill in the table below and save to `research/reddit-threads.md`:

  | Thread URL | Subreddit | Comment count | Best template | Receptivity | Target reply day |
  |---|---|---|---|---|---|
  | | | | | | |

---

### WS-016 · Reddit karma warm-up — continue
- **Owner:** Human
- **Day:** 8–14 (daily)
- **Status:** `[ ]`
- **Details:**
  - 2–3 genuine replies per day in r/blogging and r/sidehustle (non-affiliate topics)
  - Target: ≥100 karma across target subreddits before Sprint 3 Day 15

---

### Sprint 2 Exit Criteria

| Criteria | Owner | Done? |
|---|---|---|
| Comparison post published + SEO audited | @content-creator + @seo-specialist | `[ ]` |
| "Best AI affiliate programs" post published | @content-creator | `[ ]` |
| 3 TikTok videos published (Hook #3, #1, #4) | Human + @tiktok-strategist | `[ ]` |
| 5 Reddit threads identified and lurked | Human | `[ ]` |
| Reddit karma ≥100 in target subs | Human | `[ ]` |
| Both post URLs submitted to Search Console | Human | `[ ]` |

---

## Sprint 3 — Community Engagement (Days 15–21)

> **Sprint goal:** First Reddit replies live in low-risk subreddits. TikTok engagement loop running. Existing Jasper content updated.
> **Acceptance criteria:** ≥4 Reddit replies posted across r/blogging and r/sidehustle with positive karma, Hook #2 published, existing site content updated with pivot angle.

---

### WS-017 · Reddit engagement — r/blogging (first replies)
- **Owner:** Human (using templates from playbook.md Section 7)
- **Day:** 15–17
- **Status:** `[ ]`
- **Depends on:** WS-015 (thread selection), WS-016 (karma warm-up)
- **Rules (non-negotiable):**
  - Maximum 2 Reddit replies per day across ALL subreddits
  - No more than 1 reply per thread
  - Never post in the same subreddit more than once every 3 days
  - Always use Template 1 (Practical Recovery Reply) for r/blogging
  - Always disclose affiliate status
  - Never post raw affiliate link — link to hub page only
- **Template to use:** Template 1 from playbook.md Section 7
- **UTM link:** `reddit-blogging`
- **Log each reply in tracking spreadsheet (WS-004)**

---

### WS-018 · Reddit engagement — r/sidehustle (first replies)
- **Owner:** Human
- **Day:** 16–19
- **Status:** `[ ]`
- **Depends on:** WS-015, WS-016
- **Rules:** Same as WS-017
- **Template to use:** Template 1 (personal income recovery angle fits this subreddit best)
- **UTM link:** `reddit-sidehustle`
- **Log each reply in tracking spreadsheet**

---

### WS-019 · Reddit thread discovery — second pass
- **Owner:** @reddit-community-builder
- **Day:** 15
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Run a second Reddit thread discovery pass. It has been ~2 weeks since the initial
  search. Find newly posted threads (past 14 days) in:
  r/entrepreneur, r/SEO, r/sidehustle, r/blogging, r/artificial, r/digital_marketing

  Focus on threads posted after [insert Sprint 1 start date].
  Use same search operators as initial pass plus:
    site:reddit.com "writesonic" 2025
    site:reddit.com "AI affiliate" "2025" after:2025-02-01

  Deliverable: List of new threads not in the original discovery list,
  sorted by receptivity and activity level.
  ```
- **Output:** Add new threads to `research/reddit-threads.md`.

---

### WS-020 · Update existing Jasper content on site
- **Owner:** Human + @content-creator (assist) + @seo-specialist (audit)
- **Day:** 15–17
- **Status:** `[ ]`
- **Details:**
  - Find any existing blog posts, YouTube descriptions, or Notion pages that mention Jasper
  - Update titles to reference the closure (e.g., add "— [Updated: Jasper Closed in 2025]")
  - Update first paragraph to acknowledge Jasper's program closure
  - Add internal link to new comparison post (WS-009)
  - These pages now rank for "Jasper alternative" searches — this is a traffic recovery move
- **@content-creator prompt (for rewrite assist):**
  ```
  Rewrite the intro paragraph of this existing blog post to acknowledge that
  Jasper closed its affiliate program in January 2025 and transition to positioning
  this post as an updated guide to alternatives:
  [paste existing intro]
  Keep the same tone. Add a sentence linking to: [comparison post URL from WS-009]
  ```
- **@seo-specialist prompt (after updates):**
  ```
  The following pages have been updated with new content about Jasper's closure
  and now link to our Writesonic comparison post. Confirm:
  1. The new internal links are crawlable
  2. The updated titles are within recommended length
  3. Submit updated URLs to Search Console for re-indexing
  URLs: [list updated page URLs]
  ```

---

### WS-021 · TikTok Hook #2 — Pattern Interrupt (record + publish)
- **Owner:** Human + @tiktok-strategist
- **Day:** 17
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Finalize Hook #2 (Pattern Interrupt / Provocative) as a full 45–60 second script.

  Current draft:
  On screen: "This AI company lied to their affiliates"
  "Not clickbait. Jasper literally had 'lifetime commissions' in their program terms.
  Then: 25% cap. Then: 12 months only. Then: closed entirely. Here's how to vet a
  program so this doesn't happen to you."

  This hook should generate the highest reach of all five. Expand with:
  - Beat script with text overlays
  - Documentation suggestions (show screenshots of Jasper's old terms)
  - Natural pivot to Writesonic as the vetted alternative
  - FTC disclosure
  - CTA
  - Hashtags: #affiliatetips #jasperal #aitools #makemoneyonline #contentcreator
  - Strategy for handling negative/skeptical comments (they increase reach — engage, don't delete)
  ```
- **UTM link:** `tiktok-hook2`
- **Note:** This is the controversy hook. Negative comments are algorithmically good. Respond to all skeptical comments directly and honestly.

---

### WS-022 · Mid-campaign cross-channel alignment check
- **Owner:** @social-media-strategist
- **Day:** 18
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Review the current state of a Writesonic affiliate campaign at the midpoint (Day 18 of 30):

  Active content:
  - TikTok: 4 videos published (Hook #3, #1, #4, #2)
  - Reddit: Replies active in r/blogging and r/sidehustle (low-risk phase)
  - Blog: 2 posts published — "Writesonic vs. Jasper 2025" and "Best AI Affiliate 2025"
  - Bio link: Hub page routing all traffic

  Identify:
  1. Content gaps (angles not yet covered across any channel)
  2. Cross-promotion opportunities (e.g., Reddit replies that could reference a TikTok,
     TikTok videos that could reference the blog post)
  3. Any channel conflicts or overlaps creating redundancy
  4. Recommended priority for Sprint 4 content based on mid-campaign signals

  Output: Prioritized action list for Days 22–30.
  ```

---

### Sprint 3 Exit Criteria

| Criteria | Owner | Done? |
|---|---|---|
| ≥4 Reddit replies posted in r/blogging + r/sidehustle | Human | `[ ]` |
| No replies removed by mods | Human | `[ ]` |
| Hook #2 published on TikTok | Human + @tiktok-strategist | `[ ]` |
| Existing Jasper content updated + re-indexed | Human + @content-creator | `[ ]` |
| New Reddit thread list from second discovery pass | @reddit-community-builder | `[ ]` |
| Cross-channel alignment review complete | @social-media-strategist | `[ ]` |

---

## Sprint 4 — Scale & Optimize (Days 22–30)

> **Sprint goal:** Scale the highest-performing channel, expand Reddit to medium-risk subreddits, complete 30-day performance report.
> **Acceptance criteria:** Hook #5 published, replies active in r/entrepreneur and r/digital_marketing, full analytics report generated, Month 2 plan drafted.

---

### WS-023 · Pull Week 2–3 analytics — first data review
- **Owner:** @analytics-reporter
- **Day:** 22
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Generate a mid-campaign performance report for a Writesonic affiliate campaign
  (Days 1–21 of a 30-day sprint).

  Data to analyze (human will paste in):
  1. Affiliate dashboard UTM breakdown: clicks and signups per source
     (reddit-sidehustle, reddit-blogging, tiktok-hook1, tiktok-hook3, tiktok-hook4, etc.)
  2. TikTok analytics per video: views, average watch time %, click-through rate to bio
  3. Reddit: karma earned per reply, upvote rate, any replies removed by mods
  4. Blog: Google Search Console impressions and clicks for both posts

  Deliverable:
  - Top performing channel by clicks
  - Top performing channel by signups (if any)
  - Best TikTok hook by watch-time and CTR
  - Reddit reply with highest karma
  - Cost-per-acquisition estimate by channel (time invested vs. signups)
  - Recommended allocation shift for Days 22–30
  - Red flags to address immediately
  ```
- **Output:** Share summary in `reports/week3-analytics.md` (create if needed).

---

### WS-024 · Reddit engagement — r/entrepreneur (medium-risk, Template 1 or 3)
- **Owner:** Human
- **Day:** 22–26
- **Status:** `[ ]`
- **Depends on:** WS-017/018 (≥10 successful replies in low-risk subs with positive karma)
- **Rules:**
  - Only graduate to r/entrepreneur if ≥10 prior replies with net positive karma
  - Use Template 1 for income-recovery threads, Template 3 for megathreads/comparison threads
  - Maximum 1 reply per thread, 1 reply per 3 days in this subreddit
- **UTM link:** `reddit-entrepreneur`

---

### WS-025 · Reddit engagement — r/digital_marketing (medium-risk, Template 3)
- **Owner:** Human
- **Day:** 23–27
- **Status:** `[ ]`
- **Depends on:** WS-024 (same graduation criteria)
- **Template:** Template 3 (Community Resource Reply) — position Writesonic as one of several options, not the only recommendation
- **UTM link:** `reddit-digitalmarketing`

---

### WS-026 · TikTok Hook #5 — Comparison / Conversion (record + publish)
- **Owner:** Human + @tiktok-strategist
- **Day:** 25
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Finalize Hook #5 (Comparison / Highest Click Intent) as a full 45–60 second script.

  Current draft:
  Visual: Split screen — Jasper logo crossed out / Writesonic logo
  "Jasper vs. Writesonic in 2025. One of these has a dead affiliate program.
  One pays 30% lifetime recurring. I'll show you the actual dashboard."

  This is the conversion-focused hook — designed to drive bio link clicks.
  Expand with:
  - Full script with dashboard screen-recording instructions
  - Commission comparison visual (text overlay showing Jasper 0% vs Writesonic 30%)
  - Strong CTA: "Link in bio — I break down the full program"
  - FTC disclosure (verbal + caption)
  - Hashtags: #writesonic #jasperal #aiwriting #affiliateincome #contenttools
  - A/B suggestion: test two different CTAs (one curiosity-based, one direct)
  ```
- **UTM link:** `tiktok-hook5`

---

### WS-027 · Scale highest-performing TikTok hook
- **Owner:** Human + @tiktok-strategist
- **Day:** 23–28
- **Status:** `[ ]`
- **Depends on:** WS-023 (analytics report identifying top hook)
- **Agent prompt:**
  ```
  TikTok Hook #[X from analytics] has the highest performance metrics:
  - Views: [N]
  - Watch time: [%]
  - Bio link CTR: [%]

  Create 2 variation scripts based on the same hook angle (same psychology,
  different opening line and visual treatment). Goal: test if the angle scales
  or if the original was a one-time spike.

  Also suggest: best time to post variations, whether a Duet or Stitch could
  extend reach, and whether this angle should anchor Month 2 content strategy.
  ```

---

### WS-028 · Reddit third discovery pass + identify r/SEO opportunities
- **Owner:** @reddit-community-builder
- **Day:** 22
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Run a third Reddit thread discovery pass focused on r/SEO and r/artificial —
  the two highest-risk, highest-reward subreddits in the campaign.

  For each thread found, assess:
  - Is the thread asking a technical question (SEO workflow, AI search optimization)?
  - Is there a genuine gap in the replies where a technical Writesonic answer adds value?
  - What is the mod activity level in this thread?

  Only flag threads where Template 2 (Technical Comparison Reply) is a natural fit —
  not where a product mention would feel forced.

  Also: check if any comments in these threads are already mentioning Writesonic
  (we should reply to those specifically — high credibility to add onto an existing mention).
  ```
- **Output:** Shortlist of ≤3 r/SEO or r/artificial threads approved for Template 2 engagement.

---

### WS-029 · SEO ranking check — comparison post
- **Owner:** @seo-specialist
- **Day:** 24
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Check ranking progress for the post targeting "jasper alternative 2025":
  [post URL from WS-009]

  Pull from Google Search Console:
  - Current average position for primary keyword
  - Impressions and clicks (past 7 days)
  - Any other queries the post is ranking for unexpectedly

  If position is >20: recommend 3 specific on-page or off-page actions to improve ranking.
  If position is ≤10: recommend internal linking strategy to consolidate authority.
  ```

---

### WS-030 · 30-day full performance report
- **Owner:** @analytics-reporter
- **Day:** 30
- **Status:** `[ ]`
- **Agent prompt:**
  ```
  Generate the final 30-day performance report for a Writesonic affiliate campaign.

  Campaign channels: TikTok (5 hooks), Reddit (6 subreddits), Blog (2 posts + updates)

  Data to analyze (human will paste in):
  1. Affiliate dashboard: total clicks, total signups, revenue, UTM breakdown
  2. TikTok: per-video stats (views, watch time, CTR, saves, shares)
  3. Reddit: per-reply karma, upvote rate, removals, subreddit breakdown
  4. Blog: Search Console data for both posts (impressions, clicks, avg position)

  Deliverable:
  - Executive summary (3 bullet points: what worked, what didn't, top insight)
  - Channel ROI comparison (time invested vs. signups generated)
  - Best performing content unit across all channels
  - Recommended Month 2 channel allocation (% effort per channel)
  - 3 specific content angles for Month 2 based on data
  - Any compliance red flags (mod warnings, FTC risk areas)

  Format: structured report, ready to paste into Month 2 planning doc.
  ```
- **Output:** Save to `reports/30-day-report.md`.
- **Payment timing note:** Per affiliate terms, commissions are paid on the 1st of the month,
  at least 30 days after a trial converts to paid, with a $50 minimum threshold. No payments
  will have been received by Day 30 — the report should track signups and projected commission,
  not cash received. First payment is realistically Month 3.

---

### WS-031 · Draft Month 2 plan
- **Owner:** Human + @social-media-strategist
- **Day:** 30
- **Status:** `[ ]`
- **Depends on:** WS-030 (30-day report)
- **Agent prompt:**
  ```
  Based on the attached 30-day performance report [paste WS-030 output], draft a
  Month 2 content and channel strategy for a Writesonic affiliate campaign.

  New comparison angles to consider for Month 2:
  - Writesonic vs. Copy.ai
  - Writesonic for agencies vs. individual creators
  - Writesonic GEO features for AI search ranking (ChatGPT/Perplexity visibility)
  - YouTube long-form review (adapt top TikTok scripts as outline)
  - Paid Reddit/social promotion test — generic keywords only (e.g. "AI writing tools",
    "AI affiliate programs"); branded keywords (Writesonic, Chatsonic, Botsonic,
    Photosonic) and combos (e.g. "Writesonic review", "Writesonic pricing") are
    PROHIBITED under affiliate terms and will result in immediate account cancellation.

  Deliverable:
  - 4-week roadmap for Month 2 with the same sprint structure
  - Agent assignments for each major task
  - KPI targets for Month 2 (based on Month 1 actuals)
  ```

---

### Sprint 4 Exit Criteria

| Criteria | Owner | Done? |
|---|---|---|
| Analytics report complete (Days 1–21) | @analytics-reporter | `[ ]` |
| r/entrepreneur replies live | Human | `[ ]` |
| r/digital_marketing replies live | Human | `[ ]` |
| Hook #5 published | Human + @tiktok-strategist | `[ ]` |
| Hook variation scripts drafted for top performer | @tiktok-strategist | `[ ]` |
| r/SEO thread shortlist identified | @reddit-community-builder | `[ ]` |
| SEO ranking check complete | @seo-specialist | `[ ]` |
| 30-day report generated | @analytics-reporter | `[ ]` |
| Month 2 plan drafted | @social-media-strategist | `[ ]` |

---

## Master Ticket Index

| Ticket | Title | Owner | Sprint | Day |
|---|---|---|---|---|
| WS-001 | Sign up for Writesonic affiliate program | Human | 1 | 1 |
| WS-002 | Create UTM-tagged tracking links | Human | 1 | 1 |
| WS-003 | Build comparison/review hub page | Human + @content-creator | 1 | 1–2 |
| WS-004 | Set up tracking spreadsheet | Human | 1 | 2 |
| WS-005 | Keyword research pass | @trend-researcher | 1 | 3 |
| WS-006 | Reddit thread discovery — initial pass | @reddit-community-builder | 1 | 3–4 |
| WS-007 | Reddit account karma warm-up — begin | Human | 1 | 4–7 |
| WS-008 | TikTok Hook #3 — Personal Narrative | Human + @tiktok-strategist | 1 | 5–7 |
| WS-009 | Brief and draft comparison post | @content-creator | 2 | 8–9 |
| WS-010 | SEO audit of comparison post | @seo-specialist | 2 | 10 |
| WS-011 | Draft "Best AI Affiliate Programs 2025" post | @content-creator | 2 | 10–11 |
| WS-012 | TikTok Hook #1 — Income Loss Story | Human + @tiktok-strategist | 2 | 10 |
| WS-013 | TikTok Hook #4 — Educational | Human + @tiktok-strategist | 2 | 14 |
| WS-014 | TikTok comment engagement (ongoing) | Human | 2 | 8–14 |
| WS-015 | Reddit lurk phase — select top 5 threads | Human | 2 | 8–14 |
| WS-016 | Reddit karma warm-up — continue | Human | 2 | 8–14 |
| WS-017 | Reddit engagement — r/blogging | Human | 3 | 15–17 |
| WS-018 | Reddit engagement — r/sidehustle | Human | 3 | 16–19 |
| WS-019 | Reddit thread discovery — second pass | @reddit-community-builder | 3 | 15 |
| WS-020 | Update existing Jasper content on site | Human + @content-creator + @seo-specialist | 3 | 15–17 |
| WS-021 | TikTok Hook #2 — Pattern Interrupt | Human + @tiktok-strategist | 3 | 17 |
| WS-022 | Mid-campaign cross-channel alignment check | @social-media-strategist | 3 | 18 |
| WS-023 | Pull Week 2–3 analytics | @analytics-reporter | 4 | 22 |
| WS-024 | Reddit engagement — r/entrepreneur | Human | 4 | 22–26 |
| WS-025 | Reddit engagement — r/digital_marketing | Human | 4 | 23–27 |
| WS-026 | TikTok Hook #5 — Comparison/Conversion | Human + @tiktok-strategist | 4 | 25 |
| WS-027 | Scale highest-performing TikTok hook | Human + @tiktok-strategist | 4 | 23–28 |
| WS-028 | Reddit discovery — r/SEO opportunities | @reddit-community-builder | 4 | 22 |
| WS-029 | SEO ranking check — comparison post | @seo-specialist | 4 | 24 |
| WS-030 | 30-day full performance report | @analytics-reporter | 4 | 30 |
| WS-031 | Draft Month 2 plan | Human + @social-media-strategist | 4 | 30 |

---

## Agent Quick Reference

| Agent | Tickets | When to invoke |
|---|---|---|
| @trend-researcher | WS-005 | Day 3, Day 22 |
| @reddit-community-builder | WS-006, WS-019, WS-028 | Day 3, Day 15, Day 22 |
| @tiktok-strategist | WS-008, WS-012, WS-013, WS-021, WS-026, WS-027 | Before each video + Day 22 with analytics |
| @content-creator | WS-003, WS-009, WS-011, WS-020 | Day 1, Day 8, Day 10, Day 15 |
| @seo-specialist | WS-010, WS-020, WS-029 | Day 10, Day 15, Day 24 |
| @analytics-reporter | WS-023, WS-030 | Day 22, Day 30 |
| @social-media-strategist | WS-022, WS-031 | Day 18, Day 30 |

---

*tasks.md v1.0 | Parsed from playbook.md v1.0 | 31 tickets across 4 sprints*
