"""Shared offline audio computations; no microphone or source AAC decoder required."""
from pathlib import Path
import json, wave
import numpy as np
ROOT = Path(__file__).resolve().parents[1]

def quantize(x, bits):
    """Uniform midpoint quantizer on [-1, 1); clip overload inputs to endpoint bins."""
    if isinstance(bits, bool) or int(bits) != bits or not 1 <= int(bits) <= 16:
        raise ValueError('bits must be 1..16')
    x = np.asarray(x, dtype=float)
    if not np.isfinite(x).all():
        raise ValueError('Quantizer input must be finite')
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
    """Teaching resampler: zero-padded FFT lowpass with transition band, then interpolation."""
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

def show_audio(name, label=None):
    from IPython.display import Audio, HTML, display
    from html import escape
    if label:
        display(HTML(f'<p style="font-size:24px;margin:8px 0">{escape(label)}</p>'))
    display(Audio(filename=str(ROOT / 'assets' / 'audio' / name)))

def show_pcm_evidence(stage='size'):
    """D4: reveal one evidence table at a time, using actual WAV measurements."""
    from IPython.display import HTML, display
    evidence = [
        ('2秒样例', 'size-check-8000-2s-16-mono.wav'),
        ('开场A', 'music-44100-16-mono.wav'),
        ('开场B', 'music-8000-16-mono.wav')
    ]
    if stage not in ['size', 'opening']:
        raise ValueError('stage must be size or opening')
    selected = evidence[:1] if stage == 'size' else evidence[1:]
    records = [(label, pcm_info(ROOT / 'assets/audio' / name)) for label, name in selected]
    style = 'border-collapse:collapse;font-size:24px;line-height:1.6;color:#262626;'
    cell = 'padding:8px 14px;border-bottom:1px solid #ddd;text-align:right;'
    def table(rows):
        headers = ['文件', '采样率Hz', '时长s', '存储bit', '声道数', '样本数据B', '完整文件B']
        markup = f'<table style="{style}"><thead><tr>'
        markup += ''.join(f'<th style="{cell}">{h}</th>' for h in headers) + '</tr></thead><tbody>'
        for label, info in rows:
            values = [label, f"{info['sample_rate']:,}", f"{info['duration']:g}",
                      info['stored_bits'], info['channels'], f"{info['payload_bytes']:,}", f"{info['file_bytes']:,}"]
            markup += '<tr>' + ''.join(f'<td style="{cell}">{v}</td>' for v in values) + '</tr>'
        return markup + '</tbody></table>'
    heading = '核对2秒样例：样本数据与完整文件' if stage == 'size' else '回看开场：A、B的哪个记录参数不同？'
    display(HTML(f'<h3>{heading}</h3>' + table(records)))
    return {label: info for label, info in records}

def show_waveform():
    """Display the teaching waveform before discrete recording is discussed."""
    return plot_sampling(12, False)

def show_recorded_values():
    """Reveal the recorded values only after the class has proposed a method."""
    return plot_sampling(12, True)

def plot_sampling(fs=12, reveal=False):
    import matplotlib.pyplot as plt
    t = np.linspace(0, 1, 1001)
    s = np.arange(fs) / fs
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(t, .8*np.sin(2*np.pi*2*t+.3), color='#8C64E1', linewidth=3)
    if reveal: ax.plot(s, .8*np.sin(2*np.pi*2*s+.3), 'o', color='#E65050', markersize=9)
    ax.set(xlabel='Time (s)', ylabel='Normalized amplitude', xlim=(0,1), ylim=(-1.1,1.1))
    ax.tick_params(labelsize=14); ax.xaxis.label.set_size(16); ax.yaxis.label.set_size(16)
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
    ax.legend(); ax.tick_params(labelsize=14); ax.xaxis.label.set_size(16); ax.yaxis.label.set_size(16)
    ax.grid(alpha=.15); plt.show()

def plot_quantization_compare():
    """D3: one output, identical sample times, scales and ticks on both sides."""
    import matplotlib.pyplot as plt
    t = np.arange(48) / 48
    x = .68 * np.sin(2*np.pi*2*t + .3)
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.7), sharex=True, sharey=True)
    for ax, bits, color in zip(axes, [2, 4], ['#8C64E1', '#007C9B']):
        _, q = quantize(x, bits)
        ax.plot(t, x, color='#737373', linewidth=2, label='Reference samples')
        ax.plot(t, q, 'o', color=color, markersize=5, label=f'{bits} bit: {2**bits} levels')
        ax.vlines(t, x, q, color='#E65050', linewidth=1)
        ax.set(xlabel='Time (s)', xlim=(0, 1), ylim=(-1.1, 1.1), title=f'{bits}-bit quantization')
        ax.set_yticks([-.75, -.25, .25, .75]); ax.grid(alpha=.15)
        ax.tick_params(labelsize=14); ax.xaxis.label.set_size(16); ax.title.set_size(18)
        ax.legend(loc='lower left', fontsize=14)
    axes[0].set_ylabel('Normalized amplitude',fontsize=16)
    fig.tight_layout(); plt.show()

def show_quantization_evidence():
    """Revisit Q5's -0.10 without changing the input between quantizers."""
    from IPython.display import HTML, display
    rows = []
    result = {}
    for bits in [2, 4]:
        _, q = quantize([-.10], bits)
        error = abs(float(q[0]) + .10)
        result[bits] = dict(input=-.10, representative=float(q[0]), error=error)
        rows.append(f'<tr><td>{bits}bit</td><td>−0.10</td><td>{q[0]:g}</td><td>{error:g}</td></tr>')
    display(HTML('<div style="font-size:24px;line-height:1.6">沿用Q5的一个样本：'
                 '<table style="border-collapse:collapse;text-align:center">'
                 '<thead><tr><th>量化位数</th><th>同一输入</th><th>近似值</th><th>绝对误差</th></tr></thead>'
                 '<tbody>'+''.join(rows)+'</tbody></table></div>'
                 '<style>th,td{padding:8px 20px}</style>'))
    return result


def show_opening():
    """Show anonymous opening audio without filenames or parameter labels."""
    from IPython.display import HTML, display
    for label, name in [('A', 'music-44100-16-mono.wav'), ('B', 'music-8000-16-mono.wav')]:
        display(HTML(f'<p style="font-size:24px">{label}</p>'))
        show_audio(name)


def show_frequency_baseline():
    """Expose baseline playback without revealing the result fixture name."""
    return show_audio('tone-6000-at24000.wav', label='6kHz纯音：24kHz采样基准')


def show_frequency_result():
    """Display the filtered result only after the independent prediction."""
    return show_audio('tone-lowpass-at8000.wav', label='同一纯音：先低通，再降为8kHz')


def show_quantization_audio():
    """Display the controlled audio comparison after the error task."""
    show_audio('music-22050-effective4-stored16-mono.wav', label='4bit有效量化模型；存储16bit')
    show_audio('music-22050-16-mono.wav', label='16bit基准；存储16bit')
