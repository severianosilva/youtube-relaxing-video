#!/usr/bin/env python3
"""Relaxing Music Video Completo - Stock Real + Audio + HD"""

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()
OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def download_pexels_videos(query, count=3):
    """Baixa videos reais do Pexels"""
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print("PEXELS_API_KEY nao configurado")
        return []
    
    print(f"Baixando stock footage: {query}")
    videos = []
    headers = {"Authorization": api_key}
    
    response = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={"query": query, "per_page": count, "orientation": "landscape"}
    )
    
    if response.status_code == 200:
        for v in response.json().get("videos", [])[:count]:
            video_url = v["video_files"][0]["link"]
            output_path = OUTPUT / f"stock_{len(videos)}.mp4"
            r = requests.get(video_url, timeout=60)
            if r.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(r.content)
                videos.append(str(output_path))
                print(f"  [OK] {output_path.name}")
    
    return videos

def generate_audio():
    """Gera ou baixa musica relaxante"""
    print("Gerando audio relaxante...")
    
    # Criar audio ambiente simples com FFmpeg
    output = OUTPUT / "relaxing_audio.mp3"
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'anoise=amount=0.02:color=brown:duration=600',
        '-c:a', 'libmp3lame', '-b:a', '96k',
        str(output)
    ]
    subprocess.run(cmd, capture_output=True)
    
    if output.exists():
        print(f"  [OK] Audio gerado")
        return str(output)
    return None

def create_hd_video():
    """Cria video HD com stock real"""
    print("\n=== CRIANDO VIDEO RELAXING COMPLETO ===")
    
    # 1. Baixar stock footage
    stock_videos = download_pexels_videos("relaxing nature", count=3)
    
    # 2. Gerar audio
    audio_file = generate_audio()
    
    # 3. Montar video final
    output = OUTPUT / "relaxing_music_HD.mp4"
    
    if stock_videos and Path(stock_videos[0]).exists():
        print("\nMontando video com stock footage...")
        
        # Criar lista de videos
        list_file = OUTPUT / "list.txt"
        with open(list_file, 'w') as f:
            for v in stock_videos:
                f.write(f"file '{v}'\n")
        
        # Concatenar + adicionar audio
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0', '-i', str(list_file),
            '-i', audio_file if audio_file else 'anullsrc',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-vf', 'scale=1920:1080,drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-100',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac' if audio_file else 'copy',
            '-t', '600',
            str(output)
        ]
    else:
        print("\nCriando video HD basico (sem stock)...")
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1920x1080:d=600:rate=30',
            '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-pix_fmt', 'yuv420p',
            str(output)
        ]
    
    print("Renderizando video HD (isso pode demorar alguns minutos)...")
    subprocess.run(cmd, capture_output=True)
    
    if output.exists():
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"\nFINALIZADO!")
        print(f"  Arquivo: {output.name}")
        print(f"  Tamanho: {size_mb:.2f} MB")
        print(f"  Duracao: 10 minutos")
        print(f"  Resolucao: 1920x1080")
        return str(output)
    
    return None

if __name__ == "__main__":
    create_hd_video()