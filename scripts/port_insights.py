import os
import re

SRC_DIR = r"..\aju.lu\content\posts"
DST_DIR = r"content\blog"

# Articles to port
FEATURED_ARTICLES = [
    {
        "src": "the-great-cloud-exit.md",
        "dst": "the-great-cloud-exit.md",
        "image": "images/posts/cloud_exit_hero.jpg"
    },
    {
        "src": "enterprise-grade-open-source.md",
        "dst": "enterprise-grade-open-source.md",
        "image": "images/posts/open_source_hero.jpg"
    },
    {
        "src": "blueprint-digital-sovereignty.md",
        "dst": "blueprint-digital-sovereignty.md",
        "image": "images/posts/digital_sovereignty_hero.jpg"
    },
    {
        "src": "the-era-of-personal-software.md",
        "dst": "the-saaspocalypse-and-personal-software.md",
        "image": "images/posts/saaspocalypse_hero.jpg"
    },
    {
        "src": "sovereign-cyberdeck-decentralized-mesh.md",
        "dst": "the-sovereign-cyberdeck.md",
        "image": "images/posts/sovereign_cyberdeck.jpg"
    },
    {
        "src": "how-ai-is-killing-open-source.md",
        "dst": "the-tragedy-of-the-digital-commons.md",
        "image": "images/posts/digital_commons_tragedy_hero.jpg"
    },
    {
        "src": "personal-ai-infrastructure-cognitive-sovereignty.md",
        "dst": "personal-ai-infrastructure.md",
        "image": "images/posts/personal_ai_hero.jpg"
    },
    {
        "src": "web-2-3-5-sovereignty-architecture.md",
        "dst": "web-2-3-5-sovereignty-architecture.md",
        "image": "images/posts/web_evolution_sovereignty.jpg"
    },
    {
        "src": "biomimetic-code-resilient-networks.md",
        "dst": "biomimetic-code-resilient-networks.md",
        "image": "images/posts/biomimetic_network_hero.jpg"
    },
    {
        "src": "solarpunk-architectures-tech-nature.md",
        "dst": "solarpunk-architectures.md",
        "image": "images/posts/solarpunk_architecture_hero.jpg"
    },
    {
        "src": "cybernetic-horizon-human-autonomy.md",
        "dst": "the-cybernetic-horizon.md",
        "image": "images/posts/cybernetic_autonomy_hero.jpg"
    }
]

DUMMY_FILES = [
    "function-of-design.md",
    "interior-designer.md",
    "street-photography.md",
    "why-fonts-matter.md",
    "working-from-home.md",
    "workplace.md"
]

def clean_frontmatter(content):
    # Split frontmatter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_raw = parts[1]
    body = parts[2].strip()
    
    metadata = {}
    for line in fm_raw.split("\n"):
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip("\"'")
            metadata[key] = val
    return metadata, body

def main():
    # 1. Delete dummy posts
    for d in DUMMY_FILES:
        dp = os.path.join(DST_DIR, d)
        if os.path.exists(dp):
            os.remove(dp)
            print(f"Removed dummy insight: {d}")
            
    # 2. Port and format real tech articles
    for item in FEATURED_ARTICLES:
        src_path = os.path.join(SRC_DIR, item["src"])
        if not os.path.exists(src_path):
            print(f"Source not found: {src_path}")
            continue
            
        with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
            
        meta, body = clean_frontmatter(raw_text)
        
        title = meta.get("title", item["dst"].replace(".md", "").replace("-", " ").title())
        subtitle = meta.get("subtitle", "")
        description = meta.get("description", subtitle)
        date_str = meta.get("date", "2026-07-14")
        if "T" in date_str:
            date_str = date_str.split("T")[0]
            
        excerpt = description if description else subtitle
        if len(excerpt) > 180:
            excerpt = excerpt[:177] + "..."
            
        img_path = item["image"]
        
        # Build new post content with julz.co1 frontmatter schema
        new_fm = f"""---
title: "{title}"
subtitle: "{subtitle}"
excerpt: >-
  {excerpt}
date: '{date_str}'
thumb_image: {img_path}
thumb_image_alt: "{title}"
image: {img_path}
image_alt: "{title}"
seo:
  title: "{title} | JULZ Insights"
  description: >-
    {excerpt}
  extra:
    - name: 'og:type'
      value: article
      keyName: property
    - name: 'og:title'
      value: "{title} | JULZ Insights"
      keyName: property
    - name: 'og:description'
      value: >-
        {excerpt}
      keyName: property
    - name: 'og:image'
      value: {img_path}
      keyName: property
      relativeUrl: true
    - name: 'twitter:card'
      value: summary_large_image
    - name: 'twitter:title'
      value: "{title} | JULZ Insights"
    - name: 'twitter:description'
      value: >-
        {excerpt}
    - name: 'twitter:image'
      value: {img_path}
      relativeUrl: true
layout: post
---

{body}
"""
        dst_path = os.path.join(DST_DIR, item["dst"])
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(new_fm)
        print(f"Ported real insight: {item['dst']}")

if __name__ == "__main__":
    main()
