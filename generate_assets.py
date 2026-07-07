#!/usr/bin/env python3
"""
Gerador Procedural de Ativos para WhaleOS
Cria ícones flat-design e wallpaper abstrato usando Pillow.
"""

import os
from PIL import Image, ImageDraw, ImageFilter
import random
import math

ROOTFS_PATH = "./rootfs"
ICON_DIR = os.path.join(ROOTFS_PATH, "usr/share/icons/whaleos/apps/64")
BG_DIR = os.path.join(ROOTFS_PATH, "usr/share/backgrounds/whaleos")

def ensure_dirs():
    """Garante que os diretórios de destino existem."""
    os.makedirs(ICON_DIR, exist_ok=True)
    os.makedirs(BG_DIR, exist_ok=True)

def draw_dialer_icon(size=64):
    """Gera ícone do Discador (Dialer)."""
    img = Image.new('RGBA', (size, size), (46, 204, 113, 255))  # Verde Flat
    draw = ImageDraw.Draw(img)
    
    # Desenhar teclado numérico simplificado
    pad_size = size // 4
    margin = size // 8
    for r in range(3):
        for c in range(3):
            x = margin + c * (pad_size + 2)
            y = margin + r * (pad_size + 2)
            draw.rounded_rectangle([x, y, x+pad_size, y+pad_size], radius=4, fill=(255, 255, 255, 230))
    
    # Botão de chamada
    draw.rounded_rectangle([margin, size-margin-pad_size, size-margin, size-margin], 
                           radius=pad_size//2, fill=(255, 255, 255, 255))
    
    img.save(os.path.join(ICON_DIR, "dialer.png"))

def draw_settings_icon(size=64):
    """Gera ícone de Configurações (Engrenagem)."""
    img = Image.new('RGBA', (size, size), (149, 165, 166, 255))  # Cinza Flat
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    outer_r = size // 2 - 4
    inner_r = size // 4
    
    # Corpo da engrenagem
    draw.ellipse([center-outer_r, center-outer_r, center+outer_r, center+outer_r], fill=(236, 240, 241, 255))
    # Centro vazado
    draw.ellipse([center-inner_r, center-inner_r, center+inner_r, center+inner_r], fill=(149, 165, 166, 255))
    
    # Dentes da engrenagem
    for i in range(8):
        angle = i * 45 * math.pi / 180
        x1 = center + int((outer_r - 6) * math.cos(angle))
        y1 = center + int((outer_r - 6) * math.sin(angle))
        x2 = center + int((outer_r + 2) * math.cos(angle))
        y2 = center + int((outer_r + 2) * math.sin(angle))
        draw.line([x1, y1, x2, y2], fill=(236, 240, 241, 255), width=6)
        
    img.save(os.path.join(ICON_DIR, "settings.png"))

def draw_browser_icon(size=64):
    """Gera ícone do Navegador (Globo)."""
    img = Image.new('RGBA', (size, size), (52, 152, 219, 255))  # Azul Flat
    draw = ImageDraw.Draw(img)
    
    margin = 8
    # Círculo externo
    draw.ellipse([margin, margin, size-margin, size-margin], outline=(255, 255, 255, 255), width=3)
    # Linha horizontal
    draw.line([margin, size//2, size-margin, size//2], fill=(255, 255, 255, 255), width=2)
    # Elipse vertical
    draw.ellipse([size//4, margin, size*3//4, size-margin], outline=(255, 255, 255, 255), width=2)
    
    img.save(os.path.join(ICON_DIR, "browser.png"))

def generate_wallpaper(width=1920, height=1080):
    """Gera wallpaper abstrato/tecnológico procedural."""
    img = Image.new('RGB', (width, height), (15, 23, 42))  # Fundo escuro profundo
    draw = ImageDraw.Draw(img)
    
    # Gerar grade tecnológica com pontos e linhas conectadas
    grid_spacing = 60
    points = []
    
    for x in range(0, width, grid_spacing):
        for y in range(0, height, grid_spacing):
            # Adicionar variação aleatória para efeito orgânico
            ox = random.randint(-10, 10)
            oy = random.randint(-10, 10)
            px, py = x + ox, y + oy
            points.append((px, py))
            
            # Desenhar ponto
            alpha = random.randint(50, 150)
            color = (0, 255, 200, alpha)  # Ciano neon
            r = random.randint(1, 3)
            draw.ellipse([px-r, py-r, px+r, py+r], fill=color[:3])
    
    # Conectar pontos próximos para formar rede neural/topológica
    for i, p1 in enumerate(points):
        for p2 in points[i+1:i+10]:
            dist = math.hypot(p1[0]-p2[0], p1[1]-p2[1])
            if dist < grid_spacing * 1.5 and random.random() > 0.7:
                line_alpha = int(255 * (1 - dist / (grid_spacing * 1.5)))
                line_color = (0, 200, 180, max(20, line_alpha))
                draw.line([p1, p2], fill=line_color[:3], width=1)
    
    # Aplicar blur suave para dar profundidade
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    
    output_path = os.path.join(BG_DIR, "whaleos-default.jpg")
    img.save(output_path, quality=95)
    print(f"Wallpaper gerado em: {output_path}")

if __name__ == "__main__":
    print("Iniciando geração procedural de ativos do WhaleOS...")
    ensure_dirs()
    draw_dialer_icon()
    draw_settings_icon()
    draw_browser_icon()
    generate_wallpaper()
    print("Ativos gerados com sucesso.")
