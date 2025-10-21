```markdown
# KiboVentures Scout: AI-Powered Startup Sourcing Engine

**ALERT: FREE API KEY (I already revoked it you greedy user)**
*Old API key left as example - replace with your own OpenAI API key before running*

## 🚀 Overview

Automated pipeline that identifies investment-ready AI startups for venture capital analysis. This system replicates a VC analyst's workflow through web scraping, data cleaning, and AI-powered company assessment.

## 📊 Pipeline Architecture

```
Raw Data → Filtering → AI Analysis → Investment Portfolio
    ↓          ↓           ↓             ↓
  800+      192 Clean    37 AI-at-core  VC-Ready
Articles   Startups      Companies      Presentation
```

## 🛠️ Tech Stack

- **Web Scraping:** Crawl4ai, Playwright
- **AI Analysis:** OpenAI GPT-4, Web Search
- **Data Processing:** Python, Regex, JSON
- **Output:** Markdown, JSON, PowerPoint

## 📁 Project Structure

```
kiboventures-scout/
├── vc_crawl.py              # Web scraping pipeline
├── EDA_Data_cleaning.py     # Data filtering & cleaning
├── run_screening.py         # AI analysis & scoring
├── reorganize_results.py    # Portfolio assembly
├── spanish_startups_raw.md  # Raw scraped data
├── spanish_startups_clean.md # Filtered companies
└── startup_analysis.json    # AI analysis results
```

## ⚡ Quick Start

### 1. Installation
```bash
# Install Python dependencies
pip install crawl4ai playwright openai

# Install browser for scraping
playwright install chromium
```

### 2. Configuration
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Or add to your environment variables
```

### 3. Execution
```bash
# Run the complete pipeline
python vc_crawl.py
python EDA_Data_cleaning.py  
python run_screening.py
python reorganize_results.py
```

## 🔧 How It Works

### Phase 1: Data Collection (`vc_crawl.py`)
- Scrapes EU-Startups.com Spain section
- Extracts 800+ funding announcements
- Output: `spanish_startups_raw.md`

### Phase 2: Data Cleaning (`EDA_Data_cleaning.py`)
- Filters for Spanish companies
- Targets €1-10M funding range  
- Removes duplicates
- Output: `spanish_startups_clean.md` (192 companies)

### Phase 3: AI Analysis (`run_screening.py`)
- Researches each company using web search
- Scores AI integration (1-10 scale)
- Identifies "AI-at-core" companies (score ≥8)
- Output: `startup_analysis.json`

### Phase 4: Portfolio Assembly (`reorganize_results.py`)
- Sorts companies by AI score
- Generates investment portfolio
- Output: Console report + `portfolio_winners.md`

## 🎯 Investment Criteria

Companies are scored on:
- **9-10:** AI IS the product (infrastructure, platforms)
- **7-8:** AI as fundamental differentiator  
- **5-6:** AI-enhanced features
- **<5:** Minimal/no AI focus

**Only companies scoring ≥8 advance to final portfolio.**

## 📈 Output

**Final Portfolio:** 37 Spanish AI startups including:
- **QBeast** (AI data infrastructure) - Score: 9/10
- **Orbio** (AI-native HR platform) - Score: 9/10  
- **SLNG** (Speech AI infrastructure) - Score: 9/10
- **Nymiz** (AI data anonymization) - Score: 8/10

## ⚠️ Important Notes

- **Ethical Scraping:** Respects robots.txt and rate limits
- **API Costs:** Uses OpenAI API (costs apply)
- **Data Freshness:** Results depend on current web data
- **VC Validation:** Always verify findings with traditional due diligence

## 🎓 Use Cases

- **VC Firms:** Automated sourcing and initial screening
- **Angel Investors:** Deal flow generation
- **Startup Ecosystems:** Market landscape analysis
- **Research:** AI adoption trends in startups

---

**Built for Kibo Ventures Investment Analyst Assessment**
*Demonstrating systematic sourcing and AI-powered analysis capabilities*
```

This README:
- Starts with your security notice upfront
- Provides clear visual pipeline overview
- Includes specific installation/execution steps
- Explains the investment scoring methodology
- Shows concrete output examples
- Maintains professional VC-focused tone
- Highlights the practical business value

