#!/usr/bin/env python3
"""Integração ElevenLabs - Narração profissional AI"""

import requests
import os
from pathlib import Path

class ElevenLabsIntegration:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {"xi-api-key": self.api_key}
        self.output = Path("workspace/output/audio")
        self.output.mkdir(parents=True, exist_ok=True)
    
    def generate_voice(self, text, voice_id="21mMNb8T1QyujqDPfW9c"):
        """Gera narração em áudio"""
        
        if not self.api_key:
            print("ELEVENLABS_API_KEY não configurada")
            return None
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8
            }
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        
        if response.status_code == 200:
            output_path = self.output / f"voice_{hash(text)}.mp3"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Narração criada: {output_path.name}")
            return str(output_path)
        else:
            print(f"Erro ElevenLabs: {response.status_code}")
            print(response.text)
            return None
    
    def create_voiceover(self, script_lines):
        """Cria narração para script completo"""
        audio_files = []
        
        for i, line in enumerate(script_lines):
            audio = self.generate_voice(line)
            if audio:
                audio_files.append(audio)
        
        return audio_files

# Voices disponíveis:
# Brazilian Portuguese: "21mMNb8T1QyujqDPfW9c"
# English: "EXAVITQu4vr4xnSDxMaL"
# Spanish: "ErXwobaYiN019PkyGqhk"