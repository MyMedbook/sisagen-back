# SISAGENcardio API Structure

## Base URL
```
/api/v1/patients/{patient_id}/
```

## 1. ANAMNESI
```
GET/PUT/POST /anamnesi/fattori-rischio/
{
    "ipertensione_arteriosa": {
        "presente": boolean,  // 1 = no, 2 = si
        "anni": integer
    },
    "dislipidemia": {
        "tipo": enum["no", "ipercolesterolemia", "ipertrigliceridemia", "mista"],  // 1-4
        "anni": integer
    },
    "diabete_mellito": {
        "presente": boolean,  // 1 = no, 2 = si
        "anni": integer
    },
    "fumo": {
        "stato": enum["no", "si", "passato"],  // 1-3
        "anni": integer,
        "anni_smesso": integer
    },
    "obesita": enum["normopeso", "sovrappeso", "obeso"]  // 1-3
}

GET/PUT/POST /anamnesi/comorbidita/
{
    "malattia_renale_cronica": {
        "presente": boolean,  // 1 = no, 2 = si
        "stadio": integer
    },
    "bpco": boolean,  // 1 = no, 2 = si
    "steatosi_epatica": {
        "presente": boolean,  // 1 = no, 2 = si
        "grado": string
    },
    "anemia": {
        "presente": boolean,  // 1 = no, 2 = si
        "tipo": string
    },
    "distiroidismo": enum["no", "ipotiroidismo", "ipertiroidismo", "tiroidectomia"]  // 1-4
}
GET/PUT/POST /anamnesi/sintomatologia/
{
    "dolore_toracico": {
        "presente": boolean,  // 1 = no, 2 = si
        "tipo": enum["tipico", "atipico"],  // 1-2
        "frequenza": enum["raro", "frequente"]  // 1-2
    },
    "dispnea": {
        "presente": boolean,  // 1 = no, 2 = si
        "classe_nyha": integer
    },
    "cardiopalmo": {
        "presente": boolean,  // 1 = no, 2 = si
        "frequenza": enum["raro", "frequente"]  // 1-2
    },
    "sincope": {
        "tipo": enum["no", "lipotimia", "sincope"],  // 1-3
        "verosimile": enum["vasovagale", "aritmica"]  // 1-2
    },
    "altro": {
        "presente": boolean,  // 1 = no, 2 = si
        "descrizione": string  // Optional, only when presente = true
    }
}

GET/PUT/POST /anamnesi/coinvolgimento-multisistemico/
{
    "sistema_nervoso": enum["no", "difficolta_apprendimento", "ritardo_psicomotorio", "atassia", "parestesie"],
    "occhio": enum["no", "ipovisione", ""],
    "orecchio": enum["no", "difficolta_apprendimento", "ritardo_psicomotorio", "atassia"],
    "sistema_muscoloscheletrico": enum["no", "miotonia", "tunnel_carpale_bilaterale", "debolezza_muscolare"],
    "pelle": enum["no", "lentiggini", "angiocheratoma", "cheratodermia"]
}

GET/PUT/POST /anamnesi/terapia-farmacologica/
{
    "farmaci": [string]
}

paziente id
operatore id
status 'draft' 'completed'
```

## 2. PEDIGREE
```
GET/PUT /pedigree/
{
    "padre": {
        "stessa_malattia": boolean,  // 1 = no, 2 = si
        "eta_esordio": integer,
        "severita": enum["lieve", "severa"],  // 1-2
        "morte_improvvisa": boolean,  // 1 = no, 2 = si
        "eta_morte": integer,
        "device": enum["no", "pm", "icd", "crt"]  // 1-4
    },
    "madre": { /* same structure as padre */ },
    "nonno_paterno": { /* same structure */ },
    "nonna_paterna": { /* same structure */ },
    "nonno_materno": { /* same structure */ },
    "nonna_materna": { /* same structure */ },
    "fratelli": [
        {
            "numero": integer,
            /* same structure as above */
        }
    ],
    "figli": [
        {
            "numero": integer,
            /* same structure as above */
        }
    ]
}
```

## 3. GENETICA
```
GET/PUT /genetica/
{
    "trasmissione": enum["ad", "ar", "x_linked", "materna"],  // 1-4
    "gene": {
        "nome": string,
        "tipo": enum["patogenetica", "prob_patogenetica", "vus", "prob_benigna", "benigna"]  // 1-5
    }
}
```

## 4. ECG
```
GET/PUT /ecg/
{
    "ritmo": enum["ritmo_sinusale", "fa", "besv", "bev"],  // 1-4
    "pr": enum["nei_limiti", "bav_i", "corto_preeccitazione"],  // 1-3
    "qrs": enum["nei_limiti", "ivs", "onde_q", "bbd", "bbs", "bassi_voltaggi"],  // 1-6
    "rv": {
        "stato": enum["nei_limiti", "t_negative"],  // 1-2
        "dettagli": string
    }
}
```

## 5. ESAMI DI LABORATORIO
```
GET/PUT /esami-laboratorio/
{
    "cpk": float,
    "troponina_hs": float,
    "nt_pro_bnp": float,
    "d_dimero": float,
    "creatinina": float,
    "azotemia": float,
    "na": float,
    "k": float,
    "gfr": float,
    "albuminuria": float,
    "alt": float,
    "ast": float,
    "bilirubina": {
        "totale": float,
        "diretta": float,
        "indiretta": float
    },
    "ggt": float,
    "alfa_galattosidasi": float,
    "componente_monoclonale_sierica": string,
    "immunofissazione_sierica": string,
    "immunofissazione_urinaria": string
}
```

## 6. ECOCARDIOGRAMMA
```
GET/PUT /ecocardiogramma/
{
    "diametro_telediastolico_vs": float,
    "spessore_siv": float,
    "spessore_pp": float,
    "diametro_anteroposteriore_as": float,
    "volume_as": float,
    "radice_aortica": float,
    "aorta_ascendente": float,
    "fe": float,
    "gp_aortico": {
        "medio": float,
        "max": float
    },
    "gp_mitralico": {
        "medio": float,
        "max": float
    },
    "paps": float,
    "lvot": float
}
```

Common Features:
- All endpoints support GET/PUT/PATCH operations
- URLs in English for RESTful conventions
- Field names in Italian matching the medical form
- Numeric enums matching the form's options (1, 2, 3, etc.)
- Support for pagination and filtering
- Validation rules matching the form's requirements

Would you like me to:
1. Add validation rules for specific fields?
2. Add more detailed documentation for any section?
3. Show implementation examples for specific endpoints?




