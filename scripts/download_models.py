import os
import urllib.request

MODELS = {
    # English
    'kokoro-v1.0.onnx': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx',
    'voices-v1.0.bin': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin',
    # Chinese
    'kokoro-v1.1-zh.onnx': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.1-zh.onnx',
    'voices-v1.1-zh.bin': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.1-zh.bin',
    'config.json': 'https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh/raw/main/config.json',
    # Quantized
    'kokoro-v0_19.int8.onnx': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.int8.onnx'
}

def main():
    for name, url in MODELS.items():
        if os.path.exists(name):
            print(f"{name} already exists, skipping.")
            continue
        print(f"Downloading {name} from {url}...")
        try:
            urllib.request.urlretrieve(url, name)
            print(f"Successfully downloaded {name}")
        except Exception as e:
            print(f"Failed to download {name}: {e}")

if __name__ == '__main__':
    main()
