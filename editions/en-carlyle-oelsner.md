# Carlyle's English and Oelsner's revision

This report compares John A. Carlyle's prose translation of the Inferno, as printed in his own fifth edition (1889; [`texts/en/`](../texts/en/)), with the same translation revised by Hermann Oelsner for The Temple Classics (1903; [`texts/en-oelsner/`](../texts/en-oelsner/)). Oelsner printed his own Italian text beside it, and marked many of his revisions with square brackets (`I [came to] myself`). It does not list every difference: the differences of punctuation, spelling, and grammatical endings are described by their features with examples, and only the changes of words are listed in full.

In short, Oelsner's revision goes deep, yet it is still Carlyle's translation. Oelsner set the English against an Italian text of his own, and where that text reads otherwise, he made the English follow it (109 of the 358 differences in words): *Livio* → *Lino* is "Livy" → "Linus", *dal sommo* → *dal sonno* is "within the topmost part" → "since my slumber", *tre dì* → *due dì* is "three days" → "two days". Still more often (168 differences) he changed the words where the two Italian texts agree, mostly to render the Italian more closely: *Mi ritrovai* is no longer "I found myself" but "I [came to] myself", with a note that "the *ri*- has escaped the notice of the great majority of translators"; *del maggior Piero* is no longer "of great Peter" but "of [the greatest] Peter". He also gives some names in the form of his Italian text or of later usage, and repunctuates throughout. But the 358 changes of words come to about ten a canto, and the rest of the prose is Carlyle's; most of the changes are marked with square brackets, so that the edition shows itself as Carlyle's translation revised, not as a new one. Each English is thus to be read with its own Italian: Carlyle's with the Italian of his edition (the `en` source of [grammar.py](../grammar/README.md#scriptsgrammarpy)), Oelsner's with Oelsner's.

## Method

The two English texts are not divided alike: Carlyle's edition prints the prose page by page above the verse it renders, Oelsner's prints it one paragraph per tercet facing the Italian. So each canto is compared as a whole, word by word, by [`scripts/compare_editions.py`](scripts/compare_editions.py) `en`, and each difference is placed on the page of Carlyle's edition where it falls; the lines of that page (`I 22–33`) locate it. Oelsner's square brackets and his italics are not counted as differences; a difference is "marked" if Oelsner's brackets cover his side of it.

| Kind of difference | Count |
|---|---|
| punctuation only | 602 |
| case only, or punctuation with a change of case (`. And` / `; and`) | 377 |
| words: substituted, inserted, or deleted | 358 |

The 358 differences in words were read and sorted by hand into the sections below; differences close together are shown as one row. 212 of them are marked by Oelsner (some only in part); the words he deleted cannot be marked, and a number of changes of single words are unmarked as well.

The judgments are kept in [judge-en.txt](judge-en.txt), and the tables are rendered from them by [`scripts/render_editions.py`](scripts/render_editions.py) `en`. In the tables, the differing words are in bold, with a few words of context. "Marked" says whether Oelsner's brackets cover the change (yes, no, or partly).

## Punctuation and case

Oelsner repunctuates throughout: he often joins Carlyle's sentences with a semicolon or colon (*. And* → *; and*; most of the 377 differences of case are of this kind), and exchanges semicolons and colons (*;* → *:* 96 times, *:* → *;* 71 times). Most of the other differences of punctuation are of quotation marks: the transcription of Oelsner's edition has straight quotation marks (`"`) in many places where Carlyle's has curly ones (`“ ”`, about 250 times), which is a matter of the transcription, not of the edition.

## Spelling

Oelsner's spelling is sometimes the modern one, sometimes not; the changes go both ways:

| Carlyle | Oelsner |
|---|---|
| whilst | while |
| entrance | entrancy |
| squinteyed | squint-eyed |
| forwards | forward |
| panders / barators | pandars / barrators |
| recognized | recognised |
| shows | shews |
| sorb-trees | sorbtrees |
| d’ Accorso | d’Accorso |
| stedfast | steadfast |
| tormentors | tormenters |
| toward | towards |
| trumpet | trump |
| re-change | rechange |
| license | licence |
| fosse | foss |
| shews | shows |
| shew | show |
| florens | florins |
| showest | shewest |
| dextrous | dexterous |
| callous | callus |
| d’ Oria | d’Oria |

## Proper names

Oelsner gives several names in the form of his Italian text or of later usage:

| Lines | Carlyle | Oelsner | Marked |
|---|---|---|---|
| IV 128–139 | … and Thales; Empedocles, **Heraclítus**, and Zeno. And … | … and Thales; Empedocles, **Heraclitus**, and Zeno; and … | no |
| VII 1–10 | “**Papè** Satan! **papè** Satan, **aleppè**!” began Plutus, … | “**Pape** Satan! **pape** Satan, **aleppe**!” began Plutus, … | no |
| XIII 120–133 | … in vain. “O **Jacopo** da Sant’ Andrea! … | … in vain. “O **Jacomo** da Sant’ Andrea! … | no |
| XVI 28–38 | … Gualdrada, his name was **Guidoguerra**; and in his lifetime … | … Gualdrada, his name was **Guido Guerra**; and in his lifetime … | no |
| XVI 94–105 | … own, first from Monte **Viso** toward the east, on … | … of its own from Monte **Veso** toward the east, on … | no |
| XX 27–37 | … ‘Whither rushest thou, **Amphiaraüs**? Why leavest thou the … | … ’ Whither rushest thou, **Amphiaräus**? Why leavest thou the … | no |
| XX 63–75 | … , and more, the **Pennine**, between Garda and Val … | … , and more, the **Apennine**, between Garda and Val … | yes |
| XX 112–118 | … about the flanks was Michael **Scot**; and of a truth … | … about the flanks was Michael **Scott**; and of a truth … | no |
| XXI 104–114 | … “Quiet, quiet, **Scaramiglione**!” Then he said … | … " Quiet, quiet, **Scarmiglione**! " Then he said … | no |
| XXVIII 134–142 | … know, that I am **Bertram** de Born, he who … | … know, that I am **Bertran** de Born, he who … | no |
| XXIX 98–109 | … the one, “and **Albert** of Siena had me burned … | … the one, “and **Albero** of Siena had me burned … | no |
| XXXI 13–24 | … lost the holy emprise, **Orlando** did not sound with his … | … lost the holy emprise, **Roland** did not sound with his … | yes |
| XXXI 54–67 | … spans of him. “**RAAFEL MAAEE AAMECH ZAABEE ALMEE**,” began to shout … | … spans of him. “**Rafel mai amech zabi almi**,” began to shout … | no |
| XXXII 14–28 | … was here; for if **Tabernicch** had fallen on it, … | … was here: for if **Tambernic** had fallen on it, … | no |
| XXXII 64–73 | … , know that I was **Camiccion** de’ Pazzi, and … | … , know that I was **Camicion** de’ Pazzi, and … | no |
| XXXII 115–123 | … thou hast beside thee the **Beccaria** whose gorge was slit by … | … thou hast beside thee the **Beccheria** whose gorge was slit by … | no |
| XXXII 115–123 | … slit by Florence. Gianni **del** Soldanier, I think, … | … slit by Florence. Gianni **de’** Soldanier, I think, … | no |
| XXXIII 81–91 | … punish thee, let the **Capraia** and Gorgona move, and … | … punish thee, let the **Caprara** and Gorgona move, and … | no |

