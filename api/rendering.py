from pdfdocument.document import PDFDocument
from io import BytesIO, BufferedReader
from urllib.parse import quote
import requests

# per formattazione https://docs.reportlab.com/rmlfornewbies/
translation = {"structure": "Struttura"}
structure_fields = {"name", "phone_number"}
user_fields = ["first_name", "last_name", "birthday"]
ignore_fields = ["structure", "paziente_id", "operatore_id", "datamanager_id", "status", "updated_at"]

def renderjson(file: PDFDocument, key, value, depth=1):
    if value is None:
        return
    tkey = translation.get(key, key)
    if isinstance(value, (str, int, float)):
        file.p_markup(f"<para><B>{tkey}</B>: {value}</para>")
    elif isinstance(value, (bool)):
        if value:
            file.p(f"**{tkey}**: Sì")
        else:
            file.p(f"**{tkey}**: No")
    else:
        
        if depth == 1:
            file.h1(tkey)
        if depth == 2:
            file.h2(tkey)
        if depth >= 3:
            file.h3(tkey)

        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                renderjson(file, subkey, subvalue, depth+1)

        elif isinstance(value, (list, tuple)):
            if value and isinstance(value[0], dict):
                for element in value:
                    for subkey, subvalue in element.items():
                        renderjson(file, subkey, subvalue, depth+1)
            else:
                file.ul(value)

class PdfMixin:

    def render_report(self, operator, patient, report, dossier_id):
        f = BytesIO()
        pdf = PDFDocument(f)
        pdf.init_report()

    
        renderjson(pdf, "Struttura", f"{report.get('structure').get('name')}")
        renderjson(pdf, "Specialista", f"Dr. {operator['first_name']} {operator['last_name']}")
        renderjson(pdf, "Paziente", f"{patient['first_name']} {patient['last_name']}")

        for key, value in report.items():
            if key not in ignore_fields:
                renderjson(pdf, key, value)
        
        pdf.generate()
        
        fname = "{report} {name} {date}.pdf".format(
            report=self.__class__.__name__[:-7],
            name= f"{patient['first_name']} {patient['last_name']}",
            date=report["created_at"][:10]
        )
        f.seek(0)
        
        auth_header = self.request.META.get('HTTP_AUTHORIZATION')
        headers = {"Authorization": auth_header,
                "Content-Disposition": f"inline; filename*=UTF-8''{quote(fname)}",
                "Content-Type": "application/pdf"}
                #'Accept': 'application/json'}
        response = requests.post(
            f"https://mymedbook.it/api/v1/upload/dossier/{dossier_id}/",
            headers=headers,
            files={"file": BufferedReader(f)}
        )
        return response
    
