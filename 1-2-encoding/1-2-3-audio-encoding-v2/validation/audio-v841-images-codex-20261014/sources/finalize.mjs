import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const ROOT=path.resolve(process.env.AUDIO_BUILD_DIR??'/private/tmp/audio841-images-codex/build');
const WORK=path.resolve(ROOT,'..');
const LESSON=path.resolve(process.env.AUDIO_LESSON_DIR??path.join(path.dirname(new URL(import.meta.url).pathname),'../../..'));
const SKILL='/Users/chran/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const plan=JSON.parse(await fs.readFile(path.join(ROOT,'plan-2.json'),'utf8'));
const finalDir=path.resolve(process.env.AUDIO_FINAL_DIR??path.join(WORK,'output'));await fs.mkdir(finalDir,{recursive:true});
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
// The canonical project design specifies these faces; source inheritance has unresolved entries.
const result=await finalizePresentation({workspaceDir:WORK,candidatePath:path.join(ROOT,'candidate-2.pptx'),finalPath:path.join(finalDir,'1-2-3-audio-encoding-v8.4.1.with-images-by-codex.pptx'),pythonExecutable:'/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12191695,6858000','--expected-slide-count',String(plan.slideCount),'--validate-heading-fit','--validate-bullet-geometry'],fontPolicy:{basis:'design',families:['Alibaba PuHuiTi 3.0 55 Regular','Alibaba PuHuiTi 3.0 115 Black']},verifyArtifactToolImport:true,receiptPath:process.env.AUDIO_RECEIPT_PATH??path.join(ROOT,'finalizer-receipt.json')});
console.log(JSON.stringify(result));
