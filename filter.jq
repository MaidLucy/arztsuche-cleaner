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
                contains({tszDesTyps: [{typ: "Telefonische Erreichbarkeit"}]})
            ) 
        ) |
        map (
            {
                datum: .d,
                tag: .t,
                sprechzeiten: ( .tszDesTyps |
                    map( . |
                        select(.typ=="Telefonische Erreichbarkeit") |
                        .sprechzeiten[]
                    )
                )
            }
        )
    )
} )
