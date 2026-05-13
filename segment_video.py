#!/usr/bin/env python3
"""Relaxing Video - 60 segmentos de 10 segundos"""

import subprocess
from pathlib import Path

OUTPUT = Path(r"C:\Users\User\.openclaw\workspace\youtube-agents\workspace\output")
OUTPUT.mkdir(parents=True, exist_ok=True)

def create_video():
    print("Criando 60 segmentos de 10 segundos cada...")
    
    for i in range(60):
        seg_file = OUTPUT / f"seg_{i:02d}.mp4"
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', 'color=c=#0a0a23:s=1280x720:d=10:rate=24',
            '-vf', 'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=Relaxing Music:fontsize=32:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '35',
            '-pix_fmt', 'yuv420p',
            str(seg_file)
        ]
        subprocess.run(cmd, capture_output=True)
        if i % 10 == 0:
            print(f"  Segmentos: {i}/60")
    
    # Concatenar todos
    print("Concatenando segmentos...")
    list_file = OUTPUT / "segments.txt"
    with open(list_file, 'w') as f:
        for i in range(60):
            f.write(f"file '{OUTPUT / f'seg_{i:02d}.mp4'}'\n")
    
    output = OUTPUT / "relaxing_complete.mp4"
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0', '-i', str(list_file),
        '-c', 'copy',
        str(output)
    ]
    subprocess.run(cmd, capture_output=True)
    
    if output.exists():
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"CONCLUIDO! {size_mb:.2f} MB")

if __name__ == "__main__":
    create_video()