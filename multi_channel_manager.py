#!/usr/bin/env python3
"""YouTube Multi-Channel Manager - Gerencia varios canais simultaneos"""

import json
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
CHANNELS_DIR = BASE_DIR / "channels"

# Configuração dos canais
CHANNELS = {
    "estoica_pro": {
        "niche": "filosofia_estoica",
        "name": "Estoica Pro",
        "target_countries": ["United States", "Germany", "Netherlands"],
        "language": "multi",
        "schedule": ["tuesday", "thursday", "saturday"]
    },
    "doc_explorer": {
        "niche": "documentarios",
        "name": "Doc Explorer",
        "target_countries": ["Norway", "Luxembourg", "Switzerland"],
        "language": "english",
        "schedule": ["monday", "wednesday", "friday"]
    },
    "deep_focus": {
        "niche": "relaxing_music",
        "name": "Deep Focus Music",
        "target_countries": ["Denmark", "Netherlands", "Germany"],
        "language": "instrumental",
        "schedule": ["daily"]
    },
    "money_empire": {
        "niche": "financas",
        "name": "Money Empire BR",
        "target_countries": ["Brazil", "United States"],
        "language": "pt-br",
        "schedule": ["monday", "wednesday", "friday"]
    }
}

class MultiChannelManager:
    def __init__(self):
        self.channels = CHANNELS
        os.makedirs(CHANNELS_DIR, exist_ok=True)
        
    def create_all_channels(self):
        results = []
        for channel_id, config in self.channels.items():
            result = self._create_channel_config(channel_id, config)
            results.append(result)
        return results
    
    def _create_channel_config(self, channel_id: str, config: dict):
        channel_dir = CHANNELS_DIR / channel_id
        os.makedirs(channel_dir, exist_ok=True)
        
        channel_config = {
            "id": channel_id,
            "config": config,
            "created_at": str(datetime.now()),
            "status": "configured"
        }
        
        config_file = channel_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(channel_config, f, indent=2)
        
        return {
            "channel": channel_id,
            "niche": config["niche"],
            "countries": config["target_countries"],
            "status": "created"
        }
    
    def estimate_revenue(self) -> dict:
        projections = {}
        total_monthly = 0
        
        for channel_id, config in self.channels.items():
            views_per_video = 50000
            rpm_global = 8.0
            
            videos_per_week = len(config["schedule"])
            monthly_videos = videos_per_week * 4
            
            monthly_revenue = monthly_videos * (views_per_video / 1000) * rpm_global
            total_monthly += monthly_revenue
            
            projections[channel_id] = {
                "monthly_videos": monthly_videos,
                "estimated_revenue_usd": round(monthly_revenue, 2),
                "estimated_revenue_brl": round(monthly_revenue * 5.5, 2)
            }
        
        projections["total"] = {
            "usd": round(total_monthly, 2),
            "brl": round(total_monthly * 5.5, 2)
        }
        
        return projections

if __name__ == "__main__":
    manager = MultiChannelManager()
    
    print("=" * 60)
    print("YOUTUBE MULTI-CHANNEL MANAGER")
    print("=" * 60)
    
    results = manager.create_all_channels()
    
    print("\n[OK] CANAIS CRIADOS:")
    for r in results:
        countries = ", ".join(r["countries"])
        print(f"   - {r['channel']}: {r['niche']} ({countries})")
    
    projections = manager.estimate_revenue()
    
    print("\n[$$] PROJECAO MENSAL:")
    for channel, data in projections.items():
        if channel != "total":
            print(f"   {channel}: US$ {data['estimated_revenue_usd']} / R$ {data['estimated_revenue_brl']}")
    
    print(f"\n   TOTAL: US$ {projections['total']['usd']} / R$ {projections['total']['brl']}")