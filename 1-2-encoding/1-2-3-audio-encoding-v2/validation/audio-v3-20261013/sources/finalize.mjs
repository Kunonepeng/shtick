import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const workspaceDir = path.resolve(process.argv[2] ?? path.join(path.dirname(fileURLToPath(import.meta.url)), 'build-output'));
const skillTools = process.env.AUDIO_V3_PRESENTATION_TOOLS ?? '/Users/chran/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations/container_tools';
const { finalizePresentation } = await import(pathToFileURL(path.join(skillTools, 'artifact_tool_utils.mjs')).href);
const tableOwners = [2, 3, 12, 13, 51, 52, 53, 54];
await fs.mkdir(`${workspaceDir}/output`, {recursive: true});
const receipt = await finalizePresentation({
  workspaceDir,
  candidatePath: `${workspaceDir}/candidate.pptx`,
  finalPath: process.argv[3] ?? `${workspaceDir}/output/1-2-3-audio-encoding-v3.pptx`,
  pythonExecutable: process.env.AUDIO_V3_PYTHON ?? '/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
  integrityValidatorPath: `${skillTools}/inspect_presentation_package_integrity.py`,
  layoutValidatorPath: `${skillTools}/inspect_presentation_layout_geometry.py`,
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-bullet-geometry', '--validate-heading-fit', ...tableOwners.flatMap(n => ['--require-native-table-slide', String(n)])],
  requiredNativeTableOwnerSlides: tableOwners,
  requiredNativeChartOwnerSlides: [],
  explicitTotalSlideCount: 54,
  fontPolicy: {basis: 'design', families: ['Alibaba PuHuiTi 3.0 55 Regular', 'Alibaba PuHuiTi 3.0 115 Black']},
  verifyArtifactToolImport: true,
  receiptPath: `${workspaceDir}/final-validation.json`,
});
console.log(JSON.stringify(receipt));
