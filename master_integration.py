#!/usr/bin/env python3
"""Master Integration - YouTube Video Generator PRO"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

# Importar integrações (quando API keys configuradas)
try:
    from integrations.pexels_integration import PexelsIntegration
    from integrations.elevenlabs_integration import ElevenLabsIntegration
    integrations_ready = True
except ImportError:
    integrations_ready = False

OUTPUT = Path("workspace/output")

def create_professional_video(channel, topic, script_text=None):
    """Cria video profissional COM elementos reais"""
    
    print(f"\n{'='*60}")
    print(f"GERANDO VIDEO PROFISSIONAL: {topic}")
    print(f"{'='*60}")
    
    # 1. Baixar stock footage (se API configurada)
    broll_files = []
    if integrations_ready and os.getenv('PEXELS_API_KEY'):
        print("\n[Baixando stock footage...]")
        pexels = PexelsIntegration()
        broll_files = pexels.search_videos(topic, count=3)
        print(f"  [OK] {len(broll_files)} videos baixados")
    
    # 2. Gerar narracao (se API configurada)
    voice_file = None
    if integrations_ready and os.getenv('ELEVENLABS_API_KEY') and script_text:
        print("\n[Gerando narracao profissional...]")
        eleven = ElevenLabsIntegration()
        voice_file = eleven.generate_voice(script_text[:500])  # Limitar texto
        if voice_file:
            print(f"  [OK] Narracao criada")
    
    # 3. Montar video final
    print("\n[Montando video final...]")
    final_video = compose_video_final(channel, topic, broll_files, voice_file)
    
    print(f"\nCONCLUIDO!")
    print(f"   Arquivo: {final_video}")
    print(f"   Tamanho: {os.path.getsize(final_video)/1024:.1f}KB")
    
    return final_video

def compose_video_final(channel, topic, broll_files, voice_file):
    """Montagem final do video profissional"""
    
    output = OUTPUT / f"{channel}_PROFESSIONAL.mp4"
    
    # Se temos broll real, usar
    if broll_files:
        # Usar FFmpeg para montar
        cmd = [
            'ffmpeg', '-y',
            '-i', broll_files[0] if broll_files else 'color=c=blue',
            '-vf', f"drawtext=text='{topic}':fontsize=72:fontcolor=white:x=100:y=100",
            '-c:v', 'libx264',
            str(output)
        ]
    else:
        # Video basico como fallback
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', 'color=c=#667eea:s=1920x1080:d=60:rate=30',
            '-vf', f"drawtext=text='{topic}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=h/2",
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            str(output)
        ]
    
    import subprocess
    subprocess.run(cmd, capture_output=True)
    
    return str(output)

# Exemplo de uso:
if __name__ == "__main__":
    # Criar .env se nao existir
    env_file = Path(".env")
    if not env_file.exists():
        env_file.write_text(
            "PEXELS_API_KEY=sua_chave_aqui\n"
            "ELEVENLABS_API_KEY=sua_chave_aqui\n"
        )
        print("Arquivo .env criado - configure suas API keys!")
    
    # Gerar video de exemplo
    create_professional_video(
        "estoica_pro",
        "5 Licoes de Sabedoria Estoica",
        script_text="Os estoicos ensinavam que a felicidade vem do controle interno..."
    )