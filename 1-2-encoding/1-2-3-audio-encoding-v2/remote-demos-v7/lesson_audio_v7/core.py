"""Small standard-library audio samples for browser-side Jupyter demos.

No microphone, ffmpeg or sounddevice required. This module executes on macOS.
The resulting WAV and sample arrays are transferred to the browser widget.
"""
from __future__ import annotations

import base64
import io
import math
import struct
import wave
import zlib
from typing import Sequence


def demo_samples(rate: int = 12000, seconds: float = 4.0) -> list[float]:
    """Deterministic original recording-like demo with three audible segments."""
    if rate < 2000 or seconds <= 0:
        raise ValueError("invalid audio rate/duration")
    length = round(rate * seconds)
    out = []
    for i in range(length):
        t = i / rate
        if t < 1.1:
            a = 0.44 * math.sin(2*math.pi*220*t)
        elif t < 2.3:
            a = 0.16 * math.sin(2*math.pi*330*t) + 0.18 * math.sin(2*math.pi*440*t)
        elif t < 2.7:
            a = 0.02 * math.sin(2*math.pi*220*t)
        else:
            e = math.exp(-3*(t-2.7))
            a = e * (0.6*math.sin(2*math.pi*180*t) + 0.08*math.sin(2*math.pi*600*t))
        out.append(max(-1, min(1, a)))
    return out


def wav_base64(samples: Sequence[float], rate: int) -> str:
    """Playable mono PCM-16 WAV suitable for HTMLAudioElement in a remote browser."""
    with io.BytesIO() as buf:
        with wave.open(buf, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(rate)
            ints = [max(-32768, min(32767, int(round(x*32767)))) for x in samples]
            w.writeframes(struct.pack('<'+'h'*len(ints),*ints))
        return base64.b64encode(buf.getvalue()).decode('ascii')


def extrema(samples: Sequence[float], bins: int = 600) -> list[list[float]]:
    """Envelope with true min/max per display bin; do not mistake these for samples."""
    if not samples or bins < 1:
        raise ValueError('empty samples or bad bins')
    step = max(1, math.ceil(len(samples)/bins))
    return [[round(min(samples[i:i+step]),5),round(max(samples[i:i+step]),5)]
            for i in range(0,len(samples),step)]


def player_data(detail: bool = True) -> dict:
    rate = 12000
    samples = demo_samples(rate=rate, seconds=4.0)
    return {
        'rate':rate,
        'length':len(samples),
        'duration':len(samples)/rate,
        'audio_b64':wav_base64(samples,rate),
        'envelope':extrema(samples,720),
        'samples': [round(x,5) for x in samples] if detail else [],
    }


def quantize(sample: float, bits: int) -> tuple[int,float]:
    """Uniform mid-rise toy quantizer on [-1,1]; code is *unsigned level index*."""
    if bits not in (2,3,4):
        raise ValueError('use 2,3,4 bits for display')
    levels = 1 << bits
    v = min(1.0,max(-1.0,float(sample)))
    code = max(0,min(levels-1,int(math.floor((v+1)*levels/2))))
    representative = -1 + (code+.5)*2/levels
    return code, representative


def lab_data() -> dict:
    """Precompute exact points, quantization and codes for all choices on the Mac."""
    # One 4ms window of a 250Hz wave, shown as a conceptual source waveform.
    # Rates here are illustrative; audio recording typically uses much higher rates.
    frequency=250
    duration_ms=4.0
    phase=0.22
    out={}
    for rate in (2000,4000,8000):
        series=[]
        for i in range(round(rate*duration_ms/1000)):
            t=i/rate
            original=.83*math.sin(2*math.pi*frequency*t+phase)
            representations={}
            for bits in (2,3,4):
                code,y=quantize(original,bits)
                representations[str(bits)]={'level':code,'quant':round(y,6),'binary':format(code,f'0{bits}b')}
            series.append({'t_ms':round(t*1000,6),'amplitude':round(original,6),'by_bits':representations})
        out[str(rate)]=series
    return {'rates':out,'frequency':frequency,'duration_ms':duration_ms,'phase':phase,'amplitude':.83}


def compression_data() -> list[dict]:
    """Same input size, zlib with default settings; deterministic comparison."""
    a=b'A'*1000
    # Deterministic pseudo-random byte stream with far less repeated structure.
    import random
    rng=random.Random(2026)
    b=bytes(rng.randrange(256) for _ in range(1000))
    return [
        {'label':'A：重复字节','before':len(a),'after':len(zlib.compress(a))},
        {'label':'B：变化字节','before':len(b),'after':len(zlib.compress(b))},
    ]
