# pip install pandas polars fastparquet
import subprocess
import pandas as pd
import polars as pl
from datetime import datetime

subprocess.run('cls', shell=True)

ENDERECO_DADOS = './../DADOS/BOLSA_FAMILIA/'

try:
    inicio = datetime.now()
    print('Obtendo dados parquet...')

    # Pandas: Tempo total: 0:00:24.67
    # df_bolsa_familia = pd.read_parquet(ENDERECO_DADOS + 'bolsa_familia.parquet')
    # print(df_bolsa_familia.head())

    # Polars: Tempo total: 0:00:08.82
    # Polars - Leitura direta
    # df_bolsa_familia = pl.read_parquet(ENDERECO_DADOS + 'bolsa_familia.parquet') 
    # print(df_bolsa_familia.head())
    
    # Scan Parquet: 
    # Cria um plano de execução. Não obtem os dados direto.
    # Polars Leitura preguiçosa
    df_bolsa_familia = pl.scan_parquet(ENDERECO_DADOS + 'bolsa_familia.parquet') 

    # Collect: Executa o plano de execução e traz os dados
    df_bolsa_familia = df_bolsa_familia.collect()
    print(df_bolsa_familia.head())







    fim = datetime.now()
    print(f'Tempo total{fim - inicio}')

except Exception as e:
    print(f'Erro ao obter dados parquet - {e}')
    print(f'Linha: {e.__traceback__.tb_lineno}')