# kokoro-onnx

![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
[![PyPI Release](https://img.shields.io/pypi/v/kokoro-onnx.svg)](https://pypi.org/project/kokoro-onnx/)
[![Github Model Releases](https://img.shields.io/github/v/release/thewh1teagle/kokoro-onnx)](https://github.com/thewh1teagle/kokoro-onnx/releases)
[![License](https://img.shields.io/github/license/thewh1teagle/kokoro-onnx)](https://github.com/thewh1teagle/kokoro-onnx/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/thewh1teagle/kokoro-onnx?style=social)](https://github.com/thewh1teagle/kokoro-onnx/stargazers)
[![PyPI Downloads](https://img.shields.io/pypi/dm/kokoro-onnx?style=plastic)](https://pypi.org/project/kokoro-onnx/)

[![ONNX Runtime](https://img.shields.io/badge/ONNX%20Runtime-%E2%89%A51.20.1-blue)](https://github.com/microsoft/onnxruntime)
![CPU](https://img.shields.io/badge/CPU-supported-brightgreen)
![GPU](https://img.shields.io/badge/GPU-supported-brightgreen)

TTS with onnx runtime based on [Kokoro-TTS](https://huggingface.co/spaces/hexgrad/Kokoro-TTS)

🚀 Version 1.0 models are out now! 🎉

[https://github.com/user-attachments/assets/00ca06e8-bbbd-4e08-bfb7-23c0acb10ef9](https://github.com/user-attachments/assets/00ca06e8-bbbd-4e08-bfb7-23c0acb10ef9)

## Features

- Supports multiple languages
- Fast performance near real-time on macOS M1
- Offer multiple voices
- Lightweight: ~300MB (quantized: ~80MB)

## Setup

```console
pip install -U kokoro-onnx
```

<details>

<summary>Instructions</summary>

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation) for isolated Python (Recommend).

```console
pip install uv
```

2. Create new project folder (you name it)
3. Run in the project folder

```console
uv init -p 3.12
uv add kokoro-onnx soundfile
```

4. Paste the contents of [`examples/save.py`](https://github.com/thewh1teagle/kokoro-onnx/blob/main/examples/save.py) in `hello.py`
5. Download the files [`kokoro-v1.0.onnx`](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx), and [`voices-v1.0.bin`](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin) and place them in the same directory.
6. Run

```console
uv run hello.py
```

You can edit the text in `hello.py`

That's it! `audio.wav` should be created.

</details>

## Examples

See [examples](examples) folder for various use cases.

### 运行说明与注意事项 (Notes on running examples)

* **量化模型运行 (`examples/with_quant.py`)**：
  该示例需要显式指定所使用的 ONNX 模型路径（作为第一个命令行参数）。例如：

  ```console
  python examples/with_quant.py kokoro-v0_19.int8.onnx
  ```

  如果没有传参，会引发 `IndexError: list index out of range` 错误。
* **Web UI 运行 (`examples/app.py`)**：
  该示例基于 Gradio 框架。在运行前需要确保安装了 `gradio`：

  ```console
  pip install gradio
  ```

## Voices

See the latest voices and languages in [Kokoro-82M/VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)

## 关于 espeak-ng 的依赖说明 (About espeak-ng Dependency)

在合成英文（`en-us` 等）或直接合成文本时，`kokoro-onnx` 底层依赖 `espeak-ng` 进行文字转音素（G2P）。

* **无需手动安装：** `kokoro-onnx` 默认包含了 `espeakng-loader` 依赖。它会自动检测并加载随 Python 包一同打包下载的 `espeak-ng` 动态库及字典数据。因此，**用户不需要在系统上全局安装 `espeak-ng` 即可直接运行**。
* **自定义字典路径 (例如 `examples/with_espeak_data.py`)：** 如果需要指定自定义的 `espeak-ng-data` 字典路径，可以使用 `EspeakConfig(data_path="your-data-path")`。需要确保该路径是存在的且可读的目录，否则会因无法读取数据引发报错。

## 关于中文合成的注意事项 (Important Note on Chinese Synthesis)

在合成中文（Mandarin/cmn）语音时，**不推荐**直接将中文文本传入 `kokoro.create(..., lang="cmn")`。

* **原因**：`kokoro-onnx` 内部默认使用 `espeak-ng` 进行文字转音素（G2P），但其对中文（多音字、分词、变调等）支持较差，会导致合成的音频**变音、声调怪异或发音极不自然**。
* **解决方案**：强烈建议配合使用 [`misaki`](https://github.com/thewh1teagle/misaki)（专门针对中文优化的 G2P 模块）先将中文转换为音素，然后再传入合成器。

**示例代码：**

```python
from kokoro_onnx import Kokoro
from misaki import zh

# 1. 初始化 Misaki 中文 G2P
g2p = zh.ZHG2P(version="1.1")

# 2. 初始化 Kokoro
kokoro = Kokoro("kokoro-v1.1-zh.onnx", "voices-v1.1-zh.bin", vocab_config="config.json")

# 3. 将中文转换为音素
text = "寒风凛冽，如刀割般划过脸颊。"
phonemes, _ = g2p(text)

# 4. 传入音素合成音频 (设置 is_phonemes=True)
samples, sample_rate = kokoro.create(
    phonemes,
    voice="zf_001",
    speed=1.0,
    is_phonemes=True
)
```

## 开发与资源构建脚本说明 (Developer & Resource Scripts)

在 `scripts` 文件夹下，包含两个主要面向开发者和资源构建的脚本，运行它们通常需要安装额外的依赖（如 `torch`、`tqdm`、`requests` 等）：

* **`scripts/fetch_voices.py` —— 声音包拉取与打包工具**：

  * **作用**：将官方（Hugging Face 上）零散的声音特征文件（如 `af_maple.pt` 等）打包合并为单个二进制文件 `voices-v1.0.bin` 或 `voices-v1.1-zh.bin`，以方便本库在推理时进行一键加载。
  * **运行方式**：`uv run scripts/fetch_voices.py`（会自动通过 pip 下载依赖并合并生成二进制声音文件）。
  * **详细原理** ：

  1. 官方（Hugging Face 上）的每个人物音色（如 `af_maple`, `zf_001` 等）的声音特征都是单独存放的 PyTorch 格式文件（以 `.pt` 结尾，如 `af_maple.pt`）。
  2. 如果在代码中每次用到新音色都去实时下载，会非常慢。
  3. 这个脚本会首先请求 Hugging Face 获取所有音色列表，然后 **批量下载这几十甚至上百个音色文件** 。
  4. 下载后，它会使用 PyTorch (`torch.load`) 将它们读入，转化为 Numpy 数组，最后通过 `np.savez` 把它们 **合并压缩成一个单独的大二进制包** （如 `voices-v1.1-zh.bin`）。
* **`scripts/export.py` —— 模型导出 ONNX 工具**：

  * **作用**：将官方的原始 PyTorch 模型（`.pth` 格式）转换导出为可在 ONNX Runtime 下免 PyTorch 环境直接运行的 `.onnx` 模型文件。
  * **运行方式**：`uv run scripts/export.py --config_file <path_to_config> --checkpoint_path <path_to_pth>`。它还包含 `--check` 和 `--inference` 参数来检测导出模型的发音正确性。
  * **详细原理** ：

  1. 官方发布的 Kokoro 模型是基于 PyTorch 框架开发的，后缀为 `.pth`。这种模型运行需要安装庞大的 PyTorch 库，且部署麻烦。
  2. 我们的项目叫 `kokoro-onnx`，目标是使用体积小、速度快的 ONNX Runtime 推理引擎来运行它。
  3. 这个脚本会加载官方的 `kokoro` Python 库（包含原始模型结构定义），读取 `.pth` 权重，然后调用 `torch.onnx.export` 将其编译转换，最终生成我们在例子中使用的 `.onnx` 模型文件（如 `kokoro-v1.0.onnx`）。
  4. 它还包含测试选项，转换后可以立马用 ONNX 跑一下并播放声音，检查转换出来的模型声音有没有变味。

## Contribute

See [CONTRIBUTE.md](CONTRIBUTE.md)

## License

- kokoro-onnx: MIT
- kokoro model: Apache 2.0
