#!/usr/bin/env python3
"""Relaxing Music Video - 10 MINUTOS SIMPLIFICADO"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_video():
    print("=== CRIANDO RELAXING MUSIC VIDEO 10 MINUTOS ===")
    
    output = OUTPUT / "relaxing_music_10min.mp4"
    
    print("Renderizando video HD (1920x1080, 10 minutos)...")
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1920x1080:d=600:rate=30',
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2,fps=30',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28',
        '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output.exists() and output.stat().st_size > 100000:
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"\n=== SUCESSO ===")
        print(f"Video: {output.name}")
        print(f"Tamanho: {size_mb:.2f} MB")
        print(f"Duracao: 10 minutos")
        print(f"Resolucao: 1920x1080")
        return str(output)
    
    print(f"Erro: {result.stderr[:200] if result.stderr else 'unknown'}")
    return None

if __name__ == "__main__":
    create_video()