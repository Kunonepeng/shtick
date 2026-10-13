"""Deterministic checks for the Mac-side classroom data model."""
import io
import unittest
import wave
from lesson_audio_v7.core import demo_samples, wav_base64, extrema, player_data, quantize, lab_data, compression_data
import base64

class AudioCoreTests(unittest.TestCase):
    def test_wav_size_and_pcm_header(self):
        a=demo_samples(rate=12000,seconds=4)
        self.assertEqual(len(a),48000)
        self.assertTrue(all(-1<=v<=1 for v in a))
        binary=base64.b64decode(wav_base64(a,12000))
        with wave.open(io.BytesIO(binary),'rb') as w:
            self.assertEqual(w.getnchannels(),1)
            self.assertEqual(w.getframerate(),12000)
            self.assertEqual(w.getsampwidth(),2)
            self.assertEqual(w.getnframes(),48000)
    def test_envelope_extremes_not_faked_samples(self):
        self.assertEqual(extrema([0,1,-1,0],bins=2),[[0,1],[-1,0]])
    def test_browser_player_data(self):
        p=player_data(False)
        self.assertEqual(p['length'],p['rate']*p['duration'])
        self.assertFalse(p['samples'])
        self.assertTrue(p['audio_b64'])
        p=player_data(True)
        self.assertEqual(len(p['samples']),48000)
    def test_quantize_boundaries_and_codes(self):
        for bits in (2,3,4):
            maxcode=(1<<bits)-1
            self.assertEqual(quantize(-1,bits)[0],0)
            self.assertEqual(quantize(+1,bits)[0],maxcode)
            for x in [-1,-.39,-.001,0,.4,1]:
                code,value=quantize(x,bits)
                self.assertTrue(0<=code<=maxcode)
                self.assertTrue(-1<value<1)
        with self.assertRaises(ValueError):quantize(.1,0)
    def test_lab_sample_counts_and_stability(self):
        dat=lab_data()
        self.assertEqual(len(dat['rates']['2000']),8)
        self.assertEqual(len(dat['rates']['4000']),16)
        self.assertEqual(len(dat['rates']['8000']),32)
        for rate, points in dat['rates'].items():
            for p in points:
                for b in (2,3,4):
                    info=p['by_bits'][str(b)]
                    self.assertEqual(len(info['binary']),b)
                    self.assertEqual(int(info['binary'],2),info['level'])
        self.assertEqual([p['t_ms'] for p in dat['rates']['4000']], [round(i/4,6) for i in range(16)])
    def test_compression_theory(self):
        rows=compression_data()
        self.assertEqual([r['before'] for r in rows],[1000,1000])
        self.assertLess(rows[0]['after'],rows[1]['after'])
        self.assertLess(rows[0]['after'],50)
        self.assertGreaterEqual(rows[1]['after'],1000)

if __name__=='__main__':unittest.main()
