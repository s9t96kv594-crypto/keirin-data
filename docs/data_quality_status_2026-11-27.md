# Keirin data quality status (2026-11-27)

## Scope audited

The read-only audit covered 59 monthly CSV files in `keirin_data/`, totaling 936,309 rider rows and 132,290 race IDs summed across monthly files.

- CSV row widths: no malformed rows found.
- Duplicate race/rider keys within individual monthly files: none found.
- Prefecture field split: 850,487 rows can be repaired deterministically by combining the final one-character token in `player_name` with `pref`, but only when the result exactly matches one of Japan's 47 prefectures.
- Unrepairable prefecture anomalies: 105 rows. These remain unchanged and should be excluded from features that depend on prefecture/line membership until reviewed.

The original monthly CSVs are not modified. `scripts/data_cleaning.py` applies only exact-match repairs in memory before prediction features are built.

## Result completeness

| Period | Rider rows | Rank-populated rows | Rank coverage |
|---|---:|---:|---:|
| 2022-2025 | 774,796 | 773,404 | 99.82% |
| 2026 | 161,513 | 93,102 | 57.64% |

Recent 2026 files are particularly incomplete:

- 2026-09: 1.1% of rows have rank values.
- 2026-10: 0.0%.
- 2026-11 through Nov 27: 0.2%.

These files must not be treated as completed historical results. The prediction pipeline now marks blank result fields as missing (not losses) and trains only on races where every listed rider has a nonblank result field.

## Odds limitation

The monthly CSVs contain result payouts (for example, the winning 3連単 payout), not historical pre-race odds snapshots. Therefore, a full historical ROI/EV backtest cannot be honestly calculated from these files alone. Use them for outcome/rider modeling only; use odds snapshots collected before each future race for live EV decisions and prospective paper-trading ROI.

## Validation

The audit workflow runs:
1. Unit tests for player identity parsing and prefecture repair.
2. Python syntax compilation for modified scripts.
3. Structural and completeness audit of monthly CSVs.

The 2026-11-27 run completed successfully. The detailed JSON report is retained as a GitHub Actions artifact for 30 days.
