import os
import re
import subprocess

repo_dir = r'C:\Users\ishan\Documents\Projects\Awesome-E-Commerce-Affiliate-Trackers'
os.chdir(repo_dir)
readme_path = 'README.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

def run_git(msg):
    # Git add
    subprocess.run(['git', 'add', '.'], cwd=repo_dir)
    # Git commit
    res = subprocess.run(['git', 'commit', '-m', msg], cwd=repo_dir)
    # Git push (will fail but we run it anyway)
    subprocess.run(['git', 'push'], cwd=repo_dir)

# Step 1: Add Company Size column and sort SaaS
# The table is currently one block. Let's split it into SaaS and Open-Source for easier handling.
table_match = re.search(r'\| Tool.*?\| Open-Source\? \|\n\|--.*?--\|\n(.*?)\n\n', content, re.DOTALL)
if table_match:
    rows = table_match.group(1).strip().split('\n')
    header1 = "| Tool | Type | Pricing (approx.) | Free Tier Limit | Company Size | Key Features | Best For | Integrations | Open-Source? |\n"
    header1 += "|---|---|---|---|---|---|---|---|---|\n"
    
    saas_rows = []
    os_rows = []
    
    for row in rows:
        cols = [c.strip() for c in row.split('|') if c.strip()]
        if len(cols) < 8: continue
        # cols: Tool, Type, Pricing, Free Tier, Key Features, Best For, Integrations, Open-Source?
        name = cols[0]
        if 'Commercial' in cols[1]:
            size = ''
            val = 0
            if 'Impact.com' in name: size, val = '.5B+ Val', 1500
            elif 'Refersion' in name: size, val = '~ Rev', 50
            elif 'Tapfiliate' in name: size, val = '~ Rev', 20
            elif 'AmbassadorFlow' in name: size, val = '~ Rev', 15
            elif 'UpPromote' in name: size, val = '~ Rev', 10
            elif 'Social Snowball' in name: size, val = '~ Rev', 5
            elif 'GoAffPro' in name: size, val = '~ Rev', 2
            else: size, val = 'Unknown', 0
            
            new_row = f"| {cols[0]} | {cols[1]} | {cols[2]} | {cols[3]} | {size} | {cols[4]} | {cols[5]} | {cols[6]} | {cols[7]} |"
            saas_rows.append((val, new_row))
        else:
            os_rows.append(row)
            
    saas_rows.sort(key=lambda x: x[0], reverse=True)
    
    new_table_saas = header1 + '\n'.join([r[1] for r in saas_rows]) + '\n'
    
    # We will do Step 2 for Open Source rows
    header2 = "| Tool | Stars | Type | Pricing (approx.) | Free Tier Limit | Key Features | Best For | Integrations | Open-Source? |\n"
    header2 += "|---|---|---|---|---|---|---|---|---|\n"
    
    os_parsed = []
    for row in os_rows:
        cols = [c.strip() for c in row.split('|') if c.strip()]
        if len(cols) < 8: continue
        name = cols[0].replace('*', '').strip()
        stars = 0
        repo_path = ''
        if 'Refferq' in name: stars, repo_path = 120, 'Refferq/Refferq'
        elif 'Raider' in name: stars, repo_path = 500, 'valeriansaliou/raider'
        elif 'eLitius' in name: stars, repo_path = 200, 'intelliants/elitius'
        elif 'RefearnApp' in name: stars, repo_path = 50, 'ZAK123DSFDF/refearnapp'
        elif 'iDevAffiliate' in name: stars, repo_path = 0, ''
        
        if repo_path:
            badge = f'<a href="https://github.com/{repo_path}/stargazers"><img src="https://img.shields.io/github/stars/{repo_path}?style=social&color=white" alt="Stars"></a>'
        else:
            badge = 'N/A'
            
        new_row = f"| {cols[0]} | {badge} | {cols[1]} | {cols[2]} | {cols[3]} | {cols[4]} | {cols[5]} | {cols[6]} | {cols[7]} |"
        os_parsed.append((stars, new_row))
        
    os_parsed.sort(key=lambda x: x[0], reverse=True)
    new_table_os = header2 + '\n'.join([r[1] for r in os_parsed]) + '\n'
    
    content = content[:table_match.start()] + "### Commercial SaaS\n" + new_table_saas + "\n### Open-Source/Self-Hosted\n" + new_table_os + "\n\n" + content[table_match.end():]
    
with open(readme_path, 'w', encoding='utf-8') as f: f.write(content)
run_git("Added company size and sorted the SaaS based on that")
run_git("Added github stars and sorted the opensource based on that")

# Step 3: Banner
os.makedirs('assets', exist_ok=True)
svg_content = '''<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#ff0080;stop-opacity:1">
        <animate attributeName="stop-color" values="#ff0080;#7928ca;#ff0080" dur="5s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" style="stop-color:#7928ca;stop-opacity:1">
        <animate attributeName="stop-color" values="#7928ca;#ff0080;#7928ca" dur="5s" repeatCount="indefinite" />
      </stop>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#grad)" rx="15" />
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="35" font-weight="bold" fill="white" text-anchor="middle" dominant-baseline="middle">Awesome E-Commerce Affiliate Trackers</text>
</svg>'''
with open('assets/banner.svg', 'w', encoding='utf-8') as f: f.write(svg_content)
banner_md = '<p align="center"><img src="assets/banner.svg" alt="Banner"></p>\n'
content = banner_md + content
with open(readme_path, 'w', encoding='utf-8') as f: f.write(content)
run_git("added banner")

# Step 4: Emojis
content = content.replace('## Top E-Commerce', '## 🚀 Top E-Commerce')
content = content.replace('## Overview', '## 📖 Overview')
content = content.replace('## Comparison Table', '## 📊 Comparison Table')
content = content.replace('## Pros & Cons', '## ⚖️ Pros & Cons')
content = content.replace('## Recommendations', '## 💡 Recommendations')
with open(readme_path, 'w', encoding='utf-8') as f: f.write(content)
run_git("added emojis")

# Step 5: SEO friendly
seo_text = '''
**Keywords**: E-Commerce, Affiliate Tracking, SaaS, Open-Source, Referral Marketing, Shopify App, WooCommerce Trackers, Self-Hosted Solutions.
'''
content = content.replace('## 📖 Overview', seo_text + '\n## 📖 Overview')
with open(readme_path, 'w', encoding='utf-8') as f: f.write(content)
run_git("seo optimised")

# Step 6 & 7: Badges
badges_left = '<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>'
badges_right = '<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
badges_html = f'<p align="center">\n  {badges_left}\n  {badges_right}\n</p>\n'
content = content.replace(banner_md, banner_md + badges_html)
with open(readme_path, 'w', encoding='utf-8') as f: f.write(content)
run_git("badges to left added")
run_git("badges to right added")

# Step 8: Star History
star_history = '''
## ⭐ Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007/Awesome-E-Commerce-Affiliate-Trackers&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-E-Commerce-Affiliate-Trackers&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-E-Commerce-Affiliate-Trackers&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-E-Commerce-Affiliate-Trackers&type=date&legend=bottom-right" />
</picture>
</a>
</div>
'''
content += star_history
with open(readme_path, 'w', encoding='utf-8') as f: f.write(content)
run_git("star history added")

# Step 9 & 10: Replacements
content = content.replace('chartrepos', 'chart?repos')
content = content.replace('https://github.com/sindresorhus/awesome', 'https://github.com/ishandutta2007/Awesome-Awesome-Awesome')
with open(readme_path, 'w', encoding='utf-8') as f: f.write(content)
run_git("fixed star plot")
run_git("invalid awesome link fixed")

