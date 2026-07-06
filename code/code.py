"""
Módulo Code
-----------
Traduz os campos mnemônicos (comp, dest, jump) de uma C-instruction
para os bits binários correspondentes.
"""

COMP_TABLE = {
    # a = 0 (usa A)
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    # a = 1 (usa M no lugar de A)
    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}

JUMP_TABLE = {
    '':    '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


class Code:
    @staticmethod
    def comp(comp_str):
        if comp_str not in COMP_TABLE:
            raise ValueError(f"Campo comp inválido: '{comp_str}'")
        return COMP_TABLE[comp_str]

    @staticmethod
    def dest(dest_str):
        # ddd = bit(A) bit(D) bit(M), nessa ordem, independente de como
        # o usuário escreveu (ex: "MD" e "DM" resultam no mesmo binário)
        d1 = '1' if 'A' in dest_str else '0'
        d2 = '1' if 'D' in dest_str else '0'
        d3 = '1' if 'M' in dest_str else '0'
        return d1 + d2 + d3

    @staticmethod
    def jump(jump_str):
        if jump_str not in JUMP_TABLE:
            raise ValueError(f"Campo jump inválido: '{jump_str}'")
        return JUMP_TABLE[jump_str]
