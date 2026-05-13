#!/usr/bin/env python3
"""Master Integration - YouTube Video Generator PRO (Fixed)"""

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

OUTPUT = Path("workspace/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_video_simple(channel, topic):
    """Cria video profissional usando FFmpeg"""
    
    print(f"\n{'='*60}")
    print(f"GERANDO VIDEO PROFISSIONAL: {topic}")
    print(f"{'='*60}")
    
    # Caminho de saida
    output = OUTPUT / f"{channel}_PROFESSIONAL.mp4"
    
    # Video basico com FFmpeg (funciona sem stock)
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#667eea:s=1920x1080:d=60:rate=30',
        '-vf', f"drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text='{topic}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=h/2",
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    print("\n[Montando video final...]")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and output.exists():
        print(f"\nCONCLUIDO!")
        print(f"   Arquivo: {output}")
        print(f"   Tamanho: {output.stat().st_size/1024:.1f}KB")
        return str(output)
    else:
        print(f"Erro FFmpeg: {result.stderr}")
        return None

if __name__ == "__main__":
    # Gerar video de exemplo
    create_video_simple(
        "estoica_pro",
        "5 Licoes de Sabedoria Estoica"
    )