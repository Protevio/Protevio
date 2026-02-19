#!/usr/bin/env python3
"""
Deploy: Admin newsletter endpoint + public stats endpoint for social proof
"""

SERVER_PATH = '/root/protevio/backend/server.py'

with open(SERVER_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

NEW_ENDPOINTS = '''

# ===================== ADMIN: NEWSLETTER =====================

@app.route('/api/admin/newsletter')
@require_admin
def admin_newsletter():
    """List all newsletter subscribers for admin panel"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT id, email, source, subscribed_at, unsubscribed_at 
                 FROM newsletter_subscribers ORDER BY subscribed_at DESC""")
    rows = c.fetchall()
    conn.close()
    
    subscribers = []
    for r in rows:
        subscribers.append({
            'id': r[0],
            'email': r[1],
            'source': r[2],
            'subscribed_at': str(r[3]) if r[3] else None,
            'unsubscribed_at': str(r[4]) if r[4] else None
        })
    
    return jsonify({'subscribers': subscribers})


# ===================== PUBLIC STATS (for social proof) =====================

@app.route('/api/stats/public')
@limiter.limit('30 per minute')
def public_stats():
    """Return public-facing stats for landing page social proof.
    Only returns aggregate counts, no personal data."""
    conn = get_db()
    c = conn.cursor()
    
    # Total users
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    # Total searches performed
    c.execute("SELECT COALESCE(SUM(total_searches), 0) FROM users")
    total_searches = c.fetchone()[0]
    
    # Total takedown requests
    try:
        c.execute("SELECT COUNT(*) FROM takedowns")
        total_takedowns = c.fetchone()[0]
    except:
        total_takedowns = 0
    
    # Total alerts created
    try:
        c.execute("SELECT COUNT(*) FROM alerts")
        total_alerts = c.fetchone()[0]
    except:
        total_alerts = 0
    
    conn.close()
    
    # Round down for social proof (looks more natural)
    def round_down(n, base=10):
        if n < 100: return n
        if n < 1000: return (n // 10) * 10
        return (n // 100) * 100
    
    return jsonify({
        'users': round_down(total_users),
        'searches': round_down(total_searches),
        'takedowns': total_takedowns,
        'alerts': total_alerts,
        'faces_indexed': '1.5M+'
    })

'''

main_marker = "if __name__ == '__main__':"
if '/api/admin/newsletter' not in content:
    content = content.replace(main_marker, NEW_ENDPOINTS + '\n' + main_marker)
    print("[1/1] Added admin/newsletter + public stats endpoints")
else:
    print("[1/1] Endpoints already exist")

with open(SERVER_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("""
New endpoints:
  GET /api/admin/newsletter       - List all newsletter subscribers (admin only)
  GET /api/stats/public           - Public aggregate stats for social proof

Restart: systemctl restart protevio
""")
