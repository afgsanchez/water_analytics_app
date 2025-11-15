import os
import re
import fitz  # PyMuPDF
import pandas as pd

def extract_fecha(lines, label, offset):
    for i, line in enumerate(lines):
        if label in line:
            idx = i + offset
            if 0 <= idx < len(lines):
                match = re.search(r"\d{2}/\d{2}/\d{4}", lines[idx])
                if match:
                    return match.group(0)
    return ""

def is_param_line(line):
    # Ajusta este filtro según tus parámetros reales
    excl = [
        "AUSENCIA", "<", "=", "mg/l", "NTU", "UFC", "Factor", "Sensorial", "Filtración", "Siembra",
        "Fotometría", "Espetrofotometría", "Nefelometría", "Electrodo", "Método", "Comentarios",
        "Real Decreto", "Página", "Laboratorio", "Dirección", "Nombre", "Teléfonos", "Fax",
        "Identificación", "ANÁLISIS", "RESULTADOS", "CALIBRACIÓN", "METODOLOGÍA", "Fecha", "Nº",
        "MVCI", "100303", "Cami", "Tª", "Recogida", "Motivo", "Más información", "URB.", "CRTA.",
        "Visible", "Visual", "Sonda Termométrica", "Fotometría.", "Filtración Membrana"
    ] 


    if not line.strip():
        return False
    if any(line.strip().startswith(e) for e in excl):
        return False
    # Si la línea tiene letras y no es solo número o símbolo, es parámetro
    return bool(re.search(r"[A-Za-z]", line)) and not line.strip().startswith("*")

def analyze_pdf_parameters(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    text = page.get_text()
    lines = text.splitlines()

    print(f"\n--- Analizando PDF: {pdf_path} ---")
    print("Líneas extraídas del PDF:")
    for l in lines:
        print(l)

    fecha_toma = extract_fecha(lines, "Fecha Toma Muestra", 4)
    fecha_emision = extract_fecha(lines, "Fecha Emisión Informe", 2)
    print(f"Fecha toma muestra detectada: {fecha_toma}")
    print(f"Fecha emisión informe detectada: {fecha_emision}")

    referencia = ""
    for i, line in enumerate(lines):
        if "Referencia Cliente" in line and i > 0:
            referencia = lines[i-1].strip()
            break
    print(f"Referencia detectada: {referencia}")

    issues = []
    last_param = None
    for i, line in enumerate(lines):
        l = line.strip()
        if is_param_line(l):
            last_param = l
            print(f"Parámetro detectado: {last_param}")
        elif l.startswith("*"):
            result_val = l.replace("*", "").strip()
            # Busca la unidad en la línea anterior
            result_unit = ""
            if i > 0:
                unit_line = lines[i-1].strip()
                # Solo acepta como unidad si contiene típicas unidades de laboratorio
                unidades_posibles = [
                    "UFC/ml", "UFC/100 ml", "mg/l", "NTU", "µS/cm", "mg/l (Pt/Co)", "ºC", "CFU/ml", "UFC/l"
                ]
                if any(u in unit_line for u in unidades_posibles):
                    result_unit = unit_line
            print(f"Incumplimiento detectado: parámetro={last_param}, valor={result_val}, unidad={result_unit}")
            if last_param and result_val and result_unit:
                issues.append({
                    "IDENTIFICACION DE LA MUESTRA": referencia,
                    "FECHA TOMA MUESTRA": fecha_toma,
                    "FECHA EMISION INFORME": fecha_emision,
                    "PARÁMETRO": last_param,
                    "RESULTADO": f"{result_val} {result_unit}"
                })

    print(f"Issues encontrados en {pdf_path}: {issues}")
    return issues


def extract_value(text):
    match = re.search(r"Valor Crítico:\s*(\d+)", text)
    if match:
        return int(match.group(1))
    return None

def analyze_pdfs_in_folder(folder_path):
    all_issues = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            issues = analyze_pdf_parameters(pdf_path)
            all_issues.extend(issues)

    return pd.DataFrame(all_issues)

def main():
    input_folder = "output_pdfs"
    compliance_issues_df = analyze_pdfs_in_folder(input_folder)

    if not compliance_issues_df.empty:
        print("Se encontraron problemas de cumplimiento:")
        print(compliance_issues_df)
    else:
        print("Todos los PDFs cumplen con los criterios.")

if __name__ == "__main__":
    main()