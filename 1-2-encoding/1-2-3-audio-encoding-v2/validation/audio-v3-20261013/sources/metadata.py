"""Set v3 identity without changing slide, notes, or layout parts."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import sys

PPTX = Path(sys.argv[1])
NS = {
    'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)
with ZipFile(PPTX) as source:
    parts = [(info, source.read(info.filename)) for info in source.infolist()]
root = ET.fromstring(dict((info.filename, data) for info, data in parts)['docProps/core.xml'])
values = {
    'dc:title': '声音的数字化 · v3',
    'dc:subject': '采样、量化、编码与未压缩PCM计数',
    'dc:description': '54 editable slides: 50 main slides and 4 optional appendix slides. Two ranked review/fix/recheck rounds completed. Local validation only; classroom application, projection, audio, and observed pacing remain unverified.',
    'dc:creator': 'Codex',
    'cp:lastModifiedBy': 'Codex',
}
for key, value in values.items():
    prefix, local = key.split(':')
    node = root.find(key, NS)
    if node is None:
        node = ET.SubElement(root, '{' + NS[prefix] + '}' + local)
    node.text = value
updated = ET.tostring(root, encoding='utf-8', xml_declaration=True)
staged = PPTX.with_suffix('.metadata-stage.pptx')
with ZipFile(staged, 'w') as target:
    for info, data in parts:
        target.writestr(info, updated if info.filename == 'docProps/core.xml' else data)
staged.replace(PPTX)
