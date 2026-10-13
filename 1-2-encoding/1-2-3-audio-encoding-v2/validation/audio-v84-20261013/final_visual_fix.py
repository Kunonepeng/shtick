#!/usr/bin/env python3
"""Final accessibility audit fix for the published tenth visual round."""
from pathlib import Path
from pptx import Presentation
import hashlib,json
root=Path(__file__).resolve().parents[2]
target=root/"1-2-3-audio-encoding-v8.4.10.pptx"
report=Path(__file__).resolve().parent/"round-10-audit.json"
p=Presentation(target)
assert len(p.slides)==70
sl=p.slides[15]
old="下一页请预测3.71的归属，再揭示区间规则。"
new="下一页再研究具体采样值属于哪个区间。"
changes=0
for sh in sl.shapes:
    if not sh.has_text_frame:continue
    for para in sh.text_frame.paragraphs:
        for run in para.runs:
            if old in run.text:
                run.text=run.text.replace(old,new)
                changes+=1
assert changes==1, changes
p.save(target)
j=json.loads(report.read_text(encoding="utf-8"))
j["output_sha256"]=hashlib.sha256(target.read_bytes()).hexdigest()
j["output_bytes"]=target.stat().st_size
j["post_round_quality_fix"]="Removed forward-looking 3.71 numeric hint from the 8-level counting slide; preserves prediction on next slide."
report.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding="utf-8")
q16=" ".join(x.text for x in p.slides[15].shapes if x.has_text_frame)
q49=" ".join(x.text for x in p.slides[48].shapes if x.has_text_frame)
assert "3.71" not in q16 and "压缩编码" not in q49
assert j["speaker_notes"]==70
print("FINAL PREDICTION GATE PASS",target.stat().st_size,j["output_sha256"])
