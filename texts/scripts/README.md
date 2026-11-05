# Conversion scripts for `texts/`

One script per book converts its page transcriptions in `ocr/{dir}/` into the section files
of `texts/{dir}/`, overwriting them: the files are not edited by hand, and corrections go
into `ocr/`. Run them with [uv](https://docs.astral.sh/uv/) from the repository root, e.g.
`uv run texts/scripts/convert_en.py`. The layout and the per-book decisions they implement
are in [texts/PLAN.md](../PLAN.md).

| Script | Book | Output |
|---|---|---|
| `convert_en.py` | Carlyle's edition (`ocr/en/`, 1889) | `texts/en/` |
| `convert_en_oelsner.py` | Temple Classics edition, revised by Oelsner (`ocr/en-oelsner/`, 1903) | `texts/en-oelsner/` |
| `convert_la.py` | Serravalle's translation and commentary (`ocr/la/`, 1891) | `texts/la/` |
| `convert_grc.py` | Musurus's Greek translation (`ocr/grc/`, 1882) | `texts/grc/` |

A script reports what it leaves for review (`convert_la.py`: `HYPHEN` for each line-end
hyphen it resolved, `NO NUMBER` for the tercets printed without a number).
`ocr/la/scripts/lemmacheck.py` imports `convert_la.py` for its list of canto pages.
