"""Check scoped changes and whitespace without altering captured or vendor bytes."""
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
tracked=subprocess.run(['git','diff','--check'],cwd=REPO,text=True,capture_output=True)
names=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z','--',str(ROOT)],cwd=REPO).decode().split('\0')
authored=[];raw=[];binary=0;scanned=0
for name in filter(None,names):
    path=REPO/name
    try: text=path.read_text()
    except (UnicodeDecodeError,ValueError): binary+=1;continue
    scanned+=1
    captured=('/exports/reference-v4/' in str(path) or '/validation/history/v3-sources/' in str(path) or path.suffix=='.txt' and '/validation/v4/' in str(path))
    for line_number,line in enumerate(text.splitlines(),1):
        if line.rstrip(' \t')!=line:
            (raw if captured else authored).append(dict(file=name,line=line_number,kind='trailing whitespace'))
    if text.endswith('\n\n'):
        (raw if captured else authored).append(dict(file=name,kind='blank line at EOF'))
changed=subprocess.check_output(['git','diff','--name-only'],cwd=REPO,text=True).splitlines()
scope=all(name.startswith('1-2-encoding/1-2-3-audio-encoding/') for name in changed)
report=dict(date='2026-10-01',passed=tracked.returncode==0 and not authored and scope,tracked_diff_check_passed=tracked.returncode==0,tracked_output=tracked.stdout+tracked.stderr,scope_only_this_lesson=scope,new_text_files_scanned=scanned,new_binary_files=binary,authored_issues=authored,preserved_raw_output_whitespace=raw,preservation_rule='Scan includes new output and historical files. Quarto generated markup/vendor code, original snapshots and raw tool logs retain upstream whitespace; these are recorded observations, not author-source defects.')
(ROOT/'validation/v4/diff-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=report['passed'],new_text_files_scanned=scanned,authored_issues=len(authored),raw_observations=len(raw))))
raise SystemExit(0 if report['passed'] else 1)
