#!/usr/bin/env python3
"""
Add structured data (ld+json) to pages missing it.
Run in your Git repo folder: python3 add_structured_data.py
"""
import json, os

STRUCTURED_DATA = {
    'contact.html': {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact Protevio AI",
        "description": "Get in touch with the Protevio AI team for questions about facial recognition search, privacy, partnerships, or support.",
        "url": "https://protevio.com/contact.html",
        "publisher": {"@type": "Organization", "name": "Protevio AI", "url": "https://protevio.com"}
    },
    'csr.html': {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Corporate Social Responsibility – Protevio AI",
        "description": "Learn about Protevio AI's commitment to ethical facial recognition, privacy protection, and responsible technology use.",
        "url": "https://protevio.com/csr.html",
        "publisher": {"@type": "Organization", "name": "Protevio AI", "url": "https://protevio.com"}
    },
    'login.html': {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Log In – Protevio AI",
        "description": "Log in to your Protevio AI account to search for your face online, manage alerts, and access your results.",
        "url": "https://protevio.com/login.html",
        "publisher": {"@type": "Organization", "name": "Protevio AI", "url": "https://protevio.com"}
    },
    'opt-out.html': {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Opt-Out Request – Remove Your Face From Protevio",
        "description": "Request removal of your facial data from Protevio AI's database. We respect your right to privacy and process all opt-out requests promptly.",
        "url": "https://protevio.com/opt-out.html",
        "publisher": {"@type": "Organization", "name": "Protevio AI", "url": "https://protevio.com"}
    },
    'privacy-policy.html': {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Privacy Policy – Protevio AI",
        "description": "Protevio AI's privacy policy. Learn how we collect, use, and protect your data, including facial recognition data and uploaded photos.",
        "url": "https://protevio.com/privacy-policy.html",
        "publisher": {"@type": "Organization", "name": "Protevio AI", "url": "https://protevio.com"}
    },
    'signup.html': {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Sign Up – Protevio AI",
        "description": "Create a free Protevio AI account. Search for your face online, set up monitoring alerts, and protect your digital identity.",
        "url": "https://protevio.com/signup.html",
        "publisher": {"@type": "Organization", "name": "Protevio AI", "url": "https://protevio.com"}
    },
    'terms-of-service.html': {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Terms of Service – Protevio AI",
        "description": "Protevio AI's terms of service. Rules governing the use of our facial recognition search engine and related services.",
        "url": "https://protevio.com/terms-of-service.html",
        "publisher": {"@type": "Organization", "name": "Protevio AI", "url": "https://protevio.com"}
    }
}

count = 0
for filename, data in STRUCTURED_DATA.items():
    if not os.path.exists(filename):
        print(f'  ✗ {filename} not found, skipping')
        continue

    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    if 'application/ld+json' in content:
        print(f'  – {filename} already has structured data, skipping')
        continue

    script_tag = '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n</script>\n</head>'
    content = content.replace('</head>', script_tag, 1)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    count += 1
    print(f'  ✓ {filename} — @type: {data["@type"]}')

print(f'\nDone. Added structured data to {count} pages.')
print('Commit: git add -A && git commit -m "Add structured data to remaining pages" && git push')
