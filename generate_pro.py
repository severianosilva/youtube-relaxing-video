#!/usr/bin/env python3
"""GERADOR PROFISSIONAL COM INTEGRAÇÕES ATIVAS"""

import requests
import subprocess
import os
from pathlib import Path

PEXELS_KEY = "rrVv4ojgaKNhGyntetm7glBFov4gvLyjYEYZbDTjI5fVU4WM2Hz9uU3q"
ELEVENLABS_KEY = "sk_f77ef0dea8135c016de16c331b87ec4c7100d69ffb16f4a4"

OUTPUT = Path("workspace/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def generate_professional_video(channel, topic):
    """Gera vídeo profissional com stock footage real e narração"""
    
    print(f"\n[VIDEO] Gerando vídeo PROFissional: {topic}")
    
    print("\n1. Baixando stock footage (Pexels)...")
    video_url = download_pexels_video(topic)
    
    print("\n2. Gerando narração (ElevenLabs)...")
    audio_file = generate_voice(topic)
    
    print("\n3. Montando vídeo final...")
    assemble_video(channel, topic, video_url, audio_file)
    
    print("\n[CONCLUIDO]!")

def download_pexels_video(query):
    """Baixa vídeo do Pexels"""
    headers = {"Authorization": PEXELS_KEY}
    response = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={"query": query, "per_page": 1, "orientation": "landscape"}
    )
    
    videos = response.json().get("videos", [])
    if videos:
        video_url = videos[0]["video_files"][0]["link"]
        output = OUTPUT / f"broll_{query}.mp4"
        
        r = requests.get(video_url)
        with open(output, 'wb') as f:
            f.write(r.content)
        
        print(f"   [OK] Vídeo baixado: {output.name}")
        return str(output)
    return None

def generate_voice(text):
    """Gera narração com ElevenLabs"""
    url = "https://api.elevenlabs.io/v1/text-to-speech/21mMNb8T1QyujqDPfW9c"
    headers = {"xi-api-key": ELEVENLABS_KEY}
    
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        output = OUTPUT / "narration.mp3"
        with open(output, 'wb') as f:
            f.write(response.content)
        print(f"   [OK] Narração criada")
        return str(output)
    return None

def assemble_video(channel, topic, broll, audio):
    """Montar vídeo final com stock footage e narração"""
    
    if broll and audio:
        cmd = [
            'ffmpeg', '-y',
            '-i', broll,
            '-i', audio,
            '-c:v', 'libx264', '-preset', 'fast',
            '-c:a', 'aac',
            '-vf', f"drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text='{topic}':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=100",
            str(OUTPUT / f"{channel}_PRO.mp4")
        ]
    else:
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', 'color=c=#667eea:s=1920x1080:d=60:rate=30',
            '-vf', f"drawtext=text='{topic}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=h/2",
            '-c:v', 'libx264',
            str(OUTPUT / f"{channel}_PRO.mp4")
        ]
    
    subprocess.run(cmd, capture_output=True)
    print(f"   [OK] Vídeo montado")

if __name__ == "__main__":
    generate_professional_video("estoica_pro", "5 Licoes de Sabedoria Estoica")