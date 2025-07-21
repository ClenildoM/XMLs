from openpyxl import load_workbook
from datetime import date
from XMLToExcel_NFe import ToExcel
def OverWriteExcel():
    # Executa a função que retorna um DataFrame
    df = ToExcel()

    # Carrega o arquivo existente
    workbook = load_workbook("NFe_distribuidoras.xlsx")

    # Cria nova aba com a data de hoje
    datetoday = date.today().strftime("%d-%b-%Y")
    new_sheet = workbook.create_sheet(datetoday)

    # Escreve o cabeçalho na linha 1
    new_sheet.append(df.columns.tolist())

    # Escreve os dados linha a linha
    for row in df.itertuples(index=False):
        new_sheet.append(list(row))

    # Salva o arquivo modificado
    workbook.save("NFe_distribuidoras.xlsx")
