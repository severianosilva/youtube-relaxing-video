#!/usr/bin/env python3
"""Relaxing Music Video - 10 minutos SIMPLES"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_relaxing_video():
    """Cria video de relaxing music de 10 minutos"""
    
    print("\nGERANDO RELAXING MUSIC VIDEO - 10 MINUTOS")
    print("="*50)
    
    output = OUTPUT / "relaxing_music_10min.mp4"
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=black:s=1920x1080:d=600:rate=30',
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28',
        '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    print("Renderizando video...")
    result = subprocess.run(cmd, capture_output=True)
    
    if output.exists():
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"\nCONCLUIDO!")
        print(f"  Arquivo: {output.name}")
        print(f"  Tamanho: {size_mb:.2f} MB")
        return str(output)
    
    print(f"Erro")
    return None

if __name__ == "__main__":
    create_relaxing_video()