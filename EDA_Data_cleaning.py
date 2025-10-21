

## load data
# Simple file loading in PyCharm
def load_startup_data():
    try:
        with open("spanish_million_startups.md", "r", encoding="utf-8") as f:
            content = f.read()
        print(f"✅ Successfully loaded file: {len(content)} characters")
        return content
    except FileNotFoundError:
        print("❌ File not found! Make sure 'spanish_million_startups.md' is in the same folder as your script")
        return None




# Load the data
content = load_startup_data()

if content:
    # Parse the startups
    startups = []
    sections = content.split('---')

    for section in sections:
        if section.strip() and '##' in section:
            startups.append(section.strip())

    print(f"📊 Found {len(startups)} startup entries")

    # Show samples
    for i, startup in enumerate(startups[:3], 1):
        print(f"\nSample {i}:")
        print(startup[:200] + "...")

# first screening of the 800 companies manual filter raised > 10 million
import re


def filter_by_funding(startups, max_funding=10):
    """Filter startups by funding amount mentioned in titles"""

    filtered_startups = []

    for startup in startups:
        # Extract funding amount from title
        title = startup.split('\n')[0]  # First line is usually the title

        # Look for funding patterns: "raises €X million", "€X million", "X million"
        funding_patterns = [
            r'raises\s*€?\s*([0-9.]+)\s*million',
            r'€\s*([0-9.]+)\s*million',
            r'\$?\s*([0-9.]+)\s*million',
            r'raised\s*€?\s*([0-9.]+)\s*million'
        ]

        funding_amount = None
        for pattern in funding_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                try:
                    funding_amount = float(match.group(1))
                    break
                except:
                    continue

        # Keep if funding is between 1-10 million, or if no funding mentioned (needs manual check)
        if funding_amount is None:
            print(f"⚠️  No funding found: {title[:50]}...")
            filtered_startups.append(startup)  # Keep for manual review
        elif 1 <= funding_amount <= max_funding:
            print(f"✅ Funding OK (€{funding_amount}M): {title[:50]}...")
            filtered_startups.append(startup)
        else:
            print(f"❌ Funding excluded (€{funding_amount}M): {title[:50]}...")

    return filtered_startups


# Apply funding filter first
print("💰 APPLYING FUNDING FILTER (€1-10M)...")
filtered_startups = filter_by_funding(startups)

print(f"\n📊 FUNDING FILTER RESULTS:")
print(f"   Original: {len(startups)} startups")
print(f"   After funding filter: {len(filtered_startups)} startups")

# filter 2 some compnies are not spanish based they're european so lets filter b spanish based
import re


def filter_by_spanish_location(funding_filtered_startups):
    """Filter startups by Spanish location (cities/regions)"""

    # Major Spanish cities and regions
    spanish_locations = [
        'spain', 'spanish', 'españa', 'español',
        'madrid', 'barcelona', 'valencia', 'bilbao', 'sevilla', 'seville',
        'zaragoza', 'málaga', 'murcia', 'palma', 'granada', 'alicante',
        'córdoba', 'valladolid', 'vigo', 'gijón', 'hospitalet', 'la coruña',
        'oviedo', 'pamplona', 'santander', 'logroño', 'san sebastián',
        'cartagena', 'jerez', 'salamanca', 'albacete', 'huelva', 'badalona',
        'lérida', 'marbella', 'dénia', 'torrevieja', 'girona', 'cáceres',
        'baleares', 'canarias', 'andalucía', 'cataluña', 'galicia', 'basque',
        'euskadi', 'navarra', 'aragon', 'castilla', 'extremadura', 'mallorca'
    ]

    location_filtered_startups = []

    for startup in funding_filtered_startups:
        title = startup.split('\n')[0].lower()  # First line is the title

        # Check if location is Spanish
        is_spanish = any(location in title for location in spanish_locations)

        if is_spanish:
            print(f"✅ Spanish: {title[:60]}...")
            location_filtered_startups.append(startup)
        else:
            print(f"❌ Non-Spanish: {title[:60]}...")

    return location_filtered_startups


# Apply location filter to funding-filtered companies
print("🌍 APPLYING SPANISH LOCATION FILTER...")
location_filtered_startups = filter_by_spanish_location(filtered_startups)

print(f"\n📊 LOCATION FILTER RESULTS:")
print(f"   After funding filter: {len(filtered_startups)} startups")
print(f"   After location filter: {len(location_filtered_startups)} startups")

# lets remove duplicates

def remove_duplicates(startups):
    """Remove duplicate startups based on title similarity"""

    seen_titles = set()
    unique_startups = []

    for startup in startups:
        # Extract just the title (first line)
        title = startup.split('\n')[0].strip()

        # Create a simplified version for comparison
        simplified = title.lower()

        # Remove common prefixes and normalize
        simplified = simplified.replace('## ', '').replace('**', '')

        # Check if we've seen this title before
        if simplified not in seen_titles:
            seen_titles.add(simplified)
            unique_startups.append(startup)
        else:
            print(f"🗑️  Duplicate removed: {title[:60]}...")

    return unique_startups


# Remove duplicates from location-filtered startups
print("\n🧹 REMOVING DUPLICATES...")
unique_startups = remove_duplicates(location_filtered_startups)

print(f"\n📊 DEDUPLICATION RESULTS:")
print(f"   After location filter: {len(location_filtered_startups)} startups")
print(f"   After removing duplicates: {len(unique_startups)} startups")

# Show the unique companies
print(f"\n🎯 UNIQUE SPANISH STARTUPS (€1-10M):")
print("=" * 80)
for i, startup in enumerate(unique_startups[:20], 1):  # Show first 20
    title = startup.split('\n')[0]
    print(f"{i}. {title}")

# overview of the cleaning

# Now you have clean, unique Spanish startups in the €1-10M range
print(f"\n✅ FINAL CLEAN DATASET:")
print(f"   📁 Original: {len(startups)} startups")
print(f"   💰 After funding filter: {len(filtered_startups)}")
print(f"   🌍 After location filter: {len(location_filtered_startups)}")
print(f"   🧹 After deduplication: {len(unique_startups)}")
print(f"   🎯 Ready for AI screening: {len(unique_startups)} unique Spanish startups")

# Save the clean dataset
with open("clean_spanish_startups.md", "w", encoding="utf-8") as f:
    f.write("# Clean Spanish Startups (€1-10M)\n\n")
    for startup in unique_startups:
        f.write(startup + "\n\n")

print(f"\n💾 Saved clean dataset to 'clean_spanish_startups.md'")

# Print all clean, unique Spanish startups
print("\n🎯 CLEAN SPANISH STARTUPS (€1-10M):")
print("=" * 80)
for i, startup in enumerate(unique_startups, 1):
    title = startup.split('\n')[0].strip()
    print(f"{i}. {title}")
# Remove first entry (header) before saving and printing
cleaned_startups = unique_startups[1:]  # skip "# Million-Funded Spanish Startups"

# Show the unique companies (first 20)
print(f"\n🎯 UNIQUE SPANISH STARTUPS (€1-10M):")
print("=" * 80)
for i, startup in enumerate(cleaned_startups[:20], 1):
    title = startup.split('\n')[0]
    print(f"{i}. {title}")

# Save the clean dataset with the same file name
with open("clean_spanish_startups.md", "w", encoding="utf-8") as f:
    f.write("# Clean Spanish Startups (€1-10M)\n\n")
    for startup in cleaned_startups:
        f.write(startup + "\n\n")

print(f"\n💾 Saved clean dataset to 'clean_spanish_startups.md'")




