import os

posts_dir = r"..\aju.lu\content\posts"
tech_articles = []
tech_keywords = [
    'tech', 'cyber', 'security', 'ai', 'cloud', 'data', 'open source', 
    'software', 'linux', 'infrastructure', 'digital', 'sovereign', 
    'hacker', 'hardware', 'code', 'programming', 'network', 'system',
    'privacy', 'surveillance', 'automation', 'intelligence', 'bitcoin',
    'crypto', 'identity', 'mosbi', 'server', 'database'
]

exclude_keywords = [
    'perfume', 'masculine', 'women', 'marriage', 'meat-only', 'diet', 'red flags',
    'body language', 'dating', 'fashion', 'clothing', 'suits', 'hygiene', 'fitness',
    'testosterone', 'grooming', 'fatherhood', 'divorce', 'facial hair', 'minerals',
    'books all men should read'
]

for f in os.listdir(posts_dir):
    if not f.endswith(".md") or f == "_index.md":
        continue
    p = os.path.join(posts_dir, f)
    with open(p, encoding="utf-8", errors="ignore") as fp:
        txt = fp.read()
    
    lines = txt.split("\n")
    title = f
    date = ""
    tags = ""
    in_fm = False
    for line in lines[:30]:
        line_s = line.strip()
        if line_s == "---":
            if not in_fm:
                in_fm = True
            else:
                break
        elif in_fm and line_s.startswith("title:"):
            title = line_s.split("title:", 1)[1].strip().strip("\"'")
        elif in_fm and line_s.startswith("date:"):
            date = line_s.split("date:", 1)[1].strip().strip("\"'")
        elif in_fm and (line_s.startswith("tags:") or line_s.startswith("categories:")):
            tags += " " + line_s
            
    meta = (title + " " + tags + " " + f).lower()
    
    # Exclude non-tech lifestyle articles
    if any(ex in meta for ex in exclude_keywords):
        continue
        
    if any(k in meta for k in tech_keywords):
        tech_articles.append((date, title, f, len(txt)))

tech_articles.sort(key=lambda x: x[0], reverse=True)
print("Total tech articles found:", len(tech_articles))
for d, t, f, l in tech_articles:
    print(f"{d[:10]:10} | {t} | {f} ({l} chars)")
