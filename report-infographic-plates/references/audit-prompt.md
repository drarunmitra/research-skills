# Audit prompt for a fresh agent

Give the agent this prompt, the plate text files, the PNG or HTML files, the numbers file, the output files the data feed reads, and the report text. Do not give it the generator code or your conclusions.

---

You are auditing a set of infographic plates for a report. Work from the files named below. Do not edit any file except your report.

Files: [plate text folder], [plate PNGs], [numbers.csv], [output files], [report text].

Tasks:

A. Trace. For every number on every plate, find its source in numbers.csv or an output file. Report any number you cannot trace.

B. Geometry. For each bar, dot, area or position, check that its size matches its value (bar widths in proportion, dots at the right place on the scale).

C. Scope words. For every total, say what it includes and leaves out, and compare with the report's definition. A total with no scope is a finding.

D. Wording against the report. Check each sentence on a plate against the report. Check dates, "all" and "none" claims, and any caption that says every item is labelled (count the labels).

E. Status. A drawing that is not data must say "illustrative". A proposal must say "proposal". An item the report marks as unverified must not appear as fact.

F. Labels and credits. A credit or footnote must match what is on the plate (no map credit without a map, no weighting note that fits only some values).

G. Line and shape reading. Could a line be read as a forecast or a link that the data do not support?

H. Style. White page, one token set, no emoji, no em dashes.

Report format: a table with columns id, severity (must fix, should fix, note), plate, what, evidence, fix. Then a short list of what you could not check. Plain English.
