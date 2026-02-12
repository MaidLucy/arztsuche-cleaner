#!/bin/python3
import json
import jq
import sys
import os
import datetime

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
    \\subsection{{{11}}}

    \\begin{{minipage}}{{8cm}}
    \\makebox[1.85cm][l]{{Name:}}    {1} {0}\\\\
    \\makebox[1.85cm][l]{{Entfernung:}}    {2} km\\\\
    \\makebox[1.85cm][l]{{Adresse:}} {3} {4}\\\\
    \\makebox[1.85cm][l]{{ \\ }}     {5} {6}\\\\
    \\makebox[1.85cm][l]{{Telefon:}} \\texttt{{{7}}}\\\\
    \\makebox[1.85cm][l]{{Handy:}}   \\texttt{{{8}}}\\\\
    \\makebox[1.85cm][l]{{E-Mail:}}  \\href{{mailto:{{9}}}}{{{9}}}\\\\
    \\makebox[1.85cm][l]{{Web:}}     \\url{{{10}}}\\\\

    \\end{{minipage}}"""
    .format(
        doctor["name"],
        doctor["anrede"],
        format(int(doctor["entfernung"])/1000, '.3f'),
        doctor["strasse"],
        doctor["hausnummer"],
        doctor["plz"],
        doctor["ort"],
        doctor["telefon"],
        doctor["handy"],
        doctor["email"],
        doctor["web"],
        doctor["ag"],
        ))

    if len(doctor["anrufzeiten"]) > 0:
        document.append("""    \\begin{minipage}{8cm}
    \\textbf{Anrufzeiten}\\\\

        """)
    for anrufzeit in doctor["anrufzeiten"]:
        document.append("""        \\makebox[3cm][l]{{{0} {1}:}} {2}\\
        """.format(
            datetime.datetime.strptime(anrufzeit["datum"], "%Y-%m-%d").date()
                .strftime("%a"),
            anrufzeit["datum"],
            ", ".join(map(lambda z: z["z"], anrufzeit["sprechzeiten"]))
            ))

    if len(doctor["anrufzeiten"]) > 0:
        document.append("    \\end{minipage}")

document.append("\\end{document}")

with open("./output/arztsuche.tex", 'w') as f:
    f.write('\n'.join(document))

os.chdir('./output/')
os.system('pdflatex arztsuche.tex')
