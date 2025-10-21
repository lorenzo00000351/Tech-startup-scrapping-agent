import os
import json
import time
from openai import OpenAI

# Set API key directly as you specified
os.environ[
    'OPENAI_API_KEY'] = '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'

client = OpenAI()


def research_company_with_fallback(company_name):
    """Complete research pipeline with fallback strategy"""

    print(f"\n🚀 RESEARCHING: {company_name}")
    print("=" * 50)

    # Phase 1: Direct search
    print(f"   🔍 Phase 1: Direct search for {company_name}...")

    prompt = f"""Research the Spanish startup: {company_name}

Find:
1. Official website URL
2. Business model description
3. Core technology

Return EXACT JSON:
{{
    "company_name": "{company_name}",
    "official_website": "url_or_null",
    "business_description": "1-2 specific sentences",
    "confidence": "high/medium/low"
}}"""

    try:
        response = client.responses.create(
            model="gpt-4o",
            tools=[{"type": "web_search"}],
            input=prompt
        )

        result_text = response.output_text

        # Extract JSON from response
        try:
            start_idx = result_text.find('{')
            end_idx = result_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = result_text[start_idx:end_idx]
                direct_result = json.loads(json_str)
            else:
                direct_result = {
                    "company_name": company_name,
                    "official_website": None,
                    "business_description": "Search failed",
                    "confidence": "low"
                }
        except:
            direct_result = {
                "company_name": company_name,
                "official_website": None,
                "business_description": "JSON parse failed",
                "confidence": "low"
            }

    except Exception as e:
        print(f"   ❌ Direct search error: {e}")
        direct_result = {
            "company_name": company_name,
            "official_website": None,
            "business_description": f"Error: {str(e)}",
            "confidence": "low"
        }

    # Phase 2: AI Assessment
    print(f"   🤖 Phase 2: AI assessment for {company_name}...")

    assessment_prompt = f"""Based on this business description, assess if {company_name} is AI-at-core:

Business: {direct_result.get('business_description', 'No description found')}

AI SCORING GUIDE (be strict but recognize AI infrastructure companies):
- 9-10: AI IS the product (AI infrastructure, ML platforms, AI-native, data infrastructure for AI)
- 7-8: AI as fundamental differentiator (AI-first approach, core AI algorithms)
- 5-6: AI as important features (AI-enhanced but not core business)
- 3-4: Minimal AI usage (basic automation, simple AI features)
- 1-2: No AI focus (traditional software/services)

SPECIAL NOTE: Companies like QBeast that provide data infrastructure for AI workloads ARE AI-at-core because they enable AI systems to function efficiently.

Return EXACT JSON:
{{
    "company_name": "{company_name}",
    "ai_core_score": 1-10,
    "ai_assessment": "brief explanation",
    "keep_for_review": true_or_false
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": assessment_prompt}],
            temperature=0.1
        )

        result_text = response.choices[0].message.content

        # Extract JSON from response
        try:
            start_idx = result_text.find('{')
            end_idx = result_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = result_text[start_idx:end_idx]
                ai_assessment = json.loads(json_str)
            else:
                ai_assessment = {
                    "company_name": company_name,
                    "ai_core_score": 1,
                    "ai_assessment": "Assessment failed",
                    "keep_for_review": False
                }
        except:
            ai_assessment = {
                "company_name": company_name,
                "ai_core_score": 1,
                "ai_assessment": "JSON parse failed",
                "keep_for_review": False
            }

    except Exception as e:
        print(f"   ❌ AI assessment error: {e}")
        ai_assessment = {
            "company_name": company_name,
            "ai_core_score": 1,
            "ai_assessment": f"Error: {str(e)}",
            "keep_for_review": False
        }

    # FIXED LOGIC: If score >= 8, automatically keep for review
    ai_score = ai_assessment.get("ai_core_score", 1)
    should_keep = ai_score >= 8  # This is the fix!

    # Compile final result
    final_result = {
        "company_name": company_name,
        "official_website": direct_result.get("official_website"),
        "business_description": direct_result.get("business_description", ""),
        "ai_core_score": ai_score,
        "ai_assessment": ai_assessment.get("ai_assessment", ""),
        "keep_for_review": should_keep,  # Use our fixed logic
        "research_confidence": direct_result.get("confidence", "low")
    }

    # Display result
    status = "✅ KEEP" if final_result["keep_for_review"] else "❌ EXCLUDE"
    print(f"   {status}: {company_name}")
    print(f"   🌐 Website: {final_result['official_website'] or 'Not found'}")
    print(f"   🤖 AI Score: {final_result['ai_core_score']}/10")
    print(f"   📝 Business: {final_result['business_description']}")
    print()

    return final_result


def main():
    print("🚀 ENHANCED STARTUP RESEARCH WITH FALLBACK STRATEGY")
    print("=" * 60)

    # Your 192 companies

    # Load all startups dynamically from your cleaned dataset
    def load_clean_startups():
        try:
            with open("clean_spanish_startups.md", "r", encoding="utf-8") as f:
                content = f.read()
            # Split by markdown headings
            sections = [s.strip() for s in content.split('##') if s.strip()]
            startup_names = []
            for s in sections:
                name_line = s.split('\n')[0].strip()
                clean_name = name_line.replace('*', '').replace('#', '').strip()
                if clean_name:
                    startup_names.append(clean_name)
            print(f"✅ Loaded {len(startup_names)} startups.")
            for i, name in enumerate(startup_names, 1):
                print(f"   {i}. {name}")
            return startup_names
        except FileNotFoundError:
            print("❌ File 'clean_spanish_startups.md' not found. Make sure it's in the same directory.")
            return []

    # Load all startups for full run
    STARTUPS = load_clean_startups()

    print(f"Researching {len(STARTUPS)} Spanish startups...")
    print()

    all_results = []
    kept_companies = []

    for i, startup in enumerate(STARTUPS, 1):
        print(f"📊 Company {i}/{len(STARTUPS)}")
        result = research_company_with_fallback(startup)
        all_results.append(result)

        if result.get("keep_for_review"):
            kept_companies.append(result)

        # Small delay to avoid rate limits
        if i < len(STARTUPS):
            time.sleep(2)

    # Final Summary
    print("🎯 RESEARCH SUMMARY")
    print("=" * 50)
    print(f"✅ Companies to research further: {len(kept_companies)}")
    print(f"❌ Companies excluded: {len(STARTUPS) - len(kept_companies)}")
    print(f"📈 Success rate: {len(kept_companies)}/{len(STARTUPS)} ({len(kept_companies) / len(STARTUPS) * 100:.1f}%)")

    # Show kept companies
    if kept_companies:
        print(f"\n🏆 COMPANIES FOR DEEP DIVE:")
        for company in kept_companies:
            print(f"   - {company['company_name']} (AI Score: {company['ai_core_score']}/10)")

    # Save detailed results
    with open("enhanced_startup_research.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Detailed results saved to 'enhanced_startup_research.json'")
    return all_results


if __name__ == "__main__":
    results = main()