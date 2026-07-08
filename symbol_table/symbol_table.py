"""
Módulo SymbolTable
------------------
Responsável por gerenciar a tabela de símbolos do montador Hack.

Armazena o mapeamento entre símbolos (labels e variáveis)
e seus respectivos endereços de memória, incluindo os
símbolos predefinidos da arquitetura Hack.
"""


class SymbolTable:
    """
    Classe que implementa a tabela de símbolos utilizada
    durante a montagem do programa Assembly.
    """

    def __init__(self):
        """
        Inicializa a tabela de símbolos com todos os
        símbolos predefinidos da arquitetura Hack.
        """

        # Dicionário contendo os símbolos reservados
        # e seus respectivos endereços de memória.
        self.symbols = {
            # Registradores de uso geral.
            'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4,
            'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9,
            'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13,
            'R14': 14, 'R15': 15,

            # Ponteiros do sistema.
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,

            # Endereços especiais de memória.
            'SCREEN': 16384,
            'KBD': 24576,
        }

        # Primeiro endereço disponível para armazenar variáveis.
        # Na arquitetura Hack, as variáveis começam no endereço 16.
        self.next_address = 16

    def addEntry(self, symbol, address):
        """
        Adiciona um símbolo à tabela com um endereço específico.

        Geralmente utilizado para registrar labels
        encontrados durante a primeira passagem.
        """

        self.symbols[symbol] = address

    def contains(self, symbol):
        """
        Verifica se um símbolo já existe na tabela.

        Retorna:
            True  -> símbolo encontrado.
            False -> símbolo não existe.
        """

        return symbol in self.symbols

    def addVariable(self, symbol):
        """
        Adiciona uma variável à tabela.

        Caso a variável ainda não exista, ela recebe
        automaticamente o próximo endereço livre,
        iniciando no endereço 16.

        Retorna o endereço associado à variável.
        """

        if symbol not in self.symbols:
            self.symbols[symbol] = self.next_address

            # Atualiza o próximo endereço disponível.
            self.next_address += 1

        return self.symbols[symbol]

    def getAddress(self, symbol):
        """
        Retorna o endereço associado ao símbolo informado.

        Caso o símbolo não exista, retorna None.
        """

        return self.symbols.get(symbol)