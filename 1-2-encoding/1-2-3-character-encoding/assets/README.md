# Encoding lab assets

These files support \`1-2-3-character-encoding-v6-2.pptx\`.

Generate / regenerate:

\`\`\`bash
python 1-2-encoding/1-2-3-character-encoding/demos/create_lab_files.py
\`\`\`

Both represent:

\`\`\`text
A中B国C文
\`\`\`

Expected bytes:

\`\`\`text
gb2312-lab.txt
41 D6 D0 42 B9 FA 43 CE C4

utf8-lab.txt
41 E4 B8 AD 42 E5 9B BD 43 E6 96 87
\`\`\`

Generated-image provenance:

\`\`\`text
assets/generated/image-prompts.md
\`\`\`