## Endings

Oelsner marks a changed ending by bracketing it alone (`lord[s]`, `raise[d]`):

| Lines | Carlyle | Oelsner | Marked |
|---|---|---|---|
| II 54–61 | … eyes shone brighter than the **Star**; and she began soft … | … eyes shone brighter than the **stars**; and she began soft … | yes |
| IV 87–100 | … goodly school of that lord of highest song, who … | … goodly school of those lord**s** of highest song, which … | yes |
| V 65–79 | … to us, I raise my voice: “O … | … to us, I raise**d** my voice: “O … | yes |
| VIII 76–88 | … spirits, rained from Heaven, who angrily exclaimed: … | … , rained from the Heaven**s**, who angrily exclaimed: … | yes |
| XIII 1–12 | … unseemly Harpies make their nest, who chased the Trojans … | … unseemly Harpies make their nest**s**, who chased the Trojans … | yes |
| XIII 93–107 | … yet none shall thereby clothe **himself** with them again: for … | … that any may be clothe**d** with them again: for … | yes |
| XIX 47–57 | … , recalls him to delay the death. And he … | … recalls him and thus delay**s** the death; and he … | yes |
| XIX 71–84 | … , cowering along the fissure of the stone. I … | … , cowering within the fissure**s** of the stone. I … | yes |
| XXI 124–135 | … not see how they grin their teeth, and with … | … not see how they grin**d** their teeth, and with … | yes |
| XXI 124–135 | … afraid. Let them grin on at their will; … | … afraid; let them grin**d** on at their will: … | yes |

## Revisions that follow Oelsner's Italian

Every change of words where Oelsner's Italian differs from Carlyle's in the same place and the revision follows it. The last column gives the Italian line of Carlyle's edition and of Oelsner's (on the reading of these two and of dante-corpus, see [it-carlyle.md](it-carlyle.md)).

