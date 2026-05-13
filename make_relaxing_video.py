#!/usr/bin/env python3
"""Gerador de Relaxing Music Video - 10 minutos"""

import os
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
OUTPUT = Path("workspace/output")

def download_background_videos(query, count=3):
    """Baixa videos de fundo do Pexels"""
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print("PEXELS_API_KEY nao configurada")
        return []
    
    videos = []
    headers = {"Authorization": api_key}
    
    response = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={"query": query, "per_page": count, "orientation": "landscape", "size": "large"}
    )
    
    if response.status_code == 200:
        for v in response.json().get("videos", [])[:count]:
            # Pegar o video de maior qualidade
            video_url = max(v["video_files"], key=lambda x: x.get("width", 0))["link"]
            output_path = OUTPUT / f"broll_{query}_{len(videos)}.mp4"
            
            print(f"Baixando: {v.get('id', 'video')}")
            r = requests.get(video_url, timeout=60)
            if r.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(r.content)
                videos.append(str(output_path))
                print(f"  [OK] {output_path.name}")
    
    return videos

def generate_relaxing_audio(duration=600):
    """Gera áudio de relaxamento (som de água/natureza) usando FFmpeg"""
    output_path = OUTPUT / "relaxing_audio.mp3"
    
    # Criar áudio ambiente com sons relaxantes (simulado com ruído ambiente)
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'anoise=amount=0.05:color=brown:duration=600',
        '-af', 'aeval=color=brown:d=600[s0];[s0]atempo=0.5[audio]',
        '-c:a', 'libmp3lame', '-b:a', '128k',
        str(output_path)
    ]
    
    print("Gerando áudio relaxante...")
    subprocess.run(cmd, capture_output=True)
    
    if output_path.exists():
        print(f"  [OK] Áudio gerado: {output_path.name}")
        return str(output_path)
    
    return None

def create_relaxing_video():
    """Cria video de relaxing music de 10 minutos"""
    
    print("\n" + "="*60)
    print("GERANDO RELAXING MUSIC VIDEO - 10 MINUTOS")
    print("="*60)
    
    # 1. Baixar videos de fundo
    print("\n[1/3] Baixando vídeos de fundo do Pexels...")
    broll_videos = download_background_videos("relaxing nature meditation", count=3)
    
    # 2. Gerar áudio
    print("\n[2/3] Gerando áudio relaxante...")
    audio_file = generate_relaxing_audio(600)
    
    # 3. Montar video final
    print("\n[3/3] Montando vídeo final...")
    output = OUTPUT / "relaxing_music_10min.mp4"
    
    if broll_videos and Path(broll_videos[0]).exists():
        # Criar lista de arquivos para concatenar
        list_file = OUTPUT / "video_list.txt"
        with open(list_file, 'w') as f:
            for v in broll_videos:
                f.write(f"file '{v}'\n")
        
        # Concatenar videos e adicionar áudio
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0', '-i', str(list_file),
            '-i', audio_file if audio_file else 'anullsrc',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac' if audio_file else 'copy',
            '-t', '600',  # 10 minutos
            str(output)
        ]
    else:
        # Video com cores suaves
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', 'color=c=#2c3e50:s=1920x1080:d=600:rate=30',
            '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'Relaxing Music - 10 Minutes\':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-100',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-pix_fmt', 'yuv420p',
            str(output)
        ]
    
    subprocess.run(cmd, capture_output=True)
    
    if output.exists():
        size_kb = output.stat().st_size / 1024
        print(f"\n{'='*60}")
        print("CONCLUIDO!")
        print(f"  Arquivo: {output.name}")
        print(f"  Tamanho: {size_kb/1024:.2f} MB")
        print(f"  Duração: 10 minutos")
        print("="*60)
        return str(output)
    
    return None

if __name__ == "__main__":
    create_relaxing_video()