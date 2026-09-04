# Scorecard — UFC Fight Night: Medić vs. Rodriguez (2026-08-01)

11 of 14 winners called correctly (79%). Graded against ufcstats results.

Probabilities are the frozen ones saved when the card was predicted.

| fight | pick | P(pick) | actual | winner | method | round |
|---|---|---|---|---|---|---|
| Uros Medic vs. Daniel Rodriguez | Uros Medic | 78% | Uros Medic, KO/TKO R1 | ✓ | hit | hit |
| Jan Blachowicz vs. Navajo Stirling | Navajo Stirling | 67% | Navajo Stirling, KO/TKO R1 | ✓ | hit | hit |
| Aleksandar Rakic vs. Marcin Tybura | Aleksandar Rakic | 78% | Aleksandar Rakic, U-DEC | ✓ | said ko | — |
| Dusko Todorovic vs. Robert Valentin | Robert Valentin | 61% | Robert Valentin, SUB R1 | ✓ | said dec | hit |
| Vlasto Čepo vs. Gilbert Urbina | Vlasto Čepo | 75% | Gilbert Urbina, KO/TKO R1 | ✗ | hit | hit |
| Noah Gugnon vs. Miloš Janičić | Miloš Janičić | 52% *(no call)* | Noah Gugnon, SUB R1 | ✗ | said ko | hit |
| Ludovit Klein vs. Tofiq Musayev | Ludovit Klein | 71% | Tofiq Musayev, KO/TKO R2 | ✗ | said dec | said R1 |
| Oban Elliott vs. Michael Oliveira | Michael Oliveira | 73% | Michael Oliveira, KO/TKO R1 | ✓ | said dec | hit |
| Borislav Nikolić vs. Mark Vologdin | Borislav Nikolić | 51% *(no call)* | Borislav Nikolic, U-DEC | ✓ | hit | — |
| Dennis Buzukja vs. Bogdan Grad | Bogdan Grad | 71% | Bogdan Grad, SUB R2 | ✓ | said dec | said R1 |
| Mateusz Rebecki vs. Kyle Prepolec | Mateusz Rebecki | 83% | Mateusz Rebecki, KO/TKO R1 | ✓ | said dec | hit |
| Nina Nikolija Milošević vs. Hailey Cowan | Nina Nikolija Milošević | 76% | Nina Milosevic, KO/TKO R1 | ✓ | said dec | hit |
| Jovan Leka vs. Alexander Poppeck | Jovan Leka | 64% | Jovan Leka, KO/TKO R1 | ✓ | hit | hit |
| Stephanie Luciano vs. Marina Spasić | Stephanie Luciano | 74% | Stephanie Luciano, SUB R1 | ✓ | said dec | hit |

## Aggregates

| metric | model | no-skill reference |
|---|---|---|
| winners correct | 11/14 (79%) | 7.0/14 (50%) |
| winners correct, excluding no-calls | 10/12 (83%) | 6.0/12 (50%) |
| log loss (winner) | 0.5200 | 0.6931 |
| Brier (winner) | 0.1695 | 0.2500 |
| method called (KO/sub/dec) | 5/14 (36%) | — |
| round called, given fighter + method | 10/12 | — |
| mean P(exact outcome) | 0.130 | 0.095 (base rate) |

The last row is the honest summary of the whole 'how does it end' machinery: across fighter x method x round, how much probability did the model put on the thing that actually happened, against a coin flip times the historical method and round mix.