#!/usr/bin/env python3
"""Sistema 100% AUTOMATIZADO de geração de vídeos profissionais"""

import os
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

OUTPUT = Path(__file__).parent / "workspace" / "output"
ASSETS = OUTPUT / "assets"

# Configuração automática
CHANNEL_CONFIGS = {
    "estoica_pro": {
        "title": "5 Licoes de Sabedoria Estoica",
        "duration": 540,  # 9 minutos
        "color": "#1a73e8",
        "scenes": [
            {"time": 0, "text": "Você sabia que estoicos eram mais felizes?", "broll": "nature"},
            {"time": 30, "text": "Marco Aurelio - Imperador Filosofo", "broll": "ancient"},
            {"time": 90, "text": "Licão 1: Controle o que está em seu controle", "broll": "meditation"},
            {"time": 210, "text": "Licão 2: Aceite o que não pode mudar", "broll": "acceptance"},
            {"time": 330, "text": "Desafio 7 dias - Inscreva-se!", "broll": "challenge"}
        ]
    },
    "doc_explorer": {
        "title": "O Enigma das Pirâmides",
        "duration": 900,  # 15 minutos
        "color": "#4285f4",
        "scenes": [
            {"time": 0, "text": "Descoberta de 2024 muda tudo!", "broll": "mystery"},
            {"time": 60, "text": "Construção secreta revelada", "broll": "construction"},
            {"time": 360, "text": "Conexões cósmicas", "broll": "stars"}
        ]
    },
    "deep_focus": {
        "title": "Deep Focus - 2 Horas de Concentração",
        "duration": 7200,  # 2 horas
        "color": "#34a853",
        "scenes": [
            {"time": 0, "text": "Frequências binaurais 40Hz", "broll": "waves"},
            {"time": 1800, "text": "Música ambiente contínua", "broll": "ambient"},
            {"time": 3600, "text": "Loop otimizado", "broll": "focus"}
        ]
    },
    "money_empire": {
        "title": "Gerar R$ 5.000 por Mês",
        "duration": 720,  # 12 minutos
        "color": "#ea4335",
        "scenes": [
            {"time": 0, "text": "Método que funcionou para 500 pessoas!", "broll": "money"},
            {"time": 480, "text": "Yield Farming Passivo", "broll": "crypto"},
            {"time": 840, "text": "FIIs - Renda Imobiliária", "broll": "realestate"}
        ]
    }
}

class AutoVideoGenerator:
    def __init__(self):
        os.makedirs(OUTPUT, exist_ok=True)
        os.makedirs(ASSETS, exist_ok=True)
    
    def generate_all(self):
        """Gera todos os vídeos automaticamente"""
        results = []
        
        for channel_id, config in CHANNEL_CONFIGS.items():
            print(f"\n[Geração] {channel_id}...")
            video_path = self.create_professional_video(channel_id, config)
            results.append({"channel": channel_id, "path": str(video_path)})
        
        return results
    
    def create_professional_video(self, channel_id, config):
        """Cria vídeo profissional com elementos visuais"""
        
        # 1. Baixar/B-roll simulado (animações geradas)
        self.create_animated_broll(channel_id, config)
        
        # 2. Criar vídeo completo
        video_path = OUTPUT / f"{channel_id}_PRO.mp4"
        
        # Montar vídeo com múltiplas cenas
        self.assemble_video(channel_id, config, video_path)
        
        return video_path
    
    def create_animated_broll(self, channel_id, config):
        """Cria elementos visuais animados"""
        
        for i, scene in enumerate(config["scenes"]):
            broll_path = ASSETS / f"{channel_id}_scene_{i}.mp4"
            
            # Cena com animação de texto + overlay visual
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi', '-i', f'color=c={config["color"]}:s=1920x1080:d={scene.get("duration", 30)}:rate=30',
                '-vf', self.build_scene_filters(scene, config),
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                '-t', str(scene.get("duration", 30)),
                str(broll_path)
            ]
            
            subprocess.run(cmd, capture_output=True)
    
    def build_scene_filters(self, scene, config):
        """Constrói filtros visuais para cena"""
        
        text = scene.get("text", "")
        # Dividir texto em linhas para melhor visualização
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(" ".join(current_line)) > 30:
                lines.append(" ".join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        
        text_filters = []
        for i, line in enumerate(lines[:3]):  # Máximo 3 linhas
            text_filters.append(
                f"drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text='{line}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y={300+i*80}"
            )
        
        # Adicionar efeito visual baseado no tipo
        broll_type = scene.get("broll", "generic")
        effect = self.get_visual_effect(broll_type)
        
        return ",".join(text_filters + [effect])
    
    def get_visual_effect(self, broll_type):
        """Retorna efeito visual específico"""
        effects = {
            "nature": "hue=s=5",
            "ancient": "sepia",
            "meditation": "geq=r='if(eq(mod(X+Y,80),0),0,r(X,Y))':g='if(eq(mod(X+Y,80),0),255,g(X,Y))'",
            "mystery": "noise=alls=20:allf=t+u",
            "waves": "geq=lum='(sin(X*0.05)+1)*127.5'",
            "money": "hue=s=10",
            "stars": "geq=lum='(random(1)*255)'"
        }
        return effects.get(broll_type, "hue=s=2")
    
    def assemble_video(self, channel_id, config, output_path):
        """Junta todas as cenas em um vídeo final"""
        
        # Criar lista de arquivos
        list_file = OUTPUT / f"{channel_id}_scenes.txt"
        with open(list_file, 'w') as f:
            for i in range(len(config["scenes"])):
                scene_path = ASSETS / f"{channel_id}_scene_{i}.mp4"
                if scene_path.exists():
                    f.write(f"file '{scene_path}'\n")
        
        # Concatenar
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0', '-i', str(list_file),
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-pix_fmt', 'yuv420p',
            str(output_path)
        ]
        
        subprocess.run(cmd, capture_output=True)

if __name__ == "__main__":
    print("=" * 60)
    print("GERADOR AUTOMÁTICO DE VÍDEOS PROFISSIONAIS v2.0")
    print("=" * 60)
    
    generator = AutoVideoGenerator()
    results = generator.generate_all()
    
    print("\n" + "=" * 60)
    print("CONCLUÍDO!")
    for r in results:
        size = os.path.getsize(r["path"]) / 1024
        print(f"  {r['channel']}: {size:.1f}KB")