# Scorecard — UFC Fight Night: Hernandez vs. Rodrigues (2026-08-22)

9 of 13 winners called correctly (69%). Graded against ufcstats results.

Probabilities are the frozen ones saved when the card was predicted.

| fight | pick | P(pick) | actual | winner | method | round |
|---|---|---|---|---|---|---|
| Anthony Hernandez vs. Gregory Rodrigues | Anthony Hernandez | 70% | Gregory Rodrigues, U-DEC | ✗ | said ko | — |
| Serghei Spivac vs. Vitor Petrino | Vitor Petrino | 64% | Vitor Petrino, U-DEC | ✓ | said ko | — |
| Reinier de Ridder vs. Roman Dolidze | Reinier de Ridder | 81% | Reinier de Ridder, KO/TKO R1 | ✓ | said dec | hit |
| MarQuel Mederos vs. Mason Jones | Mason Jones | 76% | MarQuel Mederos, KO/TKO R2 | ✗ | said dec | said R1 |
| Carli Judice vs. Jeisla Chaves | Carli Judice | 84% | Carli Judice, KO/TKO R1 | ✓ | said dec | hit |
| Anthony Wint vs. Terrance Chatman | Anthony Wint | 89% | Anthony Wint, SUB R1 | ✓ | said ko | hit |
| Jamall Emmers vs. Lerryan Douglas | Lerryan Douglas | 78% | Jamall Emmers, KO/TKO R1 | ✗ | hit | hit |
| Shamil Gaziev vs. Kennedy Nzechukwu | Shamil Gaziev | 54% *(no call)* | Shamil Gaziev, KO/TKO R1 | ✓ | hit | hit |
| Nasrat Haqparast vs. Chris Padilla | Chris Padilla | 52% *(no call)* | Chris Padilla, SUB R3 | ✓ | said dec | said R1 |
| Marcio Barbosa vs. Ryan Kuse | Marcio Barbosa | 87% | Marcio Barbosa, KO/TKO R1 | ✓ | hit | hit |
| Gauge Young vs. Stan Dorsainvil | Gauge Young | 60% | Stan Dorsainvil, U-DEC | ✗ | hit | — |
| Jackson McVey vs. Wes Schultz | Jackson McVey | 63% | Jackson McVey, KO/TKO R1 | ✓ | said sub | hit |
| Shanelle Dyer vs. Elise Reed | Shanelle Dyer | 90% | Shanelle Dyer, KO/TKO R3 | ✓ | said dec | said R1 |

## Aggregates

| metric | model | no-skill reference |
|---|---|---|
| winners correct | 9/13 (69%) | 6.5/13 (50%) |
| winners correct, excluding no-calls | 7/11 (64%) | 5.5/11 (50%) |
| log loss (winner) | 0.6149 | 0.6931 |
| Brier (winner) | 0.2190 | 0.2500 |
| method called (KO/sub/dec) | 4/13 (31%) | — |
| round called, given fighter + method | 7/10 | — |
| mean P(exact outcome) | 0.122 | 0.103 (base rate) |

The last row is the honest summary of the whole 'how does it end' machinery: across fighter x method x round, how much probability did the model put on the thing that actually happened, against a coin flip times the historical method and round mix.