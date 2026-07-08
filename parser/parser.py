"""
Módulo Parser
-------------
Responsável por ler um arquivo .asm, remover comentários e espaços
desnecessários e disponibilizar cada instrução separadamente,
permitindo acessar seus campos (symbol, dest, comp e jump).
"""


class Parser:
    """
    Classe responsável pela leitura e análise (parse) das instruções
    de um arquivo Assembly da arquitetura Hack.
    """

    # Constantes que representam os tipos de instrução.
    A_INSTRUCTION = 'A_INSTRUCTION'
    C_INSTRUCTION = 'C_INSTRUCTION'
    L_INSTRUCTION = 'L_INSTRUCTION'  # Label, exemplo: (LOOP)

    def __init__(self, filename):
        """
        Lê o arquivo .asm, remove comentários e espaços
        desnecessários e armazena apenas as instruções válidas.
        """

        # Abre o arquivo Assembly para leitura.
        with open(filename, 'r', encoding='utf-8') as f:
            raw_lines = f.readlines()

        # Lista onde serão armazenadas as instruções limpas.
        self.instructions = []

        # Processa cada linha do arquivo.
        for line in raw_lines:

            # Remove comentários (tudo após "//").
            clean = line.split('//')[0].strip()

            # Remove espaços e tabulações.
            clean = clean.replace(' ', '').replace('\t', '')

            # Adiciona somente linhas que não estejam vazias.
            if clean:
                self.instructions.append(clean)

        # Inicializa o ponteiro das instruções.
        self.current_index = -1

        # Armazena a instrução atualmente sendo processada.
        self.current_instruction = None

    def hasMoreInstructions(self):
        """
        Verifica se ainda existem instruções
        para serem processadas.

        Retorna:
            True  -> ainda há instruções.
            False -> chegou ao final do arquivo.
        """
        return self.current_index < len(self.instructions) - 1

    def advance(self):
        """
        Avança para a próxima instrução,
        tornando-a a instrução atual.
        """

        self.current_index += 1
        self.current_instruction = self.instructions[self.current_index]

    def instructionType(self):
        """
        Identifica o tipo da instrução atual.

        Retorna:
            A_INSTRUCTION -> instrução iniciada por '@'
            L_INSTRUCTION -> label entre parênteses
            C_INSTRUCTION -> instrução de cálculo
        """

        instr = self.current_instruction

        if instr.startswith('@'):
            return self.A_INSTRUCTION

        elif instr.startswith('(') and instr.endswith(')'):
            return self.L_INSTRUCTION

        else:
            return self.C_INSTRUCTION

    def symbol(self):
        """
        Retorna o símbolo associado à instrução atual.

        Deve ser utilizado apenas para:
        - A_INSTRUCTION (@valor ou @simbolo)
        - L_INSTRUCTION ((LABEL))
        """

        instr = self.current_instruction

        if self.instructionType() == self.A_INSTRUCTION:
            # Remove o caractere '@'.
            return instr[1:]

        elif self.instructionType() == self.L_INSTRUCTION:
            # Remove os parênteses.
            return instr[1:-1]

        # Gera erro caso seja chamado para C_INSTRUCTION.
        raise ValueError(
            'symbol() só pode ser chamado em A_INSTRUCTION ou L_INSTRUCTION'
        )

    def dest(self):
        """
        Retorna o campo 'dest' de uma C-instruction.

        Exemplos:
            D=M   -> D
            MD=D+1 -> MD
            0;JMP -> ""
        """

        instr = self.current_instruction

        # Se existir '=', tudo antes dele corresponde ao destino.
        if '=' in instr:
            return instr.split('=')[0]

        # Caso contrário, não existe campo dest.
        return ''

    def comp(self):
        """
        Retorna o campo 'comp' da instrução.

        Exemplos:
            D=M+1   -> M+1
            D;JGT   -> D
            MD=D|A  -> D|A
        """

        instr = self.current_instruction

        # Remove a parte do destino, caso exista.
        body = instr.split('=')[-1] if '=' in instr else instr

        # Remove a parte do salto, caso exista.
        body = body.split(';')[0]

        return body

    def jump(self):
        """
        Retorna o campo 'jump' da instrução.

        Exemplos:
            D;JGT -> JGT
            0;JMP -> JMP
            D=A   -> ""
        """

        instr = self.current_instruction

        # Se existir ';', tudo após ele corresponde ao salto.
        if ';' in instr:
            return instr.split(';')[1]

        # Caso contrário, não existe campo jump.
        return ''

    def reset(self):
        """
        Reinicia o parser para o início do arquivo.

        Utilizado quando é necessário fazer uma
        segunda passagem pelas instruções.
        """

        self.current_index = -1
        self.current_instruction = None