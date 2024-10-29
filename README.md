# MyMedBook - Sisagen Cardio

# Anamnesi API Endpoints - Complete Examples

## Common Headers for All Requests
```
Authorization: Bearer $accessToken
Content-Type: application/json
```
### Common Values: 
status:
- "draft"
- "complete"
- "archived"

## 1. Fattori Rischio
dislipidemia.tipo:
- "no"
- "ipercolesterolemia"
- "ipertrigliceridemia"
- "mista"

fumo.stato:
- "no"
- "si"
- "passato"

obesita:
- "normopeso"
- "sovrappeso"
- "obeso"

distiroidismo:
- "no"
- "ipotiroidismo"
- "ipertiroidismo"
- "tiroidectomia"

Base URL: `http://localhost:8000/api/anamnesi/fattori-rischio/{paziente_id}/`

### GET Request
```http
GET http://localhost:8000/api/anamnesi/fattori-rischio/699/
```

Response (200 OK):
```json
{
    "status": "complete",
    "data": {
        "paziente_id": 699,
        "operatore_id": 1992,
        "status": "complete",
        "created_at": "2024-03-20T10:30:00Z",
        "updated_at": "2024-03-20T10:30:00Z",
        "ipertensione_arteriosa": {
            "presente": true,
            "anni": 5
        },
        "dislipidemia": {
            "tipo": "ipercolesterolemia",
            "anni": 3
        },
        "diabete_mellito": {
            "presente": false,
            "anni": 0
        },
        "fumo": {
            "stato": "passato",
            "anni": 10,
            "anni_smesso": 2
        },
        "obesita": "normopeso"
    }
}
```

### PUT Request
```http
PUT http://localhost:8000/api/anamnesi/fattori-rischio/699/

{
    "operatore_id": 1992,
    "status": "complete",
    "ipertensione_arteriosa": {
        "presente": true,
        "anni": 5
    },
    "dislipidemia": {
        "tipo": "ipercolesterolemia",
        "anni": 3
    },
    "diabete_mellito": {
        "presente": false,
        "anni": 0
    },
    "fumo": {
        "stato": "passato",
        "anni": 10,
        "anni_smesso": 2
    },
    "obesita": "normopeso"
}
```

### DELETE Request
```http
DELETE http://localhost:8000/api/anamnesi/fattori-rischio/699/
```
## 2. Comorbidita 
### Values:
malattia_renale_cronica:
  presente: boolean
  stadio: number (0-5)

steatosi_epatica:
  presente: boolean
  grado: string (optional)

anemia:
  presente: boolean
  tipo: string (optional)

bpco: boolean

distiroidismo:
- "no"
- "ipotiroidismo"
- "ipertiroidismo"
- "tiroidectomia"

### Base URL: `http://localhost:8000/api/anamnesi/comorbidita/{paziente_id}/`

### GET Request
```http
GET http://localhost:8000/api/anamnesi/comorbidita/699/
```

Response (200 OK):
```json
{
    "status": "complete",
    "data": {
        "paziente_id": 699,
        "operatore_id": 1992,
        "status": "complete",
        "created_at": "2024-03-20T10:30:00Z",
        "updated_at": "2024-03-20T10:30:00Z",
        "malattia_renale_cronica": {
            "presente": true,
            "stadio": 2
        },
        "bpco": false,
        "steatosi_epatica": {
            "presente": true,
            "grado": "moderata"
        },
        "anemia": {
            "presente": true,
            "tipo": "sideropenica"
        },
        "distiroidismo": "ipotiroidismo"
    }
}
```

### PUT Request
```http
PUT http://localhost:8000/api/anamnesi/comorbidita/699/

{
    "operatore_id": 1992,
    "status": "complete",
    "malattia_renale_cronica": {
        "presente": true,
        "stadio": 2
    },
    "bpco": false,
    "steatosi_epatica": {
        "presente": true,
        "grado": "moderata"
    },
    "anemia": {
        "presente": true,
        "tipo": "sideropenica"
    },
    "distiroidismo": "ipotiroidismo"
}
```

### DELETE Request
```http
DELETE http://localhost:8000/api/anamnesi/comorbidita/699/
```

## 3. Sintomatologia

### Values:
dolore_toracico.tipo:
- "tipico"
- "atipico"

