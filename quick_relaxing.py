#!/usr/bin/env python3
"""Relaxing Music Video - Versão Simples 10 minutos"""

import subprocess
from pathlib import Path

OUTPUT = Path("workspace/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_relaxing_video():
    """Cria video de relaxing music de 10 minutos"""
    
    print("\nGERANDO RELAXING MUSIC VIDEO - 10 MINUTOS")
    print("="*50)
    
    output = OUTPUT / "relaxing_music_10min.mp4"
    
    # Video com gradiente suave e textos
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#1a1a2e:s=1920x1080:d=600:rate=30',
        '-vf', 
        'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'Relaxing Music - 10 Minutes\':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h/3,'
        'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'Peaceful Atmospheric Sounds\':fontsize=36:fontcolor=#aaa:x=(w-text_w)/2:y=h/2,'
        'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'Relax \\\\u2776 Breathe \\\\u2777 Peace\':fontsize=42:fontcolor=#888:x=(w-text_w)/2:y=2h/3',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    print("Renderizando video... (isso pode levar alguns minutos)")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output.exists():
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"\nCONCLUIDO!")
        print(f"  Arquivo: {output.name}")
        print(f"  Tamanho: {size_mb:.2f} MB")
        print(f"  Duração: 10 minutos")
        return str(output)
    else:
        print(f"Erro: {result.stderr}")
        return None

if __name__ == "__main__":
    create_relaxing_video()