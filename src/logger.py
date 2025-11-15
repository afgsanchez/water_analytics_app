import pandas as pd
import os

# def log_non_compliance(non_compliance_list, output_excel_path):
#     if not isinstance(non_compliance_list, (list, tuple)) or not non_compliance_list:
#         print("No non-compliance issues to log.")
#         return

#     # Solo las columnas deseadas
#     columns = [
#         "IDENTIFICACION DE LA MUESTRA",
#         "FECHA TOMA MUESTRA",
#         "FECHA EMISION INFORME",
#         "PARÁMETRO",
#         "RESULTADO"
#     ]
#     df = pd.DataFrame(non_compliance_list)
#     df = df[columns]

#     if os.path.exists(output_excel_path):
#         try:
#             existing_df = pd.read_excel(output_excel_path)
#             df = pd.concat([existing_df, df], ignore_index=True)
#         except Exception as e:
#             print(f"Error reading existing Excel file: {e}")
#     df.to_excel(output_excel_path, sheet_name='NonCompliance', index=False)
#     print(f"Non-compliance issues logged to: {output_excel_path}")

def log_non_compliance(non_compliance_list, output_excel_path):
    if not isinstance(non_compliance_list, (list, tuple)) or not non_compliance_list:
        print("No non-compliance issues to log.")
        return

    columns = [
        "IDENTIFICACION DE LA MUESTRA",
        "FECHA TOMA MUESTRA",
        "FECHA EMISION INFORME",
        "PARÁMETRO",
        "RESULTADO"
    ]
    df = pd.DataFrame(non_compliance_list)
    df = df[columns]
    df.to_excel(output_excel_path, sheet_name='NonCompliance', index=False)
    print(f"Non-compliance issues logged to: {output_excel_path}")