frequenza:
- "raro"
- "frequente"

sincope.tipo:
- "no"
- "lipotimia"
- "sincope"

sincope.verosimile:
- "vasovagale"
- "aritmica"

Base URL: `http://localhost:8000/api/anamnesi/sintomatologia/{paziente_id}/`

### GET Request
```http
GET http://localhost:8000/api/anamnesi/sintomatologia/699/
```

Response (200 OK):
```json
{
    "status": "complete",
    "data": {
        "paziente_id": 699,
        "operatore_id": 1992,
        "status": "draft",
        "created_at": "2024-03-20T10:30:00Z",
        "updated_at": "2024-03-20T10:30:00Z",
        "dolore_toracico": {
            "presente": true,
            "tipo": "tipico",
            "frequenza": "frequente"
        },
        "dispnea": {
            "presente": true,
            "classe_nyha": 2
        },
        "cardiopalmo": {
            "presente": true,
            "frequenza": "frequente"
        },
        "sincope": {
            "tipo": "sincope",
            "verosimile": "vasovagale"
        },
        "altro": {
            "presente": true,
            "descrizione": "Affaticamento cronico e vertigini occasionali"
        }
    }
}
```

### PUT Request
```http
PUT http://localhost:8000/api/anamnesi/sintomatologia/699/

{
    "operatore_id": 1992,
    "status": "draft",
    "dolore_toracico": {
        "presente": true,
        "tipo": "tipico",
        "frequenza": "frequente"
    },
    "dispnea": {
        "presente": true,
        "classe_nyha": 2
    },
    "cardiopalmo": {
        "presente": true,
        "frequenza": "frequente"
    },
    "sincope": {
        "tipo": "sincope",
        "verosimile": "vasovagale"
    },
    "altro": {
        "presente": true,
        "descrizione": "Affaticamento cronico e vertigini occasionali"
    }
}
```

### DELETE Request
```http
DELETE http://localhost:8000/api/anamnesi/sintomatologia/699/
```

Response (204 No Content)

## 4. Coinvolgimento Multisistemico

### Values:

sistema_nervoso:
- "no"
- "difficolta_apprendimento"
- "ritardo_psicomotorio"
- "atassia"
- "parestesie"

occhio:
- "no"
- "ipovisione"
- "ptosi_palpebrale"

orecchio:
- "no"
- "difficolta_apprendimento"
- "ritardo_psicomotorio"
- "atassia"

sistema_muscoloscheletrico:
- "no"
- "miotonia"
- "tunnel_carpale_bilaterale"
- "debolezza_muscolare"

pelle:
- "no"
- "lentiggini"
- "angiocheratoma"
- "cheratodermia"

Base URL: `http://localhost:8000/api/anamnesi/coinvolgimento-multisistemico/{paziente_id}/`

### GET Request
```http
GET http://localhost:8000/api/anamnesi/coinvolgimento-multisistemico/699/
```

Response (200 OK):
```json
{
    "status": "complete",
    "data": {
        "paziente_id": 699,
        "operatore_id": 1992,
        "status": "draft",
        "created_at": "2024-03-20T10:30:00Z",
        "updated_at": "2024-03-20T10:30:00Z",
        "sistema_nervoso": "difficolta_apprendimento",
        "occhio": "ptosi_palpebrale",
        "orecchio": "difficolta_apprendimento",
        "sistema_muscoloscheletrico": "debolezza_muscolare",
        "pelle": "angiocheratoma"
    }
}
```

### PUT Request
```http
PUT http://localhost:8000/api/anamnesi/coinvolgimento-multisistemico/699/

{
    "operatore_id": 1992,
    "status": "draft",
    "sistema_nervoso": "difficolta_apprendimento",
    "occhio": "ptosi_palpebrale",
    "orecchio": "difficolta_apprendimento",
    "sistema_muscoloscheletrico": "debolezza_muscolare",
    "pelle": "angiocheratoma"
}
```

### DELETE Request
```http
DELETE http://localhost:8000/api/anamnesi/coinvolgimento-multisistemico/699/
```

# 5. Terapia Farmaologica

### Values:
farmaci: array of strings
- Each entry should be a valid medication name
- Array can be empty but must be present
- No specific restrictions on medication names

