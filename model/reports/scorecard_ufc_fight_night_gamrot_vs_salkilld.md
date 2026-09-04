# Scorecard — UFC Fight Night: Gamrot vs. Salkilld (2026-08-08)

10 of 12 winners called correctly (83%). Graded against ufcstats results.

Probabilities are the frozen ones saved when the card was predicted.

| fight | pick | P(pick) | actual | winner | method | round |
|---|---|---|---|---|---|---|
| Mateusz Gamrot vs. Quillan Salkilld | Quillan Salkilld | 59% | Quillan Salkilld, SUB R1 | ✓ | said ko | hit |
| Billy Quarantillo vs. Diego Ferreira | Diego Ferreira | 69% | Diego Ferreira, U-DEC | ✓ | said ko | — |
| Darren Elkins vs. Yadier del Valle | Yadier del Valle | 79% | Yadier del Valle, KO/TKO R1 | ✓ | hit | hit |
| Amanda Lemos vs. Alexia Thainara | Alexia Thainara | 76% | Alexia Thainara, U-DEC | ✓ | hit | — |
| Ty Miller vs. Billy Ray Goff | Ty Miller | 80% | Ty Miller, KO/TKO R3 | ✓ | hit | said R1 |
| Steven Asplund vs. Guilherme Pat | Steven Asplund | 58% | Steven Asplund, U-DEC | ✓ | said ko | — |
| Diyar Nurgozhay vs. Bruno Lopes | Bruno Lopes | 57% | Diyar Nurgozhay, KO/TKO R1 | ✗ | hit | hit |
| José Luiz Montanha vs. Louie Sutherland | Louie Sutherland | 63% | Jose Montanha, SUB R1 | ✗ | said ko | hit |
| Manoel Sousa vs. Richie Miranda | Manoel Sousa | 82% | Manoel Sousa, U-DEC | ✓ | said ko | — |
| Miles Johns vs. Gianni Vazquez | Miles Johns | 62% | Miles Johns, KO/TKO R1 | ✓ | said dec | hit |
| Juliana Miller vs. Ravena Oliveira | Juliana Miller | 63% | Juliana Miller, SUB R2 | ✓ | said dec | said R1 |
| Giovanna Canuto vs. Carol Foro | Carol Foro | 68% | Carol Foro, U-DEC | ✓ | said ko | — |

## Aggregates

| metric | model | no-skill reference |
|---|---|---|
| winners correct | 10/12 (83%) | 6.0/12 (50%) |
| winners correct, excluding no-calls | 10/12 (83%) | 6.0/12 (50%) |
| log loss (winner) | 0.4637 | 0.6931 |
| Brier (winner) | 0.1443 | 0.2500 |
| method called (KO/sub/dec) | 4/12 (33%) | — |
| round called, given fighter + method | 5/7 | — |
| mean P(exact outcome) | 0.174 | 0.133 (base rate) |

The last row is the honest summary of the whole 'how does it end' machinery: across fighter x method x round, how much probability did the model put on the thing that actually happened, against a coin flip times the historical method and round mix.