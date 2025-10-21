import json

# Load your results
with open("enhanced_startup_research.json", "r", encoding="utf-8") as f:
    all_companies = json.load(f)

# Simple split and sort
winners = [c for c in all_companies if c.get('ai_core_score', 0) >= 8]
losers = [c for c in all_companies if c.get('ai_core_score', 0) < 8]

# Sort winners from highest to lowest score
winners.sort(key=lambda x: x.get('ai_core_score', 0), reverse=True)

# Print winners in readable format
print("🏆 WINNERS (Score >= 8) - Sorted Highest to Lowest")
print("=" * 60)

for i, company in enumerate(winners, 1):
    print(f"\n{i}. {company['company_name']}")
    print(f"   Score: {company['ai_core_score']}/10")
    print(f"   Website: {company.get('official_website', 'Not found')}")
    print(f"   Business: {company.get('business_description', 'No description')}")
    print(f"   Assessment: {company.get('ai_assessment', 'No assessment')}")
    print("-" * 50)

print(f"\n✅ Total Winners: {len(winners)}")
print(f"📉 Total Losers: {len(losers)}")