### PUT Request
```http
PUT http://localhost:8000/api/anamnesi/terapia-farmacologica/699/

{
    "operatore_id": 1992,
    "status": "complete",
    "farmaci": [
        "Metoprololo 100mg",
        "Ramipril 5mg",
        "Furosemide 25mg",
        "Levotiroxina 75mcg"
    ]
}
```

### DELETE Request
```http
DELETE http://localhost:8000/api/anamnesi/terapia-farmacologica/699/
```

## Important Notes
- 200: Successful GET/PUT
- 204: Successful DELETE
- 400: Invalid request data
- 401: Authentication failure
- 404: Record not found
- 500: Server error


# Pedigree
### Valid Values:
status:
- "draft"
- "complete"
- "archived"

severita:
- "lieve"
- "severa"

device:
- "no"
- "pm" (pacemaker)
- "icd" (implantable cardioverter-defibrillator)
- "crt" (cardiac resynchronization therapy)

### Base URL: http://localhost:8000/api/pedigree/{paziente_id}/

### GET http://localhost:8000/api/pedigree/699/

### PUT REQUEST
```json
{
    "paziente_id": 699,
    "operatore_id": 1992,
    "status": "complete",
    "padre": {
        "stessa_malattia": false,
        "eta_esordio": null,
        "severita": null,
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "no"
    },
    "madre": {
        "stessa_malattia": true,
        "eta_esordio": 45,
        "severita": "lieve",
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "pm"
    },
    "nonno_paterno": {
        "stessa_malattia": true,
        "eta_esordio": 60,
        "severita": "severa",
        "morte_improvvisa": true,
        "eta_morte": 65,
        "device": "icd"
    },
    "nonna_paterna": {
        "stessa_malattia": false,
        "eta_esordio": null,
        "severita": null,
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "no"
    },
    "nonno_materno": {
        "stessa_malattia": false,
        "eta_esordio": null,
        "severita": null,
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "no"
    },
    "nonna_materna": {
        "stessa_malattia": false,
        "eta_esordio": null,
        "severita": null,
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "no"
    },
    "fratelli": [
        {
            "numero": 1,
            "stessa_malattia": true,
            "eta_esordio": 30,
            "severita": "lieve",
            "morte_improvvisa": false,
            "eta_morte": null,
            "device": "no"
        },
        {
            "numero": 2,
            "stessa_malattia": false,
            "eta_esordio": null,
            "severita": null,
            "morte_improvvisa": false,
            "eta_morte": null,
            "device": "no"
        }
    ],
    "figli": [
        {
            "numero": 1,
            "stessa_malattia": true,
            "eta_esordio": 15,
            "severita": "lieve",
            "morte_improvvisa": false,
            "eta_morte": null,
            "device": "no"
        }
    ]
}
```

### DELETE http://localhost:8000/api/pedigree/699/

# ECG

### Valid Values : 
ritmo:
- "ritmo_sinusale"
- "fa"
- "besv"
- "bev"

pr:
- "nei_limiti"
- "bav_i"
- "corto_preeccitazione"

qrs:
- "nei_limiti"
- "ivs"
- "onde_q"
- "bbd"
- "bbs"
- "bassi_voltaggi"

rv.stato:
- "nei_limiti"
- "t_negative"

### GET REQUEST http://localhost:8000/api/ecg/699/

### PUT REQUEST http://localhost:8000/api/ecg/699/
Request Body: 
```json
{
    "paziente_id": 699,
    "operatore_id": 1992,
    "status": "complete",
    "padre": {
        "stessa_malattia": false,
        "eta_esordio": null,
        "severita": null,
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "no"
    },
    "madre": {
        "stessa_malattia": true,
        "eta_esordio": 44,
        "severita": "lieve",
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "pm"
    },
    "nonno_paterno": {
        "stessa_malattia": true,
        "eta_esordio": 60,
        "severita": "severa",
        "morte_improvvisa": true,
        "eta_morte": 65,
        "device": "icd"
    },
    "nonna_paterna": {
        "stessa_malattia": false,
        "eta_esordio": null,
        "severita": null,
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "no"
    },
    "nonno_materno": {
        "stessa_malattia": false,
        "eta_esordio": null,
        "severita": null,
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "no"
    },
    "nonna_materna": {
        "stessa_malattia": false,
        "eta_esordio": null,
        "severita": null,
        "morte_improvvisa": false,
        "eta_morte": null,
        "device": "no"
    },
    "fratelli": [
        {
            "numero": 1,
            "stessa_malattia": true,
            "eta_esordio": 30,
            "severita": "lieve",
            "morte_improvvisa": false,
            "eta_morte": null,
            "device": "no"
        },
        {
            "numero": 2,
            "stessa_malattia": false,
            "eta_esordio": null,
            "severita": null,
            "morte_improvvisa": false,
            "eta_morte": null,
            "device": "no"
        }
    ],
    "figli": [
        {
            "numero": 1,
            "stessa_malattia": true,
            "eta_esordio": 15,
            "severita": "lieve",
            "morte_improvvisa": false,
            "eta_morte": null,
            "device": "no"
        }
    ]
}
```
### DELETE REQUEST http://localhost:8000/api/pedigree/699/

