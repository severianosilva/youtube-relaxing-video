#!/usr/bin/env python3
"""Integração Pexels - Stock footage gratuito"""

import requests
import os
from pathlib import Path

class PexelsIntegration:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('PEXELS_API_KEY')
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {"Authorization": self.api_key}
        self.output = Path("workspace/output/assets")
        self.output.mkdir(parents=True, exist_ok=True)
    
    def search_videos(self, query, count=3):
        """Busca vídeos no Pexels"""
        
        if not self.api_key:
            print("PEXELS_API_KEY não configurada")
            return []
        
        response = requests.get(
            f"{self.base_url}/search",
            headers=self.headers,
            params={
                "query": query,
                "per_page": count,
                "orientation": "landscape"
            }
        )
        
        if response.status_code == 200:
            videos = response.json().get("videos", [])
            downloaded = self._download_videos(videos[:count], query)
            return downloaded
        else:
            print(f"Erro Pexels: {response.status_code}")
            return []
    
    def _download_videos(self, videos, query):
        """Baixa vídeos do Pexels"""
        downloaded = []
        
        for i, video in enumerate(videos):
            video_url = video["video_files"][0]["link"]
            output_path = self.output / f"{query}_{i}.mp4"
            
            print(f"Baixando: {output_path.name}")
            response = requests.get(video_url)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                downloaded.append(str(output_path))
        
        return downloaded

# Exemplo de uso:
# pexels = PexelsIntegration("SUA_API_KEY")
# videos = pexels.search_videos("philosophy", count=3)