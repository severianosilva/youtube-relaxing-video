#!/usr/bin/env python3
"""YouTube Video Generator - Otimizado para Colab/Local"""

import subprocess
from pathlib import Path

OUTPUT = Path("workspace/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_video():
    """Cria video usando metodo confiavel"""
    output = OUTPUT / "relaxing_music_10min_FINAL.mp4"
    
    print("YouTube Video Generator")
    print("="*40)
    
    # Metodo 1: FFmpeg otimizado
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1280x720:d=600:rate=24',
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '30',
        '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    print("Renderizando... (isso pode demorar alguns minutos)")
    result = subprocess.run(cmd, capture_output=True)
    
    if output.exists() and output.stat().st_size > 100000:
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"\nSUCESSO!")
        print(f"Arquivo: {output.name}")
        print(f"Tamanho: {size_mb:.2f} MB")
        return str(output)
    
    print("Falha no renderizado")
    return None

if __name__ == "__main__":
    create_video()