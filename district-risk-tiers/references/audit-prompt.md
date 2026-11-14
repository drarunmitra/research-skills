# Audit prompt for a fresh agent

Give the agent this prompt, the rule file, the input files, and the tier output files. Do not give it the project code or your conclusions.

---

You are auditing a set of risk tiers. Work only from the written rule and the input files named below. Do not read the project code. Do not edit any file except your report.

Files: [rule file], [input files], [tier output files], [document text, if claims are to be checked].

Tasks:

A. Rebuild. From the rule and the inputs only, rebuild the scores, the tiers, the stability under each what-if run, and the headline counts. For each check, report MATCH or DIFFERENT, with the numbers. List every unit whose tier differs.

B. Sub-areas. If the rule has sub-areas, rebuild their tiers from the parent values and report the same way.

C. Spot checks. Pick five units at random. Trace each input back to the raw file and report whether the value is correct.

D. Rule gaps. List every place where the rule is silent or unclear. Check these in particular: how ties break (count tied scores at each cut), the direction of every input, what happens to a missing input, whether each what-if run is described well enough to rebuild, and whether the code's runs match the rule's runs.

E. Claims. If a document is given, list each claim about the tiers (counts, names, "consistent" labels, "hazard" or "risk" wording, "children and mothers") and say whether the files support it. Check that a map labelled hazard is built from hazard scores and not risk tiers.

F. Coverage. For each group the document names, say whether the vulnerability score has an indicator for it.

Report format: a table of findings with columns id, severity (must fix, should fix, note), where, what, evidence, fix. Then a short list of what you could not check. Plain English. No em dashes.
