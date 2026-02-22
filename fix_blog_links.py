#!/usr/bin/env python3
"""
Fix blog.html:
1. Change relative link blog/${slug}.html to /blog/${slug}.html (absolute)
2. Replace BLOG_POSTS array with all 23 articles

Run from protevio-deploy root:
    python3 fix_blog_links.py
"""
import re
import json

BLOG_FILE = 'blog.html'

# All blog articles - using a clean data structure, no escaping headaches
ALL_ARTICLES = [
    {"slug": "how-to-find-where-your-photos-appear-online", "title": "How to Find Where Your Photos Appear Online", "excerpt": "Your face could be on websites you have never visited. Learn how to discover every place your photos appear online.", "category": "guide", "catLabel": "Guide", "date": "Feb 8, 2026", "readTime": "8 min read", "emoji": "&#128269;", "gradient": "linear-gradient(135deg, #1e3a5f 0%, #2a3349 100%)"},
    {"slug": "someone-using-my-photos-without-permission", "title": "Someone Is Using My Photos Without Permission \u2014 What to Do", "excerpt": "Discovering unauthorized use of your photos can be alarming. A step-by-step action plan to identify the scope and get images removed.", "category": "legal", "catLabel": "Legal", "date": "Feb 5, 2026", "readTime": "10 min read", "emoji": "&#9878;", "gradient": "linear-gradient(135deg, #2d1b69 0%, #2a3349 100%)"},
    {"slug": "what-is-reverse-face-search", "title": "What Is Reverse Face Search and How Does It Work?", "excerpt": "Facial recognition search technology explained in plain language \u2014 how AI matches faces across millions of images.", "category": "guide", "catLabel": "Guide", "date": "Feb 2, 2026", "readTime": "7 min read", "emoji": "&#129302;", "gradient": "linear-gradient(135deg, #0f3460 0%, #16213e 100%)"},
    {"slug": "how-to-remove-your-photos-from-the-internet", "title": "How to Remove Your Photos from the Internet: Complete Guide", "excerpt": "A practical guide to getting your photos taken down from websites, social media, and search engines.", "category": "privacy", "catLabel": "Privacy", "date": "Jan 28, 2026", "readTime": "12 min read", "emoji": "&#128737;", "gradient": "linear-gradient(135deg, #1a3c34 0%, #2a3349 100%)"},
    {"slug": "gdpr-right-to-be-forgotten", "title": "GDPR and Your Right to Be Forgotten \u2014 A Practical Guide", "excerpt": "The GDPR gives you powerful rights over your personal data, including your photos. Learn how to exercise your right to erasure.", "category": "legal", "catLabel": "Legal", "date": "Jan 22, 2026", "readTime": "9 min read", "emoji": "&#128220;", "gradient": "linear-gradient(135deg, #3b1f2b 0%, #2a3349 100%)"},
    {"slug": "how-catfishers-steal-photos", "title": "How Catfishers Steal Photos \u2014 And How to Stop Them", "excerpt": "Catfishers use real photos to create fake identities. Learn the warning signs and how facial recognition search can protect you.", "category": "awareness", "catLabel": "Awareness", "date": "Jan 18, 2026", "readTime": "8 min read", "emoji": "&#127917;", "gradient": "linear-gradient(135deg, #4a1942 0%, #2a3349 100%)"},
    {"slug": "reverse-image-search-vs-face-recognition", "title": "Reverse Image Search vs Face Recognition \u2014 The Difference", "excerpt": "Google reverse image search and AI face recognition work very differently. Learn which tool is right for finding your photos.", "category": "guide", "catLabel": "Guide", "date": "Jan 15, 2026", "readTime": "7 min read", "emoji": "&#128200;", "gradient": "linear-gradient(135deg, #0d2137 0%, #1a1a4e 100%)"},
    {"slug": "catfish-photo-check", "title": "Catfish Photo Check \u2014 Verify If Someone Is Using Fake Photos", "excerpt": "Suspect someone is catfishing you? Upload their photo and find where that image really comes from with AI-powered search.", "category": "awareness", "catLabel": "Awareness", "date": "Jan 12, 2026", "readTime": "7 min read", "emoji": "&#128270;", "gradient": "linear-gradient(135deg, #5c2a6e 0%, #2a3349 100%)"},
    {"slug": "deepfake-monitoring", "title": "Deepfake Monitoring \u2014 Find Where Your Face Is Being Used", "excerpt": "Monitor the web for unauthorized use of your face, including AI-generated deepfakes. Get alerts when your likeness appears.", "category": "security", "catLabel": "Security", "date": "Jan 10, 2026", "readTime": "9 min read", "emoji": "&#129504;", "gradient": "linear-gradient(135deg, #1a1a4e 0%, #2a3349 100%)"},
    {"slug": "executive-image-protection", "title": "Executive Image Protection \u2014 Protect CEO and Leadership Photos", "excerpt": "Protect your executives from image fraud, fake endorsements, and impersonation. Monitor where leadership photos appear.", "category": "security", "catLabel": "Security", "date": "Jan 8, 2026", "readTime": "8 min read", "emoji": "&#128188;", "gradient": "linear-gradient(135deg, #1e3a5f 0%, #162447 100%)"},
    {"slug": "face-recognition-search", "title": "Face Recognition Search Engine \u2014 AI-Powered Face Finder", "excerpt": "Search the internet by face with AI facial recognition. Upload a photo, find matches across tens of millions of indexed faces.", "category": "guide", "catLabel": "Guide", "date": "Jan 6, 2026", "readTime": "6 min read", "emoji": "&#129302;", "gradient": "linear-gradient(135deg, #0d2137 0%, #2a3349 100%)"},
    {"slug": "face-search-for-photographers", "title": "Copyright Protection for Photographers \u2014 Find Unlicensed Use", "excerpt": "Track unauthorized use of your portrait photography with AI facial recognition. Find unlicensed photos across the web.", "category": "guide", "catLabel": "Guide", "date": "Jan 4, 2026", "readTime": "7 min read", "emoji": "&#128247;", "gradient": "linear-gradient(135deg, #2d3436 0%, #2a3349 100%)"},
    {"slug": "find-my-face-online", "title": "Find Where My Face Appears Online \u2014 Face Search Tool", "excerpt": "Worried about your photos being used without permission? Discover every website where your face appears with AI-powered search.", "category": "guide", "catLabel": "Guide", "date": "Jan 2, 2026", "readTime": "6 min read", "emoji": "&#128373;", "gradient": "linear-gradient(135deg, #1a3c34 0%, #162447 100%)"},
    {"slug": "gdpr-face-data-rights", "title": "GDPR Face Data Rights \u2014 Find and Remove Your Face From Databases", "excerpt": "Exercise your GDPR right to erasure for facial data. Discover where your biometric face data exists and demand its removal.", "category": "legal", "catLabel": "Legal", "date": "Dec 28, 2025", "readTime": "10 min read", "emoji": "&#127988;", "gradient": "linear-gradient(135deg, #2d1b69 0%, #162447 100%)"},
    {"slug": "is-someone-using-my-photo-on-dating-sites", "title": "Is Someone Using My Photo on Dating Sites?", "excerpt": "Find out if your photos are being used on dating apps and sites without your permission. AI-powered search across dating platforms.", "category": "awareness", "catLabel": "Awareness", "date": "Dec 25, 2025", "readTime": "8 min read", "emoji": "&#128148;", "gradient": "linear-gradient(135deg, #4a1942 0%, #1a1a4e 100%)"},
    {"slug": "model-portfolio-tracking", "title": "Model Portfolio Tracking \u2014 Find Where Your Photos Appear", "excerpt": "Track where your modeling portfolio photos are published online. Find unauthorized use and enforce contract terms.", "category": "guide", "catLabel": "Guide", "date": "Dec 22, 2025", "readTime": "7 min read", "emoji": "&#128248;", "gradient": "linear-gradient(135deg, #3b1f2b 0%, #162447 100%)"},
    {"slug": "online-identity-protection", "title": "Online Identity Protection \u2014 Monitor and Defend Your Digital Face", "excerpt": "Take control of your digital identity. Find where your face appears online and set up monitoring alerts for new appearances.", "category": "privacy", "catLabel": "Privacy", "date": "Dec 20, 2025", "readTime": "8 min read", "emoji": "&#128272;", "gradient": "linear-gradient(135deg, #1e3a5f 0%, #1a1a4e 100%)"},
    {"slug": "online-sextortion-what-to-do", "title": "Online Sextortion \u2014 What to Do If You Are Being Blackmailed", "excerpt": "Being threatened with intimate images? Learn the immediate steps to protect yourself, collect evidence, and report sextortion.", "category": "security", "catLabel": "Security", "date": "Dec 18, 2025", "readTime": "10 min read", "emoji": "&#128721;", "gradient": "linear-gradient(135deg, #6b2d5b 0%, #1a1a4e 100%)"},
    {"slug": "protect-photos-online", "title": "Protect Your Photos Online \u2014 Monitor and Prevent Image Theft", "excerpt": "Set up continuous monitoring for your face online. Get alerted when your photos appear on new websites.", "category": "privacy", "catLabel": "Privacy", "date": "Dec 15, 2025", "readTime": "7 min read", "emoji": "&#128274;", "gradient": "linear-gradient(135deg, #1a3c34 0%, #1a1a4e 100%)"},
    {"slug": "remove-photos-from-internet", "title": "Find and Remove Your Photos From the Internet \u2014 DIY Takedown Tools", "excerpt": "Find unauthorized photos of your face online and get the legal tools to remove them yourself.", "category": "privacy", "catLabel": "Privacy", "date": "Dec 12, 2025", "readTime": "9 min read", "emoji": "&#128465;", "gradient": "linear-gradient(135deg, #4a1942 0%, #162447 100%)"},
    {"slug": "reverse-face-search", "title": "Reverse Face Search Engine \u2014 Find Any Face Online", "excerpt": "Search the web by face, not keywords. Find where any face appears across millions of indexed pages.", "category": "guide", "catLabel": "Guide", "date": "Dec 10, 2025", "readTime": "6 min read", "emoji": "&#128269;", "gradient": "linear-gradient(135deg, #0f3460 0%, #1a1a4e 100%)"},
    {"slug": "social-media-photo-leak", "title": "Social Media Photo Leak Check \u2014 Find Where Your Photos Spread", "excerpt": "Discover if your social media photos have leaked beyond the platforms you posted them on.", "category": "awareness", "catLabel": "Awareness", "date": "Dec 8, 2025", "readTime": "8 min read", "emoji": "&#128225;", "gradient": "linear-gradient(135deg, #5c2a6e 0%, #1a1a4e 100%)"},
    {"slug": "stolen-photos-search", "title": "Someone Using My Photos? Find Stolen Images of Your Face", "excerpt": "Discover if someone is using your photos without permission. Find stolen images, catfish profiles, and unauthorized use.", "category": "awareness", "catLabel": "Awareness", "date": "Dec 5, 2025", "readTime": "7 min read", "emoji": "&#128680;", "gradient": "linear-gradient(135deg, #6b2d5b 0%, #162447 100%)"},
]


