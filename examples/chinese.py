"""
Usage:
1.
    Install uv from https://docs.astral.sh/uv/getting-started/installation
2.
    Copy this file to new folder
3.
    Run
    uv venv -p 3.12
    uv pip install -U kokoro-onnx soundfile 'misaki-fork[zh]'
3.
    Download these files
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.1-zh.onnx
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.1-zh.bin
    https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh/raw/main/config.json
4. Run
    uv run main.py
"""

import soundfile as sf
from misaki import zh

from kokoro_onnx import Kokoro

# Misaki G2P with espeak-ng fallback
g2p = zh.ZHG2P(version="1.1")

text = "千里之行，始于足下。冬天，像是大自然精心绘制的一幅水墨画。洁白的雪纷纷扬扬，如鹅毛般飘落，为大地铺上一层厚厚的银毯。光秃秃的树枝上挂满了晶莹剔透的冰凌，在阳光的映照下闪烁着五彩光芒，宛如玉树琼枝。寒风凛冽，如刀割般划过脸颊，却也吹不散冬日独特的宁静。湖面上结了一层厚厚的冰，仿佛一面巨大的镜子，倒映着天空与周边的雪景。偶尔有几个孩子在冰面上嬉笑玩耍，打破这份寂静，为冬日增添几分活泼生气。远处的山峦也被白雪覆盖，连绵起伏，像是大地酣睡时隆起的脊背，沉稳而又壮阔，构成了冬日里一幅美不胜收的画卷。"
voice = "zf_001"
kokoro = Kokoro("kokoro-v1.1-zh.onnx", "voices-v1.1-zh.bin", vocab_config="config.json")
phonemes, _ = g2p(text)
samples, sample_rate = kokoro.create(phonemes, voice=voice, speed=1.0, is_phonemes=True)
sf.write("audio.wav", samples, sample_rate)
print("Created audio.wav")
