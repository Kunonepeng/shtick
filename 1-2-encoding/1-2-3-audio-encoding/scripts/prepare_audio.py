"""Prepare controlled evidence from decoded PCM; preserve the source M4A."""
from pathlib import Path
import sys, hashlib, json
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'demos'))
from audio_core import read_pcm, write_pcm, resample_filtered, quantize, pcm_info
source = ROOT/'assets/nizhan-zhangjie.m4a'
decoded = ROOT/'assets/source/excerpt-45-51-decoded-pcm16.wav'
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--decoded', type=Path, default=decoded)
parser.add_argument('--decoded-start', type=float, default=45)
parser.add_argument('--output-dir', type=Path, default=ROOT/'assets/audio')
parser.add_argument('--manifest', type=Path, default=ROOT/'assets/audio-manifest.json')
args = parser.parse_args()
fs, stereo = read_pcm(args.decoded)
# Use the same six-second excerpt starting at 45 seconds for all comparisons.
start, seconds = 45, 6
clip = stereo[int((start-args.decoded_start)*fs):int((start+seconds-args.decoded_start)*fs)].copy()
assert len(clip) == seconds*fs
mono = clip.mean(axis=1)
# Apply one shared gain and a 10 ms fade; never normalize versions independently.
gain = .72 / max(np.max(np.abs(clip)), 1e-12)
clip *= gain; mono *= gain
fade = int(.01*fs); env = np.ones(len(clip))
env[:fade] = np.linspace(0,1,fade); env[-fade:] = np.linspace(1,0,fade)
clip *= env[:,None]; mono *= env
out = args.output_dir
out.mkdir(parents=True, exist_ok=True)
write_pcm(out/'music-44100-16-mono.wav', mono, fs)
write_pcm(out/'music-44100-16-stereo.wav', clip, fs)
x22 = resample_filtered(mono, fs, 22050)[:,0]
x8 = resample_filtered(mono, fs, 8000)[:,0]
write_pcm(out/'music-22050-16-mono.wav', x22, 22050)
write_pcm(out/'music-8000-16-mono.wav', x8, 8000)
# Store effective 2/4/8-bit model results in 16-bit PCM for playback compatibility.
for bits in [2,4,8]:
    _, q = quantize(x22, bits)
    write_pcm(out/f'music-22050-effective{bits}-stored16-mono.wav', q, 22050)
# Generate a reproducible tone fixture for the frequency constraint.
t = np.arange(3*24000)/24000
base = .24*np.sin(2*np.pi*6000*t)
base[:240] *= np.linspace(0,1,240); base[-240:] *= np.linspace(1,0,240)
write_pcm(out/'tone-6000-at24000.wav', base, 24000)
write_pcm(out/'tone-lowpass-at8000.wav', resample_filtered(base,24000,8000)[:,0],8000)
# Diagnostic only: deliberately omit anti-alias filtering.
write_pcm(out/'tone-alias-naive-at8000.wav', base[::3],8000)
# Prepare the two-second, 8 kHz, 16-bit mono counting fixture.
write_pcm(out/'size-check-8000-2s-16-mono.wav', x8[:16000],8000)
records=[]
for p in sorted(out.glob('*.wav')):
    item=pcm_info(p); item['file']=p.name; item['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    item['effective_bits']=int(p.name.split('effective')[1].split('-')[0]) if 'effective' in p.name else 16
    records.append(item)
manifest=dict(source_file='assets/nizhan-zhangjie.m4a',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              source_format='AAC in M4A; 44100 Hz; stereo; afinfo reported ~65536 bit/s',
              source_duration_seconds=275.6422,excerpt_start_seconds=start,excerpt_duration_seconds=seconds,
              shared_gain=float(gain),fade_seconds=.01,files=records,
              caveat='PCM WAV由有损AAC解码而来，不恢复已损失信息。低位数量化音频使用16bit存储，不能按有效位数计算这些文件大小。')
args.manifest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'excerpt':f'{start}..{start+seconds}s','files':len(records),'size_check':pcm_info(out/'size-check-8000-2s-16-mono.wav')},ensure_ascii=False))
