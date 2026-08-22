import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace variables
content = content.replace("--purple: #8b5cf6;", "--purple: #e07a3a; /* remapped to copper */")
content = content.replace("--purple-glow: rgba(139, 92, 246, 0.3);", "--purple-glow: rgba(224, 122, 58, 0.3); /* remapped */")

# Title gradient
content = content.replace("var(--purple) 100%", "var(--copper) 100%")

# Linear gradients
content = content.replace("var(--accent), var(--purple)", "var(--accent), var(--copper)")

# #1a0a2e is the purple background section. Let's make it a dark teal #040d0a or dark copper #1a0f0a
content = content.replace("#1a0a2e", "#050505")

# Globe colors (rgba(139, 92, 246...)
content = content.replace("rgba(139, 92, 246, 0.5)", "rgba(224, 122, 58, 0.5)")
content = content.replace("rgba(139, 92, 246, 0.2)", "rgba(224, 122, 58, 0.2)")
content = content.replace("rgba(139, 92, 246, 0.12)", "rgba(224, 122, 58, 0.12)")
content = content.replace("rgba(139,92,246,0.9)", "rgba(224,122,58,0.9)")
content = content.replace("rgba(139,92,246,0.4)", "rgba(224,122,58,0.4)")

# Palette section
content = content.replace("Electric Purple", "Deep Copper")
content = content.replace("#8b5cf6", "#e07a3a")

# The word "purple" in class names
content = content.replace("marquee-item purple", "marquee-item copper")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced all purple with copper/dark theme in index.html")
