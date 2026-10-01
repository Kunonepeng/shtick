"""Check measured image evidence and stage-by-stage knowledge disclosure."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib
import json
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demos"))
import compression_lab as lab
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}

def main():
    issues = []
    def check(ok, message):
        if not ok: issues.append(message)
    photo = json.loads((ROOT / "sources/photo-evidence.json").read_text())
    check(photo["input_sha256"] == hashlib.sha256((ROOT/photo["input_file"]).read_bytes()).hexdigest(), "Supplied image changed")
    measured = json.loads(json.dumps(lab.photo_evidence()))
    check(photo["evidence"] == measured, "Photo pixel/byte record drift")
    check(json.loads((ROOT/"sources/evidence-manifest.json").read_text())["D5_photo"] == measured, "Notebook manifest photo drift")
    check(measured["结果"][0]["回读像素一致"] and not measured["结果"][1]["回读像素一致"], "Photo reversible/lossy evidence failed")
    for name, crop in [("painting-source.png", "painting-crop-source.png"),
                       ("painting-quality80.jpg", "painting-crop-quality80.png")]:
        with Image.open(ROOT/"assets/evidence"/name) as im:
            expected = im.convert("RGB").crop((368,310,560,438)).resize((768,512), Image.Resampling.NEAREST)
        with Image.open(ROOT/"assets/evidence"/crop) as im:
            check(im.convert("RGB").tobytes() == expected.tobytes(), f"Inconsistent crop: {crop}")
    tree = json.loads((ROOT/"sources/knowledge-tree.json").read_text())
    plan = json.loads((ROOT/"sources/slide-plan.json").read_text())
    stages = []
    positions = {}
    with ZipFile(sys.argv[1]) as z:
        for i, row in enumerate(plan, 1):
            if not row["stage"].startswith("knowledge-"): continue
            stage = int(row["stage"].split("-")[1])
            stages.append(stage)
            if stage > 0:
                check(plan[i-2]["q"] == tree["checkpoints"][stage]["after"], "Checkpoint placed before its Q group finishes")
            xml = ET.fromstring(z.read(f"ppt/slides/slide{i}.xml"))
            shapes = {s.find("p:nvSpPr/p:cNvPr",NS).get("name"): s for s in xml.findall("p:cSld/p:spTree/p:sp",NS)}
            expected_ids = {"tree-leaf-"+n["id"] for n in tree["leaves"] if n["stage"] <= stage}
            actual_ids = {n for n in shapes if n.startswith("tree-leaf-") and not n.startswith("tree-leaf-link-")}
            check(actual_ids == expected_ids, f"Stage {stage}: missing or premature knowledge leaf")
            for name in ["tree-root", *["tree-branch-"+b["id"] for b in tree["branches"]], *sorted(actual_ids)]:
                shape = shapes[name]
                signature = (ET.tostring(shape.find("p:spPr/a:xfrm",NS)),
                             "".join(n.text or "" for n in shape.findall(".//a:t",NS)))
                if name in positions: check(signature == positions[name], f"Unstable knowledge geometry: {name}")
                positions[name] = signature
            fresh_branches = {n["branch"] for n in tree["leaves"] if n["stage"] == stage} if stage else set()
            actual_focus = {n.removeprefix("tree-focus-") for n in shapes if n.startswith("tree-focus-")}
            check(actual_focus == fresh_branches, f"Stage {stage}: red focus not limited to new nodes")
            check(not xml.findall(".//p:pic",NS), "Knowledge tree rasterized instead of editable")
        q7 = next(row["slide"] for row in plan if row["q"] == "Q7" and row["stage"] == "question")
        xml = ET.fromstring(z.read(f"ppt/slides/slide{q7}.xml"))
        visible = "".join(n.text or "" for n in xml.findall(".//a:t",NS))
        check(not any(v in visible for v in ["504,742", "240,848", "PNG", "quality", "像素一致"]), "Q7 image question reveals answer")
    check(stages == list(range(5)), "Knowledge checkpoints missing/out of order")
    for role in ["teacher", "student"]:
        doc = json.loads((ROOT/f"demo-lab-{role}.ipynb").read_text())
        text = "\n".join("".join(c["source"]) for c in doc["cells"])
        check(text.count("### 阶段小结：") == 4, f"{role} notebook lacks stage summaries")
        check(("assets/knowledge/tree-" in text) == (role == "teacher"), f"{role} map audience separation failed")
    result = {"pass": not issues, "issues": issues, "knowledge_stages": stages,
              "image_input_sha256": photo["input_sha256"], "D5_photo": measured,
              "crop_xywh": photo["crop_xywh"], "stable_native_nodes": len(positions)}
    (ROOT/"validation/improvement-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({"pass": result["pass"], "issues": issues, "knowledge_stages": stages, "stable_native_nodes": len(positions)}))
    raise SystemExit(bool(issues))

if __name__ == "__main__":
    main()