| Lines | Carlyle | Oelsner | Marked | Italian (Carlyle / Oelsner) |
|---|---|---|---|---|
| I 22–33 | … had rested my wearied body, I took the way … | … had rested my wearied body **a short while**, I took the way … | yes | 28: Poi ch’ ebbi riposato il corpo lasso, / Poi ch' ei posato un poco il corpo lasso, |
| I 48–60 | … that the air seemed to **quake** thereat. And a She … | … that the air seemed to **have fear** thereat; and a She … | yes | 48: Sì che parea che l’aer ne tremesse. / sì che parea che l' aer ne temesse; |
| III 29–42 | … dyed, as sand when **the** whirlwind **breathes**. And I, my … | … dyed, as sand when **it eddies in a** whirlwind. And I, my … | partly | 30: Come la rena quando il turbo spira. / come la rena quando a turbo spira. |
| III 29–42 | … , my head begirt with **error**, said: “Master … | … , my head begirt with **horror**, said: “Master … | no | 31: Ed io, ch’ avea d’ error la testa cinta, / Ed io, ch' avea d' orror la testa cinta, |
| III 58–69 | … some amongst them, I **looked** and **saw** the shadow of him who … | … some amongst them, I **saw** and **knew** the shadow of him who … | yes | 59: Guardai, e vidi l’ ombra di colui / vidi e conobbi l’ombra di colui |
| III 121–136 | … ground gave out wind, **and** flashed **with** a crimson light **, which** conquered all my senses: … | … ground gave out wind, **which** flashed **forth** a crimson light **that** conquered all my senses; … | partly | 134: E balenò d’ una luce vermiglia, / che balenò una luce vermiglia, |
| IV 60–71 | … way was not yet far **within the topmost part**, when I saw a … | … way was not yet far **since my slumber**, when I saw a … | yes | 68: Di qua dal sommo, quand’ io vidi un foco, / di qua dal sonno, quando’ io vidi un foco, |
| IV 114–127 | … to me the great spirits **whom** I glory within myself **in** having seen. I saw Electra with … | … to me the great spirits **, so that** I glory within myself **for** having seen **them**. I saw Electra with … | yes | 120: Che di vederli in me stesso m’ esalto. / che del vederli in me stesso n’ esalto. |
| IV 114–127 | … . On the other hand **I** saw the Latian king, … | … Penthesilea on the other hand **, and** saw the Latian king, … | yes | 125: Dall’ altra parte vidi il re Latino, / dall’ altra parte, e vidi il re Latino, |
| IV 140–151 | … saw Orpheus, Tully, **Livy**, and Seneca the moralist … | … saw Orpheus, Tully, **Linus**, and Seneca the moralist … | yes | 141: Tullio, e Livio, e Seneca morale: / Tullio, e Lino, e Seneca morale; |
| V 27–40 | … learnt that to such torment **were** doomed the carnal sinners, … | … learnt that to such torment **are** doomed the carnal sinners, … | yes | 38: Eran dannati i peccator carnali, / enno dannati i peccator carnali, |
| V 56–64 | … luxurious Cleopatra.” Helena **I saw**, for whom so long … | … comes luxurious Cleopatra. Helena **see**, for whom so long … | yes | 64: Elena vidi, per cui tanto reo / Elena vedi, per cui tanto reo |
| V 65–79 | … of ill revolved; and **I saw** the great Achilles, who … | … of ill revolved; and **see** the great Achilles, who … | yes | 67: Vidi Paris, Tristano; e più di mille / vedi Paris, Tristano”; e più di mille |
| V 65–79 | … fought at last with love **. I saw** Paris, Tristan. And … | … fought at last with love **; see** Paris, Tristan”; … | yes | 67: Vidi Paris, Tristano; e più di mille / vedi Paris, Tristano”; e più di mille |
| V 65–79 | … with his finger, named **them,** whom love had parted from … | … with his finger, named **to me those** whom love had parted from … | yes | 68: Ombre mostrommi, e nominolle a dito, / ombre mostrommi, e nominommi a dito, |
| V 65–79 | … dames and cavaliers, pity **conquered** me, and I was … | … dames and cavaliers, pity **came over** me, and I was … | yes | 72: Pietà mi vinse, e fui quasi smarrito. / pietà mi giunse, e fui quasi smarrito. |
| V 80–90 | … called by desire, with **open** and steady wings **fly** through the air to their … | … called by desire, with **raised** and steady wings **come** through the air to their … | yes | 83: Con l’ ali aperte e ferme al dolce nido / con l’ ali alzate e ferme al dolce nido<br>84: Volan per l’ aer dal voler portate: / vengon per l’ aer dal voler portate: |
| V 91–104 | … as now, is silent. “The town, … | … as now, is silent **for us**. The town, where … | yes | 96: Mentrechè il vento, come fa, si tace. / mentrechè il vento, come fa, ci tace. |
| VI 87–102 | … mayest see them. But **if ever** thou **return to** the sweet world, I … | … mayest see them. But **when** thou **shalt be in** the sweet world, I … | yes | 88: Ma se tu torni mai nel dolce mondo, / Ma quando tu sarai nel dolce mondo, |
| VII 1–10 | … , he shall not hinder **us** from descending this rock. … | … , he shall not hinder **thee** from descending this rock. … | yes | 6: Non ci terrà lo scender questa roccia. / non ti torrà lo scender questa roccia.” |
| VII 11–23 | … is willed on high, where Michael took vengeance of … | … is willed on high, **there** where Michael took vengeance of … | yes | 11: Vuolsi così nell’ alto, ove Michele / vuolsi nell’ alto, là dove Michele |
| VII 24–35 | … to the opposite point, shouting **always in** their reproachful measure. Then … | … to the opposite point, **again** shouting **at each other** their reproachful measure. Then … | yes | 33: Gridando sempre in loro ontoso metro. / gridandosi anche loro ontoso metro. |
| VIII 1–9 | … catch it. And I **, turning** to the Sea of all … | … catch it. And I **turned** to the Sea of all … | yes | 7: Ed io, rivolto al mar di tutto il senno, / Ed io mi volsi al mar di tutto il senno; |
| VIII 1–9 | … the Sea of all intelligence **,** said: “What says … | … the Sea of all intelligence **; I** said: “What says … | yes | 7: Ed io, rivolto al mar di tutto il senno, / Ed io mi volsi al mar di tutto il senno; |
| VIII 103–117 | … could not hear that which **he** offered to them. But … | … could not hear that which **was** offered to them; but … | yes | 112: Udir non potei quello che a lor porse: / Udir non potei quello ch’ a lor si porse: |
| IX 35–47 | … , where all at once **I saw erect** three Hellish Furies, stained … | … , where all at once **had risen up** three Hellish Furies, stained … | yes | 37: Ove in un punto vidi dritte ratto / ove in un punto furon dritte ratto |
| IX 48–60 | … stone,” they all **cried**, looking downwards. “ … | … stone,” they all **said**, looking downwards; “ … | yes | 53: Gridavan tutte riguardando in giuso: / dicevan tutte riguardando in giuso; |
| IX 85–98 | … wand opened it; for **in it** there was no resistance. … | … wand opened it: for there was no resistance. … | no | 90: L’ aperse, chè non v’ ebbe alcun ritegno. / l' aperse, chè non ebbe alcun ritegno. |
| X 1–11 | Now by a **narrow** path, between the city … | Now by a **secret** path, between the city … | yes | 1: Ora sen va per uno stretto calle, / Ora sen va per un secreto calle, |
| X 36–49 | … words be numbered.” **As soon as** I was at the foot … | … words be numbered.” **When** I was at the foot … | yes | 40: Tosto che al piè della sua tomba fui, / Com’ io al piè della sua tomba fui, |
| XI 47–57 | … a man may practise upon **those** who confide in him; and upon **those** who repose no confidence. This latter … | … a man may practise upon **one** who confide**s** in him; and upon **him** who repose**s** no confidence. This latter … | yes | 53: Può l’ uomo usare in quei, ch’ in lui si fida, / può l’ uomo usare in colui, ch’ in lui fida, |
| XII 40–51 | … others. O blind cupidity **! O** foolish **anger!** which so incites us in … | … .” O blind cupidity **both wicked and** foolish **,** which so incites us in … | partly | 49: O cieca cupidigia, o ira folle, / O cieca cupidigia, e ria e folle, |
| XII 116–126 | … grew shallow, until it **covered** the feet only: and … | … grew shallow, until it **cooked** the feet only; and … | yes | 125: Quel sangue sì, che copria pur li piedi: / quel sangue sì che cocea pur li piedi; |
| XIII 13–24 | … and thou shalt see things **that will confirm** my speech.” Already … | … and thou shalt see things **which would take away belief from** my speech.” Already … | no | 21: Cose, che daran fede al mio sermone. / cose che torrien fede al mio sermone." |
| XIV 1–13 | … . Here we stayed our **feet** close to its very edge … | … ; here we stayed our **steps** close to its very edge … | yes | 12: Quivi fermammo i piedi a randa a randa. / quivi fermammo i passi a randa a randa. |
| XIV 72–87 | … As from the Bulicame issues **the** streamlet, which the sinful … | … As from the Bulicame issues **a** streamlet, which the sinful … | yes | 79: Quale del Bulicame esce il ruscello, / Quale del Bulicame esce un ruscello, |
| XV 83–96 | … my heart, the dear **,** kind, paternal image of … | … my heart, the dear **and** kind, paternal image of … | yes | 83: La cara buona imagine paterna / la cara e buona imagine paterna |
| XVI 28–38 | … loose place, and our **dreary** and scorched aspect, bring … | … loose place, and our **stained** and scorched aspect, bring … | yes | 30: Cominciò l’ uno, e il tristo aspetto e brollo; / cominciò l' uno, “e il tinto aspetto e brollo, |
| XVI 79–93 | … , “happy thou, **who** thus speakest at thy will! … | … , “happy thou, **if** thus **thou** speakest at thy will! … | yes | 81: Felice te, che sì parli a tua posta! / felice te, se sì parli a tua posta! |
| XVI 112–126 | … should close his lips, **if possible;** for, though blameless, … | … should close his lips, **so far as he is able,** for, though blameless, … | yes | 125: De’ l’ uom chiuder le labbra quant’ ei puote, / de' l' uom chiuder le labbra finch' ei puote, |
| XVII 14–27 | … Never did Tartars or Turks with more colours **make ground or** broidery **in cloth**; nor by Arachne were … | … never did Tartars or Turks **make cloth** with more colours **, groundwork and** broidery; nor by Arachne were … | partly | 17: Non fer mai in drappo Tartari nè Turchi, / non fer mai drappo Tartari nè Turchi, |
| XVII 28–40 | … of this round, go **now** and see the state of … | … of this round, go and see the state of … | no | 39: Mi disse, or va, e vedi la lor mena. / mi disse, “va, e vedi la lor mena. |
| XVII 55–67 | … saw another of them, **redder than** blood, display a goose … | … saw another of them, **red as** blood, display a goose … | yes | 62: Vidine un’ altra più che sangue rossa / vidine un’ altra come sangue rossa |
| XVIII 1–9 | … and deep, whose structure its own place **shall tell**. The border therefore that … | … and deep, whose structure **I shall tell in** its own place. The border therefore that … | partly | 6: Di cui suo luogo conterà l’ ordigno. / di cui suo loco dicerò l' ordigno. |
| XVIII 35–49 | … at the first strokes! **And** truly none waited for the … | … at the first strokes! truly none waited for the … | no | 38: Alle prime percosse! E già nessuno / alle prime percosse! già nessuno |
| XVIII 61–72 | … say Sipa between Savena and **the** Reno. And if thou … | … say sipa between Savena and Reno; and if thou … | no | 61: A dicer sipa tra Savena e il Reno: / a dicer ‘sipa’ tra Savena e Reno; |
| XVIII 125–136 | … the visage of that unclean **,** dishevelled strumpet, who yonder … | … the visage of that unclean **and** dishevelled strumpet, who yonder … | no | 130: Di quella sozza scapigliata fante, / di quella sozza e scapigliata fante, |
| XX 1–12 | … each seemed wondrously distorted, **from** the chin **to** the commencement of the chest … | … each seemed wondrously distorted, **between** the chin **and** the commencement of the chest … | yes | 12: Ciascun dal mento al principio del casso, / ciascun tra il mento e'l principio del casso : |
| XX 27–37 | … eyes of the Thebans, **when** they all cried, ‘ … | … eyes of the Thebans, **whereat** they all cried,’ … | no | 33: Quando gridavan tutti: Dove rui, / per ch' ei gridavan tutti: ' Dove rui, |
| XX 48–62 | … that dwells beneath, amongst white marbles had the cave … | … that dwells beneath, amongst **the** white marbles had the cave … | yes | 49: Ebbe tra bianchi marmi la spelonca / ebbe tra i bianchi marmi la spelonca |
| XX 48–62 | … Germany above the Tyrol, **and it** is called Benacus. Through … | … Germany above the Tyrol, **which** is called Benacus. Through … | yes | 63: Sovra Tiralli, ed ha nome Benaco. / sopra Tiralli, ch’ ha nome Benaco. |
| XXI 29–40 | … others to that city which **is** well **provided** with them. Every man … | … others to that city which **I have provided** well with them: every one … | partly | 40: A quella terra che n’ è ben fornita. / a quella terra ch' i' n' ho ben fornita: |
| XXII 124–138 | … freed himself. Thereat each **suddenly** was stung with **rage**; but he most who … | … freed himself. Thereat each was stung with **guilt**; but he most who … | partly | 124: Di che ciascun di colpo fu compunto, / Di che ciascun di colpa fu compunto, |
| XXII 124–138 | … ” But little it availed; for wings could not … | … ” But little it availed **him**; for wings could not … | yes | 127: Ma poco valse; chè l’ ale al sospetto / Ma poco i valse, chè l’ ale al sospetto |
| XXIII 1–10 | … the other after; as **the** Minor Friars go their way … | … the other after; as Minor Friars go their way … | no | 3: Come i frati Minor vanno per via. / come frati minor vanno per via. |
| XXIII 11–26 | … pursue us, fiercer than **a** dog that leveret which he … | … pursue us, fiercer than **the** dog that leveret which he … | yes | 18: Che cane a quella levre ch’ egli acceffa. / che il cane a quella lepre ch' egli acceffa.” |
| XXIII 43–57 | … depth below, when they **reached** the height above us: … | … depth below, when they **were on** the height above us; … | yes | 53: Del fondo giù ch’ ei giunsero in sul colle / del fondo giù, ch' ei furono in sul colle |
| XXIV 99–113 | … upon the ground, the **ashes** reunited **,** and **of themselves** at once resumed the former … | … upon the ground, the **powder** reunited **of itself** and at once resumed the former … | partly | 104: La cener si raccolse, e per sè stessa / la polver si raccolse per sè stessa, |
| XXIV 114–126 | … sinner when he rose. **Justice** of God! O how … | … sinner when he rose. **Power** of God! o how … | yes | 119: O Giustizia di Dio, quant’ è severa! / O potenzia di Dio, quant' è severa, |
| XXV 139–151 | … me, if my tongue goes aught astray. And … | … me, if my tongue **pen** goes aught astray. And … | yes | 144: La novità, se fior la lingua abborra. / la novità, se fior la penna abborra. |
| XXVII 27–40 | … her tyrants; but open **war** just now I there left … | … her tyrants; but open**ly** just now I there left … | yes | 39: Ma palese nessuna or ven lasciai. / ma ’n palese nessuna or vi lasciai. |
| XXVII 41–48 | … , and sanguinary heap of Frenchmen, finds itself again … | … , and sanguinary heap of **the** Frenchmen, finds itself again … | yes | 44: E di Franceschi sanguinoso mucchio, / e de’ Franceschi sanguinoso mucchio, |
| XXVIII 1–9 | … wailed for their blood, **shed** by the **Romans;** and **in** that long war which made … | … wailed for their blood, by **reason of** the **Trojans,** and **of** that long war which made … | partly | 10: Per li Romani, e per la lunga guerra / per li Troiani, e per la lunga guerra |
| XXVIII 58–71 | … , and said: “**O thou**! whom guilt condemns not … | … , and said: “**Thou**! whom guilt condemns not … | no | 70: E disse: O tu, cui colpa non condanna, / e disse: "Tu, cui colpa non condanna, |
| XXVIII 58–71 | … seen above on Latian ground **ere now**, unless too much resemblance … | … seen above on Latian ground, unless too much resemblance … | no | 71: E cui già vidi su in terra Latina, / e cui io vidi su in terra Latina, |
| XXVIII 134–142 | … to the Young King gave **the** evil counsels. I made … | … to the Young King gave evil counsels. I made … | no | 135: Che al Re Giovane diedi i mal conforti. / che diedi al re giovane mai comforti. |
| XXIX 83–97 | … pincers of them; tell **me** if there be any Latian … | … pincers of them; tell **us** if there be any Latian … | yes | 88: Dimmi s’ alcun Latino è tra costoro / dinne s' alcun Latino è tra costoro |
| XXIX 124–131 | … my words: “Except **the** Stricca who contrived to spend … | … my words: " Except Stricca who contrived to spend … | no | 125: Rispose al detto mio: Tranne lo Stricca, / rispose al detto mio: “Trammene Stricca, |
| XXX 1–11 | … with the two sons, **come** laden on either hand, … | … , with two sons, **go** laden on either hand, … | yes | 6: Venir carcata di ciascuna mano, / andar carcata da ciascuna mano, |
| XXX 25–34 | … limbs; as I saw two shadows, pale and … | … limbs; as I saw **in** two shadows, pale and … | yes | 25: Quant’ io vidi due ombre smorte e nude, / quant' io vidi in due ombre smorte e nude, |
| XXXI 13–24 | … Short while had I kept **looking up** in that direction, when … | … Short while had I kept **my head turned** in that direction, when … | yes | 19: Poco portai in là alta la testa, / Poco portai in là volta la testa, |
| XXXI 39–53 | … towards the brink, error **flees** from me, and fear **comes over me: for** as on its round wall … | … towards the brink, error **fled** from me, and **my** fear **increased. For** as on its round wall … | yes | 39: Fuggemi errore, e giungemi paura: / fuggìemi errore, e cresce' mi paura. |
| XXXI 137–145 | … so, that it hangs **opposed;** such Antæus seemed to me … | … so, that it hangs **in the contrary direction:** such Antæus seemed to me … | yes | 138: Sovr’ essa sì, ch’ ella in contrario penda; / sopr' essa sì che ella incontro penda: |
| XXXII 1–13 | If I had rhymes **both** rough and hoarse, as … | If I had rhymes rough and hoarse, as … | no | 1: S’ io avessi le rime e aspre e chiocce, / S' io avessi le rime aspre e chiocce, |
| XXXIII 68–80 | … over each; and for **three** days called them, after … | … over each, and for **two** days called them, after … | yes | 74: E tre dì li chiamai, poi ch’ ei fur morti: / e due dì li chiamai poi che fur morti; |
| XXXIV 1–12 | … hemisphere, a mill, **turning with** the wind, appears at distance: … | … hemisphere, a mill, **which** the wind **turns**, appears at distance: … | yes | 6: Par da lungi un mulin che al vento gira; / par da lungi un molin che il vento gira : |
| XXXIV 1–12 | … it into verse) where **all** the souls were covered, and shone through … | … it into verse) where the souls were **wholly** covered, and shone through … | partly | 11: Là, dove l’ ombre tutte eran coverte, / là dove l’ ombre eran tutte coperte, |
| XXXIV 13–26 | … straw in glass. Some **keep** lying; some stand upright … | … straw in glass. Some **are** lying; some stand upright … | yes | 13: Altre stanno a giacere, altre stanno erte, / Altre sono a giacere, altre stanno erte, |
| XXXIV 78–93 | … people who see not what **a** point **it was that** I had passed, even … | … people who see not what **that** point **is which** I had passed, let … | yes | 93: Qual era il punto ch’ io avea passato. / qual è quel punto ch' io avea passato. |

