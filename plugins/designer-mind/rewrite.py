import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# I will construct a completely new index.html to guarantee we purge all generic SaaS patterns.
new_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Designer Mind OS — Master Edition v5.0</title>
    <meta name="description" content="Cinematic Experimental Web Design Engine.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg: #050505;
            --text-1: #ffffff;
            --text-2: #a3a3a3;
            --text-3: #525252;
            --accent: #e07a3a; /* Copper */
            
            --font-display: 'Inter', -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * {
            margin: 0; padding: 0; box-sizing: border-box;
            cursor: none;
        }

        body {
            background-color: var(--bg);
            color: var(--text-1);
            font-family: var(--font-display);
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
            line-height: 1.4;
        }

        /* Custom Cursor */
        #cursor-dot, #cursor-ring {
            position: fixed; top: 0; left: 0; transform: translate(-50%, -50%);
            border-radius: 50%; pointer-events: none; z-index: 9999;
        }
        #cursor-dot { width: 8px; height: 8px; background: var(--text-1); transition: width 0.3s, height 0.3s; }
        #cursor-ring { width: 40px; height: 40px; border: 1px solid rgba(255,255,255,0.2); transition: width 0.3s, height 0.3s, border-color 0.3s; }
        body:hover #cursor-ring { border-color: rgba(255,255,255,0.5); }
        a:hover ~ #cursor-dot, button:hover ~ #cursor-dot { width: 0; height: 0; }
        a:hover ~ #cursor-ring, button:hover ~ #cursor-ring { width: 60px; height: 60px; border-color: var(--accent); background: rgba(224,122,58,0.1); }

        /* Typography */
        h1, h2, h3 { font-weight: 800; letter-spacing: -0.03em; line-height: 1; }
        .text-massive { font-size: clamp(4rem, 10vw, 9rem); text-transform: uppercase; }
        .text-huge { font-size: clamp(3rem, 7vw, 6rem); }
        .text-large { font-size: clamp(2rem, 4vw, 3.5rem); }
        .text-sub { font-size: clamp(1rem, 1.5vw, 1.25rem); color: var(--accent); letter-spacing: 0.2em; text-transform: uppercase; font-weight: 600;}

        /* Minimal Nav */
        nav {
            position: fixed; top: 0; width: 100%; padding: 32px 48px;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 100; mix-blend-mode: difference;
        }
        .nav-logo { font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; }
        
        /* Buttons */
        .btn {
            display: inline-flex; align-items: center; justify-content: center;
            padding: 16px 32px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;
            text-decoration: none; border: 1px solid transparent; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .btn-primary { background: var(--text-1); color: var(--bg); }
        .btn-primary:hover { background: transparent; color: var(--text-1); border-color: var(--text-1); }
        
        /* Sections */
        section { position: relative; width: 100%; }
        
        /* Noise Overlay */
        .noise {
            position: fixed; inset: 0; pointer-events: none; z-index: 9000; opacity: 0.04;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        }

        /* Scroll Showcase */
        .showcase-container {
            height: 400vh; /* 4 slides */
            position: relative;
        }
        .showcase-sticky {
            position: sticky; top: 0; height: 100vh; width: 100%; overflow: hidden;
            display: flex; align-items: center; justify-content: center;
        }
        .showcase-slide {
            position: absolute; inset: 0; opacity: 0;
            display: flex; align-items: center; justify-content: center;
        }
        .showcase-slide img {
            width: 100%; height: 100%; object-fit: cover; filter: brightness(0.4);
            transform: scale(1.1); will-change: transform;
        }
        .showcase-content {
            position: absolute; z-index: 2; text-align: center;
        }
        .showcase-mask {
            position: absolute; inset: 0; background: var(--bg); transform-origin: bottom;
        }
        
        /* Editorial Manifesto */
        .manifesto {
            padding: 20vh 5vw; display: flex; flex-direction: column; gap: 15vh;
        }
        .manifesto-line {
            display: flex; flex-direction: column;
        }
        .manifesto-line p { margin-top: 24px; max-width: 600px; color: var(--text-2); font-size: 1.25rem; }
        
        .footer { padding: 20vh 5vw 10vh; text-align: center; }
    </style>
</head>
<body>
    <div id="cursor-dot"></div>
    <div id="cursor-ring"></div>
    <div class="noise"></div>

    <nav>
        <div class="nav-logo">DM OS</div>
        <a href="https://github.com/wahyunuriman999/Designer-Mind-Skill" class="text-sub" style="text-decoration:none; color:var(--text-1);">GITHUB</a>
    </nav>

    <!-- HERO -->
    <section id="hero" style="height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center;">
        <div style="position: absolute; inset: 0; z-index: 1;">
            <img src="images/01-fintech.jpg" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.25);">
            <div style="position: absolute; inset: 0; background: linear-gradient(to top, #050505 0%, transparent 40%, #050505 100%);"></div>
        </div>
        
        <div class="hero-content" style="position: relative; z-index: 3; padding: 0 24px;">
            <h1 class="text-massive hero-title" style="margin-bottom: 24px;">Designer<br>Mind OS</h1>
            <div class="text-sub hero-sub" style="margin-bottom: 40px; color: var(--accent);">MASTER EDITION V5.0</div>
            <p class="hero-p" style="font-size: 1.25rem; color: var(--text-2); max-width: 600px; margin: 0 auto 40px;">
                An elite design intelligence. We do not generate templates.<br>We design digital experiences.
            </p>
        </div>
        
        <div class="hero-scroll" style="position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); z-index: 3; color: var(--text-3); letter-spacing: 0.2em; text-transform: uppercase; font-size: 0.85rem;">
            Scroll to Experience
        </div>
    </section>

    <!-- CINEMATIC SCROLL SHOWCASE (REPLACES OUTPUT GALLERY) -->
    <section class="showcase-container" id="showcase">
        <div class="showcase-sticky">
            
            <div class="showcase-slide slide-1">
                <img src="images/02-analytics.jpg">
                <div class="showcase-content">
                    <div class="text-sub slide-sub">Data & Analytics</div>
                    <h2 class="text-huge slide-title">ABSOLUTE<br>PRECISION.</h2>
                </div>
                <div class="showcase-mask mask-1"></div>
            </div>

            <div class="showcase-slide slide-2">
                <img src="images/03-mobile-app.jpg">
                <div class="showcase-content">
                    <div class="text-sub slide-sub">Mobile Interfaces</div>
                    <h2 class="text-huge slide-title">TACTILE<br>PERFECTION.</h2>
                </div>
                <div class="showcase-mask mask-2"></div>
            </div>

            <div class="showcase-slide slide-3">
                <img src="images/04-arc.jpg">
                <div class="showcase-content">
                    <div class="text-sub slide-sub">Product Campaigns</div>
                    <h2 class="text-huge slide-title">CINEMATIC<br>REVEALS.</h2>
                </div>
                <div class="showcase-mask mask-3"></div>
            </div>

            <div class="showcase-slide slide-4">
                <img src="images/05-pottery.jpg">
                <div class="showcase-content">
                    <div class="text-sub slide-sub">Editorial Spaces</div>
                    <h2 class="text-huge slide-title">SPATIAL<br>HARMONY.</h2>
                </div>
                <div class="showcase-mask mask-4"></div>
            </div>

        </div>
    </section>

    <!-- EDITORIAL MANIFESTO (REPLACES GENERIC CARDS) -->
    <section class="manifesto">
        <div class="manifesto-line">
            <h2 class="text-huge">HIERARCHY<br>BEFORE<br>DECORATION.</h2>
            <p>We strip away the unnecessary. No meaningless gradients. No generic grids. Every pixel must earn its existence through pure visual reasoning.</p>
        </div>
        <div class="manifesto-line" style="align-items: flex-end; text-align: right;">
            <h2 class="text-huge">MOTION<br>WITH<br>PURPOSE.</h2>
            <p style="margin-left: auto; margin-right: 0;">We do not bounce or jiggle. Our motion language is rooted in cinematic camera movement, creating depth, tension, and release.</p>
        </div>
        <div class="manifesto-line">
            <h2 class="text-huge">PRODUCT<br>IS HERO.</h2>
            <p>The interface should disappear. The product should dominate. We design the stage, lighting, and atmosphere to elevate the core subject.</p>
        </div>
    </section>

    <!-- FOOTER CTA -->
    <section class="footer">
        <div class="text-sub" style="margin-bottom: 24px;">THE FINAL COMMAND</div>
        <h2 class="text-massive" style="margin-bottom: 64px;">NEVER BE<br>GENERIC.</h2>
        <a href="https://github.com/wahyunuriman999/Designer-Mind-Skill" target="_blank" class="btn btn-primary">INSTALL SKILL</a>
    </section>

    <!-- SCRIPTS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script>
        gsap.registerPlugin(ScrollTrigger);

        // Cursor Logic
        const cursorDot = document.getElementById('cursor-dot');
        const cursorRing = document.getElementById('cursor-ring');
        window.addEventListener('mousemove', (e) => {
            gsap.to(cursorDot, { x: e.clientX, y: e.clientY, duration: 0.1 });
            gsap.to(cursorRing, { x: e.clientX, y: e.clientY, duration: 0.3 });
        });

        // Hero Entrance
        const heroTl = gsap.timeline();
        heroTl
            .from('.hero-title', { y: 60, opacity: 0, duration: 1.5, ease: 'power4.out', delay: 0.2 })
            .from('.hero-sub', { y: 20, opacity: 0, duration: 1.2, ease: 'power3.out' }, '-=1')
            .from('.hero-p', { y: 20, opacity: 0, duration: 1.2, ease: 'power3.out' }, '-=0.9')
            .from('.hero-scroll', { opacity: 0, duration: 1 }, '-=0.5');

        // Cinematic Scroll Showcase (The core product gallery)
        const slides = gsap.utils.toArray('.showcase-slide');
        
        // Initial state
        gsap.set(slides[0], { opacity: 1 });
        gsap.set(slides[0].querySelector('img'), { scale: 1 });
        
        const showcaseTl = gsap.timeline({
            scrollTrigger: {
                trigger: "#showcase",
                start: "top top",
                end: "+=400%", // 4 slides
                scrub: 1,
                pin: true
            }
        });

        // Loop through slides 1 to 3 to transition FROM previous TO next
        slides.forEach((slide, i) => {
            if(i === 0) return; // Skip first slide as it's already visible
            
            const prevSlide = slides[i-1];
            const mask = slide.querySelector('.showcase-mask');
            const img = slide.querySelector('img');
            const title = slide.querySelector('.slide-title');
            const sub = slide.querySelector('.slide-sub');

            showcaseTl
                // Reveal the next slide by pulling up its mask
                .set(slide, { opacity: 1 })
                .to(mask, { scaleY: 0, duration: 1, ease: 'power2.inOut' })
                
                // Animate elements inside the new slide
                .fromTo(img, { scale: 1.2 }, { scale: 1, duration: 1.5, ease: 'power1.out' }, '-=1')
                .fromTo(title, { y: 100, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: 'power3.out' }, '-=0.8')
                .fromTo(sub, { opacity: 0 }, { opacity: 1, duration: 0.8 }, '-=0.5')
                
                // Push the previous slide image slightly for parallax depth
                .to(prevSlide.querySelector('img'), { scale: 1.1, opacity: 0.5, duration: 1 }, '-=1.5');
        });

        // Editorial Manifesto scroll reveals
        gsap.utils.toArray('.manifesto-line').forEach(line => {
            gsap.from(line.querySelectorAll('h2, p'), {
                y: 60,
                opacity: 0,
                duration: 1.2,
                stagger: 0.1,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: line,
                    start: 'top 80%'
                }
            });
        });
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Rewrote index.html for maximum cinematic purity.")
