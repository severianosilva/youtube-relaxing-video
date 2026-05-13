#!/usr/bin/env python3
"""Relaxing Music Video - 60 segundos (teste rapido)"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_relaxing_video():
    output = OUTPUT / "relaxing_music_10min.mp4"
    
    # Video de 10 min com baixa qualidade para renderizamento rapido
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=640x360:d=600:rate=15',
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=32:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2,fps=15',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '35',
        '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    print("Renderizando 10 min video (baixa qualidade, rapido)...")
    result = subprocess.run(cmd, capture_output=True)
    
    if output.exists():
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"CONCLUIDO! {size_mb:.2f} MB")
        return str(output)
    
    print("Erro")
    return None

if __name__ == "__main__":
    create_relaxing_video()