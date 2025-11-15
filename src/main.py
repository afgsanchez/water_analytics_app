import os
from pdf_splitter import split_pdf_by_reference
from logger import log_non_compliance
from analyzer import analyze_pdfs_in_folder, analyze_pdf_parameters

def main(input_pdf_path, output_folder, log_file):
    split_pdf_by_reference(input_pdf_path, output_folder)

    all_issues = []
    for filename in os.listdir(output_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(output_folder, filename)
            non_compliance_issues = analyze_pdf_parameters(pdf_path)
            if non_compliance_issues:
                all_issues.extend(non_compliance_issues)

    if all_issues:
        log_non_compliance(all_issues, log_file)
        
    else:
        print("\n--- TODOS LOS ANÁLISIS CUMPLEN CON LOS CRITERIOS. ---")
        
    # Abrir el Excel automáticamente en Windows
    os.startfile(log_file)
        # Abrir la carpeta de salida automáticamente en Windows
    os.startfile(output_folder)

if __name__ == "__main__":
    input_pdf = input("Introduce la ruta del archivo PDF a procesar: ").strip()
    output_dir = "output_pdfs"
    log_file = "non_compliance_log.xlsx"
    main(input_pdf, output_dir, log_file)