"""
Assembler Hack - Nand2Tetris Project 6
--------------------------------------
Programa principal do montador (Assembler) da arquitetura Hack.

Recebe um arquivo Assembly (.asm), realiza duas passagens sobre ele
para resolver labels e variáveis e gera o arquivo binário (.hack).

Uso:
    python main.py caminho/para/arquivo.asm
"""

import sys
import os

# Adiciona o diretório atual ao caminho de busca do Python.
# Isso garante que os módulos parser, symbol_table e code
# possam ser importados independentemente do diretório
# de onde o programa foi executado.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa os módulos responsáveis pela análise,
# tabela de símbolos e tradução para código binário.
from parser.parser import Parser
from symbol_table.symbol_table import SymbolTable
from code.code import Code


def encode_a_instruction(symbol, symbol_table):
    """
    Converte uma A-instruction para seu formato binário.

    Se o símbolo for um número, ele é utilizado diretamente.
    Caso contrário, busca seu endereço na tabela de símbolos.

    Retorna uma string de 16 bits iniciada por '0'.
    """

    # Verifica se o símbolo representa um endereço numérico.
    if symbol.isdigit():
        value = int(symbol)
    else:
        # Obtém o endereço associado ao símbolo.
        value = symbol_table.getAddress(symbol)

    # Converte o endereço para binário de 15 bits
    # e adiciona o bit inicial da A-instruction.
    return '0' + format(value, '015b')


def encode_c_instruction(dest, comp, jump):
    """
    Converte uma C-instruction para sua representação binária.

    Estrutura:
        111 + comp + dest + jump

    Retorna uma string de 16 bits.
    """

    return '111' + Code.comp(comp) + Code.dest(dest) + Code.jump(jump)


def first_pass(filename, symbol_table):
    """
    Primeira passagem pelo arquivo Assembly.

    Percorre todas as instruções procurando labels
    (por exemplo: (LOOP), (END)).

    Cada label é armazenada na tabela de símbolos
    com o endereço da próxima instrução executável.
    """

    parser = Parser(filename)

    # Endereço atual da memória de instruções.
    address = 0

    while parser.hasMoreInstructions():
        parser.advance()

        itype = parser.instructionType()

        # Se encontrar uma label, registra seu endereço.
        if itype == Parser.L_INSTRUCTION:
            label = parser.symbol()
            symbol_table.addEntry(label, address)

        else:
            # Apenas instruções A e C ocupam posições
            # na memória de instruções.
            address += 1


def second_pass(filename, symbol_table, output_file):
    """
    Segunda passagem pelo arquivo.

    Resolve variáveis, traduz todas as instruções
    para código binário e gera o arquivo .hack.
    """

    parser = Parser(filename)

    # Lista que armazenará todas as instruções binárias.
    lines_out = []

    while parser.hasMoreInstructions():
        parser.advance()

        itype = parser.instructionType()

        # Processa instruções do tipo A.
        if itype == Parser.A_INSTRUCTION:

            symbol = parser.symbol()

            # Se não for um endereço numérico,
            # trata como variável.
            if not symbol.isdigit():
                symbol_table.addVariable(symbol)

            # Converte para binário.
            binary = encode_a_instruction(symbol, symbol_table)

            lines_out.append(binary)

        # Processa instruções do tipo C.
        elif itype == Parser.C_INSTRUCTION:

            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()

            # Converte para binário.
            binary = encode_c_instruction(dest, comp, jump)

            lines_out.append(binary)

        # Labels não geram código binário,
        # portanto são ignoradas nesta etapa.

    # Escreve todas as instruções no arquivo de saída.
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write('\n'.join(lines_out) + '\n')


def main():
    """
    Função principal do programa.

    Realiza a validação do arquivo de entrada,
    executa as duas passagens do montador
    e gera o arquivo .hack correspondente.
    """

    # Verifica se o usuário informou exatamente um argumento.
    if len(sys.argv) != 2:
        print('Uso: python main.py caminho/para/arquivo.asm')
        sys.exit(1)

    input_file = sys.argv[1]

    # Verifica se o arquivo possui extensão .asm.
    if not input_file.endswith('.asm'):
        print('Erro: o arquivo de entrada deve ter extensão .asm')
        sys.exit(1)

    # Verifica se o arquivo realmente existe.
    if not os.path.isfile(input_file):
        print(f'Erro: arquivo não encontrado: {input_file}')
        sys.exit(1)

    # Define o nome do arquivo de saída.
    output_file = input_file.replace('.asm', '.hack')

    # Cria a tabela de símbolos já inicializada
    # com os símbolos reservados da arquitetura.
    symbol_table = SymbolTable()

    # Primeira passagem: registra todas as labels.
    first_pass(input_file, symbol_table)

    # Segunda passagem: gera o código binário.
    second_pass(input_file, symbol_table, output_file)

    # Informa ao usuário que o processo foi concluído.
    print(f'✅ Arquivo gerado com sucesso: {output_file}')


# Executa o programa apenas quando este arquivo
# for chamado diretamente pela linha de comando.
if __name__ == '__main__':
    main()