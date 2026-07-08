"""
Módulo Code
-----------
Responsável por traduzir os campos mnemônicos (comp, dest e jump)
das instruções do tipo C da linguagem Hack para seus respectivos
códigos binários.
"""

# Tabela de conversão do campo "comp" para binário.
# Cada chave representa uma operação da linguagem Hack e
# o valor corresponde aos 7 bits que representam essa operação.
COMP_TABLE = {
    # a = 0 (operações utilizando o registrador A)
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

    # a = 1 (operações utilizando a memória M)
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

# Tabela de conversão do campo "jump".
# Cada instrução de salto é convertida para um código binário de 3 bits.
JUMP_TABLE = {
    '':    '000',  # Sem salto
    'JGT': '001',  # Salta se maior que zero
    'JEQ': '010',  # Salta se igual a zero
    'JGE': '011',  # Salta se maior ou igual a zero
    'JLT': '100',  # Salta se menor que zero
    'JNE': '101',  # Salta se diferente de zero
    'JLE': '110',  # Salta se menor ou igual a zero
    'JMP': '111',  # Salto incondicional
}


class Code:
    """
    Classe responsável por converter os campos de uma instrução
    do tipo C para sua representação binária.
    """

    @staticmethod
    def comp(comp_str):
        """
        Recebe uma operação (campo comp) e retorna
        seu código binário de 7 bits.

        Exemplo:
            "D+1" -> "0011111"
        """
        # Verifica se a operação existe na tabela.
        if comp_str not in COMP_TABLE:
            raise ValueError(f"Campo comp inválido: '{comp_str}'")

        # Retorna o código binário correspondente.
        return COMP_TABLE[comp_str]

    @staticmethod
    def dest(dest_str):
        """
        Converte o campo dest para 3 bits.

        A ordem dos bits é sempre:
        A D M

        Assim, a posição das letras na string não importa.

        Exemplos:
            ""    -> 000
            "M"   -> 001
            "D"   -> 010
            "A"   -> 100
            "MD"  -> 011
            "DM"  -> 011
            "AMD" -> 111
        """

        # Define o primeiro bit (registrador A).
        d1 = '1' if 'A' in dest_str else '0'

        # Define o segundo bit (registrador D).
        d2 = '1' if 'D' in dest_str else '0'

        # Define o terceiro bit (memória M).
        d3 = '1' if 'M' in dest_str else '0'

        # Retorna os três bits concatenados.
        return d1 + d2 + d3

    @staticmethod
    def jump(jump_str):
        """
        Recebe o campo jump e retorna seu
        código binário de 3 bits.

        Exemplo:
            "JGT" -> "001"
        """

        # Verifica se o comando de salto é válido.
        if jump_str not in JUMP_TABLE:
            raise ValueError(f"Campo jump inválido: '{jump_str}'")

        # Retorna o código binário correspondente.
        return JUMP_TABLE[jump_str]