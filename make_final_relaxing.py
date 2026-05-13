#!/usr/bin/env python3
"""Relaxing Music Video Final - Com Audio Real"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")

def create_final_video():
    print("=== CRIANDO RELAXING MUSIC VIDEO FINAL ===")
    
    # Primeiro: gerar audio relaxante
    print("\n[1/2] Gerando audio relaxante...")
    audio_path = OUTPUT / "ambient_audio.mp3"
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'anoise=amount=0.03:color=brown:duration=600',
        '-c:a', 'libmp3lame', '-b:a', '128k',
        str(audio_path)
    ]
    subprocess.run(cmd, capture_output=True)
    
    # Segundo: criar video HD com audio
    print("[2/2] Renderizando video HD...")
    output = OUTPUT / "relaxing_music_FINAL.mp4"
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1920x1080:d=600:rate=30',
        '-i', str(audio_path),
        '-vf', 
        'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h/3,'
        'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Peaceful Atmospheric Sounds:fontsize=36:fontcolor=#aaa:x=(w-text_w)/2:y=h/2,'
        'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relax  Breathe  Peace:fontsize=42:fontcolor=#999:x=(w-text_w)/2:y=2h/3',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '128k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        str(output)
    ]
    
    subprocess.run(cmd, capture_output=True)
    
    if output.exists() and output.stat().st_size > 1000000:
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"\n=== CONCLUIDO ===")
        print(f"Arquivo: {output.name}")
        print(f"Tamanho: {size_mb:.2f} MB")
        print(f"Duracao: 10 minutos")
        print(f"Resolucao: 1920x1080 HD")
        print(f"Audio: Incluido")
        return str(output)
    
    print("Erro no processamento")
    return None

if __name__ == "__main__":
    create_final_video()