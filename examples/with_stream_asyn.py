import asyncio

import sounddevice as sd

from kokoro_onnx import Kokoro

text = """
We've just been hearing from Matthew Cappucci, a senior meteorologist at the weather app MyRadar, who says Kansas City is seeing its heaviest snow in 32 years - with more than a foot (30 to 40cm) having come down so far.

Despite it looking as though the storm is slowly moving eastwards, Cappucci says the situation in Kansas and Missouri remains serious.

He says some areas near the Ohio River are like "skating rinks", telling our colleagues on Newsday that in Missouri in particular there is concern about how many people have lost power, and will lose power, creating enough ice to pull power lines down.

Temperatures are set to drop in the next several days, in may cases dipping maybe below minus 10 to minus 15 degrees Celsius for an extended period of time.

There is a special alert for Kansas, urging people not to leave their homes: "The ploughs are getting stuck, the police are getting stuck, everybody’s getting stuck - stay home."
"""


async def main():
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

    stream_generator = kokoro.create_stream(
        text,
        voice="af_nicole",
        speed=1.0,
        lang="en-us",
    )

    # 1. 开启一个持续存在的单声道 24000Hz 音频输出流
    with sd.OutputStream(samplerate=24000, channels=1, dtype="float32") as stream:
        count = 0
        async for samples, _ in stream_generator:
            count += 1
            print(f"Seamlessly writing chunk ({count}) to audio stream...")
            # 2. 向同一个流中连续写入样本，声卡会自动平滑缓冲，实现无缝连续播放
            stream.write(samples)


asyncio.run(main())
