#!/usr/bin/env python3
"""Relaxing Video 10min - Ultra Rapido"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")

# Video super enxuto - 10 minutos
cmd = [
    'ffmpeg', '-y',
    '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1280x720:d=600:rate=24',
    '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '35',
    '-pix_fmt', 'yuv420p',
    str(OUTPUT / 'relaxing_10min_ultra.mp4')
]

print("Renderizando video ultra-rapido...")
subprocess.run(cmd, capture_output=True)
print("Pronto!")