# Scorecard — Noche UFC: Silva vs. Delgado (2026-09-12)

8 of 12 winners called correctly (67%). Graded against ufcstats results.

Probabilities are the frozen ones saved when the card was predicted.

| fight | pick | P(pick) | actual | winner | method | round |
|---|---|---|---|---|---|---|
| Jean Silva vs. Jose Delgado | Jean Silva | 50% *(no call)* | Jean Silva, SUB R3 | ✓ | said ko | said R1 |
| Brandon Moreno vs. Joseph Morales | Brandon Moreno | 64% | Brandon Moreno, S-DEC | ✓ | hit | — |
| Tommy McMillen vs. Marwan Rahiki | Tommy McMillen | 64% | Tommy McMillen, U-DEC | ✓ | said ko | — |
| Manon Fiorot vs. Alexa Grasso | Manon Fiorot | 63% | Alexa Grasso, U-DEC | ✗ | hit | — |
| Waldo Cortes Acosta vs. Curtis Blaydes | Waldo Cortes Acosta | 60% | Curtis Blaydes, U-DEC | ✗ | said ko | — |
| David Martinez vs. Dan Ige | David Martinez | 82% | David Martinez, U-DEC | ✓ | hit | — |
| Tim Elliott vs. Edgar Chairez | Edgar Chairez | 64% | Tim Elliott, U-DEC | ✗ | hit | — |
| Ignacio Bahamondes vs. Muslim Salikhov | Ignacio Bahamondes | 67% | Ignacio Bahamondes, U-DEC | ✓ | said ko | — |
| Yousri Belgaroui vs. Djorden Santos | Yousri Belgaroui | 72% | Yousri Belgaroui, KO/TKO R1 | ✓ | said dec | hit |
| Drakkar Klose vs. Tommy Gantt | Tommy Gantt | 77% | Tommy Gantt, SUB R3 | ✓ | said dec | said R1 |
| Rafa Garcia vs. Rongzhu | Rafa Garcia | 69% | Rongzhu, U-DEC | ✗ | hit | — |
| JJ Aldrich vs. Regina Tarin | Regina Tarin | 63% | Regina Tarin, U-DEC | ✓ | hit | — |
| Jessie Rosas vs. Sean King | — | — | did not take place | — | — | — |

## Aggregates

| metric | model | no-skill reference |
|---|---|---|
| winners correct | 8/12 (67%) | 6.0/12 (50%) |
| winners correct, excluding no-calls | 7/11 (64%) | 5.5/11 (50%) |
| log loss (winner) | 0.6105 | 0.6931 |
| Brier (winner) | 0.2129 | 0.2500 |
| method called (KO/sub/dec) | 6/12 (50%) | — |
| round called, given fighter + method | 1/3 | — |
| mean P(exact outcome) | 0.229 | 0.191 (base rate) |

P(exact outcome) is the probability assigned to the fighter × method × round that actually happened, vs a coin flip times the historical mix.