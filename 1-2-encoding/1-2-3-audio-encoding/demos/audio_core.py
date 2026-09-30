"""音频课共用计算；离线运行，不读麦克风，不需要原始 M4A 解码器。"""
from pathlib import Path
import json, wave
import numpy as np
ROOT = Path(__file__).resolve().parents[1]

def quantize(x, bits):
    """课堂等间隔中点量化模型；范围[-1,1)，上边界截到最后一档。"""
    if not 1 <= int(bits) <= 16:
        raise ValueError('bits must be 1..16')
    x = np.asarray(x, dtype=float)
    levels = 2 ** int(bits)
    indices = np.clip(np.floor((x + 1) * levels / 2), 0, levels - 1).astype(int)
    representatives = -1 + (indices + 0.5) * 2 / levels
    return indices, representatives

def codes(indices, bits):
    return [format(int(i), f'0{bits}b') for i in indices]

def read_pcm(path):
    with wave.open(str(path), 'rb') as w:
        if w.getsampwidth() != 2 or w.getcomptype() != 'NONE':
            raise ValueError('Expected 16-bit integer PCM WAV')
        fs, channels = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float) / 32768
    return fs, x.reshape(-1, channels)

def write_pcm(path, x, fs):
    x = np.asarray(x, dtype=float)
    if x.ndim == 1: x = x[:, None]
    if not np.isfinite(x).all(): raise ValueError('nonfinite sample')
    pcm = np.clip(np.rint(x * 32768), -32768, 32767).astype('<i2')
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(int(fs))
        w.writeframes(pcm.tobytes())

def resample_filtered(x, source_fs, target_fs):
    """离线课堂重采样：FFT低通(含过渡带)后插值，边缘补零；不是裸丢点。"""
    x = np.asarray(x, dtype=float)
    if x.ndim == 1: x = x[:, None]
    padding = max(source_fs // 2, 1024)
    padded = np.pad(x, ((padding, padding), (0, 0)))
    n = len(padded)
    f = np.fft.rfftfreq(n, 1 / source_fs)
    nyquist = min(source_fs, target_fs) / 2
    pass_edge, stop_edge = 0.82 * nyquist, 0.96 * nyquist
    gain = np.ones_like(f)
    gain[f >= stop_edge] = 0
    transition = (f > pass_edge) & (f < stop_edge)
    gain[transition] = .5 * (1 + np.cos(np.pi * (f[transition] - pass_edge) / (stop_edge - pass_edge)))
    filtered = np.fft.irfft(np.fft.rfft(padded, axis=0) * gain[:, None], n=n, axis=0)[padding:padding + len(x)]
    count = int(round(len(x) * target_fs / source_fs))
    target_t = np.arange(count) / target_fs
    source_t = np.arange(len(x)) / source_fs
    return np.column_stack([np.interp(target_t, source_t, filtered[:, c]) for c in range(x.shape[1])])

def pcm_info(path):
    with wave.open(str(path), 'rb') as w:
        fs, n, channels, bytes_per = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        pcm = w.readframes(n)
    return dict(sample_rate=fs, frames=n, duration=n/fs, channels=channels,
                stored_bits=bytes_per*8, payload_bytes=len(pcm), file_bytes=Path(path).stat().st_size,
                overhead_bytes=Path(path).stat().st_size-len(pcm))

def payload_size(fs, seconds, bits, channels):
    return fs * seconds * bits * channels / 8

def show_audio(name):
    from IPython.display import Audio, display
    display(Audio(filename=str(ROOT / 'assets' / 'audio' / name)))

def plot_sampling(fs=12, reveal=False):
    import matplotlib.pyplot as plt
    t = np.linspace(0, 1, 1001)
    s = np.arange(fs) / fs
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(t, .8*np.sin(2*np.pi*2*t+.3), color='#8C64E1', linewidth=3)
    if reveal: ax.plot(s, .8*np.sin(2*np.pi*2*s+.3), 'o', color='#E65050', markersize=9)
    ax.set(xlabel='Time (s)', ylabel='Normalized amplitude', xlim=(0,1), ylim=(-1.1,1.1))
    ax.grid(alpha=.15); plt.show()

def plot_quantization(bits=2, reveal=False):
    import matplotlib.pyplot as plt
    t = np.arange(48)/48
    x = .68*np.sin(2*np.pi*2*t+.3)
    idx, q = quantize(x, bits)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(t, x, color='#8C64E1', linewidth=2, label='Reference samples')
    if reveal:
        ax.plot(t, q, 'o', color='#15B5CE', label=f'{bits}-bit model')
        ax.vlines(t, x, q, color='#E65050', linewidth=1)
    ax.set(xlabel='Time (s)', ylabel='Normalized amplitude', ylim=(-1.1,1.1))
    ax.legend(); ax.grid(alpha=.15); plt.show()
