.arztPraxisDatas[0] | {
    anrede: .anrede, 
    name: .name, 
    strasse: .strasse, 
    hausnummer: .hausnummer, 
    plz: .plz, 
    ort: .ort, 
    telefon: .tel, 
    handy: .handy, 
    email: .email, 
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
}
