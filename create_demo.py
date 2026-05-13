#!/usr/bin/env python3
"""CRIA VÍDEO DE DEMONSTRAÇÃO COM ELEMENTOS VISUAIS"""

import subprocess
from pathlib import Path

OUTPUT = Path("workspace/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_demo_video():
    """Cria um vídeo de demonstração com elementos visuais reais"""
    
    output_file = OUTPUT / "DEMONSTRACAO_COMPLETA.mp4"
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#667eea:s=1920x1080:d=30:rate=30',
        '-vf', 
        # Título grande
        "drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text='YouTube Money Agents':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=200:enable='between(t,0,3)',"
        # Subtítulo
        "drawtext=fontfile=/Windows/Fonts/arial.ttf:text='Sistema Automatico de Videos':fontcolor=yellow:fontsize=40:x=(w-text_w)/2:y=300:enable='between(t,2,5)',"
        # Efeito visual
        "geq=lum='(sin(X*0.05+t*2)+cos(Y*0.05+t))*50'",
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
        '-pix_fmt', 'yuv420p',
        str(output_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output_file.exists():
        size = output_file.stat().st_size / 1024
        print(f"[OK] Video criado: {output_file.name}")
        print(f"   Tamanho: {size:.1f}KB")
        print(f"   Duracao: 30 segundos")
        return output_file
    else:
        print("[ERRO] Erro ao criar video")
        return None

if __name__ == "__main__":
    create_demo_video()