#!/usr/bin/env python3
"""YouTube Video Generator PRO - Versão Final"""

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import requests

# Carregar .env
load_dotenv()

OUTPUT = Path("workspace/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def download_pexels_video(query, count=2):
    """Baixa videos do Pexels"""
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print("PEXELS_API_KEY nao configurada")
        return []
    
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
            output_path = OUTPUT / f"broll_{query}_{len(videos)}.mp4"
            r = requests.get(video_url, timeout=30)
            if r.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(r.content)
                videos.append(str(output_path))
                print(f"  [OK] Video baixado: {output_path.name}")
    
    return videos

def generate_voice_elevenlabs(text):
    """Gera narração com ElevenLabs"""
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("ELEVENLABS_API_KEY nao configurada")
        return None
    
    # Voice ID para português brasileiro (Rachel - multilíngue)
    voice_id = "21mMNb8T1QyujqDPfW9c"
    
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": api_key},
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
        }
    )
    
    if response.status_code == 200:
        output_path = OUTPUT / "audio.mp3"
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"  [OK] Narracao criada")
        return str(output_path)
    
    print(f"Erro ElevenLabs: {response.status_code}")
    return None

def create_video(channel, topic, use_pexels=False, use_voice=False):
    """Cria video profissional"""
    
    print(f"\n{'='*60}")
    print(f"GERANDO VIDEO PROFISSIONAL: {topic}")
    print(f"{'='*60}")
    
    # 1. Baixar stock footage
    broll_files = []
    if use_pexels:
        print("\n[Baixando stock footage Pexels...]")
        broll_files = download_pexels_video(topic, count=2)
    
    # 2. Gerar narração
    voice_file = None
    if use_voice:
        script = f"Hoje vamos falar sobre {topic}. Acompanhe este conteudo educativo."
        print("\n[Gerando narração ElevenLabs...]")
        voice_file = generate_voice_elevenlabs(script)
    
    # 3. Montar video
    print("\n[Montando video final...]")
    output = OUTPUT / f"{channel}_FINAL.mp4"
    
    if broll_files and Path(broll_files[0]).exists():
        # Video com stock footage
        cmd = [
            'ffmpeg', '-y',
            '-i', broll_files[0],
            '-vf', f"drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text='{topic}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=h/2",
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-t', '60',
            str(output)
        ]
    else:
        # Video básico
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', 'color=c=#667eea:s=1920x1080:d=60:rate=30',
            '-vf', f"drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text='{topic}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=h/2",
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            str(output)
        ]
    
    subprocess.run(cmd, capture_output=True)
    
    if output.exists():
        print(f"\nCONCLUIDO!")
        print(f"   Arquivo: {output.name}")
        print(f"   Tamanho: {output.stat().st_size/1024:.1f}KB")
        return str(output)
    
    return None

if __name__ == "__main__":
    # Video de exemplo
    create_video(
        "estoica_pro",
        "5 Licoes de Sabedoria Estoica",
        use_pexels=False,
        use_voice=False
    )