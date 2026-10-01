"""Generate staged student sheets without exposing later codewords or exit data."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parent.parent
source=(ROOT/'activities/panda-v4-student.md').read_text()
header=source.split('---',2)[1]
outputs=[]
for key,title in [('a','A'),('b','B'),('exit','E1')]:
    body=re.search(rf'<!-- stage-{key}:start -->\s*([\s\S]*?)\s*<!-- stage-{key}:end -->',source).group(1)
    current_header=re.sub(r'^title:.*$',f'title: "图像编码活动单 {title}"',header,flags=re.M)
    path=ROOT/f'activities/panda-v4-student-{key}.md'
    path.write_text('---'+current_header+'---\n\n姓名：____________　班级：____________　日期：____________\n\n先独立作答，再按教师指示核对。\n\n'+body+'\n')
    outputs.append(str(path.relative_to(ROOT)))
assert '11 11 01 00 00 01 11 00' not in (ROOT/'activities/panda-v4-student-a.md').read_text()
assert '12×10' not in (ROOT/'activities/panda-v4-student-a.md').read_text()+(ROOT/'activities/panda-v4-student-b.md').read_text()
print(json.dumps({'generated':outputs,'later_answer_and_exit_data_withheld':True}))
