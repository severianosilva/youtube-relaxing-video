#!/usr/bin/env python3
"""
SISTEMA AUTOMÁTICO YOUTUBE v4.0
Gera vídeos com elementos visuais dinâmicos reais
"""

import subprocess
import os
from pathlib import Path
import random

OUTPUT = Path(__file__).parent / "workspace" / "output"
ASSETS = OUTPUT / "assets"

# Mapeamento de tipos de cenas para efeitos visuais
VISUAL_EFFECTS = {
    "philosophy": {
        "colors": ["#667eea", "#764ba2", "#f093fb"],
        "textures": ["hue", "eq", "noise"],
        "keywords": ["wisdom", "ancient", "thinking"]
    },
    "documentary": {
        "colors": ["#4facfe", "#00f2fe", "#43e97b"],
        "textures": ["noise", "eq", "hue"],
        "keywords": ["history", "mystery", "discovery"]
    },
    "music": {
        "colors": ["#fa709a", "#fee140", "#30cfd0"],
        "textures": ["geq", "hue", "eq"],
        "keywords": ["focus", "concentration", "ambient"]
    },
    "finance": {
        "colors": ["#ff9a9e", "#fad0c4", "#a1c4fd"],
        "textures": ["hue", "eq", "geq"],
        "keywords": ["money", "success", "wealth"]
    }
}

def create_professional_channel_video(channel_id, channel_name, niche, duration):
    """Cria vídeo profissional com elementos visuais dinâmicos"""
    
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(ASSETS, exist_ok=True)
    
    # Cores e efeitos do canal
    config = VISUAL_EFFECTS.get(niche, VISUAL_EFFECTS["philosophy"])
    primary_color = config["colors"][0]
    
    output_file = OUTPUT / f"{channel_id}_AUTOMATIC.mp4"
    
    # Criar vídeo com múltiplas camadas visuais
    filters = build_dynamic_filters(channel_name, config, duration)
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'color=c={primary_color}:s=1920x1080:d={duration}:rate=30',
        '-vf', filters,
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
        '-pix_fmt', 'yuv420p',
        str(output_file)
    ]
    
    subprocess.run(cmd, capture_output=True)
    return output_file

def build_dynamic_filters(channel_name, config, duration):
    """Constrói filtros visuais dinâmicos e atraentes"""
    
    # Texto animado principal
    title = f"drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text='{channel_name}':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-200)/2:enable='between(t,0,5)'"
    
    # Texto secundário
    subtitle = f"drawtext=fontfile=/Windows/Fonts/arial.ttf:text='Vídeo Automático':fontcolor=yellow:fontsize=36:x=(w-text_w)/2:y=(h+100)/2:enable='between(t,1,6)'"
    
    # Efeito visual animado
    effect = create_animated_effect(config["textures"][0], duration)
    
    # Sobreposição de partículas/simulação de movimento
    particles = "geq=lum='(sin(X*0.05+sin(t))+cos(Y*0.05+cos(t)))*127.5'"
    
    return ",".join([title, subtitle, effect, particles])

def create_animated_effect(filter_type, duration):
    """Cria efeito visual animado"""
    
    if filter_type == "hue":
        return f"hue=s='2+sin(t*0.5)':H='20*sin(t)'"
    elif filter_type == "eq":
        return f"eq=contrast='1+0.2*sin(t)':saturation='1+0.3*cos(t)'"
    elif filter_type == "geq":
        return f"geq=lum='(sin(X*0.1+t*5)+cos(Y*0.1+t))*50'"
    elif filter_type == "noise":
        return f"noise=alls='5+3*sin(t*0.1)':allf=t+u"
    else:
        return "hue=s=2"

def generate_all_channels():
    """Gera vídeos para todos os canais automaticamente"""
    
    channels = [
        ("estoica_pro", "Estoica Pro", "philosophy", 540),
        ("doc_explorer", "Doc Explorer", "documentary", 900),
        ("deep_focus", "Deep Focus Music", "music", 7200),
        ("money_empire", "Money Empire BR", "finance", 720)
    ]
    
    print("=" * 60)
    print("YOUTUBE AUTOMATIC VIDEO GENERATOR v4.0")
    print("=" * 60)
    
    results = []
    for channel_id, name, niche, duration in channels:
        print(f"\n[GERANDO] {name}...")
        output = create_professional_channel_video(channel_id, name, niche, duration)
        size = os.path.getsize(output) / 1024
        print(f"  [OK] {size:.1f}KB")
        results.append(str(output))
    
    return results

if __name__ == "__main__":
    generate_all_channels()
    print("\n[CONCLUÍDO] - Vídeos gerados automaticamente!")