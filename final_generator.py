#!/usr/bin/env python3
"""YOUTUBE VIDEO GENERATOR - Versão Funcional com Visual Dinâmico"""

import subprocess
import os
from pathlib import Path

OUTPUT = Path(__file__).parent / "workspace" / "output"

# Cores e durações por canal
CHANNELS = {
    "estoica_pro": {"color": "0x1a73e8", "title": "5 Licoes Estoicas", "dur": 540},
    "doc_explorer": {"color": "0x4285f4", "title": "Pirâmides Enigma", "dur": 900},
    "deep_focus": {"color": "0x34a853", "title": "Deep Focus 2h", "dur": 7200},
    "money_empire": {"color": "0xea4335", "title": "R$ 5000 Passivo", "dur": 720}
}

def create_video(channel_id, config):
    """Cria vídeo com elementos visuais dinâmicos"""
    
    output = OUTPUT / f"{channel_id}_final.mp4"
    
    # Criar vídeo com efeitos visuais
    cmd = create_ffmpeg_command(channel_id, config, output)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output.exists():
        size = os.path.getsize(output) / 1024
        print(f"[OK] {channel_id}: {size:.1f}KB")
        return output
    else:
        print(f"[ERRO] {channel_id}")
        return None

def create_ffmpeg_command(channel_id, config, output):
    """Constrói comando FFmpeg com efeitos visuais"""
    
    color = config["color"]
    dur = config["dur"]
    title = config["title"]
    
    # Filtros visuais
    filters = [
        # Texto principal animado
        f"drawtext=text='{title}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-200)/2:enable='between(t,0,5)'",
        # Subtítulo
        f"drawtext=text='Vídeo Automático':fontsize=36:fontcolor=yellow:x=(w-text_w)/2:y=(h+100)/2:enable='between(t,1,6)'",
        # Efeito de movimento (hue animado)
        "hue=s='2+sin(t)'"
    ]
    
    return [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'color=c={color}:s=1920x1080:d={dur}:rate=30',
        '-vf', ','.join(filters),
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        str(output)
    ]

def main():
    print("=" * 60)
    print("YOUTUBE VIDEO GENERATOR - VERSÃO FINAL")
    print("=" * 60)
    
    os.makedirs(OUTPUT, exist_ok=True)
    
    for channel_id, config in CHANNELS.items():
        print(f"\n[GERANDO] {channel_id}...")
        create_video(channel_id, config)
    
    print("\n[CONCLUÍDO]")

if __name__ == "__main__":
    main()