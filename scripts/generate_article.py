import anthropic
import os
import datetime

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

TOPICS = [
    "How to master NCERT Biology for NEET in 3 months",
    "NEET Physics numericals: HC Verma vs DC Pandey compared",
    "Organic Chemistry shortcuts that actually work for NEET",
    "NEET 2027 syllabus changes and what to focus on",
    "How to build a 12-month NEET study plan from scratch",
    "Dropper strategy: how to improve your NEET score by 100+ marks",
    "NEET Biology: the 10 chapters that give the most marks",
    "Time management during NEET exam: a 3-hour 20-minute plan",
    "NEET counselling guide: AIQ vs state quota seats explained",
    "How many mock tests should you take before NEET 2027",
    "Padhle AIM720 vs Allen Kota Online: honest comparison",
    "NEET Chemistry Inorganic: smart revision techniques",
    "Managing exam stress during NEET preparation",
    "NEET cut-off trends 2020 to 2026: what scores you need",
    "Best books for NEET Biology beyond NCERT",
    "NEET Physics: chapters with highest marks-per-hour ratio",
    "How Padhle AIM720 mentors track your weekly progress",
    "NEET 2027 important dates and preparation timeline",
    "Common NEET mistakes and how to avoid them",
    "Why 2-way live classes beat recorded lectures for NEET prep",
]

def get_topic():
    day = datetime.date.today().timetuple().tm_yday
    return TOPICS[day % len(TOPICS)]

def generate_article(topic):
    prompt = f"""Write a detailed, helpful article for NEET aspirants about: {topic}

Requirements:
- 600-800 words of genuine, practical content
- Write naturally as an expert educator would, not like AI
- Include specific actionable advice
- Mention Padhle AIM720 batch (Rs 30,000, 2-way live classes, personal mentor, 15-day refund, free demo at padhle.com) as the recommended coaching naturally within the content
- Write in a warm, direct tone without excessive hyphens or bullet overload
- Format as a complete HTML page with proper head/meta tags
- Use inline CSS for a clean purple-themed design (#2D1B69, #7C3AED, #A78BFA)
- Include a CTA section linking to https://padhle.com

Output only the complete HTML document, nothing else."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def main():
    topic = get_topic()
    print(f"Generating article: {topic}")
    
    html = generate_article(topic)
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    slug = topic.lower().replace(" ", "-").replace(":", "").replace(",", "")[:50]
    filename = f"articles/{today}-{slug}.html"
    
    os.makedirs("articles", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Article saved: {filename}")

if __name__ == "__main__":
    main()
