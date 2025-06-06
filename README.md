<!-- omit from toc -->
# MyMedBook: Sisagen-Cardio API
- [General Usage](#general-usage)
  - [Obtaining Token](#obtaining-token)
  - [Common Headers for All Requests](#common-headers-for-all-requests)
  - [Common fields for all document types](#common-fields-for-all-document-types)
    - [Presenti in GET:](#presenti-in-get)
    - [Presenti in POST e GET:](#presenti-in-post-e-get)
    - [NON ANCORA IMPLEMENTATI](#non-ancora-implementati)
  - [Common Endpoint Behaviour](#common-endpoint-behaviour)
    - [create](#create)
    - [list](#list)
    - [retrieve](#retrieve)
    - [latest](#latest)
- [Anamnesi API Endpoints - Complete Examples](#anamnesi-api-endpoints---complete-examples)
  - [1. Fattori Rischio](#1-fattori-rischio)
    - [Campi](#campi)
    - [create](#create-1)
    - [latest](#latest-1)
    - [retrieve](#retrieve-1)
    - [list](#list-1)
  - [2. Comorbidita](#2-comorbidita)
    - [Campi:](#campi-1)
    - [create](#create-2)
    - [latest](#latest-2)
    - [retrieve](#retrieve-2)
    - [retrieve](#retrieve-3)
  - [3. Sintomatologia](#3-sintomatologia)
    - [Values:](#values)
    - [create](#create-3)
    - [latest](#latest-3)
    - [retrieve](#retrieve-4)
    - [retrieve](#retrieve-5)
  - [4. Coinvolgimento Multisistemico](#4-coinvolgimento-multisistemico)
    - [Values:](#values-1)
    - [create](#create-4)
    - [latest](#latest-4)
    - [retrieve](#retrieve-6)
    - [retrieve](#retrieve-7)
  - [5. Terapia Farmacologica](#5-terapia-farmacologica)
    - [Values:](#values-2)
    - [create](#create-5)
    - [latest](#latest-5)
    - [retrieve](#retrieve-8)
    - [retrieve](#retrieve-9)
  - [Important Notes](#important-notes)
- [Pedigree](#pedigree)
    - [Valid Values:](#valid-values)
    - [Base URL: http://localhost:8000/api/pedigree/{paziente\_id}/](#base-url-httplocalhost8000apipedigreepaziente_id)
    - [GET http://localhost:8000/api/pedigree/699/](#get-httplocalhost8000apipedigree699)
    - [PUT REQUEST](#put-request)
    - [DELETE http://localhost:8000/api/pedigree/699/](#delete-httplocalhost8000apipedigree699)
- [ECG](#ecg)
    - [Valid Values :](#valid-values-)
    - [GET REQUEST http://localhost:8000/api/ecg/699/](#get-request-httplocalhost8000apiecg699)
    - [PUT REQUEST http://localhost:8000/api/ecg/699/](#put-request-httplocalhost8000apiecg699)
- [GENETICA](#genetica)
    - [Valid Values:](#valid-values-1)
    - [GET REQUEST http://localhost:8000/api/genetica/699/](#get-request-httplocalhost8000apigenetica699)
    - [PUT REQUEST http://localhost:8000/api/genetica/699/](#put-request-httplocalhost8000apigenetica699)
    - [DELETE REQUEST http://localhost:8000/api/genetica/699/](#delete-request-httplocalhost8000apigenetica699)
- [ECOCARDIOGRAMMA](#ecocardiogramma)
    - [Valid Values:](#valid-values-2)
    - [GET http://localhost:8000/api/ecocardiogramma/699/](#get-httplocalhost8000apiecocardiogramma699)
    - [PUT http://localhost:8000/api/ecocardiogramma/699/](#put-httplocalhost8000apiecocardiogramma699)
    - [DELETE http://localhost:8000/api/ecocardiogramma/699/](#delete-httplocalhost8000apiecocardiogramma699)
- [ESAMI LABORATORIO](#esami-laboratorio)
    - [Valid Values:](#valid-values-3)
    - [GET http://localhost:8000/api/esami-laboratorio/699/](#get-httplocalhost8000apiesami-laboratorio699)
    - [PUT http://localhost:8000/api/esami-laboratorio/699/](#put-httplocalhost8000apiesami-laboratorio699)
    - [DELETE http://localhost:8000/api/esami-laboratorio/699/](#delete-httplocalhost8000apiesami-laboratorio699)

# General Usage
## Obtaining Token
```http
POST https://medbooksrl.onrender.com/auth/token/
```
Body Request (x-www-form-urlencoded)
```json
grant_type:password
username:xxxx@gmail.com
password: ******
client_id:it.netfarm.mymedbook.web
client_secret:
```

## Common Headers for All Requests
```
Authorization: Bearer $accessToken
Content-Type: application/json
```

## Common fields for all document types

### Presenti in GET:
```json
{
    "_id": {"oid": str}
        // id casuale identificativo interno utilizzato da MongoDB
        
    "created_at": {"$date": int}
        // Data di creazione del documento, espressa in unix time 
        
    "updated_at": {"$date": int}
        // Data dell'aggiornamento più recente del documento, espressa in unix time [FORSE DA DEPRECARE??]
}
```

### Presenti in POST e GET:
```json
{
    "paziente_id": int 
        // Codice id utente del paziente a cui appartiene il referto.

    "operatore_id": int
        // Codice id utente dello specialista che ha effettuato la visita.

    "datamanager_id": int
        // Codice id utente della persona che ha stilato il report digitale. (default: request.user.pk)

    "status": "draft" | "complete" | "archived"
        // Status del referto [NON ANCORA UTILIZZATO] 
}
```

### NON ANCORA IMPLEMENTATI
I seguenti campi sono previsti dalla logica richiesta dal cliente ma non sono ancora implementati in quanto richiedono interfaccia più diretta con il server di autenticazione.
```json
{
    "struttura": str
        // Nome della struttura che ha rilasciato il referto.
    "anagrafica": ???
        // Anagrafica del paziente.
}
```

## Common Endpoint Behaviour

La maggior parte degli endpoint è strutturata allo stesso identico modo e supporta i seguenti metodi. Al momento non è possibile cancellare o modificare documenti una volta creati.

### create
```POST {prefix}/```

Crea un nuovo documento di tipo {prefix} a partire dal body della richiesta. Restituisce il documento salvato.

### list
```GET {prefix}/```

Restituisce tutti i documenti della tipologia associata a {prefix}. Permette anche la ricerca per vari criteri:
- paziente_id
- operatore_id
- datamanager_id

### retrieve
```GET {prefix}/{paziente_id}/```

Restituisce tutti i documenti della tipologia associata a {prefix}, relativi al paziente con id {paziente_id}.

### latest
```GET {prefix}/{paziente_id}/latest/```

Restituisce il più recente documento della tipologia associata a {prefix} relativo al paziente con id {paziente_id}.

# Anamnesi API Endpoints - Complete Examples

## 1. Fattori Rischio

Base URL: `http://localhost:8000/api/anamnesi/fattori-rischio/`

### Campi
**ipertensione_arteriosa**:
- **presente** (*bool*)
- **anno_insorgenza** (*int*): (solo se tipo != no)
- **anni** (*int*): (solo se tipo != no; se assente viene calcolato in automatico sulla base di anno_insorgenza e data corrente).

**dislipidemia**: 
- **tipo** (*choice*):
  - "no"
  - "ipercolesterolemia"
  - "ipertrigliceridemia"
  - "mista"
- **anno_insorgenza** (*int*): (solo se tipo != no)
- **anni** (*int*): (solo se tipo != no; se assente viene calcolato in automatico sulla base di anno_insorgenza e data corrente).

**diabete_mellito**:
- **presente** (*bool*)
- **anno_insorgenza** (*int*): (solo se tipo != no)
- **anni** (*int*): (solo se tipo != no; se assente viene calcolato in automatico sulla base di anno_insorgenza e data corrente).

**fumo**:
- **stato** (*choice*):
  - "no"
  - "si"
  - "passato"
- **anno_inizio** (*int*):
Anno in cui il paziente ha iniziato a fumare (presente solo se fumo.stato == si | passato).
- **anno_interruzione** (*int*): 
Anno in cui il paziente ha smesso di fumare (presente solo se fumo.stato == passato).
- **anni** (*int*): 
Numero di anni in cui il paziente ha fumato (presente solo se fumo.stato == si | passato; se non specificato dal datamanager viene calcolato in automatico sulla base dell'anno corrente o di fumo.anno_interruzione).
- **anni_smesso** (*int*): 
Numero di anni da quando il paziente ha smesso di fumare (presente solo se fumo.stato == passato; se non specificato dal datamanager viene calcolato in automatico sulla base dell'anno corrente).

**obesita** (*choice*):
- "normopeso"
- "sovrappeso"
- "obeso"


### create
```POST http://localhost:8000/api/anamnesi/fattori-rischio/```

body:
```json
{
    "paziente_id": 46993,
    "operatore_id": 1992,
    "status": "complete",
    "ipertensione_arteriosa": {
        "presente": true,
        "anno_insorgenza": 2020
    },
    "dislipidemia": {
        "tipo": "ipercolesterolemia",
        "anno_insorgenza": 2020
    },
    "diabete_mellito": {
        "presente": false
    },
    "fumo": {
        "stato": "passato",
        "anno_inizio": 2009,
        "anno_interruzione": 2011
    },
    "obesita": "normopeso"
}
```

### latest
```GET http://localhost:8000/api/anamnesi/fattori-rischio/{paziente_id}/latest/```

response:
```json
{
    "_id": {
        "$oid": "6798fd23cfb5bc93554c40c9"
    },
    "paziente_id": 46993,
    "operatore_id": 1992,
    "datamanager_id": 1992,
    "status": "complete",
    "created_at": {
        "$date": 1738079522730
    },
    "updated_at": {
        "$date": 1738079522730
    },
    "ipertensione_arteriosa": {
        "presente": true,
        "anno_insorgenza": 2020,
        "anni": 5
    },
    "dislipidemia": {
        "tipo": "ipercolesterolemia",
        "anno_insorgenza": 2020,
        "anni": 5
    },
    "diabete_mellito": {
        "presente": false
    },
    "fumo": {
        "stato": "passato",
        "anno_inizio": 2009,
        "anno_interruzione": 2011,
        "anni": 2,
        "anni_smesso": 14
    },
    "obesita": "normopeso"
}
```

### retrieve
```GET http://localhost:8000/api/anamnesi/fattori-rischio/{paziente_id}/```

Response: (come ```latest```, ma array)

### list
```GET http://localhost:8000/api/anamnesi/fattori-rischio/```

Response: (come ```latest```, ma array)

## 2. Comorbidita 
Base URL: `http://localhost:8000/api/anamnesi/fattori-rischio/`

### Campi:
**malattia_renale**:
- **presente** (*boolean*).
- **stadio** (*int 0-5*): (solo se presente == True).

**bpco** (*boolean*).

**steatosi_epatica**:
- **presente** (*boolean*).
- **grado** (*string*): (solo se presente == True).

**anemia**:
- **presente** (*boolean*).
- **tipo** (*string*): (solo se presente == True).

**distiroidismo** (*choice*):
- "no"
- "ipotiroidismo"
- "ipertiroidismo"
- "tiroidectomia"

### create
```POST http://localhost:8000/api/comorbidita/fattori-rischio/```

body:
```json
{
    "status": "complete",
    "paziente_id": 699,
    "operatore_id": 1992,
    "datamanager_id": 563,
    "malattia_renale": {
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

### latest
```GET http://localhost:8000/api/anamnesi/comorbidita/{paziente_id}/latest/```

response:
```json
{
    "_id": {
        "$oid": "6798fe84cfb5bc93554c40ca"
    },
    "paziente_id": 699,
    "operatore_id": 1992,
    "datamanager_id": 563,
    "status": "complete",
    "created_at": {
        "$date": 1738079875960
    },
    "updated_at": {
        "$date": 1738079875960
    },
    "malattia_renale": {
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

### retrieve
```GET http://localhost:8000/api/anamnesi/comorbidita/{paziente_id}/```

Response: (come ```latest```, ma array)

### retrieve
```GET http://localhost:8000/api/anamnesi/comorbidita/```

Response: (come ```latest```, ma array)

## 3. Sintomatologia

Base URL: `http://localhost:8000/api/anamnesi/sintomatologia/`

### Values:
**dolore_toracico**:
- **presente** (*boolean*).
- **tipo** (*choice*): (solo se presente == True)
  - "tipico"
  - "atipico"
- **frequenza** (*choice*): (solo se presente == True)
  - "raro"
  - "frequente"

**dispnea**:
- **presente** (*boolean*).
- **classe_nyha** (*int 1-4*): (solo se presente == True)

**cardiopalmo**:
- **presente** (*boolean*).
- **frequenza** (*choice*): (solo se presente == True)
  - "raro"
  - "frequente"

**sincope**:
- **tipo** (*choice*):
  - "no"
  - "lipotimia"
  - "sincope"
- **verosimile** (*choice*): (solo se tipo != "no")
  - "vasovagale"
  - "aritmica"

**altro**:
- **presente** (*boolean*).
- **descrizione** (*string*): (solo se presente == True)


### create
```POST http://localhost:8000/api/sintomatologia/fattori-rischio/```

body:
```json
{
    "operatore_id": 1992,
    "paziente_id": 46933,
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

### latest
```GET http://localhost:8000/api/anamnesi/sintomatologia/{paziente_id}/latest/```

response:
```json
{
    "_id": {
        "$oid": "6798ff19cfb5bc93554c40cb"
    },
    "paziente_id": 46933,
    "operatore_id": 1992,
    "datamanager_id": 1992,
    "status": "draft",
    "created_at": {
        "$date": 1738080025267
    },
    "updated_at": {
        "$date": 1738080025267
    },
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

### retrieve
```GET http://localhost:8000/api/anamnesi/sintomatologia/{paziente_id}/```

Response: (come ```latest```, ma array)

### retrieve
```GET http://localhost:8000/api/anamnesi/sintomatologia/```

Response: (come ```latest```, ma array)


## 4. Coinvolgimento Multisistemico
Base URL: `http://localhost:8000/api/anamnesi/coinvolgimento/`

### Values:

**sistema_nervoso** (*choice*):
- "no"
- "difficolta_apprendimento"
- "ritardo_psicomotorio"
- "atassia"
- "parestesie"

**occhio** (*choice*):
- "no"
- "ipovisione"
- "ptosi_palpebrale"

**orecchio** (*choice*):
- "no"
- "difficolta_apprendimento"
- "ritardo_psicomotorio"
- "atassia"

**sistema_muscoloscheletrico** (*choice*):
- "no"
- "miotonia"
- "tunnel_carpale_bilaterale"
- "debolezza_muscolare"

**pelle** (*choice*):
- "no"
- "lentiggini"
- "angiocheratoma"
- "cheratodermia"

### create
```POST http://localhost:8000/api/coinvolgimento/fattori-rischio/```

body:
```json
{
    "operatore_id": 1992,
    "paziente_id": 46933,
    "status": "draft",
    "sistema_nervoso": "difficolta_apprendimento",
    "occhio": "ptosi_palpebrale",
    "orecchio": "difficolta_apprendimento",
    "sistema_muscoloscheletrico": "debolezza_muscolare",
    "pelle": "angiocheratoma"
}
```

### latest
```GET http://localhost:8000/api/anamnesi/coinvolgimento/{paziente_id}/latest/```

response:
```json
{
    "_id": {
        "$oid": "6798ff9ecfb5bc93554c40cc"
    },
    "paziente_id": 46933,
    "operatore_id": 1992,
    "datamanager_id": 1992,
    "status": "draft",
    "created_at": {
        "$date": 1738080158541
    },
    "updated_at": {
        "$date": 1738080158541
    },
    "sistema_nervoso": "difficolta_apprendimento",
    "occhio": "ptosi_palpebrale",
    "orecchio": "difficolta_apprendimento",
    "sistema_muscoloscheletrico": "debolezza_muscolare",
    "pelle": "angiocheratoma"
}
```

### retrieve
```GET http://localhost:8000/api/anamnesi/coinvolgimento/{paziente_id}/```

Response: (come ```latest```, ma array)

### retrieve
```GET http://localhost:8000/api/anamnesi/coinvolgimento/```

Response: (come ```latest```, ma array)

## 5. Terapia Farmacologica

BASE URL: `http://localhost:8000/api/anamnesi/terapia-farmacologica/699/`

### Values:
**farmaci** (*string[]*): 
- Each entry should be a valid medication name
- Array can be empty but must be present
- No specific restrictions on medication names

### create
```POST http://localhost:8000/api/anamnesi/terapia/```

body:
```json
{
    "operatore_id": 1992,
    "paziente_id": 46933,
    "updated_at": "prova",
    "status": "complete",
    "farmaci": [
        "Metoprololo 100mg",
        "Ramipril 5mg",
        "Furosemide 25mg",
        "Levotiroxina 75mcg"
    ]
}
```

### latest
```GET http://localhost:8000/api/anamnesi/terapia/{paziente_id}/latest/```

response:
```json
{
    "_id": {
        "$oid": "67990033cfb5bc93554c40cd"
    },
    "paziente_id": 46933,
    "operatore_id": 1992,
    "datamanager_id": 1992,
    "status": "complete",
    "created_at": {
        "$date": 1738080306817
    },
    "updated_at": {
        "$date": 1738080306817
    },
    "farmaci": [
        "Metoprololo 100mg",
        "Ramipril 5mg",
        "Furosemide 25mg",
        "Levotiroxina 75mcg"
    ]
}
```

### retrieve
```GET http://localhost:8000/api/anamnesi/terapia/{paziente_id}/```

Response: (come ```latest```, ma array)

### retrieve
```GET http://localhost:8000/api/anamnesi/terapia/```

Response: (come ```latest```, ma array)

## Important Notes
- 200: Successful GET/PUT
- 204: Successful DELETE
- 400: Invalid request data
- 401: Authentication failure
- 404: Record not found
- 500: Server error


# Pedigree
### Valid Values:

*Pedigree* utilizza le seguenti strutture dati per rappresentare i vari familiari immediati:
***FamilyMemberSerializer***:
- **stessa_malattia** (*boolean*)
- **eta_esordio** (*int*)
- **severita** (*choice*):
  - "lieve"
  - "severa"
- **morte_improvvisa** (*boolean*)
- **eta_morte** (*int*)
- **device** (*choice*):
  - "no"
  - "pm" (pacemaker)
  - "icd" (implantable cardioverter-defibrillator)
  - "crt" (cardiac resynchronization therapy)

***NumberedFamilyMemberSerializer***:
- (stessi campi di *family member generico*)
- **numero** (*int > 1*)

I familiari inclusi in *Pedigree* sono:
- **padre** (*FamilyMemberSerializer*)
- **madre** (*FamilyMemberSerializer*)
- **nonno_paterno** (*FamilyMemberSerializer*)
- **nonna_paterna** (*FamilyMemberSerializer*)
- **nonno_materno** (*FamilyMemberSerializer*)
- **nonna_materna** (*FamilyMemberSerializer*)
- **fratelli** (*NumberedFamilyMemberSerializer*)
- **figli** (*NumberedFamilyMemberSerializer*)

### Base URL: http://localhost:8000/api/pedigree/{paziente_id}/

### GET http://localhost:8000/api/pedigree/699/

### PUT REQUEST
```json
{
    "paziente_id": 699,
    "operatore_id": 1992,
    "status": "complete",
    "created_at": "2024-11-15T10:44:40.008795Z",
    "updated_at": "2024-11-15T10:44:40.502434Z",
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

### DELETE http://localhost:8000/api/pedigree/699/

# ECG

### Valid Values : 
**ritmo** (*choice*):
- "ritmo_sinusale"
- "fa"
- "besv"
- "bev"

**pr** (*choice*):
- "nei_limiti"
- "bav_i"
- "corto_preeccitazione"

**qrs** (*choice*):
- "nei_limiti"
- "ivs"
- "onde_q"
- "bbd"
- "bbs"
- "bassi_voltaggi"

**rv**:
- **stato** (*choice*):
  - "nei_limiti"
  - "t_negative"
- **dettagli** (*string* opzionale)

### GET REQUEST http://localhost:8000/api/ecg/699/

### PUT REQUEST http://localhost:8000/api/ecg/699/
Request Body: 
```json
{
    "paziente_id": 1992,
    "operatore_id": 1992,
    "status": "complete",
    "ritmo": "ritmo_sinusale",
    "pr": "nei_limiti",
    "qrs": "bbd",
    "rv": {
        "stato": "nei_limiti",
        "dettagli": "Nessuna alterazione significativa"
    }
}
```


# GENETICA

### Valid Values:
**trasmissione** (*choice*):
- "ad"
- "ar"
- "x_linked"
- "materna"

**gene**:
- **nome** (*string*)
- **tipo** (*choice*):
  - "patogenetica"
  - "prob_patogenetica"
  - "vus"
  - "prob_benigna"
  - "benigna"


### GET REQUEST http://localhost:8000/api/genetica/699/

### PUT REQUEST http://localhost:8000/api/genetica/699/

```json
{
    "paziente_id": 699,
    "operatore_id": 1992,
    "status": "complete",
    "created_at": "2024-11-15T10:44:40.008795Z",
    "updated_at": "2024-11-15T10:44:40.502434Z",
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

**diametro_telediastolico_vs** (*float > 0*).

**spessore_siv** (*float > 0*).

**spessore_pp** (*float > 0*).

**diametro_anteroposteriore_as** (*float > 0*).

**volume_as** (*float > 0*).

**radice_aortica** (*float > 0*).

**aorta_ascendente** (*float > 0*).

**fe** (*float 0-100*).

**paps** (*float > 0*).

**lvot** (*float > 0*).

**gp_aortico**:
- **medio** (*float > 0*)
- **max** (*float > medio*)

**gp_mitralico**:
- **medio** (*float > 0*)
- **max** (*float > medio*)


### GET http://localhost:8000/api/ecocardiogramma/699/

### PUT http://localhost:8000/api/ecocardiogramma/699/
```json
{
    "paziente_id": 1993,
    "operatore_id": 1992,
    "status": "complete",
    "created_at": "2024-11-15T10:44:40.008795Z",
    "updated_at": "2024-11-15T10:44:40.502434Z",
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


# ESAMI LABORATORIO

### Valid Values:
All measurements must be positive numbers:

**cpk** (*float > 0*): Creatine Phosphokinase

**troponina_hs** (*float > 0*): High-sensitivity Troponin

**nt_pro_bnp** (*float > 0*): NT-proBNP

**d_dimero** (*float > 0*): D-dimer

**creatinina** (*float > 0*): Creatinine

**azotemia** (*float > 0*): Blood Urea Nitrogen

**na** (*float > 0*): Sodium

**k** (*float > 0*): Potassium

**gfr** (*float > 0*): Glomerular Filtration Rate

**albuminuria** (*float > 0*): Albuminuria

**alt** (*float > 0*): Alanine Transaminase

**ast** (*float > 0*): Aspartate Transaminase

**bilirubina**:
- **totale** (*float > 0*): Total Bilirubin
- **diretta** (*float > 0*): Direct Bilirubin
- **indiretta** (*float ~ totale - diretta*): Indirect Bilirubin

**ggt** (*float > 0*): Gamma-Glutamyl Transferase

**alfa_galattosidasi** (*float > 0*): Alpha-Galactosidase

**componente_monoclonale_sierica** (*string*): opzionale

**immunofissazione_sierica** (*string*): opzionale

**immunofissazione_urinaria** (*string*): opzionale

### GET http://localhost:8000/api/esami-laboratorio/699/

### PUT http://localhost:8000/api/esami-laboratorio/699/
```json
{
    "paziente_id": 699,
    "operatore_id": 1992,
    "status": "complete",
    "created_at": "2024-11-15T10:44:40.008795Z",
    "updated_at": "2024-11-15T10:44:40.502434Z",
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
