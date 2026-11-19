# Proper Names (`translations/ja/`)

Shared Japanese proper-name conventions for `translations/ja/`, based on the review of `translations/ja/en/002`–`040`, [041-index-of-proper-names.md](041-index-of-proper-names.md), `translations/ja/en-oelsner/`, `translations/ja/en-purgatorio/`, and `translations/ja/en-paradiso/`.

- Inferno (`en`): [PROPER_NAMES.tsv](PROPER_NAMES.tsv) (aligned 1-to-1 with [texts/en/PROPER_NAMES.tsv](../../../texts/en/PROPER_NAMES.tsv), generated from `en/041-index-of-proper-names.md`).
- Inferno (`en-oelsner`): [en-oelsner/PROPER_NAMES.tsv](../en-oelsner/PROPER_NAMES.tsv) (aligned 1-to-1 with [texts/en-oelsner/PROPER_NAMES.tsv](../../../texts/en-oelsner/PROPER_NAMES.tsv), poem body occurrences only).
- Purgatorio: [en-purgatorio/PROPER_NAMES.tsv](../en-purgatorio/PROPER_NAMES.tsv) (aligned 1-to-1 with [texts/en-purgatorio/PROPER_NAMES.tsv](../../../texts/en-purgatorio/PROPER_NAMES.tsv), poem body occurrences only).
- Paradiso: [en-paradiso/PROPER_NAMES.tsv](../en-paradiso/PROPER_NAMES.tsv) (aligned 1-to-1 with [texts/en-paradiso/PROPER_NAMES.tsv](../../../texts/en-paradiso/PROPER_NAMES.tsv), poem body occurrences only).

## Settled Decisions

### Relay translation from English

- `Lucifer` → **ルシファー** (applied across `002`–`040`; listed in [PROPER_NAMES.tsv](PROPER_NAMES.tsv)).
- `Cocytus` → **コキュートス** (applied across `002`–`040`; listed in [PROPER_NAMES.tsv](PROPER_NAMES.tsv)).

### Modern Italian pronunciation / Papal names

- `Aldobrandi, Tegghiaio` → **テッギアーヨ** (applied in `012` and `022`).
- `Celestine V.` → **ケレスティヌス** (Latin papal form, matching ボニファティウス / ニコラウス / クレメンス; applied in `025`).
- `Ser Brunetto` → **セル・ブルネット** (`Ser` short in Italian; applied in `021`).
- `Focaccia` → **フォカッチャ** (single `c` in Italian; applied in `038`).
- `Geri del Bello` → **ジェーリ・デル・ベッロ** / **ジェーリ** (Italian `/dʒ/`; applied in `035`).
- `Vellutello` → **ヴェッルテッロ** (Italian geminate `ll`; applied in `015`).
- `Benedict XI` → **ベネディクトゥス11世** (Latin papal form; applied in `en-paradiso/018`).
- `Luni` → **ルーニ** (applied across Inferno, Purgatorio, Paradiso).
- `Tiber` / `Tevere` → **テヴェレ川** (modern Italian river name; applied across Inferno, Purgatorio, Paradiso).
- `Pachynus` / `Pelorus` → **パッセロ岬** / **ペロロ岬** (modern Sicilian cape names; applied across Purgatorio, Paradiso).
- `Sordello` → **ソルデッロ** (Italian geminate `ll`; applied across Purgatorio, Paradiso).
- `Scala` → **スカーラ** (applied across Inferno, Purgatorio, Paradiso).
- `Urbisaglia` → **ウルビザーリア**, `Sinigaglia` → **シニガーリャ**, `Pratomagno` → **プラトマーニョ**, `Eliseo` → **エリゼーオ**, `Alagia` → **アラージャ**, `Guittone` → **グイットーネ**, `Corrado` (Italian) → **コッラード**, `Ugolino` → **ウゴリーノ**, `Macra` / `Magra` → **マグラ川**, `Elsa` → **エルザ川**, `Apulia` → **アプリア**, `Valdi...` compounds without middle dot (**ヴァルダルノ** / **ヴァルディキアーナ** / **ヴァルディシエーヴェ** / **ヴァルディマグラ** / **ヴァルディグレーヴェ**) (applied across Inferno, Purgatorio, Paradiso).

### Origin-country rule for distinct medieval persons

When the same given name belongs to distinct medieval figures, use the form matching each person's country/language of origin:

- `Bernard` → **ベルナール** for St. Bernard of Clairvaux (French; applied across Purgatorio, Paradiso); **ベルナルド** for Bernardo of Assisi (Italian; `en-paradiso/012`).
- `Charles` → **シャルル** / **シャルル・マルテル** for the House of Anjou (French royal branch; applied across Purgatorio, Paradiso).
- `Henry` (of Navarre) → **アンリ**, `Joanna` (of Navarre / Queen of France) → **ジャンヌ**, `Raymond Berengar` (Count of Provence) → **レーモン・ベランジェ** (French; applied across Purgatorio, Paradiso).

