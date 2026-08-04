# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

"""
AEGIS UI Design Engine
Wraps the ui-ux-pro-max-skill database (CSV) into a structured query interface
that integrates with the AEGIS CLI and Cognitive Pipeline.
"""

import os
import csv
import sys

SKILL_ROOT = os.path.join(os.path.dirname(__file__), "ui_design_engine", "src", "ui-ux-pro-max")
DATA_DIR = os.path.join(SKILL_ROOT, "data")

DOMAIN_FILES = {
    "style":      ("styles.csv",           ["name", "description", "css_keywords", "ai_prompt"]),
    "color":      ("colors.csv",           ["product_type", "palette_name", "hex_colors", "mood"]),
    "typography": ("typography.csv",       ["name", "heading_font", "body_font", "google_import"]),
    "chart":      ("charts.csv",           ["name", "use_case", "library", "description"]),
    "ux":         ("ux-guidelines.csv",    ["category", "guideline", "anti_pattern"]),
    "icons":      ("icons.csv",            ["library", "style", "import_snippet"]),
    "landing":    ("landing.csv",          ["section", "purpose", "cta_strategy"]),
    "product":    ("products.csv",         ["product_type", "style_recommendation", "color_suggestion"]),
    "motion":     ("motion.csv",           ["tier", "name", "gsap_snippet"]),
    "web":        ("app-interface.csv",    ["platform", "pattern", "description"]),
    "google-fonts": ("google-fonts.csv",  ["name", "category", "pairings"]),
    "react":      ("react-performance.csv", ["pattern", "description", "example"]),
}

def _load_csv(filename):
    """Load a CSV file and return rows as list of dicts."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def _score_row(row, query):
    """Simple relevance scoring: count how many query words appear in any field."""
    q_lower = query.lower()
    terms = q_lower.split()
    row_text = " ".join(str(v) for v in row.values()).lower()
    return sum(1 for t in terms if t in row_text)

def search(query, domain="style", max_results=3):
    """
    Query the UI/UX design database.
    
    Args:
        query: Search string (e.g., "dark SaaS dashboard")
        domain: One of style, color, typography, chart, ux, icons, landing, product, motion, web, google-fonts, react
        max_results: Max number of results to return

    Returns:
        List of matching dicts
    """
    if domain not in DOMAIN_FILES:
        available = ", ".join(DOMAIN_FILES.keys())
        print(f"[ERROR] Unknown domain '{domain}'. Available: {available}")
        return []

    filename, _ = DOMAIN_FILES[domain]
    rows = _load_csv(filename)
    if not rows:
        print(f"[WARN] Data file not found for domain '{domain}': {filename}")
        return []

    # Score and sort
    scored = [(r, _score_row(r, query)) for r in rows]
    scored.sort(key=lambda x: x[1], reverse=True)
    # Filter out zero-score rows if there are any hits
    top = [r for r, s in scored if s > 0][:max_results]
    if not top:
        top = [r for r, _ in scored[:max_results]]  # fallback: return top N
    return top

def run_design_query(query, domain="style", max_results=3):
    """CLI-facing function: prints design recommendations to stdout."""
    print(f"\n🎨 AEGIS UI Design Engine — Query: '{query}' | Domain: {domain}")
    print("=" * 65)

    results = search(query, domain, max_results)
    if not results:
        print("  No results found.")
        return

    for idx, row in enumerate(results, 1):
        print(f"\n  ── Result #{idx} ──────────────────────────────────────────")
        for key, val in row.items():
            if val and val.strip():
                label = key.replace("_", " ").title()
                # Truncate long values for readability
                display_val = val if len(val) < 120 else val[:117] + "..."
                print(f"  {label:<20}: {display_val}")

    print("\n" + "=" * 65)
    print(f"  {len(results)} result(s) from '{domain}' database.\n")

def list_domains():
    """Print all available search domains."""
    print("\n📚 Available UI/UX Design Domains:")
    print("=" * 45)
    for domain, (fname, _) in DOMAIN_FILES.items():
        exists = "✓" if os.path.exists(os.path.join(DATA_DIR, fname)) else "✗"
        print(f"  [{exists}] {domain:<15} → {fname}")
    print("=" * 45 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_domains()
    else:
        q = sys.argv[1]
        d = sys.argv[2] if len(sys.argv) > 2 else "style"
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        run_design_query(q, d, n)
