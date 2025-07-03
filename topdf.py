#!/bin/python3
import json
import jq
import sys
import os

pg = jq.compile(open("./filter.jq").read())

doctors = json.loads(pg.input_value(json.loads(sys.stdin.read())).text())

document = ["""
\\documentclass[a4paper, 10pt]{{article}}
\\usepackage[a4paper, margin=2cm]{{geometry}}
\\usepackage[ngerman]{{babel}}
\\usepackage{{hyperref}}
\\title{{{0}}}
\\author{{\\url{{https://github.com/MaidLucy/arztsuche-cleaner}}}}
\\date{{Stand: \\today}}
\\setcounter{{secnumdepth}}{{0}}

\\begin{{document}}
\\maketitle
\\pagebreak
""".format(
    str(len(doctors)) + ' ' +
    sys.argv[1]
    )]

for doctor in doctors:
    document.append("""
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
        document.append("""    \\begin{minipage}{6cm}
    \\textbf{Anrufzeiten}\\\\

        """)
    for anrufzeit in doctor["anrufzeiten"]:
        document.append("""        \\makebox[2cm][l]{{{0} {1}:}} {2}\\
        """.format(
            anrufzeit["tag"],
            anrufzeit["datum"],
            ", ".join(map(lambda z: z["zeit"], anrufzeit["sprechzeiten"]))
            ))

    if len(doctor["anrufzeiten"]) > 0:
        document.append("    \\end{minipage}")

document.append("\\end{document}")

with open("./output/arztsuche.tex", 'w') as f:
    f.write('\n'.join(document))

os.chdir('./output/')
os.system('pdflatex arztsuche.tex')
