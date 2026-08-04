# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

# Design Reference Libraries
# These repositories are curated reference libraries for UI/UX design.
# They are not executed directly but serve as knowledge sources for design decisions.

DESIGN_REFERENCES = {
    "awesome-design-md": {
        "url": "https://github.com/VoltAgent/awesome-design-md",
        "description": "73+ DESIGN.md files extracted from real websites (Vercel, Cursor, Claude, ElevenLabs, etc.)",
        "usage": "Drop a DESIGN.md into your project root. AI agents read it to generate consistent UI.",
        "categories": ["AI & LLM Platforms", "Developer Tools & IDEs", "Backend & DevOps", "SaaS Products"]
    },
    "awesome-design-skills": {
        "url": "https://github.com/bergside/awesome-design-skills",
        "description": "Registry of 67 design system skill files (SKILL.md + DESIGN.md per style).",
        "usage": "Pull any skill into your project with: npx typeui.sh pull <skill-name>",
        "preview": "https://typeui.sh/design-skills",
        "styles": [
            "agentic", "ant", "artistic", "bento", "bold", "brutalism",
            "cafe", "claymorphism", "claude", "glassmorphism", "minimalism",
            "neomorphism", "cyberpunk", "editorial", "corporate"
        ]
    }
}

def list_references():
    """List all curated design reference libraries."""
    print("\n📚 AEGIS Design Reference Libraries")
    print("=" * 60)
    for name, info in DESIGN_REFERENCES.items():
        print(f"\n  📌 {name}")
        print(f"     URL     : {info['url']}")
        print(f"     About   : {info['description']}")
        print(f"     Usage   : {info['usage']}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    list_references()