## Other changes of words

Every other change of words: a closer rendering of the same Italian, a correction, or a change of style. The unmarked changes of a single word that have no counterpart in the Italian were checked against the page images (see the last section).

| Lines | Carlyle | Oelsner | Marked |
|---|---|---|---|
| I 1–9 | … of our life, I **found** myself in a dark wood **; for** the straight way was lost … | … journey of our life I **came to** myself in a dark wood **where** the straight way was lost … | yes |
| I 22–33 | … strand, so that the **firm** foot always was the lower … | … strand, so that the **right** foot always was the lower … | yes |
| I 34–47 | … was covered with a spotted **skin: and** it went not from before … | … which was covered with spotted **hair. And** it went not from before … | yes |
| I 34–47 | … things: so that the **gay skin of that animal, the** hour of time, and … | … things: so that the hour of time and the … | no |
| I 34–47 | … , and the sweet season **, were causes** to **me of** good hope; yet not so, … | … time and the sweet season **caused me** to **have** good hope **of that animal with the gay skin**; yet not so, … | yes |
| I 107–121 | … each calls for second death **. And** thou shalt see those who … | … calls for a second death **; and then** thou shalt see those who … | yes |
| I 122–136 | … he rules; and there **he dwells. There** is his city, and … | … parts he rules and there **holds sway; there** is his city, and … | yes |
| I 122–136 | … by that God whom thou **knewest** not: in order that … | … by that God whom thou **knowest** not: in order that … | no |
| II 13–27 | … of all evil was propitious, considering the high effect … | … of all evil was propitious **to him**, considering the high effect … | yes |
| II 13–27 | … , where the Successor of **great** Peter sits. By this … | … , where the Successor of **the greatest** Peter sits. By this … | yes |
| II 54–61 | … My friend, and not of fortune, is so … | … my friend, and not **the friend** of fortune, is so … | no |
| II 62–76 | … who send thee. I **came** from a place where I … | … who send thee; I **come** from a place where I … | no |
| II 62–76 | … I began: O Lady, **single in worth;** through whom mankind excels all that is … | … began: ‘O Lady **of virtue**, through whom **alone** mankind excels all that is … | partly |
| II 105–120 | … combats him upon the river **, that swelleth not** the sea? None on earth were … | … combats him upon the river **over which** the sea **has no boast**?” None on earth … | partly |
| III 43–57 | … to exist. Mercy and **Judgment** disdains them. Let us … | … to exist; Mercy and **Justice** disdains them: let us … | yes |
| III 70–86 | … light.” And he: “The things shall … | … light.” And he **to me**: “The things shall … | yes |
| III 70–86 | … “The things shall be **told** thee, when we stay … | … “The things shall be **known to** thee, when we stay … | yes |
| IV 60–71 | … and his children, and Rachel, for whom he … | … and his children, and **with** Rachel, for whom he … | yes |
| IV 87–100 | … assembled the goodly school of **that** lord of highest song, … | … assembled the goodly school of **those** lords of highest song … | yes |
| IV 87–100 | … lord of highest song, **who**, like an eagle, … | … s of highest song, **which**, like an eagle, … | yes |
| VI 1–15 | … cold, and heavy rain **. Its course** and quality is never new … | … cold, and heavy rain **; its law** and quality is never new … | yes |
| VI 1–15 | … water, and snow, **it pours** down through the darksome air … | … water, and snow, **pour** down through the darksome air … | yes |
| VI 16–26 | … are red, his beard **gory** and black, his belly … | … are red, his beard **greasy** and black, his belly … | yes |
| VI 55–66 | … to blood, and the **savage** party shall expel the other with … | … to blood, and the party **of the woods** shall expel the other with … | no |
| VI 103–115 | … to true perfection, yet **shall** they be nearer **to** it after than before. … | … to true perfection, yet they **look to** be nearer it after than before. … | partly |
| VII 11–23 | … our journey to the deep **. Thus** it is willed on high … | … our journey to the deep **:** it is willed on high … | no |
| VII 11–23 | … monster to the ground. **Then** we descended into the fourth … | … monster to the ground. **Thus** we descended into the fourth … | yes |
| VII 24–35 | … rolling weights by force of **chest. They** smote against each other, … | … rolling weights by force of **chests; they** smote against each other, … | no |
| VII 49–62 | … fists; and these with **wasted** hair. Ill-giving, … | … fists; and these with hair **shorn off**. Ill-giving, … | no |
| VII 49–62 | … , my Son, mayest see the brief mockery of … | … , my Son, mayest **now** see the brief mockery of … | yes |
| VII 63–74 | … ; so that every part **may shine** to every part, equally … | … , so that every part **shines** to every part, equally … | no |
| VII 75–87 | … grass. Your knowledge cannot **withstand** her. She provides, … | … grass. Your knowledge cannot **understand** her: she provides, … | no |
| VII 88–99 | … makes her be swift; **so** oft **come things requiring** change. This is she, … | … makes her be swift; **thus he comes** oft **who doth a** change **obtain**. This is she, … | yes |
| VII 88–99 | … , that was ascending when **we entered;** and to stay too long … | … , that was ascending when **I set out** and to stay too long … | yes |
| VIII 10–23 | … saw come towards us then, under the guidance of … | … saw come towards us then **through the water**, under the guidance of … | yes |
| VIII 89–102 | … that I ever should return **by it**. “O my loved … | … that I ever should return **hither**. “O my loved … | yes |
| VIII 103–117 | … on the breast of my **Master,** who remained without; and … | … on the breast of my **Lord** who remained without; and … | yes |
| IX 125–133 | … And he to me: **“These** are the Arch-heretics … | … And he to me: **" Here** are the Arch-heretics … | yes |
| X 12–24 | … the wish which thou holdest **secret** from me.” And … | … the wish which thou holdest from me.” And … | no |
| XI 72–84 | … plight?” And he to me: “Wherefore … | … plight? " And he **said** to me: " Wherefore … | yes |
| XI 85–96 | … thee yet a little back, to where thou sayest … | … thee yet a little back **” I said**, “to where thou … | yes |
| XI 108–115 | … gain his bread, and **multiply the people**. And because the usurer … | … to gain his bread and **to prosper**. And because the usurer … | yes |
| XI 108–115 | … go; for the Fishes **glide** on the horizon, and … | … go: for the Fishes **are quivering** on the horizon, and … | yes |
| XII 81–93 | … my steps on such a **woody** way, give us some … | … my steps on such a **wild** way, give us some … | no |
| XII 127–139 | … he turned back, and **by himself** repassed the ford. | … he turned back, and repassed the ford. | no |
| XIII 65–79 | … against me; and these so inflamed Augustus, that … | … against me; and these **, being inflamed,** so inflamed Augustus, that … | yes |
| XIII 93–107 | … shall go for our spoils **; yet none shall thereby** clothe himself with them again … | … shall go for our spoils **, but not to the end that any may be** clothed with them again … | yes |
| XIII 120–133 | … of Toppo.” And **then,** his breath perhaps failing him, of himself … | … of Toppo.” And **since** his breath perhaps **was** failing him, of himself … | yes |
| XIV 1–13 | … , and where is seen **the** fearful **art** of justice. To make … | … , and where is seen **a** fearful **device** of justice. To make … | yes |
| XV 1–11 | … the Flemings between Bruges and **Cadsand**, dreading the flood that … | … the Flemings between Bruges and **Wissant**, dreading the flood that … | yes |
| XV 1–11 | … Brenta, to defend their **towns** and **villages,** ere Chiarentana feels the heat … | … Brenta, to defend their **villages** and **castles** ere Chiarentana feels the heat … | partly |
| XV 69–82 | … Romans who remained there when **it became** the nest of so much … | … who remained there, when the nest of so much … | no |
| XV 69–82 | … nest of so much malice.” “Were my … | … nest of so much malice **was made**. " “Were my … | yes |
| XVI 1–13 | … , recent and old, **kindled** by the flames. It pains me yet … | … , recent and old, by the flames **burnt in**. It pains me yet … | no |
| XVI 112–126 | … edge, down into that **deep** abyss. “Surely, … | … edge, down into that **steep** abyss. " Surely, … | no |
| XVII 91–101 | … myself on those huge shoulders **, and** wished to say, only … | … myself on those huge shoulders **; I** wished to say, only … | yes |
| XVII 115–126 | … Then was I more timorous **at the precipice;** for I saw fires and … | … Then was I more timorous **as regards dismounting:** for I saw fires and … | yes |
| XVII 115–126 | … lamentings, so that I **cowered** all trembling. And then … | … lamentings, so that I **cower** all trembling. And then … | no |
| XVII 115–126 | … And then I saw—**what** I had not seen before—the sinking and … | … And then I saw—**for** I had not seen **it** before—the sinking and … | yes |
| XVIII 23–34 | … bottom the sinners were naked **: from the middle,** on our side **,** they came facing us; … | … bottom the sinners were naked **;** on our side **of the middle** they came facing us; … | partly |
| XVIII 61–72 | … said: “Away! **Ruffian,** there are no women here … | … said: “Away! **pandar** there are no women here … | yes |
| XVIII 100–113 | … got upon it; and **then,** in the ditch beneath, … | … got upon it; and **thence** in the ditch beneath, … | yes |
| XIX 47–57 | … being fixed, recalls him **to** delay the death. And … | … being fixed, recalls him **and thus** delays the death; … | no |
| XIX 71–84 | … me in simony, cowering **along** the fissure of the stone … | … me in simony, cowering **within** the fissures of the … | yes |
| XIX 125–133 | … placidly set down the burden **, pleasing to him** on the rough steep cliff … | … placidly set down the burden **placidly** on the rough steep cliff … | yes |
| XX 13–26 | … the commencement of the chest **, so that** the face was turned towards … | … the commencement of the chest **: for** the face was turned towards … | yes |
| XX 48–62 | … and has all her hair on the other side, … | … and has all her hair**y skin** on the other side, … | yes |
| XX 89–99 | … gathered together on that spot **; for it** was strong by reason of … | … gathered together on that spot **which** was strong by reason of … | yes |
| XX 119–129 | … come! for Cain and **the** thorns already holds the confine … | … come! for Cain and **his** thorns already holds the confine … | no |
| XXI 1–13 | … Venetians boils the clammy pitch, to caulk their damaged … | … Venetians boils the clammy pitch **in winter**, to caulk their damaged … | no |
| XXI 1–13 | … caulk their damaged ships, **in winter when** they cannot navigate; and … | … caulk their damaged ships, **which** they cannot navigate; and … | yes |
| XXI 41–48 | … is well provided with them **. Every man** there is a barrator, … | … have provided well with them **: every one** there is a barrator, … | yes |
| XXI 49–62 | … cower down behind a jagg **which has** some screen for **thee**; and whatever outrage may … | … cower down behind a jagg **, so that thou mayest have** some screen for **thyself**; and whatever outrage may … | no |
| XXI 77–91 | … secure already against all your **weapons**, without will Divine and … | … secure already against all your **hindrances**, without will Divine and … | no |
| XXI 92–103 | … Yes, see thou nick him.” But that … | … Yes, see thou nick **it for** him. " But that … | no |
| XXI 104–114 | … But that Demon, who **had spoken** with my Guide, turned … | … But that Demon, who **was speaking** with my Guide, turned … | yes |
| XXI 104–114 | … onward, go along this **cavern**: near at hand is … | … onward, go along this **ridge**: near at hand is … | yes |
| XXI 104–114 | … later than this hour, a thousand two hundred and … | … later than this hour, **completed** a thousand two hundred and … | yes |
| XXI 104–114 | … and sixty-six years **were fulfilled** since the way here was … | … and sixty-six years since the way here was … | no |
| XXI 124–135 | … glue. Be these two **guided** safe **to** the other crag, which … | … glue; be these two safe **so far as** the other crag, which … | partly |
| XXII 38–52 | … My Guide drew close to **him,** and asked him whence he … | … My Guide drew close to **his side** and asked him whence he … | yes |
| XXII 66–80 | … was a neighbour of theirs **. Would** I still were covered with … | … was a neighbour of theirs **on the other side; would** I still were covered with … | yes |
| XXII 95–109 | … come. But let the **Malebranche stand** a little **back**, that they may not … | … come. But let the **evil claws hold back** a little, that they may not … | partly |
| XXIII 1–10 | … to Æsop’s fable where he **speaks** of the frog and mouse … | … to Æsop’s fable where he **spoke** of the frog and mouse … | yes |
| XXIII 27–42 | … . Even now thy thoughts **have entered** among mine, with similar … | … . Even now thy thoughts **were entering** among mine, with similar … | yes |
| XXIII 122–136 | … stone that moves from the **Great Barrier**, and bridges all the … | … stone that moves from the **great circular wall**, and bridges all the … | no |
| XXIII 137–148 | … broken and covers it not **. Ye may** mount up by its ruins … | … broken and covers it not **: you will be able to** mount up by its ruins … | yes |
| XXIV 1–11 | … lasts the temper of his **plumes:** the peasant, whose fodder … | … lasts the temper of his **pen,** the peasant, whose fodder … | no |
| XXIV 12–27 | … sweet aspect which I saw **before** at the foot of the … | … sweet aspect which I saw **first** at the foot of the … | yes |
| XXIV 72–86 | … : “Master, see thou get to the other **boundary**, and let us dismount … | … : " Master, see **that** thou get to the other **belt**, and let us dismount … | no |
| XXIV 114–126 | … ground, or of other **oppilation** that fetters men; who … | … ground, or of other **obstruction** that fetters men; who … | no |
| XXIV 140–151 | … in turbid clouds, and **on Piceno’s field shall be assailed** with angry and impetuous storm; whence it suddenly shall … | … in turbid clouds, and with angry and impetuous storm **a battle shall be fought on Piceno’s field**; whence it suddenly shall … | partly |
| XXIV 140–151 | … And I have said this **, for** it **must** grieve thee.” | … And I have said this **so that** it **may** grieve thee. " | yes |
| XXV 24–37 | … the cunning theft he made **from** the great herd that lay … | … the cunning theft he made **of** the great herd that lay … | yes |
| XXV 123–138 | … had become a brute, **flies** hissing along the valley, … | … had become a brute, **fled** hissing along the valley, … | yes |
| XXV 139–151 | … and my mind dismayed, **they** could not flee so covertly … | … and my mind dismayed, **those** could not flee so covertly … | yes |
| XXVI 10–18 | … by the stairs which the **bourns** had **given** us to descend before, … | … by the stairs which the **curbstones** had **made for** us to descend before, … | partly |
| XXVI 72–86 | … of you tell where he **wandering** went to die.” … | … of you tell where he **, having lost himself,** went to die.” … | no |
| XXVII 41–48 | … there where they are wont **to** ply their teeth. The … | … , where they are wont **,** ply their teeth. The … | no |
| XXVII 49–61 | … the winter. And that whose flank the Savio bathes … | … the winter; and that **city** whose flank the Savio bathes … | yes |
| XXVII 76–85 | … with repentance and confession I **yielded myself,** ah woe alas! and … | … with repentance and confession I **became a monk;** ah woe alas! and … | yes |
| XXVII 86–97 | … leaner; but as Constantine **called** Silvestro **out of** Soracte to cure his leprosy … | … leaner. But as Constantine **sought** Silvestro **within** Soracte to cure his leprosy … | yes |
| XXVIII 107–118 | … kindred!” I added **here. Wherefore** he, accumulating pain on … | … kindred! " I added **thereto; wherefore** he, accumulating pain on … | yes |
| XXVIII 119–133 | … and still seem to see a trunk going without a … | … and still seem to see **it,** a trunk going without a … | yes |
| XXIX 10–23 | … conceded to us; and **far** other things are to be … | … conceded to us; and other things are to be … | no |
| XXIX 46–56 | … with my hands. Such **grief** as there would be, … | … with my hands. Such **pain** as there would be, … | yes |
| XXIX 83–97 | … him Hell.” Then **they sprang asunder**, and each turned trembling … | … him Hell.” Then **the mutual propping broke**, and each turned trembling … | no |
| XXX 12–24 | … after she had seen Polyxena **her daughter** slain, and on the sea-strand … | … after she had seen Polyxena slain, and **, forlorn, discerned her Polydorus,** on the sea-strand … | no |
| XXX 12–24 | … the sea-strand, **forlorn, discerned the mangled body of her Polydorus:** she, out of her … | … the sea-strand, she, out of her … | no |
| XXX 12–24 | … to such a degree had sorrow wrung her soul. … | … to such a degree had **the** sorrow wrung her soul. … | yes |
| XXXI 13–24 | … any thunder weak: which **, towards it following its way,** directed my eyes all to one place. … | … any thunder weak; which directed my eyes **, that followed its course against itself,** all to one place: … | partly |
| XXXI 25–38 | … shalt see right well, **when** thou arrivest there, how … | … shalt see right well, **if** thou arrivest there, how … | yes |
| XXXI 39–53 | … he thunders, turreted the **brow** which compasses the pit: … | … he thunders, turreted the **bank** which compasses the pit. … | yes |
| XXXI 54–67 | … and prudent; for where **argument** of mind is joined to … | … and prudent: for where **the instrument** of the mind is joined … | yes |
| XXXI 68–79 | … for which no sweeter psalmody **is** fit. And towards him … | … for which no sweeter psalmody **was** fit. And towards him … | yes |
| XXXI 68–79 | … soul confused, and see itself that girdles thy huge … | … soul confused, and see **the horn** itself that girdles thy huge … | yes |
| XXXI 68–79 | … Nimrod, through whose ill **device** one language is not still … | … Nimrod, through whose ill **thought** one language is not still … | yes |
| XXXI 80–94 | … shot off, we found **another** far more fierce and large … | … shot off, we found **the next** far more fierce and large … | yes |
| XXXI 80–94 | … against high Jove,” **said** my Guide; “whence … | … against high Jove,” **saith** my Guide; “whence … | no |
| XXXI 124–136 | … in scorn: he can restore thy fame on earth … | … in scorn. He can **yet** restore thy fame on earth … | yes |
| XXXI 137–145 | … see him bend: and **at the time** I should have wished to … | … see him bend; and **it was so terrible a moment, that** I should have wished to … | yes |
| XXXI 137–145 | … Lucifer with Judas, he **placed** us; nor lingered there thus … | … Lucifer with Judas, he **set** us **down**; nor lingered there thus … | yes |
| XXXII 29–40 | … the water, when the **villager** oft dreams that she is … | … the water, when the **peasant-woman** oft dreams that she is … | yes |
| XXXII 41–54 | … said I, “who are **ye?**” And they bended their … | … said I, “who **you** are **.**” And they bended their … | no |
| XXXII 115–123 | … . Here he laments the **Frenchmen’s** silver. ‘Him of … | … . Here he laments the **Frenchman’s** silver. ‘Him of … | no |
| XXXIII 34–50 | … , I heard my sons asking for bread. Thou … | … , I heard my sons **who were with me, weeping in their sleep, and** asking for bread. Thou … | yes |
| XXXIII 81–91 | … fame of having betrayed thee **in** thy castles, thou oughtest … | … fame of having betrayed thee **of** thy castles, thou oughtest … | yes |
| XXXIII 92–106 | … another people, not bent **forwards**, but all reversed. … | … another people, not bent **downwards**, but all reversed. … | yes |
| XXXIII 107–118 | … ice.” He answered: “**Then** I am Friar Alberigo, … | … ice. " He answered **therefore**: “I am Friar Alberigo, … | partly |
| XXXIII 119–129 | … “then art thou dead **too**?” And he to … | … “then art thou dead **already**?” And he to … | yes |
| XXXIII 130–143 | … above. Thou must know, if thou art but … | … above. Thou must know **it**, if thou art but … | yes |
| XXXIV 39–51 | … ; and they were joined **up to** his crest; and the … | … ; and they were joined **at** his crest; and the … | yes |
| XXXIV 39–51 | … come from where the Nile **begins his valley**. Under each there issued … | … come from where the Nile **descends**. Under each there issued … | yes |
| XXXIV 39–51 | … winds went forth from him **, whereby** Cocytus all was frozen. … | … winds went forth from him **. Thereby** Cocytus all was frozen; … | no |
| XXXIV 78–93 | … that I had passed, **even they may** judge if I grew **toil-worn** then. “Rise up … | … which I had passed, **let them** judge if I grew **perplexed** then. “Rise up … | yes |
| XXXIV 94–105 | … difficult the road; and **now** to middle tierce the Sun … | … difficult the road; and **already** to middle tierce the Sun … | yes |

