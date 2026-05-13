"""Agente de Pesquisa - Encontra temas lucrativos por nicho"""

import json
import os
import random
from datetime import datetime
from typing import List, Dict

# CPM global (USD) - valores de mercado 2024
HIGH_CPM_CATEGORIES = {
    # Seus nichos solicitados
    "filosofia_estoica": {"cpms": 28.00, "keywords": ["estoicismo", "filosofia", "sabedoria antiga"]},
    "documentarios": {"cpms": 22.00, "keywords": ["documentário", "história", "ciência"]},
    "relaxing_music": {"cpms": 18.00, "keywords": ["música relaxante", "deep focus", "meditação"]},
    
    # Nichos de alto CPM (referência)
    "financas": {"cpms": 35.00, "keywords": ["investimento", "cripto", "renda passiva"]},
    "saude": {"cpms": 25.00, "keywords": ["fitness", "nutricao", "bem-estar"]},
    "negocios": {"cpms": 22.00, "keywords": ["empreendedorismo", "gestao", "marketing"]},
    "tecnologia": {"cpms": 20.00, "keywords": ["IA", "programacao", "gadgets"]},
    "educacao": {"cpms": 15.00, "keywords": ["curso", "tutorial", "ensino"]},
    "viagem": {"cpms": 20.00, "keywords": ["viagem", "turismo", "destinos"]}
}

# RPM por país (USD) - países com melhor performance
COUNTRY_RPM = {
    "Norway": 12.50,
    "Luxembourg": 11.80,
    "Switzerland": 11.20,
    "Denmark": 10.90,
    "Netherlands": 9.80,
    "Germany": 9.50,
    "Australia": 9.20,
    "United States": 8.90,
    "Canada": 8.50,
    "United Kingdom": 8.30,
    "Brazil": 2.50  # Comparação
}

class ResearchAgent:
    def __init__(self, memory_path: str):
        self.memory_path = memory_path
        
    def find_profitable_topics(self, niche: str = None, count: int = 5) -> List[Dict]:
        if niche and niche in HIGH_CPM_CATEGORIES:
            categories = {niche: HIGH_CPM_CATEGORIES[niche]}
        else:
            categories = HIGH_CPM_CATEGORIES
            
        topics = []
        for category, data in categories.items():
            for i in range(count // len(categories)):
                topic = {
                    "id": f"topic_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}",
                    "title": self._generate_topic_title(category, data["keywords"]),
                    "category": category,
                    "estimated_cpm": data["cpms"],
                    "keywords": data["keywords"][:3],
                    "competition": self._estimate_competition(category),
                    "potential_views": self._estimate_views(category),
                    "best_countries": self._get_best_countries(category),
                    "timestamp": str(datetime.now())
                }
                topics.append(topic)
        
        self._save_research(topics)
        return topics
    
    def find_global_topics(self, niche: str, count: int = 5) -> List[Dict]:
        """Encontra temas otimizados para múltiplos países"""
        topics = []
        countries = list(COUNTRY_RPM.keys())[:5]  # Top 5 países
        
        for i in range(count):
            topic = self.find_profitable_topics(niche, 1)[0]
            topic["global_strategy"] = {
                "target_countries": countries,
                "adjusted_cpm": topic["estimated_cpm"] * 1.5,  # Bônus internacional
                "language_strategy": "multi-language"
            }
            topics.append(topic)
        
        return topics
    
    def _generate_topic_title(self, category: str, keywords: List) -> str:
        prefixes = ["Como ", "Guia Completo de ", "10 Dicas de ", "Curso de ", "Tudo sobre "]
        prefix = prefixes[random.randint(0, len(prefixes)-1)]
        keyword = keywords[random.randint(0, len(keywords)-1)]
        return f"{prefix}{keyword.title()} em 2024"
    
    def _estimate_competition(self, category: str) -> str:
        comp = {
            "filosofia_estoica": "baixa",
            "documentarios": "baixa",
            "relaxing_music": "média",
            "financas": "alta",
            "saude": "alta",
            "negocios": "alta",
            "tecnologia": "média-alta",
            "educacao": "média",
            "viagem": "média-alta"
        }
        return comp.get(category, "média")
    
    def _estimate_views(self, category: str) -> int:
        ranges = {
            "filosofia_estoica": 40000,
            "documentarios": 50000,
            "relaxing_music": 65000,
            "financas": 50000,
            "saude": 55000,
            "negocios": 45000,
            "tecnologia": 60000,
            "educacao": 30000,
            "viagem": 45000
        }
        return ranges.get(category, 25000)
    
    def _get_best_countries(self, category: str) -> List[str]:
        """Países com melhor RPM para o nicho"""
        high_rpm_countries = [c for c, rpm in COUNTRY_RPM.items() if rpm > 8.0]
        return high_rpm_countries[:3]
    
    def _save_research(self, topics: List[Dict]):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        research_file = os.path.join(os.path.dirname(self.memory_path), "research.json")
        
        existing = []
        if os.path.exists(research_file):
            try:
                with open(research_file, 'r') as f:
                    data = json.load(f)
                    existing = data if isinstance(data, list) else []
            except:
                existing = []
        
        existing.extend(topics)
        with open(research_file, 'w') as f:
            json.dump(existing, f, indent=2)