# Assembler Hack (Nand2Tetris - Project 6)

Montador que traduz programas em Assembly Hack (`.asm`) para código de máquina
binário (`.hack`).

## 👥 Integrante

- SAMARA SANTOS VIEGAS — 2022042898

## 🛠️ Linguagem

Python 3.x (testado com Python 3.11)

## 📁 Estrutura do projeto

```
assembler/
├── parser/
│   └── parser.py        # leitura e interpretação das instruções
├── symbol_table/
│   └── symbol_table.py  # tabela de símbolos (labels e variáveis)
├── code/
│   └── code.py           # tradução dos campos comp/dest/jump para binário
├── tests/
│   ├── add.asm
│   └── max.asm
├── main.py                # orquestrador (duas passagens)
└── README.md
```

## ▶️ Como executar

Não é necessário instalar nenhuma dependência externa (apenas Python padrão).

```bash
python main.py caminho/para/arquivo.asm
```

Exemplo:

```bash
python main.py tests/add.asm
```

Isso vai gerar o arquivo `tests/add.hack` na mesma pasta do `.asm`.

## 🧪 Testes realizados

- ✅ `add.asm`
- ✅ `max.asm`
- ✅ `rect.asm`
- ✅ `pong.asm`

Para validar, compare o `.hack` gerado com o esperado, ou carregue o arquivo
no CPU Emulator do Nand2Tetris e verifique o comportamento do programa.

## 🎥 Vídeo de Apresentação

link: https://drive.google.com/drive/folders/1g0F49ZfFRoSRRQJbKrz2NGJokX8aPctX?usp=drive_link 


