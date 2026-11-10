# pip install pandas polars fastparquet
import subprocess
import pandas as pd
import polars as pl
from datetime import datetime
import os


subprocess.run('cls', shell=True)

ENDERECO_DADOS = './../DADOS/BOLSA_FAMILIA/'

# Pandas Tempo total: 0:03:36.89
# Polar Tempo total: 0:00:45.06
try:
    inicio = datetime.now()
    print('Obtendo dados de bolsa Família...')

    df_bolsa_familia = None
    lista_arquivos = []

    lista_dir_arquivos = os.listdir(ENDERECO_DADOS)

    for arquivo in lista_dir_arquivos:
        if arquivo.endswith('.csv'):
            lista_arquivos.append(arquivo)

    # ### Obtendo os DataFrames
    for arquivo in lista_arquivos:
        print(f'\nProcessando o arquivo {arquivo}...')
    # ### Pandas
    #     df = pd.read_csv(  # pd / pl
    #         ENDERECO_DADOS + arquivo,
    #         sep=';', # Sep= / separator=
    #         encoding='iso8859-1'
    # ) 
        
    # ### Polars
        df = pl.read_csv(  # pd / pl
            ENDERECO_DADOS + arquivo,
            separator=';', # Sep= / separator=
            encoding='iso8859-1'
    ) 

        if df_bolsa_familia is None:
            df_bolsa_familia = df
        else:
            df_bolsa_familia = pl.concat([df_bolsa_familia, df])  # pd / pl

        del df # Deleta o dataframe temporário 'df'

        print(df_bolsa_familia.head())
        print(f'\nArquivo {arquivo} processado com sucesso!')
    
    print(f'Dados concatenados com sucesso!!!')
    print(df_bolsa_familia)


    fim = datetime.now()
    print(f'Tempo total{fim - inicio}')
except Exception as e:
    print(f'Erro ao obter dados - {e}')
    print(f'Linha: {e.__traceback__.tb_lineno}')

try:
    df_bolsa_familia = df_bolsa_familia.with_columns(
        pl.col('VALOR PARCELA')
        .str.replace(',', '.')
        .cast(pl.Float64)
    )

    print(df_bolsa_familia)

    # Salvando em arquivo parquet
    # instalar biblioteca FASTPARQUET
    print(f'\nSalvando arquivo parquet...')
    df_bolsa_familia.write_parquet('./../DADOS/BOLSA_FAMILIA/bolsa_familia.parquet')
    print('Arquivo parquet criado com sucesso!!!')

except Exception as e:
    print(f'Erro ao salvar arquivo - {e}')
    print(f'Linha: {e.__traceback__.tb_lineno}')