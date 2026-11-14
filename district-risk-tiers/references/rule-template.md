# Tier rule (fixed before any tier result was seen)

Written: [date]. Approved by: [name or role]. Anything marked "my call" is the assistant's choice and can be changed. A change after results are seen is a deviation and goes in the log at the end.

## 1. Purpose and units
- Unit of analysis: [district / block / mandal]. Number of units: [n].
- Groups the document names: [children, mothers, ...].
- Use of the tiers: [what decisions they feed]. They are a relative screen, not a forecast, and not tested against outcomes [change if tested].

## 2. Scores (percentile ranks across the units, 0 = lowest concern, 1 = highest)
- Hazard [name]: mean of the ranks of [inputs, data source, period, direction]. Repeat for each hazard.
- Vulnerability: mean of the ranks of [inputs, source, year]. Direction of each. [my call] for any indicator the user did not choose.
- Missing vulnerability input: unit is "Data too thin" for every tier that uses it.
- Not in the score: [exposure, malaria, anything left out, and why].

## 3. Risk and tiers
- Risk for each hazard: H^w x V^(1 - w), w = [0.5]. [my call: both must be high.]
- Overall risk: mean of the hazard risks.
- Tier cut: [top third High, middle third Moderate, last third Low] or [fixed thresholds and their source].
- Tie rule: [higher score, then higher stability, then name]. Ties at a cut are listed in the audit.

## 4. What-if runs
List each run, what it changes, and why it differs in kind.
1. [run name]: [change].
2. ...
Stability = share of runs in which a unit keeps its base overall tier. Label "consistent" if at least [0.75], else "less certain". Stability is a check against these runs. It is not a confidence interval.

## 5. Coverage check
Groups named in section 1 against indicators in section 2. See coverage-check.md. Gaps: [list, and what was done].

## 6. Sub-areas (if any)
Sub-areas take the parent vulnerability on the same 0 to 1 scale. Their tiers are provisional. Flags: [shared grid cells, boundary mismatches].

## 7. Limits to print wherever tiers appear
[Provisional data, survey rounds mixed, ranks ignore sampling error, no outcome test, ...]

## 8. Deviation log
| Date | What changed | Why | Result moved |
|---|---|---|---|

## 9. Notes after the audit
[Rule gaps found, fixes, date.]
