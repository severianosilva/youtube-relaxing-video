#!/usr/bin/env python3
"""GERADOR FINAL - Vídeos com Stock Footage e Narração REAL"""

import requests
import subprocess
import os
from pathlib import Path

PEXELS_KEY = "rrVv4ojgaKNhGyntetm7glBFov4gvLyjYEYZbDTjI5fVU4WM2Hz9uU3q"
ELEVENLABS_KEY = "sk_f77ef0dea8135c016de16c331b87ec4c7100d69ffb16f4a4"

OUTPUT = Path("workspace/output")
ASSETS = OUTPUT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

def generate_video(channel, topic, keywords):
    """Gera vídeo profissional COM stock footage real"""
    
    print(f"\n{'='*60}")
    print(f"CANAL: {channel}")
    print(f"TÓPICO: {topic}")
    print(f"{'='*60}")
    
    # 1. Baixar stock footage
    print("\n[1/3] Baixando stock footage...")
    broll = download_broll(keywords[0])
    
    # 2. Gerar narração
    print("\n[2/3] Gerando narração...")
    audio = generate_audio(topic)
    
    # 3. Montar vídeo final
    print("\n[3/3] Montando vídeo...")
    output_file = OUTPUT / f"{channel}_FINAL_PRO.mp4"
    assemble_final(broll, audio, output_file)
    
    print(f"\n[CONCLUIDO] {output_file.name}")
    size = os.path.getsize(output_file) / (1024*1024)
    print(f"Tamanho: {size:.2f}MB")
    return str(output_file)

def download_broll(query):
    """Baixa vídeo do Pexels"""
    headers = {"Authorization": PEXELS_KEY}
    
    r = requests.get(
        "https://api.pexels.com/v1/videos/search",
        headers=headers,
        params={"query": query, "per_page": 1}
    )
    
    if r.status_code == 200:
        videos = r.json().get("videos", [])
        if videos:
            url = videos[0]["video_files"][-1]["link"]  # Qualidade máxima
            output = ASSETS / f"{query}.mp4"
            
            print(f"Baixando: {url[:60]}...")
            video = requests.get(url)
            with open(output, 'wb') as f:
                f.write(video.content)
            
            print(f"[OK] {output.name}")
            return str(output)
    print("[AVISO] Usando cor de fundo")
    return None

def generate_audio(text):
    """Gera narração"""
    url = "https://api.elevenlabs.io/v1/text-to-speech/21mMNb8T1QyujqDPfW9c"
    headers = {"xi-api-key": ELEVENLABS_KEY}
    
    r = requests.post(url, json={"text": text, "model_id": "eleven_multilingual_v2"}, headers=headers)
    
    if r.status_code == 200:
        output = ASSETS / "voice.mp3"
        with open(output, 'wb') as f:
            f.write(r.content)
        print(f"[OK] Narração criada")
        return str(output)
    return None

def assemble_final(broll, audio, output):
    """Montagem final"""
    if broll and audio:
        cmd = ['ffmpeg', '-y', '-i', broll, '-i', audio,
               '-c:v', 'libx264', '-c:a', 'aac',
               '-shortest', str(output)]
    else:
        cmd = ['ffmpeg', '-y', '-f', 'lavfi', '-i',
               'color=c=#4285f4:s=1920x1080:d=10:rate=30',
               '-vf', 'drawtext=text="Video Profissional":fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h/2',
               '-c:v', 'libx264', str(output)]
    
    subprocess.run(cmd, capture_output=True)

# Gerar vídeos para todos os canais
if __name__ == "__main__":
    channels = [
        ("estoica_pro", "5 Licoes de Sabedoria Estoica", ["philosophy", "stoicism"]),
        ("doc_explorer", "O Enigma das Pirâmides", ["pyramids", "history"]),
        ("money_empire", "R$ 5.000 por Mês", ["money", "success"])
    ]
    
    for ch, top, kw in channels:
        generate_video(ch, top, kw)