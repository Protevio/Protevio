#!/usr/bin/env python3
"""
Add 3 new blog articles to blog.html and sitemap.xml.
Run in your Git repo folder: python3 add_blog_posts.py
"""

import re

# =============================================================================
# 1. ADD NEW POSTS TO blog.html
# =============================================================================
with open('blog.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

NEW_POSTS = """  {
    slug: 'is-someone-using-my-photo-on-dating-sites',
    title: 'Is Someone Using My Photo on Dating Sites? How to Find Out',
    excerpt: 'Your photos could be on fake dating profiles right now. Learn how to check using facial recognition search, and what to do if you find unauthorized use.',
    category: 'security',
    catLabel: 'Security',
    date: 'Feb 18, 2026',
    readTime: '9 min read',
    emoji: '\\u{1F4AC}',
    gradient: 'linear-gradient(135deg, #1a2744 0%, #2a3349 100%)'
  },
  {
    slug: 'reverse-image-search-vs-face-recognition',
    title: 'Reverse Image Search vs Face Recognition: What\\u2019s the Difference?',
    excerpt: 'Google Images and facial recognition search solve completely different problems. Learn when to use which, and why face search finds matches Google never will.',
    category: 'guide',
    catLabel: 'Guide',
    date: 'Feb 15, 2026',
    readTime: '7 min read',
    emoji: '\\u{1F50D}',
    gradient: 'linear-gradient(135deg, #0d2137 0%, #2a3349 100%)'
  },
  {
    slug: 'online-sextortion-what-to-do',
    title: 'Online Sextortion: What to Do If Someone Threatens to Share Your Photos',
    excerpt: 'A step-by-step crisis guide for victims of sextortion. How to document evidence, report to authorities, check if images spread, and get content removed.',
    category: 'awareness',
    catLabel: 'Awareness',
    date: 'Feb 12, 2026',
    readTime: '11 min read',
    emoji: '\\u{1F6E1}',
    gradient: 'linear-gradient(135deg, #3b1f2b 0%, #1a2744 100%)'
  },
"""

# Insert new posts at the beginning of BLOG_POSTS array
old_start = "const BLOG_POSTS = [\n  {"
new_start = "const BLOG_POSTS = [\n" + NEW_POSTS + "  {"

if old_start in content:
    content = content.replace(old_start, new_start, 1)
    print('  ✓ Added 3 new blog posts to blog.html')
else:
    print('  ✗ Could not find BLOG_POSTS in blog.html')

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(content)

# =============================================================================
# 2. ADD NEW ARTICLES TO sitemap.xml
# =============================================================================
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

new_urls = [
    'https://protevio.com/blog/is-someone-using-my-photo-on-dating-sites.html',
    'https://protevio.com/blog/reverse-image-search-vs-face-recognition.html',
    'https://protevio.com/blog/online-sextortion-what-to-do.html',
]

added = 0
for url in new_urls:
    if url not in sitemap:
        entry = f"""  <url>
    <loc>{url}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        sitemap = sitemap.replace('</urlset>', entry + '</urlset>')
        added += 1

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f'  ✓ Added {added} new URLs to sitemap.xml')

print()
print('NEXT:')
print('  1. Copy the 3 new .html files into your blog/ folder')
print('  2. git add -A && git commit -m "Add 3 new blog articles" && git push')
