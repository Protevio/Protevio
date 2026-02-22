#!/usr/bin/env python3
"""
Fix blog article paths for /blog/ subfolder deployment.

Run from your protevio-deploy root:
    python3 fix_blog_paths.py

Fixes:
1. Nav/footer links in blog articles: about.html → /about.html
2. Canonical URLs: protevio.com/slug.html → protevio.com/blog/slug.html
3. Sitemap URLs: same canonical fix
"""

import os
import re
import glob

BLOG_DIR = 'blog'
SITEMAP = 'sitemap.xml'
DOMAIN = 'https://protevio.com'

# Relative links that need to become absolute (these are root-level pages)
ROOT_PAGES = [
    'about.html', 'pricing.html', 'blog.html', 'faq.html',
    'contact.html', 'login.html', 'opt-out.html', 'signup.html',
    'dashboard.html', 'results.html', 'forgot-password.html',
    'reset-password.html', 'verify-email.html', 'check-email.html',
    'privacy-policy.html', 'terms-of-service.html', 'csr.html',
    'dmca-templates.html', 'index.html',
]

def fix_blog_articles():
    """Fix relative links and canonical URLs in all blog articles."""
    if not os.path.isdir(BLOG_DIR):
        print(f'ERROR  {BLOG_DIR}/ folder not found. Run this from protevio-deploy root.')
        return False

    files = glob.glob(os.path.join(BLOG_DIR, '*.html'))
    if not files:
        print(f'ERROR  No .html files found in {BLOG_DIR}/')
        return False

    print(f'Found {len(files)} blog articles in {BLOG_DIR}/\n')
    fixed_count = 0

    for filepath in sorted(files):
        filename = os.path.basename(filepath)
        slug = filename.replace('.html', '')

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        changes = []

        # 1. Fix relative nav/footer links → absolute
        for page in ROOT_PAGES:
            # href="about.html" → href="/about.html"
            old = f'href="{page}"'
            new = f'href="/{page}"'
            if old in content:
                content = content.replace(old, new)
                changes.append(f'  {page} → /{page}')

            # Also fix any src= references (rare but possible)
            old_src = f'src="{page}"'
            new_src = f'src="/{page}"'
            if old_src in content:
                content = content.replace(old_src, new_src)

        # 2. Fix canonical URL: protevio.com/slug.html → protevio.com/blog/slug.html
        old_canonical = f'{DOMAIN}/{slug}.html'
        new_canonical = f'{DOMAIN}/blog/{slug}.html'
        if old_canonical in content:
            content = content.replace(old_canonical, new_canonical)
            changes.append(f'  canonical → /blog/{slug}.html')

        # 3. Fix og:url if present
        old_og = f'content="{DOMAIN}/{slug}.html"'
        new_og = f'content="{DOMAIN}/blog/{slug}.html"'
        if old_og in content:
            content = content.replace(old_og, new_og)
            changes.append(f'  og:url → /blog/{slug}.html')

        # 4. Fix any JS that references dashboard.html relatively
        if 'n.href="dashboard.html"' in content:
            content = content.replace('n.href="dashboard.html"', 'n.href="/dashboard.html"')
            changes.append('  JS dashboard.html → /dashboard.html')
        if 'm.href="dashboard.html"' in content:
            content = content.replace('m.href="dashboard.html"', 'm.href="/dashboard.html"')

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'OK  {filename}')
            for c in changes:
                print(c)
            fixed_count += 1
        else:
            print(f'SKIP  {filename} (no changes needed)')

    print(f'\nFixed {fixed_count}/{len(files)} articles')
    return True


def fix_sitemap():
    """Update sitemap.xml blog article URLs to include /blog/ prefix."""
    if not os.path.isfile(SITEMAP):
        print(f'\nWARN  {SITEMAP} not found, skipping')
        return

    # Get list of blog article slugs
    blog_files = glob.glob(os.path.join(BLOG_DIR, '*.html'))
    slugs = [os.path.basename(f).replace('.html', '') for f in blog_files]

    with open(SITEMAP, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixed = 0

    for slug in slugs:
        old_url = f'{DOMAIN}/{slug}.html'
        new_url = f'{DOMAIN}/blog/{slug}.html'
        if old_url in content:
            content = content.replace(old_url, new_url)
            fixed += 1

    if content != original:
        with open(SITEMAP, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'\nOK  sitemap.xml — updated {fixed} blog article URLs')
    else:
        print(f'\nSKIP  sitemap.xml (no changes needed)')


def verify():
    """Quick verification that no broken relative links remain."""
    print('\n=== Verification ===')
    issues = 0
    for filepath in glob.glob(os.path.join(BLOG_DIR, '*.html')):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = os.path.basename(filepath)
        for page in ROOT_PAGES:
            # Check for remaining bare relative links (not prefixed with /)
            pattern = f'href="{page}"'
            if pattern in content:
                print(f'  WARN  {filename} still has relative: {page}')
                issues += 1

    if issues == 0:
        print('  ALL CLEAR — no broken relative links found')
    else:
        print(f'  {issues} issues remaining')


if __name__ == '__main__':
    print('=' * 50)
    print('  Blog Path Fixer for /blog/ subfolder')
    print('=' * 50)
    print()

    if fix_blog_articles():
        fix_sitemap()
        verify()

    print('\nDone! Commit and push to deploy.')
