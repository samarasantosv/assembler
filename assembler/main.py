"""
Assembler Hack - Nand2Tetris Project 6
----------------------------------------
Uso:
    python main.py caminho/para/arquivo.asm

Gera um arquivo .hack no mesmo diretório do arquivo de entrada.
"""

import sys
import os

# Garante que as pastas parser/, symbol_table/ e code/ sejam encontradas
# mesmo que este script seja executado de outro diretório.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser.parser import Parser
from symbol_table.symbol_table import SymbolTable
from code.code import Code


def encode_a_instruction(symbol, symbol_table):
    if symbol.isdigit():
        value = int(symbol)
    else:
        value = symbol_table.getAddress(symbol)
    return '0' + format(value, '015b')


def encode_c_instruction(dest, comp, jump):
    return '111' + Code.comp(comp) + Code.dest(dest) + Code.jump(jump)


def first_pass(filename, symbol_table):
    """Primeira passagem: registra todos os labels (LOOP), (END) etc.
    com o endereço da instrução seguinte."""
    parser = Parser(filename)
    address = 0
    while parser.hasMoreInstructions():
        parser.advance()
        itype = parser.instructionType()
        if itype == Parser.L_INSTRUCTION:
            label = parser.symbol()
            symbol_table.addEntry(label, address)
        else:
            address += 1  # só A e C instructions ocupam endereço de memória


def second_pass(filename, symbol_table, output_file):
    """Segunda passagem: resolve variáveis e gera o código binário final."""
    parser = Parser(filename)
    lines_out = []

    while parser.hasMoreInstructions():
        parser.advance()
        itype = parser.instructionType()

        if itype == Parser.A_INSTRUCTION:
            symbol = parser.symbol()
            if not symbol.isdigit():
                symbol_table.addVariable(symbol)
            binary = encode_a_instruction(symbol, symbol_table)
            lines_out.append(binary)

        elif itype == Parser.C_INSTRUCTION:
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            binary = encode_c_instruction(dest, comp, jump)
            lines_out.append(binary)

        # L_INSTRUCTION (labels) não geram linha de código

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write('\n'.join(lines_out) + '\n')


def main():
    if len(sys.argv) != 2:
        print('Uso: python main.py caminho/para/arquivo.asm')
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith('.asm'):
        print('Erro: o arquivo de entrada deve ter extensão .asm')
        sys.exit(1)
    if not os.path.isfile(input_file):
        print(f'Erro: arquivo não encontrado: {input_file}')
        sys.exit(1)

    output_file = input_file.replace('.asm', '.hack')

    symbol_table = SymbolTable()

    first_pass(input_file, symbol_table)
    second_pass(input_file, symbol_table, output_file)

    print(f'✅ Arquivo gerado com sucesso: {output_file}')


if __name__ == '__main__':
    main()
