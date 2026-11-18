# Proper Names Check (`texts/en/`)

Cross-check of [041-index-of-proper-names.md](041-index-of-proper-names.md) against the canto files (`007-canto-01.md`–`040-canto-34.md`), run with [check_index.py](../scripts/check_index.py).

## Summary

- **Index entries parsed**: 558
- **Total canto/line references checked**: 698
- **Matched at reference (±3 lines)**: 640 (91.7%)
- **Unmatched (`CANTO_ONLY` or `MISS`)**: 58

Most of the 58 unmatched references are allusions, periphrases, or characters not yet named at the cited line (e.g., `Ugolino` at `xxxii. 125`, who is named in `xxxiii. 13`). Only the spelling and form variations below affect consistency in `texts/en/`.

## Spelling Variations

All differences below were verified against the page images (`ocr/en/*.png`) and match the 1889 print (not OCR errors):

| Index (`041`) | Canto prose / notes | Locations |
|---|---|---|
| `Apuglia` | `Apulia`, `Apulians`, `Apulian` | `016-canto-10.md` (`[^116-1]`, p. 170), `034-canto-28.md` (xxviii. 9, pp. 386–387) |
| `Caccianemico` | `Caccianimico` | `024-canto-18.md` (xviii. 50, p. 264, prose, verse, `[^210-1]`) |
| `Erinnys` | `Erynnis` | `015-canto-09.md` (ix. 45, p. 151, prose) |
| `Frieselanders` | `Friezelanders` | `037-canto-31.md` (xxxi. 64, p. 432, prose) |
| `Matthew, Apostle` | `Matthias` | `025-canto-19.md` (xix. 94, p. 280, prose) |
| `Ptolomæus, Claudius` | `Ptolemæus` | `010-canto-04.md` (iv. 142, p. 100, prose) |
| `Tisiphone` | `Tesiphone` | `015-canto-09.md` (ix. 48, p. 152, prose) |

Within the canto files:

- `Buondelmonti` (`034-canto-28.md` Argument, p. 385) vs `Buondelmonte` (`034-canto-28.md` `[^340-3]`, p. 394).

## Morphological / Form Variations

- **Plural / demonym vs singular / adjective / place name**:
  - `Aretines` (`xxx. 31`: `Aretine`)
  - `Bolognese` (`xi. 83`: `Bologna` / `Bolognese`)
  - `Florentines` (`viii. 62`: `Florentine`)
  - `French` (`xxvii. 44`: `Frenchmen`)
  - `Greeks` (`xxx. 98`: `Greek`)
  - `Latians (Italians)` (`xxii. 65`, `xxvii. 33`: `Latian`)
  - `Mantuans` (`i. 69`, `ii. 58`: `Mantuan`)
  - `Paduans` (`xv. 7`, `xvii. 67`: `Padua` / `Paduan`)
  - `Sardinians` (`xxii. 89`, `xxix. 48`: `Sardinia`)
  - `Thebans` (`xxx. 2`: `Theban`)
  - `Tuscan` (`xxii. 99`: `Tuscans`)
- **Latinized / English form vs Italian/adjective**:
  - `Latinus, King` (`iv. 125`: `Latian king`)
  - `Latium` (`xxvii. 27`, `xxviii. 71`: `Latian land`, Italian `terra Latina`)

## Non-Variant Unmatched References

The remaining unmatched references are not spelling variations:

- **Allusions / periphrases at the cited line**: `Adam` (`iv. 55`, "First Parent"), `Apennines` (`xxvii. 29`), `Dædalus` (`xvii. 111`, "his father"), `Dis (Satan)` (`x. 65`, `xii. 39`, `xxxiv. 20`), `Ethiopia` (`xxxiv. 45`, "where the Nile begins his valley"), `Jesus Christ alluded to` (`xxxiv. 115`), `Peleus` (`xxxi. 5`, "his father"), `Priam` (`xxx. 15`, "the King"), `Silvestro, Pope` (`xix. 117`, "the first rich Father"), `Styx` (`ix. 81`, "the marsh"), `Thebes` (`xxx. 22`).
- **Not yet named at the cited line**: `Ugolino` (`xxxii. 125`).
- **Named in Argument / notes or another passage of the same canto (`CANTO_ONLY`)**: `Aghinolfo de’ Guidi` (`xxx. 77`), `Agnello Brunelleschi` (`xxv. 63`), `Aristotle` (`xi. 101`), `Camilla` (`i. 107`), `Centaurs` (`xxv. 17`), `Fortune` (`vii. 78`), `Francesca` (`v. 74`), `Guidi, Counts` (`xxx. 77`), `Guido da Montefeltro` (`xxvii. 67`), `Maltestino` (`xxviii. 85`), `Nicholas III.` (`xix. 31`), `Polenta` (`v. 116`), `Saturn` (`xiv. 96`), `Savena, river` (`xviii. 51`).
- **Editorial / index-specific**: `Obizzo d’ Este` (`xviii. 56`, "the Marquis" in prose, named in `xii. 111`), `Rhone` (`xxviii. 86`, index citation).
