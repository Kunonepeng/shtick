# Character Encoding Classroom Package

Production baseline:

\`\`\`text
1-2-3-character-encoding-v6-2.pptx
\`\`\`

Companion artifacts:

- \`teacher-guide.qmd\`
- \`demo-lab-teacher.ipynb\`
- \`demo-lab-student.ipynb\`
- \`assets/gb2312-lab.txt\`
- \`assets/utf8-lab.txt\`
- \`assets/generated/image-prompts.md\`
- \`demos/demo_unicode_utf.py\`
- \`demos/check_classroom_package.py\`
- \`worksheets/character-encoding-exit-ticket.qmd\`
- \`worksheets/character-encoding-exit-ticket.pdf\`

The two role-specific notebooks and raw lab files are **generated artifacts** and are intentionally ignored by Git.

Before class, from the repository root run:

\`\`\`bash
python tools/build_character_encoding_classroom_package.py
python 1-2-encoding/1-2-3-character-encoding/demos/check_classroom_package.py
\`\`\`

This generates the notebooks, raw GB2312 / UTF-8 lab files, and refreshes the printable worksheet. Then open the production PPTX and the two role-specific notebooks.
