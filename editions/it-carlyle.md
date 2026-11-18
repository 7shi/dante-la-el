# The Italian of dante-corpus and of Carlyle's edition

This report compares the Italian text of the Inferno in [dante-corpus](https://github.com/7shi/dante-corpus) with the Italian printed in John A. Carlyle's edition (fifth edition, 1889; [`texts/en/`](../texts/en/)), from which Carlyle made his prose translation. Oelsner's text (The Temple Classics, 1903; [`texts/en-oelsner/`](../texts/en-oelsner/)), printed with his revision of Carlyle's translation, is given beside them where the two differ in words. It does not list every difference: the differences in spelling and in the forms of words are described by their features with examples, and only the differences in words are listed in full.

The two texts have the same lines (4,720 in 34 cantos), so they are compared line by line.

## Method

[`scripts/compare_editions.py`](scripts/compare_editions.py) `it` compares each pair of lines word by word and sorts each line by the first kind of difference it has:

| Kind | Lines |
|---|---|
| identical | 160 |
| orthography only: the same letters once accents, apostrophes, case, punctuation, and word division are left aside | 1,874 |
| word forms only: every differing word is close in spelling (luogo / loco), or an elided form of the other (il / 'l) | 2,367 |
| other words, or a word present in one text only | 319 |

The lines of the last kind, and the pairs of the third kind that are not close in meaning, were then read and sorted by hand into the categories below: a different word (89 lines), a different function word (153), a different word order (29), and a different inflection of the same word (45). The rest are words present in one text only, described by examples. A pair close in spelling can still be a different word (tuono / 'ntrono, Livio / Lino, Romani / Troiani); these were picked out of the third kind by reading its list of pairs.

The judgments are kept in [judge-it.txt](judge-it.txt), and the tables are rendered from them by [`scripts/render_editions.py`](scripts/render_editions.py) `it`. In the tables, the differing words are in bold. The column "Oelsner" says which of the two texts Oelsner's line reads with at those words (judged by the closer spelling), or gives his line if it reads with neither, or partly with each. Of the 316 lines listed, Oelsner reads with Carlyle in 167 and with dante-corpus in 136. Carlyle's English follows his Italian, and where Oelsner's Italian differs from it, Oelsner's revision of the English follows his own: III 59 *Guardai, e vidi* is Carlyle's "I looked and saw", Oelsner's *vidi e conobbi* "I [saw and knew]"; IV 68 *dal sommo* is Carlyle's "within the topmost part", Oelsner's *dal sonno* "[since my slumber]" (see [en-carlyle-oelsner.md](en-carlyle-oelsner.md)).

## Orthography

Carlyle's text is set in the conventions of the nineteenth-century editions; dante-corpus follows the spelling of a modern critical text. The differences that touch only the orthography:

| Feature | Lines | Example (Carlyle / dante-corpus) |
|---|---|---|
| Carlyle's text has no quotation marks; speeches open after a colon | 804 | I 135 E color, che tu fai cotanto mesti. / e color cui tu fai cotanto mesti». |
| every line of Carlyle's text begins with a capital | 3,528 | I 2 Mi ritrovai per una selva oscura, / mi ritrovai per una selva oscura, |
| Carlyle sets a space after an apostrophe; dante-corpus writes the straight apostrophe without a space | 1,621 | I 9 Dirò dell’ altre cose, ch’io v’ ho scorte. / dirò de l'altre cose ch'i' v'ho scorte. |
| accents differ | 730 | see below |
| Carlyle writes a preposition and an article as one word, dante-corpus as two | 57 | II 5 Sì del cammino, e sì della pietate, / sì del cammino e sì de la pietate, |

Accents: Carlyle writes the grave accent on closed final vowels (*nè* 65 times, *chè* 61, *perchè* 56, *sè* 31) where dante-corpus writes the acute (*né*, *ché*, *perché*, *sé*); dante-corpus marks a monosyllable that is stressed (*sù* 31, *fé* 25), a diaeresis that counts as a syllable (*ïo*, *vïaggio*, *fïate*), and a stress on proper names and rare words (*Minòs*, *sùbito*, *tòrre*), which Carlyle leaves unmarked. Carlyle's circumflex marks a contraction (*vêr* 10).

## Word forms

Most differences in words are forms of the same word: Carlyle's text gives the forms of literary Italian, dante-corpus the older Florentine forms of the manuscripts. The most frequent pairs (3,024 differences in 1,151 pairs):

| Carlyle / dante-corpus | Times | Example |
|---|---|---|
| il / 'l | 353 | I 30 Sì che il piè fermo sempre era il più basso. / sì che 'l piè fermo sempre era 'l più basso. |
| gli / li | 157 | I 100 Molti son gli animali / Molti son li animali |
| ed / e | 123 | I 5 Questa selva selvaggia ed aspra e forte, / esta selva selvaggia e aspra e forte |
| io / i' | 110 | I 9 ch’io v’ ho scorte / ch'i' v'ho scorte |
| della / de la, alla / a la, nella / ne la, … | 73, 53, 26, … | II 5 della pietate / de la pietate |
| egli / elli, quegli / quelli | 66, 11 | III 13 Ed egli a me / Ed elli a me |
| ogni / ogne | 56 | I 18 per ogni calle / per ogne calle |
| che / ch' | 51 | I 25 che ancor fuggiva / ch'ancor fuggiva |
| senza / sanza | 40 | I 58 la bestia senza pace / la bestia sanza pace |
| ei / el | 25 | IX 8 Cominciò ei / cominciò el |
| duo / due | 22 | IV 148 in duo si scema / in due si scema |
| rispose / rispuose | 24 | I 92 Rispose, poi che lagrimar mi vide / rispuose, … |
| fur / fuor | 19 | III 7 non fur cose create / non fuor cose create |
| luogo / loco, fuoco / foco, giuoco / gioco, nuovo / novo, uomo / omo | 15, 11, … | III 16 al luogo / al loco; I 119 Nel fuoco / nel foco |
| signor / segnor, sopra / sovra, entrare / intrare | 7, 8, 3 | II 73 al Signor mio / al segnor mio |

Words present in one text only are mostly a conjunction *e* (I 104 *Ma sapienza, e amore, e virtute* / *ma sapïenza, amore e virtute*), an article (III 30 *quando il turbo spira* / *quando turbo spira*; dante-corpus writes the article *i* elided as *'*, as in V 71 *e ' cavalieri*, which is not a difference of words), or a preposition (IV 38 *adoràr debitamente Dio* / *adorar debitamente a Dio*). A few are content words: *è* (in Carlyle only in IV 90 *e l’ ultimo è Lucano* / *e l'ultimo Lucano* and XXX 132, in dante-corpus only in XXXIII 14), and, in Carlyle only, *già* (XIII 22, XXX 3) and *or* (XVII 39).

## Different words

Every line where a word of one text is a different word in the other, not a form of the same word.

| Line | Carlyle | dante-corpus | Oelsner |
|---|---|---|---|
| I 26 | Si volse **indietro** a rimirar lo passo, | si volse **a retro** a rimirar lo passo | Carlyle |
| I 28 | Poi ch’ **ebbi riposato** il corpo lasso, | Poi ch'**èi posato un poco** il corpo lasso, | dante-corpus |
| II 60 | E durerà quanto **il moto** lontana: | e durerà quanto '**l mondo** lontana, | Carlyle |
| II 81 | Più non t’ è **uopo** aprirmi il tuo talento. | più non t'è **uo' ch**'aprirmi il tuo talento. | Carlyle |
| II 98 | E disse: Or **abbisogna** il tuo fedele | e disse:—Or **ha bisogno** il tuo fedele | dante-corpus |
| III 29 | Sempre in quell’ **aria senza** tempo tinta, | sempre in quell' **aura sanza** tempo tinta, | Carlyle |
| III 59 | **Guardai**, e **vidi** l’ ombra di colui | **vidi** e **conobbi** l'ombra di colui | dante-corpus |
| IV 9 | Che **tuono** accoglie d’ infiniti guai. | che '**ntrono** accoglie d'infiniti guai. | Carlyle |
| IV 12 | Io non vi discernea **veruna** cosa. | io non vi discernea **alcuna** cosa. | dante-corpus |
| IV 68 | Di qua dal **sommo**, quand’ io vidi un foco, | di qua dal **sonno**, quand' io vidi un foco | dante-corpus |
| IV 141 | **Tullio**, e **Livio**, e Seneca morale: | **Tulïo** e **Lino** e Seneca morale; | Tullio, e Lino, e Seneca morale; |
| V 51 | Genti, che l’ **aer nero** sì gastiga? | genti che l'**aura nera** sì gastiga?». | dante-corpus |
| V 72 | Pietà mi **vinse**, e fui quasi smarrito. | pietà mi **giunse**, e fui quasi smarrito. | dante-corpus |
| V 83 | Con l’ ali **aperte** e ferme al dolce nido | con l'ali **alzate** e ferme al dolce nido | dante-corpus |
| V 84 | **Volan** per l’ aer dal voler portate: | **vegnon** per l'aere, dal voler portate; | dante-corpus |
| V 126 | **Farò** come colui che piange e dice. | **dirò** come colui che piange e dice. | Carlyle |
| VI 88 | Ma **se** tu **torni mai** nel dolce mondo, | Ma **quando** tu **sarai** nel dolce mondo, | dante-corpus |
| VI 97 | Ciascun **ritroverà** la trista tomba, | ciascun **rivederà** la trista tomba, | Carlyle |
| VII 6 | Non ci **terrà** lo scender questa roccia. | non ci **torrà** lo scender questa roccia». | dante-corpus |
| VII 17 | **Prendendo** più della dolente ripa, | **pigliando** più de la dolente ripa | Carlyle |
| VII 33 | **Gridando sempre in** loro ontoso metro. | **gridandosi anche** loro ontoso metro; | dante-corpus |
| VII 67 | Maestro, **dissi lui**, or mi di’ anche: | «Maestro **mio», diss' io**, «or mi dì anche: | Carlyle |
| VII 103 | L’ acqua era buia **molto** più che persa: | L'acqua era buia **assai** più che persa; | dante-corpus |
| VII 106 | **Una** palude **fa, che** ha nome Stige, | **In la** palude **va c**'ha nome Stige | Carlyle |
| VII 109 | **Ed** io, che **a rimirar mi** stava inteso, | **E** io, che **di mirare** stava inteso, | Ed io, che di mirar mi stava inteso, |
| VII 118 | Che sotto l’ acqua **ha** gente che sospira, | che sotto l'acqua **è** gente che sospira, | Carlyle |
| VIII 7 | Ed io, **rivolto** al mar di tutto il senno, | E io **mi volsi** al mar di tutto 'l senno; | dante-corpus |
| VIII 24 | **Tal si fe**’ Flegiàs nell’ ira accolta. | **fecesi** Flegïàs ne l'ira accolta. | dante-corpus |
| VIII 101 | E se l’ **andar** più oltre c’ è negato, | e se 'l **passar** più oltre ci è negato, | Carlyle |
| IX 37 | Ove in un punto **vidi** dritte ratto | dove in un punto **furon** dritte ratto | dante-corpus |
| IX 53 | **Gridavan** tutte riguardando in giuso: | **dicevan** tutte riguardando in giuso; | dante-corpus |
| IX 89 | **Giunse alla** porta, e con una verghetta | **Venne a la** porta e con una verghetta | dante-corpus |
| X 1 | Ora sen va per **uno stretto** calle, | Ora sen va per **un secreto** calle, | dante-corpus |
| X 19 | Ed io: Buon Duca, non tegno **nascosto** | E io: «Buon duca, non tegno **riposto** | Carlyle |
| X 21 | E tu m’ hai non pur **ora** a ciò disposto. | e tu m'hai non pur **mo** a ciò disposto». | dante-corpus |
| X 88 | Poi ch’ ebbe sospirando il capo **scosso**; | Poi ch'ebbe sospirando il capo **mosso**, | Carlyle |
| X 133 | Appresso **volse** a man sinistra il piede: | Appresso **mosse** a man sinistra il piede: | Carlyle |
| XI 55 | Questo modo di retro par **che uccida** | Questo modo di retro par **ch'incida** | Carlyle |
| XI 90 | La divina **giustizia gli** martelli. | la divina **vendetta li** martelli». | Carlyle |
| XII 125 | Quel sangue sì, che **copria** pur li piedi: | quel sangue, sì che **cocea** pur li piedi; | dante-corpus |
| XIII 21 | Cose, che **daran** fede al mio sermone. | cose che **torrien** fede al mio sermone». | dante-corpus |
| XIII 35 | Ricominciò a **gridar**: Perchè mi scerpi? | ricominciò a **dir**: «Perché mi scerpi? | Carlyle |
| XIII 144 | **Cangiò** ’l primo padrone: ond’ ei per questo | **mutò** 'l primo padrone; ond' ei per questo | dante-corpus |
| XIV 3 | E rende’ le a colui, ch’ era già **roco**. | e rende'le a colui, ch'era già **fioco**. | dante-corpus |
| XIV 12 | Quivi fermammo i **piedi** a randa a randa. | quivi fermammo i **passi** a randa a randa. | dante-corpus |
| XIV 57 | **Gridando**: Buon Vulcano, aiuta, aiuta, | **chiamando** “Buon Vulcano, aiuta, aiuta!”, | dante-corpus |
| XIV 75 | Ma sempre al bosco **gli ritieni** stretti. | ma sempre al bosco **tien li piedi** stretti». | Carlyle |
| XV 29 | E chinando la **mia alla** sua faccia, | e chinando la **mano a la** sua faccia, | Carlyle |
| XVI 30 | Cominciò l’ uno, e **il tristo** aspetto e brollo; | cominciò l'uno, «e '**l tinto** aspetto e brollo, | dante-corpus |
| XVI 65 | Le membra tue, **rispose quegli allora**, | le membra tue», **rispuose quelli ancora**, | Carlyle |
| XVI 78 | **Guatar** l’ un l’ altro, **come** al ver si guata. | **guardar** l'un l'altro **com**' al ver si guata. | Carlyle |
| XVI 134 | **Talvolta** a solver l’ áncora, ch’ aggrappa | **talora** a solver l'àncora ch'aggrappa | dante-corpus |
| XVII 95 | Ad altro **forte**, tosto ch’ **io** montai, | ad altro **forse**, tosto ch'**i**' montai | ad altro forse, tosto ch' io montai |
| XVIII 6 | Di cui suo **luogo conterà** l’ ordigno. | di cui suo **loco dicerò** l'ordigno. | dante-corpus |
| XVIII 30 | Hanno a passar la gente modo **tolto**; | hanno a passar la gente modo **colto**, | dante-corpus |
| XVIII 104 | **Nell**’ altra bolgia, e che col muso **sbuffa**, | **ne l**'altra bolgia e che col muso **scuffa**, | Carlyle |
| XIX 94 | Nè Pier nè gli altri **chiesero** a Mattia | Né Pier né li altri **tolsero** a Matia | Carlyle |
| XXII 116 | Lascisi **il colle**, e sia la ripa scudo, | Lascisi '**l collo**, e sia la ripa scudo, | Carlyle |
| XXII 124 | Di che ciascun di **colpo** fu compunto, | Di che ciascun di **colpa** fu compunto, | dante-corpus |
| XXIII 22 | Te e me tostamente, **io** pavento | te e me tostamente, **i' ho** pavento | dante-corpus |
| XXIII 53 | Del fondo giù ch’ **ei giunsero** in sul colle | del fondo giù, ch'**e' furon** in sul colle | dante-corpus |
| XXIII 63 | Che per li monaci **in Cologna** fassi. | che **in Clugnì** per li monaci fassi. | Carlyle |
| XXIII 141 | Colui, che i peccator di **là** uncina. | colui che i peccator di **qua** uncina». | Carlyle |
| XXIV 104 | La **cener** si raccolse, **e** per sè stessa | la **polver** si raccolse per sé stessa | dante-corpus |
| XXIV 119 | **O Giustizia** di Dio, quant’ è severa! | **Oh potenza** di Dio, quant' è severa, | dante-corpus |
| XXIV 129 | Ch’ io il vidi **uom già** di sangue e di corrucci. | ch'io 'l vidi **uomo** di sangue e di crucci». | dante-corpus |
| XXV 18 | Venir **gridando**: Ov’ è, ov’ è l’ acerbo? | venir **chiamando**: «Ov' è, ov' è l'acerbo?». | dante-corpus |
| XXV 29 | Per lo **furar** frodolente **ch’ ei** fece | per lo **furto che** frodolente fece | Carlyle |
| XXV 144 | La novità, se fior la **lingua** abborra. | la novità se fior la **penna** abborra. | dante-corpus |
| XXVI 57 | Alla vendetta **corron, com’ all**’ ira: | a la vendetta **vanno come a l**'ira; | dante-corpus |
| XXVII 100 | E poi **mi disse**: Tuo **cor** non sospetti: | E' poi **ridisse**: “Tuo **cuor** non sospetti; | Carlyle |
| XXVIII 10 | Per li **Romani**, e per la lunga guerra | per li **Troiani** e per la lunga guerra | dante-corpus |
| XXVIII 20 | Mostrasse, d’ **agguagliar** sarebbe nulla | mostrasse, d'**aequar** sarebbe nulla | dante-corpus |
| XXVIII 90 | Non **farà** lor mestier voto nè preco. | non **sarà** lor mestier voto né preco». | Carlyle |
| XXIX 51 | Qual **suole uscir dalle** marcite membre. | qual **suol venir de le** marcite membre. | Carlyle |
| XXX 6 | **Venir** carcata **di** ciascuna mano, | **andar** carcata **da** ciascuna mano, | dante-corpus |
| XXX 51 | Tronca **dal lato** che l’ uomo ha forcuto. | tronca **da l'altro** che l'uomo ha forcuto. | Carlyle |
| XXX 125 | La bocca tua per **dir** mal come suole; | la bocca tua per **tuo** mal come suole; | Carlyle |
| XXXI 4 | Così od’ io che **soleva** la lancia | così od' io che **solea far** la lancia | Carlyle |
| XXXI 19 | Poco portai in là **alta** la testa, | Poco portäi in là **volta** la testa, | dante-corpus |
| XXXI 39 | Fuggemi errore, e **giungemi** paura: | fuggiemi errore e **cresciemi** paura; | dante-corpus |
| XXXI 138 | Sovr’ essa sì, **ch**’ ella **in contrario** penda; | sovr' essa sì, **ched** ella **incontro** penda: | dante-corpus |
| XXXII 20 | **Fa** sì, che tu non calchi con le piante | **va** sì, che tu non calchi con le piante | Carlyle |
| XXXII 109 | Omai, diss’ io, non vo’ che **tu** favelle, | «Omai», diss' io, «non vo' che **più** favelle, | Carlyle |
| XXXIII 74 | E **tre** dì li chiamai, poi ch’ ei fur morti: | e **due** dì li chiamai, poi che fur morti. | dante-corpus |
| XXXIII 148 | Ma distendi **oramai** in qua la mano, | Ma distendi **oggimai** in qua la mano; | Carlyle |
| XXXIV 13 | Altre **stanno** a giacere, altre stanno erte, | Altre **sono** a giacere; altre stanno erte, | dante-corpus |
| XXXIV 26 | Pensa **oramai** per te, s’ hai fior d’ ingegno, | pensa **oggimai** per te, s'hai fior d'ingegno, | Carlyle |
| XXXIV 113 | **Che** è **opposto** a quel, che la gran secca | **ch**'è **contraposto** a quel che la gran secca | dante-corpus |

## Different function words

Every line where a preposition, conjunction, pronoun, article, or particle differs (not as a form of the same word).

| Line | Carlyle | dante-corpus | Oelsner |
|---|---|---|---|
| I 11 | Tant’ era pien di sonno **in su** quel punto, | tant' era pien di sonno **a** quel punto | Carlyle |
| I 40 | Mosse **da** prima quelle cose belle; | mosse **di** prima quelle cose belle; | Carlyle |
| I 72 | **Al** tempo degli Dei falsi e bugiardi. | **nel** tempo de li dèi falsi e bugiardi. | Carlyle |
| I 74 | Figliuol d’ Anchise, che venne **da** Troia, | figliuol d'Anchise che venne **di** Troia, | Carlyle |
| I 102 | Verrà, che la farà morir **di** doglia. | verrà, che la farà morir **con** doglia. | dante-corpus |
| I 117 | **Che** la seconda morte ciascun grida: | **ch'a** la seconda morte ciascun grida; | Carlyle |
| I 135 | E color, **che** tu fai cotanto mesti. | e color **cui** tu fai cotanto mesti». | dante-corpus |
| II 13 | Tu dici, che di Silvio **lo** parente, | Tu dici che di Silvïo **il** parente, | Carlyle |
| II 39 | Sì che **del** cominciar tutto si tolle; | sì che **dal** cominciar tutto si tolle, | dante-corpus |
| II 45 | L’ anima tua è **la** viltade offesa, | «l'anima tua è **da** viltade offesa; | dante-corpus |
| II 71 | Vegno **di** loco, ove tornar disio: | vegno **del** loco ove tornar disio; | Carlyle |
| II 78 | **Da** quel ciel, che ha minori i cerchi sui: | **di** quel ciel c'ha minor li cerchi sui, | Carlyle |
| II 110 | A far lor pro, **nè** a fuggir lor danno, | a far lor pro **o** a fuggir lor danno, | Carlyle |
| II 112 | Venni **quaggiù dal** mio beato scanno, | venni **qua giù del** mio beato scanno, | Carlyle |
| II 113 | Fidandomi **nel** tuo parlare onesto, | fidandomi **del** tuo parlare onesto, | dante-corpus |
| II 134 | E **tu** cortese, ch’ ubbidisti tosto | e **te** cortese ch'ubidisti tosto | Carlyle |
| III 81 | Infino al fiume **dal** parlar mi trassi. | infino al fiume **del** parlar mi trassi. | Carlyle |
| IV 49 | **Uscinne** mai alcuno, o per suo merto, | «**uscicci** mai alcuno, o per suo merto | dante-corpus |
| IV 59 | Israel con **suo** padre, e co’ suoi nati, | Israèl con **lo** padre e co' suoi nati | dante-corpus |
| IV 70 | Di lungi **v**’ eravamo ancora un poco, | Di lungi **n**'eravamo ancora un poco, | Carlyle |
| IV 78 | Grazia acquista **nel** ciel che sì gli avanza. | grazïa acquista **in** ciel che sì li avanza». | Carlyle |
| IV 101 | Ch’ **essi** mi fecer **della** loro schiera, | ch'**e' sì** mi fecer **de la** loro schiera, | Carlyle |
| V 68 | Ombre mostrommi, e **nominolle** a dito, | ombre mostrommi e **nominommi** a dito, | dante-corpus |
| V 78 | Per **quell**’ amor che i mena; **e quei** verranno. | per **quello** amor che i mena, **ed ei** verranno». | Carlyle |
| V 92 | Noi pregheremmo lui **per** la tua pace, | noi pregheremmo lui **de** la tua pace, | Carlyle |
| V 94 | Di quel che udire e che parlar **ti** piace | Di quel che udire e che parlar **vi** piace, | Carlyle |
| V 96 | Mentrechè il vento, come fa, **si** tace. | mentre che 'l vento, come fa, **ci** tace. | dante-corpus |
| V 109 | **Da che** io intesi quelle anime offense, | **Quand**' io intesi quell' anime offense, | Carlyle |
| V 121 | **Ed ella** a me: Nessun maggior dolore, | **E quella** a me: «Nessun maggior dolore | Carlyle |
| VI 18 | Graffia **gli** spirti, **gli scuoia**, ed isquatra. | graffia **li** spirti **ed iscoia** ed isquatra. | Carlyle |
| VI 31 | Cotai **se** fecer quelle facce lorde | cotai **si** fecer quelle facce lorde | Carlyle |
| VI 43 | **Ed** io a **lei**; L’ angoscia che tu hai | **E** io a **lui**: «L'angoscia che tu hai | Carlyle |
| VI 64 | **Ed egli** a me: Dopo lunga tenzone | **E quelli** a me: «Dopo lunga tencione | Carlyle |
| VI 72 | Come che di ciò pianga, **e** che ne adonti. | come che di ciò pianga **o** che n'aonti. | Carlyle |
| VI 73 | Giusti son **duo, ma** non vi sono intesi: | Giusti son **due, e** non vi sono intesi; | Carlyle |
| VII 11 | Vuolsi **così nell**’ alto, ove Michele | vuolsi **ne l**'alto, là dove Michele | dante-corpus |
| VII 86 | **Ella provvede**, giudica, e persegue | **questa provede**, giudica, e persegue | Carlyle |
| VII 112 | **Questi** si percotean non pur con mano, | **Queste** si percotean non pur con mano, | Carlyle |
| VIII 21 | Più non ci avrai, **se non** passando il loto. | più non ci avrai **che sol** passando il loto». | dante-corpus |
| VIII 62 | **Lo** Fiorentino spirito bizzarro | **e 'l** fiorentino spirito bizzarro | Carlyle |
| VIII 67 | **E il** buon Maestro disse: Omai, figliuolo, | **Lo** buon maestro disse: «Omai, figliuolo, | dante-corpus |
| VIII 93 | Che **scorto l’ hai per** sì buia contrada. | che **li ha' iscorta** sì buia contrada». | dante-corpus |
| VIII 96 | **Ch’ io** non credetti ritornarci mai. | **ché** non credetti ritornarci mai. | Carlyle |
| IX 54 | Mal **noi** vengiammo in Teseo l’ assalto. | «mal **non** vengiammo in Tesëo l'assalto». | Carlyle |
| IX 57 | Nulla sarebbe **del** tornar mai suso. | nulla sarebbe **di** tornar mai suso». | Carlyle |
| IX 69 | Che fier la selva **senza** alcun rattento; | che fier la selva **e sanz**' alcun rattento | Carlyle |
| IX 85 | Ben m’ accorsi ch’ egli era **del** Ciel messo, | Ben m'accorsi ch'elli era **da** ciel messo, | Carlyle |
| IX 127 | **Ed egli** a me: Qui son gli eresiarche | **E quelli** a me: «Qui son li eresïarche | Carlyle |
| X 10 | **Ed egli** a me: Tutti saran serrati, | **E quelli** a me: «Tutti saran serrati | Carlyle |
| X 36 | Come avesse lo Inferno **in** gran dispitto: | com' avesse l'inferno **a** gran dispitto. | Carlyle |
| X 40 | **Tosto che** al piè della sua tomba fui, | **Com' io** al piè de la sua tomba fui, | dante-corpus |
| X 57 | **Ma** poi che il sospicar fu tutto spento, | **e** poi che 'l sospecciar fu tutto spento, | Carlyle |
| X 104 | Nostro intelletto; e, s’ altri **nol** ci apporta, | nostro intelletto; e s'altri **non** ci apporta, | Carlyle |
| X 135 | Per un sentier, **che ad** una valle fiede, | per un sentier **ch'a** una valle fiede, | Carlyle |
| XI 28 | **De**’ violenti il primo cerchio è tutto, | **Di** vïolenti il primo cerchio è tutto; | Carlyle |
| XI 53 | Può l’ uomo usare in **quei, ch’ in** lui **si** fida, | può l'omo usare in **colui che 'n** lui fida | dante-corpus |
| XI 73 | Perchè non dentro **della** città roggia | perché non dentro **da la** città roggia | Carlyle |
| XII 49 | O cieca cupidigia, **o** ira folle, | Oh cieca cupidigia **e** ira folle, | dante-corpus |
| XII 100 | **Noi** ci movemmo colla scorta fida | **Or** ci movemmo con la scorta fida | Carlyle |
| XII 126 | E **quivi** fu del fosso il nostro passo. | e **quindi** fu del fosso il nostro passo. | Carlyle |
| XIII 19 | Che tu verrai **all**’ orribil sabbione. | che tu verrai **ne l**'orribil sabbione. | dante-corpus |
| XIII 90 | S’ alcuna mai **da** tai membra si spiega. | s'alcuna mai **di** tai membra si spiega». | Carlyle |
| XIII 91 | Allor soffiò **lo** tronco forte, e poi | Allor soffiò **il** tronco forte, e poi | Carlyle |
| XIII 115 | Ed ecco **duo dalla** sinistra costa, | Ed ecco **due da la** sinistra costa, | Carlyle |
| XIII 121 | Le gambe tue **alle** giostre **del** Toppo. | le gambe tue **a le** giostre **dal** Toppo!». | Carlyle |
| XIII 139 | **E quegli** a noi: O anime, che giunte | **Ed elli** a noi: «O anime che giunte | Carlyle |
| XIII 141 | **Che** le mie **frondi ha** sì da me disgiunte, | **c'ha** le mie **fronde** sì da me disgiunte, | dante-corpus |
| XIV 35 | Con le sue schiere, **perciocchè il** vapore | con le sue schiere, **acciò che lo** vapore | Carlyle |
| XIV 55 | **E** s’ egli stanchi gli altri a muta a muta | **o** s'elli stanchi li altri a muta a muta | dante-corpus |
| XIV 59 | E me saetti **di** tutta sua forza, | e me saetti **con** tutta sua forza: | Carlyle |
| XV 53 | Questi m’ apparve, **ritornando** in quella, | questi m'apparve, **tornand' ïo** in quella, | dante-corpus |
| XV 75 | S’ alcuna surge **ancor nel** lor letame, | s'alcuna surge **ancora in** lor letame, | dante-corpus |
| XVI 1 | Già era in loco, **ove** s’ udia il rimbombo | Già era in loco **onde** s'udia 'l rimbombo | Carlyle |
| XVI 81 | Felice te, **che** sì parli a tua posta! | felice te **se** sì parli a tua posta! | dante-corpus |
| XVI 113 | E alquanto di **lungi dalla** sponda | e alquanto di **lunge da la** sponda | Carlyle |
| XVI 125 | De’ l’ uom chiuder le labbra **quant’ ei** puote, | de' l'uom chiuder le labbra **fin ch'el** puote, | dante-corpus |
| XVII 2 | Che passa i monti, e rompe **mura ed** armi; | che passa i monti e rompe **i muri e l**'armi! | Carlyle |
| XVII 24 | Su l’ orlo, che di pietra **il** sabbion serra. | su l'orlo ch'è di pietra **e 'l** sabbion serra. | Carlyle |
| XVII 60 | Che **di lione** avea faccia e contegno. | che **d'un leone** avea faccia e contegno. | dante-corpus |
| XVII 62 | Vidine un’ altra **più che** sangue rossa | vidine un'altra **come** sangue rossa, | dante-corpus |
| XVII 134 | **A piede a** piè **della** stagliata rocca: | **al** piè **al piè de la** stagliata rocca, | Carlyle |
| XVIII 19 | In questo luogo, **dalla** schiena scossi | In questo luogo, **de la** schiena scossi | Carlyle |
| XVIII 69 | **Dove** uno scoglio della ripa uscia. | **là 'v**' uno scoglio de la ripa uscia. | là dove un scoglio della ripa uscia. |
| XVIII 79 | **Dal** vecchio ponte guardavam la traccia, | **Del** vecchio ponte guardavam la traccia | Carlyle |
| XVIII 82 | **Il** buon Maestro, senza mia dimanda, | **E 'l** buon maestro, sanza mia dimanda, | Carlyle |
| XIX 43 | **E il** buon Maestro ancor dalla sua anca | **Lo** buon maestro ancor de la sua anca | dante-corpus |
| XIX 96 | **Nel luogo**, che perdè l’ anima ria. | **al loco** che perdé l'anima ria. | dante-corpus |
| XX 12 | Ciascun **dal** mento **al** principio del casso, | ciascun **tra 'l** mento **e 'l** principio del casso, | dante-corpus |
| XX 22 | Quando la nostra imagine **da** presso | quando la nostra imagine **di** presso | Carlyle |
| XX 29 | Chi è più scellerato **di** colui, | chi è più scellerato **che** colui | dante-corpus |
| XX 33 | **Quando** gridavan tutti: Dove rui, | **per ch'ei** gridavan tutti: “Dove rui, | dante-corpus |
| XX 43 | E prima poi ribatter **le** convenne | e prima, poi, ribatter **li** convenne | dante-corpus |
| XX 63 | Sovra Tiralli, **ed** ha nome Benaco. | sovra Tiralli, **c**'ha nome Benaco. | dante-corpus |
| XX 95 | Prima che la mattía **di** Casalodi, | prima che la mattia **da** Casalodi | Carlyle |
| XXI 36 | **Ed ei** tenea de’ piè ghermito **il** nerbo. | **e quei** tenea de' piè ghermito '**l** nerbo. | e quei tenea de' piè ghermito il nerbo. |
| XXI 61 | E per nulla offension, che **a me** sia fatta, | e per nulla offension che **mi** sia fatta, | dante-corpus |
| XXI 83 | **Lasciami** andar, chè nel Cielo è voluto | **Lascian**' andar, ché nel cielo è voluto | Carlyle |
| XXI 93 | Sì ch’ io temetti **non** tenesser patto. | sì ch'io temetti **ch'ei** tenesser patto; | dante-corpus |
| XXII 31 | Io vidi, ed anche il **cuor mi s**’ accapriccia, | I' vidi, e anco il **cor me n**'accapriccia, | dante-corpus |
| XXII 74 | **Giù dalle** gambe; onde **il** decurio loro | **giuso a le** gambe; onde '**l** decurio loro | giuso alle gambe; onde il decurio loro |
| XXIII 104 | Io Catalano, e **costui** Loderingo | io Catalano e **questi** Loderingo | dante-corpus |
| XXIII 118 | Attraversato e nudo **è per** la via, | Attraversato è, nudo, **ne** la via, | Carlyle |
| XXIII 122 | In questa fossa, e **gli** altri **del** Concilio, | in questa fossa, e **li** altri **dal** concilio | Carlyle |
| XXIII 136 | Salvo **ch’ a** questo è rotto, e nol coperchia. | salvo **che 'n** questo è rotto e nol coperchia; | Carlyle |
| XXIV 10 | Ritorna **a** casa, e qua e là si lagna, | ritorna **in** casa, e qua e là si lagna, | dante-corpus |
| XXIV 51 | Qual fummo in aere, **o** in acqua la schiuma: | qual fummo in aere **e** in acqua la schiuma. | dante-corpus |
| XXIV 65 | Onde una voce **uscìo dall**’ altro fosso, | onde una voce **uscì de l**'altro fosso, | Carlyle |
| XXIV 88 | **Non** tante pestilenze, nè sì ree | **né** tante pestilenzie né sì ree | dante-corpus |
| XXIV 90 | Nè con ciò che di sopra **il** mar Rosso èe. | né con ciò che di sopra **al** Mar Rosso èe. | Carlyle |
| XXIV 105 | **In** quel medesmo ritornò di butto. | **e 'n** quel medesmo ritornò di butto. | dante-corpus |
| XXIV 116 | Tutto smarrito **dalla** grande angoscia | tutto smarrito **de la** grande angoscia | Carlyle |
| XXIV 128 | E **dimanda qual** colpa quaggiù il pinse; | e **domanda che** colpa qua giù 'l pinse; | Carlyle |
| XXIV 141 | Se mai sarai di fuor **de**’ luoghi bui, | se mai sarai di fuor **da**' luoghi bui, | Carlyle |
| XXIV 151 | E detto l’ ho, perchè doler **ten** debbia. | E detto l'ho perché doler **ti** debbia!». | dante-corpus |
| XXV 15 | Non quel che cadde a Tebe giù **de**’ muri. | non quel che cadde a Tebe giù **da**' muri. | dante-corpus |
| XXV 25 | Lo mio Maestro disse: **Quegli** è Caco, | Lo mio maestro disse: «**Questi** è Caco, | Carlyle |
| XXV 42 | Che l’ un **nomare all**’ altro convenette, | che l'un **nomar un** altro convenette, | dante-corpus |
| XXV 57 | E dietro per le ren su **lo** ritese. | e dietro per le ren sù **la** ritese. | dante-corpus |
| XXV 74 | Le cosce con le gambe, **il** ventre, e il casso | le cosce con le gambe **e 'l** ventre e 'l casso | Carlyle |
| XXV 82 | **Così parea** venendo verso l’ epe | **sì pareva**, venendo verso l'epe | Carlyle |
| XXV 149 | Ed era quei che sol, **de**’ tre compagni | ed era quel che sol, **di** tre compagni | Carlyle |
| XXVI 22 | Perchè non corra, che virtù **non** guidi; | perché non corra che virtù **nol** guidi; | dante-corpus |
| XXVI 115 | **De’ vostri** sensi, ch’ è del rimanente, | **d'i nostri** sensi ch'è del rimanente | Carlyle |
| XXVI 126 | Sempre acquistando **del** lato mancino. | sempre acquistando **dal** lato mancino. | dante-corpus |
| XXVII 14 | Dal principio **del fuoco**, in suo linguaggio | dal principio **nel foco**, in suo linguaggio | Carlyle |
| XXVII 39 | Ma palese nessuna or **ven** lasciai. | ma '**n** palese nessuna or **vi** lasciai. | dante-corpus |
| XXVII 109 | Di quel peccato, **ove** mo cader deggio, | di quel peccato **ov' io** mo cader deggio, | dante-corpus |
| XXVII 114 | **Gli** disse: **Nol** portar; non mi far torto. | **li** disse: “**Non** portar: non mi far torto. | Carlyle |
| XXVIII 71 | E **cui già** vidi su in terra Latina, | e **cu' io** vidi su in terra latina, | dante-corpus |
| XXVIII 76 | E fa saper a’ duo miglior **di** Fano, | E fa saper a' due miglior **da** Fano, | Carlyle |
| XXVIII 108 | Che fu **il** mal seme **della** gente Tosca. | che fu mal seme **per la** gente tosca». | Carlyle |
| XXVIII 109 | Ed io **v**’ aggiunsi: E morte di tua schiatta; | E io **li** aggiunsi: «E morte di tua schiatta»; | dante-corpus |
| XXIX 40 | Quando noi fummo **in su** l’ ultima chiostra | Quando noi fummo **sor** l'ultima chiostra | Carlyle |
| XXIX 55 | Giù vêr lo fondo, **dove** la ministra | giù ver' lo fondo, **la 've** la ministra | Carlyle |
| XXIX 75 | Dal capo **ai** piè di schianze maculati: | dal capo **al** piè di schianze macolati; | dante-corpus |
| XXIX 88 | **Dimmi** s’ alcun Latino è tra costoro | **dinne** s'alcun Latino è tra costoro | dante-corpus |
| XXX 47 | Sovra **i quali** io avea l’ occhio tenuto, | sovra **cu**' io avea l'occhio tenuto, | dante-corpus |
| XXX 98 | L’ altro è il falso Sinon Greco **da** Troia: | l'altr' è 'l falso Sinon greco **di** Troia: | Carlyle |
| XXX 121 | **A** te sia rea la sete onde ti crepa, | «**E** te sia rea la sete onde ti crepa», | Carlyle |
| XXX 136 | E’ **quale è quei**, che suo dannaggio sogna, | **Qual** è **colui** che suo dannaggio sogna, | Carlyle |
| XXXI 20 | Che **mi** parve veder molte alte torri; | che **me** parve veder molte alte torri; | Carlyle |
| XXXII 9 | Nè da lingua che chiami mamma **e** babbo. | né da lingua che chiami mamma **o** babbo. | Carlyle |
| XXXIII 39 | Ch’ **erano** meco, e dimandar del pane. | ch'**eran con** meco, e dimandar del pane. | dante-corpus |
| XXXIII 59 | **E quei**, pensando ch’ io **il** fessi per voglia | **ed ei**, pensando ch'io '**l** fessi per voglia | dante-corpus |
| XXXIII 65 | **Quel** dì, e l’ altro stemmo tutti muti: | **lo** dì e l'altro stemmo tutti muti; | dante-corpus |
| XXXIII 91 | Noi passamm’ oltre, **dove** la gelata | Noi passammo oltre, **là 've** la gelata | dante-corpus |
| XXXIII 119 | **Io** son quel **delle frutte** del mal orto, | **i**' son quel **da le frutta** del mal orto, | Carlyle |
| XXXIII 142 | Nel fosso su, diss’ **ei, di** Malebranche, | «Nel fosso sù», diss' **el, «de**' Malebranche, | Carlyle |
| XXXIII 145 | Che questi lasciò **un** Diavolo in sua vece | che questi lasciò **il** diavolo in sua vece | dante-corpus |
| XXXIV 6 | Par **da** lungi un mulin che al vento gira; | par **di** lungi un molin che 'l vento gira, | Carlyle |
| XXXIV 9 | Al Duca mio; chè non **v**’ era altra grotta. | al duca mio, ché non **lì** era altra grotta. | dante-corpus |
| XXXIV 45 | Vengon di là, **ove il** Nilo s’ avvalla. | vegnon di là **onde 'l** Nilo s'avvalla. | dante-corpus |
| XXXIV 93 | Qual **era il** punto ch’ io avea passato. | qual **è quel** punto ch'io avea passato. | dante-corpus |

## Word order

Every line where the same words stand in a different order.

| Line | Carlyle | dante-corpus | Oelsner |
|---|---|---|---|
| I 122 | Anima fia a ciò di me **più** degna: | anima fia a ciò **più** di me degna: | Carlyle |
| II 43 | Se io ho ben la tua **parola** intesa, | «S'i' ho ben la **parola** tua intesa», | Carlyle |
| II 88 | Temer si **deve sol** di quelle cose | Temer si **dee** di **sole** quelle cose | dante-corpus |
| III 74 | Le fa **parer** di trapassar sì pronte, | le fa di trapassar **parer** sì pronte, | Carlyle |
| IV 3 | Come persona che per forza **è** desta: | come persona ch'è per forza desta; | Carlyle |
| VI 6 | E **come** ch’ io mi volga, e **ch**’ io **mi** guati. | e ch'io mi volga, e **come che** io guati. | e ch’ io mi volga, e come ch’ io mi guati. |
| VIII 11 | Già puoi **scorgere** quello che s’ aspetta, | già **scorgere** puoi quello che s'aspetta, | Carlyle |
| VIII 66 | Per ch’ io **avanti intento** l’ occhio sbarro. | per ch'io **avante** l'occhio **intento** sbarro. | Carlyle |
| X 90 | Senza cagion sarei **con gli altri** mosso: | sanza cagion **con li altri** sarei mosso. | Carlyle |
| XI 11 | Sì che s’ ausi **prima** un poco il senso | sì che s'ausi un poco **in prima** il senso | Carlyle |
| XI 94 | Ancora un poco **indietro** ti rivolvi, | Ancora **in dietro** un poco ti rivolvi», | Carlyle |
| XIV 15 | Che da’ piè di Caton già **fu** soppressa. | che **fu** da' piè di Caton già soppressa. | dante-corpus |
| XV 79 | Se fosse pieno **tutto** il mio dimando, | «Se fosse **tutto** pieno il mio dimando», | dante-corpus |
| XV 108 | D’ un medesmo **peccato** al mondo lerci. | d'un **peccato** medesmo al mondo lerci. | dante-corpus |
| XVII 85 | Qual è colui, **ch’ ha** sì presso il ribrezzo | Qual è colui **che** sì presso ha 'l riprezzo | Carlyle |
| XVIII 93 | Che prima l’ altre **avea tutte** ingannate. | che prima **avea tutte** l'altre ingannate. | dante-corpus |
| XVIII 128 | Mi disse, un poco **il viso** più avante, | mi disse, «**il viso** un poco più avante, | dante-corpus |
| XIX 25 | Le piante erano **accese** a tutti intrambe; | Le piante erano a tutti **accese** intrambe; | dante-corpus |
| XIX 57 | La bella Donna, e di **poi** farne strazio? | la bella donna, e **poi** di farne strazio?». | Carlyle |
| XXII 84 | E fe’ lor **sì**, che ciascun se ne loda: | e fé **sì** lor, che ciascun se ne loda. | dante-corpus |
| XXIII 57 | **Potere** indi **partirsi** a tutti tolle. | **poder di partirs**' indi a tutti tolle. | dante-corpus |
| XXV 14 | **Spirto** non vidi in Dio tanto superbo, | non vidi **spirto** in Dio tanto superbo, | dante-corpus |
| XXV 137 | Si fugge **sufolando** per la valle, | **suffolando** si fugge per la valle, | Carlyle |
| XXVIII 135 | Che al Re Giovane **diedi** i mal conforti. | che **diedi** al re giovane i ma' conforti. | che diedi al re giovane mai comforti. |
| XXIX 36 | E in ciò m’ ha fatto **egli** a sè più pio. | e in ciò m'ha **el** fatto a sé più pio». | dante-corpus |
| XXXII 49 | Legno **con** legno spranga mai non cinse | **Con** legno legno spranga mai non cinse | Carlyle |
| XXXII 90 | Sì che, se vivo **fossi**, troppo fora? | sì che, se **fossi** vivo, troppo fora?». | dante-corpus |
| XXXIII 144 | Non era giunto **ancora** Michel Zanche, | non era **ancora** giunto Michel Zanche, | Carlyle |
| XXXIII 155 | Trovai un tal **di voi**, che per sua opra | trovai **di voi** un tal, che per sua opra | Carlyle |

## Inflection

Every line where the same word has a different person, tense, number, or gender (forms of the same inflection, such as *soleano* / *solien*, are under word forms).

| Line | Carlyle | dante-corpus | Oelsner |
|---|---|---|---|
| III 91 | Disse: Per **altre vie**, per altri porti | disse: «Per **altra via**, per altri porti | dante-corpus |
| V 38 | **Eran** dannati i peccator carnali, | **enno** dannati i peccator carnali, | dante-corpus |
| V 64 | Elena **vidi**, per cui tanto reo | Elena **vedi**, per cui tanto reo | dante-corpus |
| V 67 | **Vidi** Paris, Tristano; e più di mille | **Vedi** Parìs, Tristano»; e più di mille | dante-corpus |
| V 80 | **Muovo** la voce: O anime affannate, | **mossi** la voce: «O anime affannate, | dante-corpus |
| VI 47 | Luogo se’ **messa, ed a** sì fatta pena, | loco se' **messo, e hai** sì fatta pena, | Carlyle |
| VI 70 | **Alto** terrà lungo tempo le fronti, | **Alte** terrà lungo tempo le fronti, | Carlyle |
| VI 86 | **Diversa colpa** giù **gli aggrava** al fondo: | **diverse colpe** giù **li grava** al fondo: | Carlyle |
| VII 52 | Ed **egli** a me: **Vani pensieri** aduni: | Ed **elli** a me: «**Vano pensiero** aduni: | Carlyle |
| VIII 57 | Di tal disio **converrà** che tu goda. | di tal disïo **convien** che tu goda». | Carlyle |
| XI 67 | **Ed** io: Maestro, assai **chiaro** procede | **E** io: «Maestro, assai **chiara** procede | Carlyle |
| XII 121 | Poi vidi **genti**, che di fuor del rio | Poi vidi **gente** che di fuor del rio | dante-corpus |
| XIII 4 | Non **frondi verdi**, ma di color fosco; | Non **fronda verde**, ma di color fosco; | Carlyle |
| XIII 10 | Quivi le brutte Arpie lor **nido** fanno, | Quivi le brutte Arpie lor **nidi** fanno, | dante-corpus |
| XIII 25 | **I’ credo** ch’ ei credette ch’ io credesse, | **Cred' ïo** ch'ei credette ch'io credesse | Carlyle |
| XIII 63 | Tanto ch’ io ne perdei lo sonno e **i** polsi. | tanto ch'i' ne perde' li sonni e ' polsi. | Carlyle |
| XIV 68 | Dicendo: **Quel** fu l’ un **de**’ sette regi | dicendo: «**Quei** fu l'un **d'i** sette regi | Carlyle |
| XIV 98 | D’ **acque** e di fronde, che si **chiama** Ida; | d'**acqua** e di fronde, che si **chiamò** Ida; | d’ acque e di fronde, che si chiamò Ida; |
| XV 32 | Se Brunetto **Latini** un poco teco | se Brunetto **Latino** un poco teco | Carlyle |
| XVI 22 | Qual **soleano** i campion far nudi **ed** unti, | Qual **sogliono** i campion far nudi **e** unti, | Carlyle |
| XVI 54 | **Tanto**, che tardi tutta si dispoglia, | **tanta** che tardi tutta si dispoglia, | Carlyle |
| XVI 102 | **Dove dovria** per mille esser **ricetto**; | **ove dovea** per mille esser **recetto**; | ove dovea per mille esser ricetto: |
| XVII 15 | **Dipinte** avea di nodi e di rotelle. | **dipinti** avea di nodi e di rotelle. | Carlyle |
| XVII 63 | **Mostrare** un’ oca bianca più che burro. | **mostrando** un'oca bianca più che burro. | Carlyle |
| XVIII 23 | **Nuovi tormenti** e **nuovi** frustatori, | **novo tormento** e **novi** frustatori, | Carlyle |
| XVIII 84 | E per dolor non par **lagrima** spanda. | e per dolor non par **lagrime** spanda: | Carlyle |
| XVIII 129 | Sì che la faccia ben con **gli occhi** attinghe | sì che la faccia ben con **l'occhio** attinghe | Carlyle |
| XVIII 132 | **Ed** or s’ accoscia, **ed** ora è in **piede** stante. | **e** or s'accoscia **e** ora è in **piedi** stante. | Carlyle |
| XXII 108 | Ch’ **egli** ha **pensato** per gittarsi giuso. | ch'**elli** ha **pensata** per gittarsi giuso!». | ch’ egli ha pensata per gittarsi giuso.” |
| XXIII 19 | Già mi sentia **tutto** arricciar li peli | Già mi sentia **tutti** arricciar li peli | dante-corpus |
| XXIII 34 | Già non **compìo** di tal consiglio rendere, | Già non **compié** di tal consiglio rendere, | dante-corpus |
| XXIII 110 | Ma più non dissi, ch’ **agli occhi** mi corse | ma più non dissi, ch'**a l'occhio** mi corse | dante-corpus |
| XXV 78 | Parea, e tal sen **gìa** con lento passo. | parea; e tal sen **gio** con lento passo. | Carlyle |
| XXV 91 | **Egli il** serpente, e quei lui riguardava: | **Elli 'l** serpente e quei lui riguardava; | Carlyle |
| XXVI 24 | M’ ha dato **il** ben, ch’ io **stesso** nol m’ invidi. | m'ha dato '**l** ben, ch'io **stessi** nol m'invidi. | Carlyle |
| XXVI 135 | Quanto veduta non **n’ aveva** alcuna. | quanto veduta non **avëa** alcuna. | Carlyle |
| XXVII 53 | Così com’ ella **s’ è** tra **il** piano e **il** monte, | così com' ella **sie**' tra '**l** piano e '**l** monte, | così com’ ella sie’ tra il piano e il monte, |
| XXVIII 102 | Curio, ch’ a **dicer** fu così ardito! | Curïo, ch'a **dir** fu così ardito! | dante-corpus |
| XXVIII 107 | Che **dissi**, lasso! Capo ha cosa fatta: | che **disse**, lasso!, “Capo ha cosa fatta”, | Carlyle |
| XXIX 120 | Dannò Minos, a cui **fallir** non lece. | dannò Minòs, a cui **fallar** non lece». | Carlyle |
| XXX 68 | Chè l’ imagine lor **via** più m’ asciuga, | ché l'imagine lor **vie** più m'asciuga | dante-corpus |
| XXX 92 | Che **fuman** come man **bagnata il** verno, | che **fumman** come man **bagnate 'l** verno, | che fuman come man bagnate il verno, |
| XXX 148 | Chè voler ciò udire è **basso** voglia. | ché voler ciò udire è **bassa** voglia». | dante-corpus |
| XXXII 104 | E **tratto** glien avea più d’ una ciocca, | e **tratti** glien' avea più d'una ciocca, | dante-corpus |
| XXXIII 10 | Io non so chi tu **sie**, nè per che modo | Io non so chi tu **se**' né per che modo | dante-corpus |
