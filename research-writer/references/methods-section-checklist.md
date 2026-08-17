# Methods section: conventions checklist

Source: MRU Workshop on Manuscript Preparation and Research Communication, Day 1 "Materials and Methods" (Dr Arun Mitra, AIIMS Bibinagar; github.com/drarunmitra/MRU_Workshop_Methods). Use alongside the main skill patterns 5-6.

## The ICMJE three-drawer structure
Organise every Methods section into three drawers. Content that fits none of them probably belongs in Results.
1. **Participants**: selection criteria, eligibility, source population.
2. **Data and measurements**: variables, tools, procedures.
3. **Statistics**: tests, models, software.

## Two framing tests for reproducibility
- "Write as if explaining it to yourself, two years from now, at a different hospital or lab with no access to your files."
- "Write your Methods so a stranger could reproduce your study without frustration."
The Methods serve three readers: replicators (reproduce exactly), systematic reviewers (assess risk of bias), and future-you. Transparent methods signal credibility, not just compliance.

## Universal elements (every study)
- Study design, explicitly named (never unnamed, never invent a novel design).
- Setting: place, level of care, timeframe.
- Ethics: IEC approval number + date, consent status, registration.
- Eligibility criteria with specific cut-offs.
- Sample size with stated assumptions (never unjustified).
- Named variables and validated measurement tools.
- Statistical tests, models, and effect measures.
- Software identified with version numbers.

## Writing principles
- Past tense ("samples were analysed"). Describe procedures in the order Results will report them. Each procedure paragraph: purpose first, then methodology. Follow journal convention on passive vs active voice.
- Write Methods before/while conducting the research, fresh, without copying grant or protocol language.

## Include vs exclude
- **Include:** reagent concentrations with kit/catalogue and lot numbers; instrument settings and calibration; protocol deviations; software names and versions; eligibility/exclusion specifics.
- **Exclude:** trivial procedural detail ("a blue 500 ml beaker"); step-by-step redescription of standard methods (cite the method instead); results/numbers; subjective critiques of alternative methods.

## Statistical methods description
Never "data were analysed using appropriate tests". Name each test, specify multivariable models with their adjusted variables, report effect measures with CIs, state the significance threshold, give software + version. Example: "chi-square for categorical and t-test for continuous variables; multivariable logistic regression adjusted for age, sex, and SES, reporting adjusted ORs with 95% CIs (R 4.3.1)."

## Design-specific emphases
- **Cross-sectional:** sampling scheme as the headline; size from prevalence + precision + design effect.
- **Case-control:** controls from the same source population; specify matching variables and ratio; blinded ascertainment.
- **Cohort:** follow-up duration, schedule, attrition rates with reasons, censoring.
- **Diagnostic:** index test read blind to the reference standard; pre-specified cut-offs; consecutive suspected patients.
- **RCT:** sequence generation, allocation concealment, implementation; blinding of participants, providers, assessors, and analysts.

## Reporting guidelines (match to design)
STROBE (observational), CONSORT (trials), STARD (diagnostic accuracy), TIDieR (intervention description). Following the design-matched checklist pre-empts the reviewer's critique.

## Ethics and registration (India-specific)
- IEC approval mandatory; the committee must be CDSCO-registered. State the approval number and date.
- CTRI registration: prospectively mandatory for trials; voluntary for observational studies.
- Follow ICMR National Ethical Guidelines 2017.
- Address ICMR Data Protection and Privacy requirements and the ICMR Health Data Management Guidelines.
- Document informed-consent procedures (or the waiver and its basis for secondary/routine-data analyses).

## Common mistakes
Unnamed/invented design; unjustified sample size; ethics compressed to one line; hidden attrition or losses; undefined control intervention; missing software versions or instrument specifications.
