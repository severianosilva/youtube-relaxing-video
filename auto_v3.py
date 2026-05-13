#!/usr/bin/env python3
"""GERADOR AUTOMÁTICO v3.0 - Vídeos com elementos visuais reais"""

import os
import subprocess
from pathlib import Path

OUTPUT = Path(__file__).parent / "workspace" / "output"
ASSETS = OUTPUT / "assets"

def generate_all_videos():
    """Gera todos os vídeos com elementos visuais"""
    
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(ASSETS, exist_ok=True)
    
    videos = [
        ("estoica_pro", "Estoica Pro", "#1a73e8", "5 Licoes de Sabedoria", 540),
        ("doc_explorer", "Doc Explorer", "#4285f4", "O Enigma das Pirâmides", 900),
        ("deep_focus", "Deep Focus Music", "#34a853", "2 Horas de Foco", 7200),
        ("money_empire", "Money Empire BR", "#ea4335", "R$ 5.000 por Mês", 720)
    ]
    
    for channel, name, color, title, duration in videos:
        print(f"Criando: {title}...")
        create_dynamic_video(channel, name, color, title, duration)

def create_dynamic_video(channel, name, color, title, total_duration):
    """Cria vídeo com elementos visuais dinâmicos"""
    
    output_path = OUTPUT / f"{channel}_final_v3.mp4"
    
    # Criar vídeo com múltiplos elementos visuais
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'color=c={color}:s=1920x1080:d={total_duration}:rate=30',
        '-vf', build_visual_filters(channel, title, total_duration),
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-pix_fmt', 'yuv420p',
        str(output_path)
    ]
    
    subprocess.run(cmd, capture_output=True)
    size = os.path.getsize(output_path) / 1024
    print(f"  [OK] {channel}: {size:.1f}KB")

def build_visual_filters(channel, title, duration):
    """Cria filtros visuais com movimento"""
    
    # Texto principal com animação
    main_text = f"drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text='{title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=100:enable='between(t,0,5)'"
    
    # Texto secundário
    subtitle = f"drawtext=fontfile=/Windows/Fonts/arial.ttf:text='Vídeo Automático Gerado':fontcolor=yellow:fontsize=32:x=(w-text_w)/2:y=200:enable='between(t,2,6)'"
    
    # Efeito visual baseado no canal
    effects = {
        "estoica": "geq=lum='(sin(X*0.02)+1)*100':sat='(cos(Y*0.02)+1)*50'",
        "documentario": "noise=alls=10:allf=t+u",
        "music": "geq=lum='(sin(X*0.1+t*10)+1)*127.5'",
        "financas": "hue=s='2+sin(t)'"
    }
    
    effect = effects.get(channel.replace("_pro", "").replace("_explorer", "").replace("_empire", ""), effects["estoica"])
    
    return ",".join([main_text, subtitle, effect])

if __name__ == "__main__":
    print("=" * 50)
    print("GERADOR AUTOMÁTICO v3.0")
    print("=" * 50)
    generate_all_videos()
    print("\n[CONCLUÍDO]")