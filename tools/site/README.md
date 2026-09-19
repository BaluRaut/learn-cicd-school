# tools/site — how the docs site is generated

The pages under `docs/` are built from one data module and four generators, then the Marathi
layer is applied with The School's shared i18n tool.

```bash
# 1) regenerate the English pages (course.py = titles, analogies, quiz, study plan)
python3 tools/site/gen_pages.py       # quiz.html, study-plan.html
python3 tools/site/gen_tradeoffs.py   # before-and-tradeoffs.html
python3 tools/site/gen_pipelines.py   # pipelines.html (reads the four real pipeline files)
python3 tools/site/gen_index.py       # index.html + lesson-diagrams.html (diagrams.html = the 12 SVG sections)

# 2) re-apply Marathi (tool + dictionary live in github.com/BaluRaut/school → i18n/)
python3 ../school/i18n/i18n_tool.py apply ../school/i18n/mr.json docs/*.html
#    new English strings show up as untranslated: extract → translate → merge → apply

# 3) the 4K poster: render docs/images/big-picture.svg with headless Chrome at 4x
#    (an <img> wrapper at 1920x1560, --force-device-scale-factor=4, then convert to RGB PNG)
```

`css/*.styles.html` are the shared page styles (same family as the sibling schools, accent swapped to green).
