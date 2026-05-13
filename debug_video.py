#!/usr/bin/env python3
"""Relaxing Music Video Final - Debug"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_final_video():
    print("=== CRIANDO RELAXING MUSIC VIDEO FINAL ===")
    
    # Criar video simples com audio
    output = OUTPUT / "relaxing_music_FINAL.mp4"
    
    # Versão mais simples - só video por enquanto
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1920x1080:d=30:rate=30',
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    print("Renderizando video de teste (30 segundos)...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Erro FFmpeg: {result.stderr}")
    
    if output.exists():
        print(f"OK: {output.stat().st_size} bytes")
        return str(output)
    
    return None

if __name__ == "__main__":
    create_final_video()