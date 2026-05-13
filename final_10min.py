#!/usr/bin/env python3
"""Relaxing Music Video - 10 MINUTOS COM AUDIO"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_video():
    print("=== CRIANDO RELAXING MUSIC VIDEO 10 MINUTOS ===")
    
    # Gerar audio ambiente
    print("\n[1] Gerando audio ambiente...")
    audio = OUTPUT / "ambient.mp3"
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'anoise=amount=0.03:color=brown:duration=600',
        '-c:a', 'libmp3lame', '-b:a', '96k',
        str(audio)
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"      Audio: {audio.stat().st_size/1024:.0f} KB")
    
    # Criar video de 10 minutos
    print("[2] Renderizando video HD...")
    output = OUTPUT / "relaxing_music_10min_FINAL.mp4"
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1920x1080:d=600:rate=30',
        '-i', str(audio),
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '25',
        '-c:a', 'aac', '-b:a', '96k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        str(output)
    ]
    
    subprocess.run(cmd, capture_output=True)
    
    if output.exists() and output.stat().st_size > 100000:
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"\n=== SUCESSO ===")
        print(f"Video: {output.name}")
        print(f"Tamanho: {size_mb:.2f} MB")
        print(f"Duracao: 10 minutos")
        return str(output)
    
    print("Falha")
    return None

if __name__ == "__main__":
    create_video()