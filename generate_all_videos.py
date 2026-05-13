#!/usr/bin/env python3
"""Gerador de vídeos completos para todos os nichos"""

import os
import subprocess
from pathlib import Path
import json

OUTPUT = Path(__file__).parent / "workspace" / "output"
EXAMPLES = Path(__file__).parent / "examples"

def generate_full_videos():
    """Gera vídeos completos baseados nos roteiros"""
    
    os.makedirs(OUTPUT, exist_ok=True)
    
    channels = [
        ("estoica_pro.json", "Estoica Pro", "5 Licoes de Sabedoria"),
        ("doc_explorer.json", "Doc Explorer", "Piramides Enigma"),
        ("deep_focus.json", "Deep Focus", "Musica Relaxante"),
        ("money_empire.json", "Money Empire", "R$ 5.000 Renda Passiva")
    ]
    
    for filename, channel, title in channels:
        script_file = EXAMPLES / filename
        if script_file.exists():
            with open(script_file) as f:
                script = json.load(f)
            
            print(f"\n[VIDEO] Gerando: {title}")
            create_channel_video(channel, title, script)

def create_channel_video(channel, title, script):
    """Cria vídeo para um canal específico"""
    
    # 1. Intro do canal
    intro_file = OUTPUT / f"{channel}_intro.mp4"
    create_intro_channel(channel, title, intro_file)
    
    # 2. Conteúdo principal (baseado no roteiro)
    main_file = OUTPUT / f"{channel}_content.mp4"
    create_content_video(channel, script, main_file)
    
    # 3. Montagem final
    final_file = OUTPUT / f"{channel}_final.mp4"
    create_final_video(intro_file, main_file, final_file)
    
    size = os.path.getsize(final_file) if final_file.exists() else 0
    print(f"   [OK] {final_file.name} ({size/1024:.1f}KB)")

def create_intro_channel(channel, title, output):
    """Intro personalizado do canal"""
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#1a73e8:s=1920x1080:d=3:rate=30',
        '-vf', f'drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text=\'{channel}\':fontcolor=white:fontsize=60:x=100:y=100,'
        f'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'{title}\':fontcolor=yellow:fontsize=40:x=100:y=200',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    subprocess.run(cmd, capture_output=True)

def create_content_video(channel, script, output):
    """Conteúdo baseado no roteiro"""
    
    chapters = script.get("chapters", [])
    duration = script.get("duration_minutes", 8)
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'color=c=#34a853:s=1920x1080:d={duration}:rate=30',
        '-vf', f'drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text=\'{script["title"]}\':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=100,'
        'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'Capitulo 1\':fontcolor=yellow:fontsize=30:x=100:y=300,'
        'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'Capitulo 2\':fontcolor=yellow:fontsize=30:x=100:y=400',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    subprocess.run(cmd, capture_output=True)

def create_final_video(intro, content, output):
    """Montagem final"""
    
    # Criar arquivo de lista
    list_file = OUTPUT / "temp_list.txt"
    with open(list_file, 'w') as f:
        f.write(f"file '{intro}'\nfile '{content}'\n")
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0', '-i', str(list_file),
        '-c:v', 'libx264', '-preset', 'medium',
        '-crf', '23', '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    subprocess.run(cmd, capture_output=True)

if __name__ == "__main__":
    print("=" * 50)
    print("GERADOR DE VIDEOS COMPLETOS")
    print("=" * 50)
    generate_full_videos()
    print("\n[DONE] Videos gerados em:", OUTPUT)