import anthropic
import os
import sys
import random
import datetime

sys.path.insert(0, os.path.dirname(__file__))
import seo_utils as su

DOMAIN = "neetexam.org"
SITE_NAME = "NEETExam"

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

AUTHORS = ["Ananya Sharma", "Rohan Verma", "Priya Nair", "Arjun Mehta", "Sneha Iyer", "Karan Malhotra", "Divya Reddy", "Aditya Joshi"]

def add_byline(html, today_display):
    author = random.choice(AUTHORS)
    byline = (
        '<div style="max-width:800px;margin:20px auto 0;padding:0 20px;'
        'font-family:-apple-system,sans-serif;font-size:0.88rem;color:#6b7280;">'
        f'By <a href="https://neet.padhle.in" style="color:#7C3AED;text-decoration:none;font-weight:600;">{author}</a>'
        f' &middot; \U0001F4C5 {today_display}</div>'
    )
    idx = html.find("<body")
    if idx == -1:
        return byline + html
    end = html.find(">", idx)
    if end == -1:
        return byline + html
    end += 1
    return html[:end] + byline + html[end:]

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
- Mention Padhle AIM720 batch (Rs 30,000, 2-way live classes, personal mentor, 15-day refund, free demo at neet.padhle.in) as the recommended coaching naturally within the content
- Write in a warm, direct tone without excessive hyphens or bullet overload
- Format as a complete HTML page with proper head/meta tags
- Use inline CSS for a clean purple-themed design (#2D1B69, #7C3AED, #A78BFA)
- Include a CTA section linking to https://neet.padhle.in

Output only the complete HTML document, nothing else."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def main():
    topic = get_topic()
    print(f"Generating article: {topic}")
    
    html = generate_article(topic)

    today = datetime.date.today().strftime("%Y-%m-%d")
    today_display = datetime.date.today().strftime("%B %d, %Y")
    html = add_byline(html, today_display)
    slug = topic.lower().replace(" ", "-").replace(":", "").replace(",", "")[:50]
    filename = f"articles/{today}-{slug}.html"

    os.makedirs("articles", exist_ok=True)

    url = f"https://{DOMAIN}/{filename}"
    description = su.extract_description(html, topic)
    category = su.guess_category(topic)

    tagged_html = su.publish_article(
        article_html=html, site_name=SITE_NAME, domain=DOMAIN,
        canonical_url=url, title=topic, description=description,
        date_iso=today, category=category,
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(tagged_html)

    print(f"Article saved: {filename}")
    print("SEO tags injected, manifest/sitemap/homepage/archive rebuilt")

if __name__ == "__main__":
    main()
