import os
import io
import math
import numpy as np
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "static/images/ventures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VENTURES = [
    {
        "id": "julz-insight",
        "name": "Julz Insight",
        "category": "DIGITAL TRANSFORMATION & IT ADVISORY",
        "tagline": "Enterprise Cloud Architecture & Sovereign Digitalization",
        "primary_color": (84, 43, 255),       # #542bff
        "secondary_color": (67, 32, 214),     # #4320d6
        "accent_color": (0, 242, 254),        # #00f2fe
        "logo_file": "venture_logos/Julz Insight.svg",
        "logo_type": "svg"
    },
    {
        "id": "tausinode",
        "name": "TausiNode",
        "category": "HARDWARE APPLIANCES & MOSBI",
        "tagline": "Managed Open-Source Business Infrastructure & Turnkey Mini PCs",
        "primary_color": (84, 43, 255),       # #542bff
        "secondary_color": (99, 32, 214),     # #6320d6
        "accent_color": (165, 138, 255),
        "logo_file": "venture_logos/TausiNode.png",
        "logo_type": "png_white"
    },
    {
        "id": "aju-studio",
        "name": "AJU studio",
        "category": "BESPOKE DESIGN ATELIER",
        "tagline": "Brand Identity, Digital Experiences & Industrial Design",
        "primary_color": (242, 44, 54),       # #f22c36
        "secondary_color": (153, 21, 28),     # #99151c
        "accent_color": (255, 99, 108),
        "logo_file": "venture_logos/AJU studio.png",
        "logo_type": "png_gray"
    },
    {
        "id": "fulcrum",
        "name": "Fulcrum",
        "category": "PRODUCTION & MEDIA LAB",
        "tagline": "Cinematic Visuals, Aerial Cinematography & Content Systems",
        "primary_color": (84, 43, 255),       # #542bff
        "secondary_color": (30, 16, 94),
        "accent_color": (120, 90, 255),
        "logo_file": "venture_logos/FULCRUM.png",
        "logo_type": "png_white"
    },
    {
        "id": "this",
        "name": "THIS",
        "category": "TROPICAL HEALTH BIOINFORMATICS",
        "tagline": "Tropical Health Information System & Botanical Pharmacology",
        "primary_color": (134, 59, 255),      # #863bff
        "secondary_color": (126, 20, 255),    # #7e14ff
        "accent_color": (71, 191, 255),       # #47bfff
        "logo_file": "venture_logos/THIS.svg",
        "logo_type": "svg"
    },
    {
        "id": "hyvaros",
        "name": "Hyvaros",
        "category": "AUTONOMOUS AI & AUTOMATION",
        "tagline": "Cognitive Agent Networks & Intelligent Process Automation",
        "primary_color": (143, 63, 179),      # #8f3fb3
        "secondary_color": (74, 21, 102),
        "accent_color": (210, 130, 255),
        "logo_file": "venture_logos/Hyvaros.png",
        "logo_type": "png_black"
    },
    {
        "id": "biomeid",
        "name": "BiomeID",
        "category": "SOVEREIGN DIGITAL IDENTITY",
        "tagline": "National Blockchain Identity Protocol & Decentralized Ledger",
        "primary_color": (0, 180, 216),       # #00b4d8
        "secondary_color": (0, 119, 182),
        "accent_color": (72, 202, 228),
        "logo_file": "venture_logos/BiomeID.png",
        "logo_type": "png_black"
    },
    {
        "id": "bioemergency",
        "name": "BioEmergency",
        "category": "EMERGENCY BIOMETRICS",
        "tagline": "Zero-Knowledge Biometric Emergency Vault & Vital Marker Ledger",
        "primary_color": (0, 229, 163),       # #00e5a3
        "secondary_color": (0, 122, 86),
        "accent_color": (114, 255, 209),
        "logo_file": "venture_logos/BioEmergency.png",
        "logo_type": "png_white"
    },
    {
        "id": "eden-julz",
        "name": "Eden Julz",
        "category": "EDENIC ARCHITECTURE & PROPERTY",
        "tagline": "Biophilic Sustainable Real Estate & Ecological Systems",
        "primary_color": (16, 185, 129),      # #10b981
        "secondary_color": (4, 120, 87),
        "accent_color": (110, 231, 183),
        "logo_file": "venture_logos/Eden Julz.png",
        "logo_type": "png_gray"
    },
    {
        "id": "owlsec",
        "name": "OwlSec Technologies",
        "category": "CYBERSECURITY & DEFENSE",
        "tagline": "Offensive Security Auditing & Mission-Critical IT Infrastructure",
        "primary_color": (245, 158, 11),      # #f59e0b
        "secondary_color": (180, 83, 9),
        "accent_color": (252, 211, 77),
        "logo_file": None,
        "logo_type": "vector_owlsec"
    },
    {
        "id": "nairobyke",
        "name": "Nairobyke",
        "category": "URBAN HARDWARE MOBILITY",
        "tagline": "Connected Urban Electric Bike Transit & Solar Swapping Network",
        "primary_color": (6, 182, 212),       # #06b6d4
        "secondary_color": (14, 116, 144),
        "accent_color": (103, 232, 249),
        "logo_file": None,
        "logo_type": "vector_nairobyke"
    },
    {
        "id": "alusa-ss",
        "name": "Alusa SS Investments",
        "category": "INFRASTRUCTURE & LOGISTICS",
        "tagline": "Strategic Industrial Procurement, Civil Engineering & Construction",
        "primary_color": (100, 116, 139),     # #64748b
        "secondary_color": (51, 65, 85),
        "accent_color": (148, 163, 184),
        "logo_file": None,
        "logo_type": "vector_alusa"
    }
]