def build_js_array(articles):
    """Build a JS array string from article dicts, avoiding quote issues."""
    entries = []
    for a in articles:
        # Use single quotes for JS strings, escape any apostrophes
        def sq(s):
            return s.replace("'", "\\'")

        entry = (
            "  {\n"
            f"    slug: '{sq(a['slug'])}',\n"
            f"    title: '{sq(a['title'])}',\n"
            f"    excerpt: '{sq(a['excerpt'])}',\n"
            f"    category: '{a['category']}',\n"
            f"    catLabel: '{a['catLabel']}',\n"
            f"    date: '{a['date']}',\n"
            f"    readTime: '{a['readTime']}',\n"
            f"    emoji: '{a['emoji']}',\n"
            f"    gradient: '{a['gradient']}'\n"
            "  }"
        )
        entries.append(entry)
    return "const BLOG_POSTS = [\n" + ",\n".join(entries) + "\n];"


def main():
    with open(BLOG_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # ── Fix 1: Make blog article links absolute ──
    old_link = 'href="blog/${p.slug}.html"'
    new_link = 'href="/blog/${p.slug}.html"'

    if old_link in content:
        content = content.replace(old_link, new_link)
        changes += 1
        print('OK  Fixed link pattern: blog/ -> /blog/ (absolute)')
    elif new_link in content:
        print('SKIP  Link pattern already absolute')
    else:
        print('WARN  Could not find link pattern')

    # ── Fix 2: Replace BLOG_POSTS array ──
    pattern = r'const BLOG_POSTS = \[.*?\];'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        old_count = content[match.start():match.end()].count('slug:')
        new_array = build_js_array(ALL_ARTICLES)
        content = content[:match.start()] + new_array + content[match.end():]
        changes += 1
        print(f'OK  Updated BLOG_POSTS: {old_count} -> {len(ALL_ARTICLES)} articles')
    else:
        print('ERROR  Could not find BLOG_POSTS array')

    # ── Write ──
    if changes > 0:
        with open(BLOG_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'\nDone! {changes} change(s) applied to {BLOG_FILE}')
    else:
        print('\nNo changes needed.')


if __name__ == '__main__':
    main()
