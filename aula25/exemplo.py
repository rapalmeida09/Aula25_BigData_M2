import subprocess
import pandas as pd
from datetime import datetime
import polars as pl

subprocess.run('cls', shell=True)
ENDERECO_DADOS = './../DADOS/'

# Obtendo Janeiro e Fevereiro
try:
    inicio = datetime.now()
    print('Obtendo os dados de Janeiro, fevereiro e março')

    lista_arquivos = [
        '202601_NovoBolsaFamilia.csv',
        '202602_NovoBolsaFamilia.csv',
        '202603_NovoBolsaFamilia.csv',
        '202604_NovoBolsaFamilia.csv',
        '202605_NovoBolsaFamilia.csv'
        ]
    
    df_bolsa_familia = None
    # Pandas - Tempo total: 0:01:07.72  -  Tempo total: 0:03:24.32
    # Polars - Tempo total: 0:00:19.99  -  Tempo total: 0:00:49.29
    for arquivo in lista_arquivos:
        df = pl.read_csv(   # pd / pl
            ENDERECO_DADOS + arquivo,
            separator=';',  # Sep= / separator=
            encoding='iso-8859-1'
    )
        print(df)

        if df_bolsa_familia is None:
            df_bolsa_familia = df
        else:
            df_bolsa_familia = pl.concat([df_bolsa_familia, df])  # pd / pl

        del df # Deleta o dataframe temporário 'df'

    print(df_bolsa_familia)

    fim = datetime.now()
    print(f'Tempo total{fim - inicio}')

except Exception as e:
    print(f'Erro ao obter dados - {e}')
    print(f'Linha: {e.__traceback__.tb_lineno}')