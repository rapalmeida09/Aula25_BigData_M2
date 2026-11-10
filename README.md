# Aula25_BigData_M2
## Análise de Dados do Novo Bolsa Família com Polars

Conjunto de scripts em Python que demonstram como carregar, consolidar e armazenar os arquivos mensais do **Novo Bolsa Família** (CSV) usando **Polars**, comparando o desempenho com o **Pandas**.

O fluxo é composto por três etapas:

1. Ler os CSVs mensais e concatenar em um único DataFrame
2. Tratar os dados e salvar tudo em um arquivo **Parquet**
3. Ler o Parquet (leitura direta e leitura preguiçosa)

---

## Estrutura de pastas

Os scripts esperam encontrar os dados em uma pasta `DADOS` um nível acima da pasta onde estão os scripts:

```
.
├── DADOS/
│   ├── 202601_NovoBolsaFamilia.csv      # usado por exemplo.py
│   ├── 202602_NovoBolsaFamilia.csv
│   ├── ...
│   └── BOLSA_FAMILIA/                   # usada por exemplo01.py e exemplo02.py
│       ├── *.csv
│       └── bolsa_familia.parquet        # gerado por exemplo01.py
└── SCRIPTS/
    ├── exemplo.py
    ├── exemplo01.py
    └── exemplo02.py
```

> Os caminhos são definidos na constante `ENDERECO_DADOS` no início de cada script. Ajuste conforme a sua organização.

---

## Requisitos

- Python 3.9+
- Bibliotecas:

```bash
pip install pandas polars fastparquet
```

> **Observação:** os scripts usam `subprocess.run('cls', shell=True)` para limpar o terminal, comando que funciona apenas no **Windows**. No Linux/macOS, troque por `'clear'`.

---

## Descrição dos scripts

### `exemplo.py` — Leitura e concatenação de CSVs

Lê uma lista fixa de arquivos mensais (`202601` a `202605`), concatena todos em um único DataFrame e mede o tempo total de execução.

- Leitura com `pl.read_csv` (separador `;`, encoding `iso-8859-1`)
- União dos arquivos com `pl.concat`
- Libera o DataFrame temporário com `del df` a cada iteração
- Exibe o tempo total e, em caso de erro, a mensagem e a linha em que ocorreu

### `exemplo01.py` — Consolidação automática e exportação para Parquet

Versão mais completa: em vez de uma lista fixa, **varre a pasta** `BOLSA_FAMILIA` e processa todos os arquivos `.csv` encontrados.

1. Lista os arquivos `.csv` com `os.listdir`
2. Lê cada arquivo com Polars e concatena
3. Converte a coluna `VALOR PARCELA` de texto (vírgula decimal) para `Float64`
4. Salva o resultado em `bolsa_familia.parquet`

O bloco de leitura com Pandas está comentado no código para facilitar a comparação.

### `exemplo02.py` — Leitura do arquivo Parquet

Mostra as formas de ler o `bolsa_familia.parquet` gerado pelo script anterior:

| Método | Descrição |
|---|---|
| `pd.read_parquet` | Leitura direta com Pandas (comentado) |
| `pl.read_parquet` | Leitura direta com Polars (comentado) |
| `pl.scan_parquet` + `.collect()` | **Leitura preguiçosa (lazy):** cria um plano de execução e só carrega os dados quando `.collect()` é chamado |

A leitura preguiçosa é útil quando se encadeiam filtros e seleções de colunas antes do `collect()`, pois o Polars otimiza a consulta e lê somente o necessário.

---

## Comparativo de desempenho

Tempos anotados nos comentários dos scripts (variam conforme a máquina e o volume de dados):

| Operação | Pandas | Polars |
|---|---|---|
| Leitura de CSVs (`exemplo.py`, 1ª medição) | 0:01:07 | 0:00:19 |
| Leitura de CSVs (`exemplo.py`, 2ª medição) | 0:03:24 | 0:00:49 |
| Leitura + consolidação de CSVs (`exemplo01.py`) | 0:03:36 | 0:00:45 |
| Leitura do Parquet (`exemplo02.py`) | 0:00:24 | 0:00:08 |

Em todos os casos o Polars foi significativamente mais rápido, e a leitura do Parquet é muito mais eficiente do que reler os CSVs.

---

## Como executar

Execute na ordem:

```bash
python exemplo.py      # (opcional) teste de leitura e concatenação
python exemplo01.py    # consolida os CSVs e gera o .parquet
python exemplo02.py    # lê o .parquet gerado
```

---

## Observações e pontos de atenção

- Em `exemplo.py`, a mensagem impressa diz "Janeiro, fevereiro e março", mas a lista inclui arquivos até maio (`202605`). Vale atualizar o texto.
- Nos `print` de tempo total falta um espaço: `f'Tempo total{fim - inicio}'` → `f'Tempo total: {fim - inicio}'`.
- O `pandas` é importado em todos os scripts, mas só é usado nos trechos comentados.
- O `fastparquet` só é necessário para o Pandas; o Polars grava e lê Parquet sem ele.
- Se algum CSV tiver colunas diferentes, o `pl.concat` falhará. Nesse caso, use `pl.concat(..., how='diagonal')`.
- Se a leitura do CSV falhar ao inferir tipos, experimente `infer_schema_length=10000` ou `infer_schema=False` em `pl.read_csv`.