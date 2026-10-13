"""Browser-first Jupyter widgets: Mac computes, remote browser displays and plays."""
from pathlib import Path
import anywidget
import traitlets
from .core import player_data, lab_data

HERE=Path(__file__).resolve().parent

class WaveWidget(anywidget.AnyWidget):
    _esm=HERE/'frontend.js'
    _css=HERE/'style.css'
    mode=traitlets.Unicode('player').tag(sync=True)
    payload=traitlets.Dict().tag(sync=True)

class EncodingWidget(anywidget.AnyWidget):
    _esm=HERE/'frontend.js'
    _css=HERE/'style.css'
    mode=traitlets.Unicode('lab').tag(sync=True)
    payload=traitlets.Dict().tag(sync=True)


def listening_demo():
    return WaveWidget(mode='player',payload=player_data(detail=False))


def zoom_demo():
    return WaveWidget(mode='zoom',payload=player_data(detail=True))


def encoding_lab():
    return EncodingWidget(mode='lab',payload=lab_data())
