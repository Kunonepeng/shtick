import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const root='/Users/chran/repo/shtick/1-2-encoding/1-2-3-image-encoding-v2';
const skill='/Users/chran/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.10847/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=path.join(root,'exports','1-2-3-image-encoding-panda-v1.pptx');
await fs.mkdir(path.dirname(finalPath),{recursive:true});
const result=await finalizePresentation({
  workspaceDir:root,
  candidatePath:path.join(root,'.codex-build','candidate-panda.pptx'),
  finalPath,
  pythonExecutable:'/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
  integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...[10,11,29,30,33,34,35,36,49,50].flatMap(n=>['--require-native-table-slide',String(n)])],
  fontPolicy:{basis:'user_request',families:['Alibaba PuHuiTi 3.0 115 Black','Alibaba PuHuiTi 3.0 55 Regular']},
  requiredNativeTableOwnerSlides:[10,11,29,30,33,34,35,36,49,50],
  verifyArtifactToolImport:true,
  receiptPath:path.join(root,'.codex-build','validation-panda-v1.json'),
});
console.log(JSON.stringify(result));