## Word order

Every phrase that Oelsner moved without changing it (none of these is marked):

| Lines | Carlyle | Oelsner | Marked |
|---|---|---|---|
| II 105–120 | … their hurt, as I **to come**, after these words were … | … their hurt, as I, after these words were … | no |
| II 105–120 | … these words were uttered, from my blessed seat; … | … these words were uttered, **to come** from my blessed seat; … | no |
| V 13–26 | … said Minos to me, leaving the act of that … | … said Minos to me, **when he saw me** leaving the act of that … | no |
| V 13–26 | … act of that great office **when he saw me**; “look how thou … | … act of that great office; " look how thou … | no |
| XVI 94–105 | … As that river—which has a path of its … | … As that river—which **first** has a path of its … | no |
| XVI 94–105 | … a path of its own **, first** from Monte Viso toward the … | … a path of its own from Monte Veso toward the … | no |
| XIX 1–9 | … and robbers ye, who **for gold and silver** prostitute the things of God … | … and robbers ye, who prostitute the things of God … | no |
| XIX 1–9 | … should be wedded unto righteousness! Now must the trumpet … | … should be wedded unto righteousness **, for gold and silver**! now must the trump … | no |
| XXXIV 116–128 | … down from Heaven; and **here** the land, which erst … | … down from Heaven; and the land, which erst … | no |
| XXXIV 116–128 | … , which erst stood out, through fear of him … | … , which erst stood out **here**, through fear of him … | no |

