#!/bin/python3
import json

doctors = json.load(open("/tmp/psychiater.json"))

print("""
\\documentclass[a4paper, 10pt]{{article}}
\\usepackage[a4paper, margin=2cm]{{geometry}}
\\usepackage[ngerman]{{babel}}
\\usepackage{{hyperref}}
\\title{{{0} Psychiater:innen in Regensburg (25km Umkreis) gefunden}}
\\author{{arztsuche-cleaner}}
\\date{{Stand: \\today}}
\\setcounter{{secnumdepth}}{{0}}

\\begin{{document}}
\\maketitle
\\pagebreak
""".format(
    len(doctors)
    ))

for doctor in doctors:
    print("""
    \\section{{{0}}}

    \\begin{{minipage}}{{8cm}}
    \\makebox[1.75cm][l]{{Name:}}    {1} {0}\\\\
    \\makebox[1.75cm][l]{{Adresse:}} {2} {3}\\\\
    \\makebox[1.75cm][l]{{ \\ }}     {4} {5}\\\\
    \\makebox[1.75cm][l]{{Telefon:}} \\texttt{{{6}}}\\\\
    \\makebox[1.75cm][l]{{Handy:}}   \\texttt{{{7}}}\\\\
    \\makebox[1.75cm][l]{{E-Mail:}}  \\href{{mailto:{8}}}{{{8}}}\\\\
    \\makebox[1.75cm][l]{{Web:}}     \\url{{{9}}}\\\\

    \\end{{minipage}}"""
    .format(
        doctor["name"],
        doctor["anrede"],
        doctor["strasse"],
        doctor["hausnummer"],
        doctor["plz"],
        doctor["ort"],
        doctor["telefon"],
        doctor["handy"],
        doctor["email"],
        doctor["web"],
        ))

    if len(doctor["anrufzeiten"]) > 0:
        print("""    \\begin{minipage}{6cm}
    \\textbf{Anrufzeiten}\\\\

        """)
    for anrufzeit in doctor["anrufzeiten"]:
        print("""        \\makebox[2cm][l]{{{0} {1}:}} {2}\\
        """.format(
            anrufzeit["tag"],
            anrufzeit["datum"],
            ", ".join(map(lambda z: z["zeit"], anrufzeit["sprechzeiten"]))
            ))

    if len(doctor["anrufzeiten"]) > 0:
        print("    \\end{minipage}")

print("\\end{document}")
