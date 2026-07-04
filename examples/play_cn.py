"""
Note: on Linux you need to run this as well: apt-get install portaudio19-dev

pip install -U kokoro-onnx sounddevice

wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python examples/play.py
"""

import sounddevice as sd
from misaki import zh

from kokoro_onnx import Kokoro

g2p = zh.ZHG2P(version="1.1")
kokoro = Kokoro("kokoro-v1.1-zh.onnx", "voices-v1.1-zh.bin", vocab_config="config.json")
text = "寒风凛冽，如刀割般划过脸颊，却也吹不散冬日独特的宁静。湖面上结了一层厚厚的冰，仿佛一面巨大的镜子，倒映着天空与周边的雪景"
phonemes, _ = g2p(text)
samples, sample_rate = kokoro.create(
    phonemes,
    voice="zf_001",
    speed=1.0,
    is_phonemes=True,
)
print("Playing audio...")
sd.play(samples, sample_rate)
sd.wait()
