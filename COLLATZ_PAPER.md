# Binary structure, 2-adic descent, and empirical predictors of Collatz trajectories

This document is the consolidated research orientation for the experiments in
this repository. It is deliberately not a proof claim. The standard Collatz
conjecture remains open; exact statements below are limited to the explicitly
proved identities, while all broader relationships are empirical hypotheses.

## Scope and contributions

The project combines four layers:

1. exact binary families and their deterministic paths;
2. canonical trajectory measurements;
3. controlled comparisons of binary features and stopping-time behaviour;
4. visual and generalized-map experiments treated as exploratory controls.

The canonical implementation is `/home/runner/work/MaffStuff/MaffStuff/collatz_core.py`.
It defines one step-count convention, one bounded-run convention, exact
secondary-harbor membership, and machine-readable feature rows. The command
line interface is `/home/runner/work/MaffStuff/MaffStuff/collatz_research.py`.

## Exact mathematical component

For `k >= 2`, define

\[
L_k = \frac{2^{2k}-1}{3}.
\]

Then `3 L_k + 1 = 2^(2k)`, and the binary representation of `L_k` is
`101...101` with `k` ones. Under the canonical conventions:

- first power-of-two hit: step `1`;
- total stopping time: `2k + 1`;
- number of visited values: `2k + 2`.

The algebraic extension `L_1=1` is retained by the implementation as the
degenerate endpoint, with stopping time zero and one visited value.

For an odd positive integer `m`, the exact secondary set is

\[
S(m)=\{2^a m:a\geq0\}.
\]

Membership is tested by removing all factors of two, not by enumerating a
finite approximation.

## Canonical measurements

For a starting value `n`, the engine records:

- total stopping time, only when `1` is reached;
- first power-of-two step and value;
- first step whose value is below `n`;
- maximum value;
- odd and even transition counts;
- termination reason (`reached_one`, `cycle_detected`, or `max_steps`);
- `v2(n)`, binary run statistics, pattern flags, and digit entropy.

`steps` counts transitions. `sequence_length` counts values, so the latter is
always one larger for a completed run.

## Experiment inventory and paper placement

| Area | Existing sources | Paper treatment |
| --- | --- | --- |
| Foundational harbor framework | `collatz.md`, `collatz_ref.md`, `collatz_v2.md`, `collatz_p2_zeroes.md` | Consolidated definitions and exact identities |
| Baseline trajectories | `collatz.py`, `collatz101.py`, `collatzmeansteps.py`, `collatz_3ntop.py`, `collatz_lprime.py` | Re-run through the canonical engine |
| Mersenne and near-Mersenne | `collatz_mersenne*.py`, `collatzadjacentmersenne.py`, `collatzbitlimit.py`, `collatznearmisses.py` | Falsification study against equal-bit-length cohorts |
| Binary and 2-adic features | `collatz_many1s.py`, `collatzbinary*.py`, `collatz*zeroes.py`, `collatz_weight*.py` | Main empirical feature section |
| Entropy and bases | `collatz_*entropy*.py`, `collatz_base4_*.py`, `collatz_maximal_numbers.py` | Standardize definitions before comparing |
| P/M/L geometry | `collatz_binary_distance.py`, `collatz_triangles.py`, `collatz_ternary_many1smap.py` | Visualization and predictive appendix |
| Generalized maps | `collatz_mersennetansforms*.py`, `collatz_parallel_universe.py` | Control experiments only |
| Interactive visualizations | `OLD_Collatz.py`, `3dfractalv5.py`, `collatz_GPU.py`, `collatzvisual.py`, `collatz_game_of_life.js` | Supplementary material |
| Prime products and chains | `collatzprimepatterns.py` and Markdown references | Future controlled study |

## Proposed paper structure

1. Introduction and scope
2. Definitions and measurement conventions
3. Exact binary families
4. Experimental design and reproducibility
5. Binary and 2-adic observables
6. Mersenne and near-Mersenne comparisons
7. Entropy and base-representation predictors
8. P/M/L visualization
9. Generalized-map controls
10. Limitations and failed hypotheses
11. Conclusion
12. Appendices with algorithms, data, figures, and source inventory

## Claims policy

The paper must label each result as one of:

- **Exact identity:** algebraically or mechanically verified for all permitted
  parameters.
- **Finite computational result:** true for a stated exhaustive range.
- **Empirical association:** a measured relationship requiring replication.
- **Open hypothesis:** not established by the repository.

In particular, “Mersenne numbers are maximum resistance,” “40 is an
attractor,” entropy correlations, and P/M/L geometry are hypotheses or
visual interpretations, not conclusions.

## Reproducible commands

From the repository root:

```text
python -m unittest -v
python collatz_research.py single 85
python collatz_research.py l-family 32 results/l_family.csv
python collatz_research.py cohort 12 results/cohort_12bit.csv
```

The cohort command is exhaustive over all values with the requested bit
length. The output is CSV or JSON based on its filename suffix, and contains
the source value, canonical metrics, and standardized binary/base features.

## Subagent work packages

1. Audit all legacy scripts for duplicate logic, undefined names, import-time
   execution, and arbitrary stopping limits.
2. Re-run all baseline experiments through `collatz_core.py`.
3. Exhaustively test Mersenne values against every equal-bit-length cohort.
4. Quantify trailing-zero, run-length, and alternating-pattern associations with
   confidence intervals and bit-length controls.
5. Standardize base entropy and compare it against simpler binary predictors.
6. Audit P/M/L definitions as features, without calling them metrics unless
   their mathematical properties are established.
7. Re-run generalized maps with explicit recurrence and growth conventions.
8. Produce tables, figures, limitations, and a provenance record from the
   generated CSV/JSON files.