## Articles and conjunctions

Oelsner adds or removes an article or an *and* here and there, mostly unmarked:

| Lines | Carlyle | Oelsner | Marked |
|---|---|---|---|
| I 34–47 | … , which was covered with **a** spotted skin: and it … | … , which was covered with spotted hair. And it … | no |
| I 107–121 | … so that each calls for second death. And thou … | … so that each calls for **a** second death; and then … | no |
| VI 76–86 | … on me. Farinata and **the** Tegghiaio, who were so … | … on me. Farinata and Tegghiaio, who were so … | no |
| VIII 62–75 | … my eyes intently forwards. **And the** kind Master said: “ … | … my eyes intently forward. **The** kind Master said: " … | no |
| VIII 76–88 | … thousand spirits, rained from Heaven, who angrily exclaimed … | … thousand spirits, rained from **the** Heavens, who angrily … | yes |
| XIII 13–24 | … on the strange trees. **And the** kind Master began to say … | … on the strange trees. **The** kind Master began to say … | no |
| XVII 68–79 | … will bring the pouch with **the** three goats!’” … | … will bring the pouch with three goats!’” … | no |
| XIX 34–46 | … perforated and narrow bottom. **And the** kind Master did not yet … | … perforated and narrow bottom. **The** kind Master did not yet … | no |
| XX 63–75 | … a river, down through **the** green pastures. Soon as … | … a river, down through green pastures. Soon as … | no |
| XXI 1–13 | … other cleft of Malebolge and other vain lamentings: and … | … other cleft of Malebolge and **the** other vain lamentings; and … | yes |
| XXVI 19–30 | … face from us, when **as** the fly yields to the … | … face from us, when the fly yields to the … | no |
| XXVII 41–48 | … under the Green Clutches. **And the** old Mastiff of Verrucchio and … | … under the Green Clutches. **The** old Mastiff of Verrucchio and … | no |
| XXVII 49–61 | … of Lamone and Santerno guides Lioncel of the white lair … | … of Lamone and Santerno guides **the** Lioncel of the white lair … | yes |
| XXX 1–11 | … seeing his wife, with **the** two sons, come laden … | … seeing his wife, with two sons, go laden … | no |
| XXXI 54–67 | … ; for where argument of mind is joined to evil … | … for where the instrument of **the** mind is joined to evil … | yes |

## Checked against the page images

These unmarked changes of a single word or ending have no counterpart in the Italian, so they could have been errors of transcription in `texts/en/` or `texts/en-oelsner/`. All were checked against the page images, and every one is printed so in both books: they are Oelsner's revisions. Two of them take up Carlyle's own footnotes: *wild* (XII 81–93; Carlyle's note: "Or: 'wild,' obstructed way") and *nick it for him* (XXI 92–103; "Properly, 'nick it for him.'").

| Lines | Carlyle | Oelsner |
|---|---|---|
| I 122–136 | knewest | knowest |
| II 62–76 | came | come |
| VII 63–74 | may shine | shines |
| VII 75–87 | withstand | understand |
| XII 81–93 | woody | wild |
| XVI 112–126 | deep | steep |
| XVII 115–126 | cowered | cower |
| XXI 92–103 | see thou nick him | see thou nick it for him |
| XXVII 41–48 | wont to ply | wont, ply |
| XXXI 80–94 | said | saith |
| XXXII 41–54 | who are ye? | who you are. |
| XXXII 115–123 | Frenchmen’s | Frenchman’s |
