import pandas as pd
import connectio_DB

def DB_search(nfList):
    conexao = connectio_DB.conexao

    # Garante que as colunas estão no formato string
    nfList['Serie'] = nfList['Serie'].astype(str)
    nfList['NF'] = nfList['NF'].astype(str)

    # Cria a lista de chaves no formato "Serie|NF"
    lista_chaves = nfList.apply(lambda row: f"{row['Serie']}|{row['NF']}", axis=1)

    # Cria placeholders para a query SQL
    place_holders = ','.join(['?'] * len(lista_chaves))

    # Query compatível com SQL Server (ajustada para Serie|NF)
    query = f'''
        SELECT STATUS, NF, SERIE FROM NFC_CAB
        WHERE CAST(SERIE AS VARCHAR) + '|' + CAST(NF AS VARCHAR) IN ({place_holders})
    '''

    # Executa a consulta
    df_resultado = pd.read_sql(query, conexao, params=lista_chaves.tolist())

    # Traduz o status para texto legível
    df_resultado['STATUS'] = df_resultado['STATUS'].map({1: 'Concluida'}).fillna('Pendente')

    # Renomeia colunas para compatibilizar com o DataFrame original
    df_resultado.rename(columns={'SERIE': 'Serie', 'NF': 'NF', 'STATUS': 'STATUS'}, inplace=True)

    # Faz o merge com base nas colunas esperadas
    resultado_final = nfList.merge(df_resultado, on=['NF', 'Serie'], how='left')

    return resultado_final