# GENETICA

### Valid Values:
trasmissione:
- "ad"
- "ar"
- "x_linked"
- "materna"

gene.tipo:
- "patogenetica"
- "prob_patogenetica"
- "vus"
- "prob_benigna"
- "benigna"


### GET REQUEST http://localhost:8000/api/genetica/699/

### PUT REQUEST http://localhost:8000/api/genetica/699/

```json
{
    "operatore_id": 1992,
    "status": "complete",
    "trasmissione": "ad",
    "gene": {
        "nome": "MYBPC3",
        "tipo": "patogenetica"
    }
}
```

### DELETE REQUEST http://localhost:8000/api/genetica/699/

# ECOCARDIOGRAMMA

### Valid Values:
All measurements must be positive numbers:
- diametro_telediastolico_vs
- spessore_siv
- spessore_pp
- diametro_anteroposteriore_as
- volume_as
- radice_aortica
- aorta_ascendente
- fe (must be between 0-100)
- paps
- lvot

Gradiente Pressorio constraints:
- medio and max must be positive
- max must be greater than medio

### GET http://localhost:8000/api/ecocardiogramma/699/

### PUT http://localhost:8000/api/ecocardiogramma/699/
```json
{
    "operatore_id": 1992,
    "status": "complete",
    "diametro_telediastolico_vs": 45.5,
    "spessore_siv": 11.2,
    "spessore_pp": 10.1,
    "diametro_anteroposteriore_as": 38.0,
    "volume_as": 52.0,
    "radice_aortica": 32.5,
    "aorta_ascendente": 34.0,
    "fe": 65.0,
    "gp_aortico": {
        "medio": 12.0,
        "max": 24.0
    },
    "gp_mitralico": {
        "medio": 3.5,
        "max": 7.0
    },
    "paps": 28.0,
    "lvot": 2.1
}
```


### DELETE http://localhost:8000/api/ecocardiogramma/699/


# ECOCARDIOGRAMMA

### Valid Values:
All measurements must be positive numbers:
- diametro_telediastolico_vs
- spessore_siv
- spessore_pp
- diametro_anteroposteriore_as
- volume_as
- radice_aortica
- aorta_ascendente
- fe (must be between 0-100)
- paps
- lvot

Gradiente Pressorio constraints:
- medio and max must be positive
- max must be greater than medio

### GET http://localhost:8000/api/esami-laboratorio/699/

### PUT http://localhost:8000/api/esami-laboratorio/699/
```json
{
    "operatore_id": 1992,
    "status": "complete",
    "cpk": 150.0,
    "troponina_hs": 0.012,
    "nt_pro_bnp": 125.0,
    "d_dimero": 250.0,
    "creatinina": 0.9,
    "azotemia": 35.0,
    "na": 140.0,
    "k": 4.2,
    "gfr": 90.0,
    "albuminuria": 15.0,
    "alt": 25.0,
    "ast": 22.0,
    "bilirubina": {
        "totale": 1.2,
        "diretta": 0.3,
        "indiretta": 0.9
    },
    "ggt": 30.0,
    "alfa_galattosidasi": 3.2,
    "componente_monoclonale_sierica": "Assente",
    "immunofissazione_sierica": "Negativa",
    "immunofissazione_urinaria": "Negativa"
}
```


### DELETE http://localhost:8000/api/esami-laboratorio/699/