### Long vowel mark (`ー`) rule

As a general rule, Latin/Greek-based forms omit `ー` unless conventional Japanese usage has `ー` (prioritizing convention), while Italian-based forms keep `ー`:

- `Acheron` → **アケロン** (applied in `006`, `020`).
- `Anchises` → **アンキセス** (applied in `007`).
- `Athamas` → **アタマス** (applied in `036`).
- `Geryon` → **ゲリュオン** (applied in `006`).
- `Phlegethon` → **プレゲトーン** (conventional `ー`, matching Japanese Wikipedia; applied in `020`, `030`).
- `Polydorus` → **ポリュドロス** (applied in `036`).
- `Polyxena` → **ポリュクセネ** (applied in `036`).
- `Priscian` → **プリスキアヌス** (applied in `021`).
- `Imola` → **イーモラ** (applied in `021`, `033`, `034`).
- `Jacopo` → **ヤーコポ** (applied in `004`, `012`, `022`, `038`, `039`).
- `Lethe` → **レテ**, `Eunoe` → **エウノエ** (applied across Inferno, Purgatorio, Paradiso).
- `Juno` → **ユノ**, `Diana` → **ディアナ**, `Venus` → **ウェヌス**, `Apollo` → **アポロン**, `Muses` → **ムーサ** (applied across Inferno, Purgatorio, Paradiso).
- `Troas` → **トロアス**, `Hippocrene` → **ヒッポクレネ**, `Lycurgus` → **リュクルゴス**, `Cincinnatus` → **キンキナトゥス**, `Isidore` → **イシドールス**, `Dionysius` (the Areopagite) → **ディオニュシウス**, `Peter Lombard` → **ペトルス・ロンバルドゥス**, `Æneid` → **アエネイス**, `Aurora` → **アウロラ**, `Antenor` → **アンテノル**, `Catiline` → **カティリナ**, `Deianeira` → **デイアネイラ**, `Diomedes` → **ディオメデス**, `Pelion` → **ペリオン** (applied across Inferno, Purgatorio, Paradiso).
- `Eve` → **エヴァ**, `Tigris` → **ティグリス**, `drachma` → **ドラクマ** (applied across Purgatorio, Paradiso).
- Conventional `ー` kept (verified against Japanese Wikipedia): `Brutus` (ブルートゥス), `Cato` (カトー), `Medusa` (メドゥーサ), `Moses` (モーセ), `Thebes` (テーバイ), `Alecto` (アレクトー), `Arethusa` (アレトゥーサ), `Chiron` (ケイローン), `Erichtho` (エリクトー), `Phaeton` (パエトーン), `Plutus` (プルートー), `Semele` (セメレー).

### Greek/Latin vs. distinct persons/terms (already consistent)

- `Achilles` → **アキレウス** (`011`, `018`, `032`, `037`); `アキレス` in `027` (`[^248-2]`) is the anatomical term アキレス腱.
- `Alexander` → **アレクサンドロス** for Alexander the Great (`018`, `020`); **アレクサンデル** for Pope Alexander IV (`038` `[^395-2]`).
- `Jason` → **イアソン** for the Greek Argonaut (`024`); **ヤソン** for the Jewish high priest of Maccabees (`025`).

### Greek `ph` / other settled choices

- `Phlegyas` → **プレギュアス** (`ph` as stop; applied in `006`, `014`).
- `Styx` → **ステュクス** (applied in `015`).
- `Brescia` → **ブレッシャ** (modern Italian `/ˈbreʃʃa/`; applied in `035`, `036`).
- `Seville` → **セビリア** (applied in `026`).
- `Camilla` → **カミラ** (applied in `007`).
- `florens` *(currency, not in 041)* → **フローリン** (applied in `035`, `036`).

### Variations matching Carlyle’s English (kept as-is)

These variations reflect differing forms in the English source and do not need unification:

- `Agnello Brunelleschi` (`031` `[^301-1]` → アニェッロ・ブルネッレスキ) vs `Agnello de’ Brunelleschi` (`031` Argument → アニェッロ・デ・ブルネッレスキ).
- `Guido da Montefeltro` (`026` `[^241-3]`, `033` Argument → グイド・ダ・モンテフェルトロ) vs `Guido di Montefeltro` (`039` Argument → グイド・ディ・モンテフェルトロ).
- `Buondelmonti` (`034` Argument → ブオンデルモンティ) vs `Buondelmonte` (`034` `[^340-3]` → ブオンデルモンテ).

## Spelling Variations Pending Decision

None remaining.
