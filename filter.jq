.arztPraxisDatas | map( . | {
    anrede: .anrede, 
    name: .name, 
    strasse: .strasse, 
    hausnummer: .hausnummer, 
    plz: .plz, 
    ort: .ort, 
    entfernung: .distance,
    telefon: .tel, 
    handy: .handy, 
    email: .email, 
    ag: (.ag[0] | .value),
    web: .web, 
    anrufzeiten: (.tsz | 
        map( . | 
            select( 
                contains({typTsz: [{typ: "07"}]})
            ) 
        ) |
        map (
            {
                datum: .d,
                sprechzeiten: ( .typTsz |
                    map( . |
                        select(.typ=="07") |
                        .sprechzeiten[]
                    )
                )
            }
        )
    )
} )