# Fonts
FONT_BOLD = "C:\\Windows\\Fonts\\segoeuib.ttf"
FONT_REGULAR = "C:\\Windows\\Fonts\\segoeui.ttf"
FONT_MONO = "C:\\Windows\\Fonts\\consolab.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_title = get_font(FONT_BOLD, 44)
font_category = get_font(FONT_MONO, 14)
font_tagline = get_font(FONT_REGULAR, 19)
font_meta = get_font(FONT_MONO, 12)

def extract_logo(venture):
    logo_type = venture["logo_type"]
    file_path = venture["logo_file"]
    
    if logo_type == "svg":
        doc = fitz.open(file_path)
        page = doc[0]
        rect = page.rect
        zoom = 500.0 / max(rect.width, rect.height)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=True)
        im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")
        return im
        
    elif logo_type in ["png_white", "png_gray", "png_black"]:
        im = Image.open(file_path).convert("RGBA")
        # Resize first if very large to optimize speed
        if max(im.width, im.height) > 1500:
            scale = 1200.0 / max(im.width, im.height)
            im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
            
        arr = np.array(im, dtype=float)
        
        if logo_type == "png_white":
            diff = 255.0 - arr[:,:,:3].mean(axis=-1)
            alpha = np.clip((diff - 8.0) * 8.0, 0, 255)
            # Lighten purely dark/black elements for dark card contrast
            sat = arr[:,:,:3].max(axis=-1) - arr[:,:,:3].min(axis=-1)
            brightness = arr[:,:,:3].mean(axis=-1)
            is_dark_mono = (brightness < 90) & (sat < 30)
            for i in range(3):
                arr[:,:,i] = np.where(is_dark_mono, 245, arr[:,:,i])
            arr[:,:,3] = alpha
            
        elif logo_type == "png_gray":
            corner = arr[0, 0, :3]
            diff = np.abs(arr[:,:,:3] - corner).max(axis=-1)
            alpha = np.clip((diff - 12.0) * 8.0, 0, 255)
            sat = arr[:,:,:3].max(axis=-1) - arr[:,:,:3].min(axis=-1)
            brightness = arr[:,:,:3].mean(axis=-1)
            is_dark_mono = (brightness < 80) & (sat < 30)
            for i in range(3):
                arr[:,:,i] = np.where(is_dark_mono, 240, arr[:,:,i])
            arr[:,:,3] = alpha
            
        elif logo_type == "png_black":
            diff = arr[:,:,:3].max(axis=-1)
            alpha = np.clip((diff - 12.0) * 6.0, 0, 255)
            arr[:,:,3] = alpha
            
        out = Image.fromarray(arr.astype(np.uint8))
        bbox = out.getbbox()
        if bbox:
            out = out.crop(bbox)
        return out
        
    else:
        # Vector procedural icon
        size = (400, 400)
        im = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        p = venture["primary_color"]
        s = venture["secondary_color"]
        a = venture["accent_color"]
        
        if logo_type == "vector_owlsec":
            draw.polygon([(200, 30), (360, 110), (360, 280), (200, 370), (40, 280), (40, 110)], outline=p, width=12)
            draw.polygon([(200, 70), (320, 130), (320, 260), (200, 330), (80, 260), (80, 130)], fill=(p[0]//5, p[1]//5, p[2]//5, 200), outline=a, width=4)
            draw.ellipse([120, 160, 180, 220], fill=p)
            draw.ellipse([220, 160, 280, 220], fill=p)
            draw.ellipse([140, 180, 160, 200], fill=(255, 255, 255))
            draw.ellipse([240, 180, 260, 200], fill=(255, 255, 255))
            draw.polygon([(185, 230), (215, 230), (200, 270)], fill=(255, 255, 255))
        elif logo_type == "vector_nairobyke":
            draw.ellipse([50, 180, 190, 320], outline=p, width=14)
            draw.ellipse([210, 180, 350, 320], outline=p, width=14)
            draw.line([(120, 250), (200, 140), (280, 250)], fill=(255, 255, 255), width=10)
            draw.line([(200, 140), (220, 90), (180, 90)], fill=a, width=10)
            draw.line([(120, 250), (280, 250)], fill=p, width=8)
            draw.line([(200, 140), (160, 250)], fill=(255, 255, 255), width=8)
        elif logo_type == "vector_alusa":
            draw.polygon([(200, 50), (340, 130), (200, 210), (60, 130)], fill=(180, 195, 210), outline=p, width=6)
            draw.polygon([(60, 130), (200, 210), (200, 350), (60, 270)], fill=(110, 125, 145), outline=p, width=6)
            draw.polygon([(340, 130), (200, 210), (200, 350), (340, 270)], fill=(70, 85, 105), outline=p, width=6)
            
        return im

def create_mesh_gradient_cover(venture):
    W, H = 1200, 675
    p_col = venture["primary_color"]
    s_col = venture["secondary_color"]
    a_col = venture["accent_color"]
    
    # 1. Base Obsidian Void Canvas
    card = Image.new("RGBA", (W, H), (7, 8, 12, 255))
    
    # 2. Multi-Node Mesh Gradient Synthesis
    # Node 1: Primary Brand Mesh Node (upper-right focal zone)
    mesh_1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(mesh_1)
    n1_x, n1_y = int(W * 0.68), int(H * 0.42)
    r1 = 380
    for r in range(r1, 0, -20):
        alpha = int(75 * (1 - (r / r1) ** 1.2))
        d1.ellipse([n1_x - r, n1_y - r, n1_x + r, n1_y + r], fill=(p_col[0], p_col[1], p_col[2], alpha))
    mesh_1 = mesh_1.filter(ImageFilter.GaussianBlur(50))
    card = Image.alpha_composite(card, mesh_1)
    
    # Node 2: Secondary Tone Mesh Node (lower-center/left)
    mesh_2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(mesh_2)
    n2_x, n2_y = int(W * 0.45), int(H * 0.65)
    r2 = 320
    for r in range(r2, 0, -20):
        alpha = int(45 * (1 - (r / r2) ** 1.3))
        d2.ellipse([n2_x - r, n2_y - r, n2_x + r, n2_y + r], fill=(s_col[0], s_col[1], s_col[2], alpha))
    mesh_2 = mesh_2.filter(ImageFilter.GaussianBlur(60))
    card = Image.alpha_composite(card, mesh_2)
    
    # Node 3: Vivid Accent Pinpoint Bloom (upper focal accent)
    mesh_3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(mesh_3)
    n3_x, n3_y = int(W * 0.78), int(H * 0.28)
    r3 = 220
    for r in range(r3, 0, -15):
        alpha = int(35 * (1 - (r / r3) ** 1.4))
        d3.ellipse([n3_x - r, n3_y - r, n3_x + r, n3_y + r], fill=(a_col[0], a_col[1], a_col[2], alpha))
    mesh_3 = mesh_3.filter(ImageFilter.GaussianBlur(40))
    card = Image.alpha_composite(card, mesh_3)
    
    # 3. Fine Geometric Texture & Subtle Grid
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Subtle 60px grid
    grid_gap = 60
    for x in range(0, W, grid_gap):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, H, grid_gap):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 6), width=1)
        
    # Concentric aura rings around focal point
    for rad in [160, 240, 320]:
        draw.ellipse([n1_x - rad, n1_y - rad, n1_x + rad, n1_y + rad], outline=(p_col[0], p_col[1], p_col[2], 28), width=1)
        
    # Architectural 1px hairline border
    draw.rectangle([20, 20, W - 20, H - 20], outline=(255, 255, 255, 20), width=1)
    
    # Corner brackets in brand color
    c_len = 20
    c_col = (p_col[0], p_col[1], p_col[2], 160)
    # top left
    draw.line([(20, 20), (20 + c_len, 20)], fill=c_col, width=2)
    draw.line([(20, 20), (20, 20 + c_len)], fill=c_col, width=2)
    # top right
    draw.line([(W - 20, 20), (W - 20 - c_len, 20)], fill=c_col, width=2)
    draw.line([(W - 20, 20), (W - 20, 20 + c_len)], fill=c_col, width=2)
    # bottom left
    draw.line([(20, H - 20), (20 + c_len, H - 20)], fill=c_col, width=2)
    draw.line([(20, H - 20), (20, H - 20 - c_len)], fill=c_col, width=2)
    # bottom right
    draw.line([(W - 20, H - 20), (W - 20 - c_len, H - 20)], fill=c_col, width=2)
    draw.line([(W - 20, H - 20), (W - 20, H - 20 - c_len)], fill=c_col, width=2)
    
    card = Image.alpha_composite(card, overlay)
    
    # 4. Venture Logo Composition
    logo = extract_logo(venture)
    if logo:
        max_lw, max_lh = 360, 250
        scale = min(max_lw / logo.width, max_lh / logo.height)
        new_w, new_h = int(logo.width * scale), int(logo.height * scale)
        logo_resized = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        lx = n1_x - new_w // 2
        ly = n1_y - new_h // 2
        
        # Soft ambient glow behind logo
        logo_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        logo_mask = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        logo_mask.paste(logo_resized, (lx, ly), logo_resized)
        
        halo_arr = np.array(logo_mask)
        if halo_arr[:,:,3].max() > 0:
            halo_arr[:,:,0] = p_col[0]
            halo_arr[:,:,1] = p_col[1]
            halo_arr[:,:,2] = p_col[2]
            halo_im = Image.fromarray(halo_arr).filter(ImageFilter.GaussianBlur(28))
            card = Image.alpha_composite(card, halo_im)
            
        card.paste(logo_resized, (lx, ly), logo_resized)
        
    # 5. High-Craft Typography Overlay
    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_layer)
    
    # Top Left Category & Taxonomy Badge
    tdraw.text((54, 52), "JULZ VENTURES", font=font_meta, fill=(p_col[0], p_col[1], p_col[2], 255))
    tdraw.text((54, 76), venture["category"], font=font_category, fill=(190, 200, 220, 220))
    
    # Top Right System Node
    tdraw.text((W - 240, 52), "● SOVEREIGN ENTERPRISE", font=font_meta, fill=(a_col[0], a_col[1], a_col[2], 240))
    tdraw.text((W - 240, 76), "ECOSYSTEM ASSET", font=font_meta, fill=(130, 140, 160, 180))
    
    # Bottom Left Title & Value Proposition
    bot_y = H - 146
    tdraw.text((54, bot_y), venture["name"], font=font_title, fill=(255, 255, 255, 255))
    tdraw.text((54, bot_y + 54), venture["tagline"], font=font_tagline, fill=(160, 172, 195, 230))
    
    # Bottom Right Spec
    tdraw.text((W - 280, H - 85), "JULZ HOLDINGS CORP // 2026", font=font_meta, fill=(p_col[0], p_col[1], p_col[2], 220))
    
    card = Image.alpha_composite(card, text_layer)
    
    # Save optimized WebP/PNG
    out_path = os.path.join(OUTPUT_DIR, f"{venture['id']}.png")
    card.convert("RGB").save(out_path, format="PNG", quality=95, optimize=True)
    print(f"Generated mesh cover: {out_path}")

def main():
    print(f"Generating mesh gradient cover images for {len(VENTURES)} ventures...")
    for v in VENTURES:
        create_mesh_gradient_cover(v)
    print("All venture mesh covers generated successfully!")

if __name__ == "__main__":
    main()
