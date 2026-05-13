#!/usr/bin/env python3
"""Gera exemplos de vídeos para todos os nichos"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
EXAMPLES_DIR = BASE_DIR / "examples"

def create_estoica_script():
    return {
        "title": "5 Lições de Sabedoria Estoica para Vida Moderna",
        "duration_minutes": 9,
        "chapters": [
            {"time": "00:00", "title": "Hook - Por que estoicos eram mais felizes?", "type": "hook"},
            {"time": "00:30", "title": "Quem foi Marco Aurélio", "type": "intro"},
            {"time": "01:30", "title": "Lição 1 - Controle o que está em seu controle", "type": "content"},
            {"time": "03:30", "title": "Lição 2 - Aceite o que não pode mudar", "type": "content"},
            {"time": "05:30", "title": "Lição 3 - Viva com simplicidade", "type": "content"},
            {"time": "07:00", "title": "Como aplicar hoje - Desafio 7 dias", "type": "cta"}
        ],
        "keywords": ["estoicismo", "filosofia", "sabedoria", "autoconhecimento"],
        "estimated_revenue": {"usd": 480, "views": 50000}
    }

def create_documentario_script():
    return {
        "title": "O Enigma das Pirâmides: O que Ninguém Contou",
        "duration_minutes": 15,
        "chapters": [
            {"time": "00:00", "title": "Hook - Descoberta de 2024 muda tudo!", "type": "hook"},
            {"time": "01:00", "title": "História oficial vs. evidências", "type": "intro"},
            {"time": "03:00", "title": "Construção e alinhamento solar", "type": "content"},
            {"time": "06:00", "title": "Câmara real e anomalias", "type": "content"},
            {"time": "10:00", "title": "Conexões com constelações", "type": "content"},
            {"time": "13:30", "title": "O que os egípcios realmente sabiam", "type": "content"},
            {"time": "14:30", "title": "Próximos vídeos - Inscreva-se!", "type": "cta"}
        ],
        "keywords": ["documentário", "pirâmides", "egito", "místico"],
        "estimated_revenue": {"usd": 480, "views": 50000}
    }

def create_music_script():
    return {
        "title": "Deep Focus - 2 Horas de Música para Concentração Extrema",
        "duration_minutes": 120,
        "chapters": [
            {"time": "00:00", "title": "Música inicia - Frequências binaurais 40Hz", "type": "music"},
            {"time": "30:00", "title": "Transição suave", "type": "music"},
            {"time": "60:00", "title": "Loop otimizado", "type": "music"}
        ],
        "keywords": ["música relaxante", "foco", "concentração", "estudo"],
        "estimated_revenue": {"usd": 960, "views": 120000}
    }

def create_financas_script():
    return {
        "title": "Como Gerar R$ 5.000 por Mês com Renda Passiva em 2024",
        "duration_minutes": 12,
        "chapters": [
            {"time": "00:00", "title": "Hook - Método que funcionou para 500 pessoas!", "type": "hook"},
            {"time": "00:45", "title": "O que é renda passiva REAL", "type": "intro"},
            {"time": "02:00", "title": "Método 1: Criptomoedas yield farming", "type": "content"},
            {"time": "04:30", "title": "Método 2: Fundos imobiliários", "type": "content"},
            {"time": "07:30", "title": "Método 3: Afiliados + automação", "type": "content"},
            {"time": "10:00", "title": "Planilha gratuita - Link na descrição!", "type": "cta"}
        ],
        "keywords": ["renda passiva", "investimento", "ganhar dinheiro", "finanças"],
        "estimated_revenue": {"usd": 600, "views": 50000}
    }

def main():
    import os
    os.makedirs(EXAMPLES_DIR, exist_ok=True)
    
    scripts = {
        "estoica_pro.json": create_estoica_script(),
        "doc_explorer.json": create_documentario_script(),
        "deep_focus.json": create_music_script(),
        "money_empire.json": create_financas_script()
    }
    
    for filename, script in scripts.items():
        filepath = EXAMPLES_DIR / filename
        with open(filepath, 'w') as f:
            json.dump(script, f, indent=2)
        print(f"[OK] {filename}")
    
    print("\n[INFO] Exemplos gerados em:", EXAMPLES_DIR)

if __name__ == "__main__":
    main()