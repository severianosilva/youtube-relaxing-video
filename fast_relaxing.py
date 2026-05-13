#!/usr/bin/env python3
"""Relaxing Music Video - Versão Rapida"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_relaxing_video():
    output = OUTPUT / "relaxing_music_10min.mp4"
    
    # Versão mais simples e rapida - 30 segundos para testar
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1280x720:d=600:rate=24',
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'stillimage', '-crf', '30',
        '-pix_fmt', 'yuv420p', '-r', '24',
        str(output)
    ]
    
    print("Renderizando video de 10 minutos...")
    result = subprocess.run(cmd, capture_output=True)
    
    if output.exists() and output.stat().st_size > 10000:
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"CONCLUIDO! {output.name} - {size_mb:.2f} MB")
        return str(output)
    
    print(f"ERRO")
    return None

if __name__ == "__main__":
    create_relaxing_video()