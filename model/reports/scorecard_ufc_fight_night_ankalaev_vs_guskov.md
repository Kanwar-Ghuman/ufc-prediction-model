# Scorecard — UFC Fight Night: Ankalaev vs. Guskov (2026-07-25)

8 of 12 winners called correctly (67%). Graded against ufcstats results.

Probabilities are the frozen ones saved when the card was predicted.

| fight | pick | P(pick) | actual | winner | method | round |
|---|---|---|---|---|---|---|
| Magomed Ankalaev vs. Bogdan Guskov | Magomed Ankalaev | 65% | Magomed Ankalaev, KO/TKO R5 | ✓ | hit | said R1 |
| Steve Erceg vs. Ramazan Temirov | Steve Erceg | 60% | Ramazan Temirov, KO/TKO R1 | ✗ | said dec | hit |
| Magomed Zaynukov vs. Damian Rzepecki | Damian Rzepecki | 53% *(no call)* | Magomed Zaynukov, U-DEC | ✗ | hit | — |
| Rizvan Kuniev vs. Tyrell Fortune | Rizvan Kuniev | 58% | Rizvan Kuniev, KO/TKO R3 | ✓ | hit | said R1 |
| Abubakar Vagaev vs. Saygid Izagakhmaev | Saygid Izagakhmaev | 58% | Abubakar Vagaev, U-DEC | ✗ | hit | — |
| Valter Walker vs. Thomas Petersen | Valter Walker | 63% | Valter Walker, SUB R1 | ✓ | said ko | hit |
| Dustin Jacoby vs. Muhammad Saidov | Dustin Jacoby | 72% | Muhammad Saidov, KO/TKO R2 | ✗ | hit | said R1 |
| Santiago Ponzinibbio vs. Sam Patterson | Sam Patterson | 70% | Sam Patterson, KO/TKO R2 | ✓ | hit | said R1 |
| Ismael Bonfim vs. Axel Sola | Axel Sola | 51% *(no call)* | Axel Sola, SUB R1 | ✓ | said dec | hit |
| Magomed Tuchalov vs. Brendson Ribeiro | Magomed Tuchalov | 56% | Magomed Tuchalov, U-DEC | ✓ | said ko | — |
| Nurullo Aliev vs. Mike Davis | Nurullo Aliev | 61% | Nurullo Aliev, U-DEC | ✓ | hit | — |
| Cody Gibson vs. Abdul Hussein | Abdul Hussein | 53% *(no call)* | Abdul Hussein, SUB R3 | ✓ | said ko | said R1 |
| Islam Dulatov vs. Wellington Turman | — | — | did not take place | — | — | — |

## Aggregates

| metric | model | no-skill reference |
|---|---|---|
| winners correct | 8/12 (67%) | 6.0/12 (50%) |
| winners correct, excluding no-calls | 6/9 (67%) | 4.5/9 (50%) |
| log loss (winner) | 0.6659 | 0.6931 |
| Brier (winner) | 0.2358 | 0.2500 |
| method called (KO/sub/dec) | 7/12 (58%) | — |
| round called, given fighter + method | 3/8 | — |
| mean P(exact outcome) | 0.110 | 0.109 (base rate) |

The last row is the honest summary of the whole 'how does it end' machinery: across fighter x method x round, how much probability did the model put on the thing that actually happened, against a coin flip times the historical method and round mix.