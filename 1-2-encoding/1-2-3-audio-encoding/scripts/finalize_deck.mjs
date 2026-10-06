// Validate the current candidate and deliver a new version without overwriting historical decks.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const SKILL=process.env.PRESENTATIONS_SKILL_DIR||'/Users/chran/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.10847/skills/presentations';
const PYTHON=process.env.ARTIFACT_PYTHON||'/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const finalPath=path.resolve(process.argv[2]||path.join(ROOT,'exports/1-2-3-audio-encoding-v4-final.pptx'));
const receiptPath=path.resolve(process.argv[3]||path.join(ROOT,'validation/v4/native-finalization.json'));
const plan=JSON.parse(await fs.readFile(path.join(ROOT,'validation/v4/slide-plan.json'),'utf8'));
process.env.RUNTIME_NODE_MODULES ||= await fs.realpath(path.join(ROOT,'.build/node_modules'));
process.env.RUNTIME_NODE ||= process.execPath;
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:path.join(ROOT,'.build/v4/audio-candidate.pptx'),finalPath,pythonExecutable:PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],explicitTotalSlideCount:plan.length,fontPolicy:{basis:'user_request',families:['Alibaba PuHuiTi 3.0 115 Black','Alibaba PuHuiTi 3.0 55 Regular']},verifyArtifactToolImport:true,receiptPath});
console.log(JSON.stringify(result));
