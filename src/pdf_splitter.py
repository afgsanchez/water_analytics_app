import os
import re
import fitz  # PyMuPDF
from analyzer import analyze_pdf_parameters
from logger import log_non_compliance

def extract_reference(text):
    """
    Extrae la referencia del cliente de la página.
    Busca la línea anterior a 'Referencia Cliente'.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "Referencia Cliente" in line:
            # Busca la línea anterior, si existe
            if i > 0:
                reference = lines[i-1].strip()
                reference = re.sub(r'[\\/*?:\"<>|]', "_", reference)
                return reference
    return f"pagina_sin_referencia"



def split_pdf_by_reference(input_pdf_path, output_folder, log_file="non_compliance_log.xlsx"):
    """
    Agrupa las páginas del PDF por referencia del cliente y guarda un PDF por referencia.
    Analiza cada PDF por cumplimiento y registra los problemas encontrados.
    """
    doc = fitz.open(input_pdf_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Diccionario para agrupar páginas por referencia
    reference_pages = {}

    for i, page in enumerate(doc):
        text = page.get_text()
        reference = extract_reference(text)

        if reference not in reference_pages:
            reference_pages[reference] = []
        reference_pages[reference].append(i)

    # Crear un PDF por referencia
    for reference, pages in reference_pages.items():
        new_doc = fitz.open()
        for page_num in pages:
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        output_path = os.path.join(output_folder, f"{reference}.pdf")
        new_doc.save(output_path)
        new_doc.close()

        print(f"PDF guardado para referencia '{reference}' con {len(pages)} página(s): {output_path}")

        # Analizar el PDF por cumplimiento
        non_compliance_issues = analyze_pdf_parameters(output_path)
        if non_compliance_issues and isinstance(non_compliance_issues, (list, tuple)):
            for issue in non_compliance_issues:
                if "Referencia" not in issue:
                    issue["Referencia"] = reference
            log_non_compliance(non_compliance_issues, log_file)


# Example usage
if __name__ == "__main__":
    input_pdf = "input_pdfs/analiticas_completas.pdf"
    output_dir = "output_pdfs"
    log_file = "non_compliance_log.xlsx"
    split_pdf_by_reference(input_pdf, output_dir, log_file)