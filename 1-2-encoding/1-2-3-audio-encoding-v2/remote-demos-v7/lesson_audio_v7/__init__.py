"""Teaching demo utilities; compression work does not require browser-widget extras."""
from .core import player_data, lab_data, quantize, compression_data


def __getattr__(name):
    if name in {'listening_demo', 'zoom_demo', 'encoding_lab'}:
        from . import widgets
        return getattr(widgets, name)
    raise AttributeError(name)
