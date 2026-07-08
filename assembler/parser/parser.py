"""
Módulo Parser
-------------
Responsável por ler um arquivo .asm, remover comentários/espaços em branco
e disponibilizar as instruções, uma por vez, já "quebradas" em suas partes
(symbol, dest, comp, jump).
"""


class Parser:
    A_INSTRUCTION = 'A_INSTRUCTION'
    C_INSTRUCTION = 'C_INSTRUCTION'
    L_INSTRUCTION = 'L_INSTRUCTION'  # Label, ex: (LOOP)

    def __init__(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            raw_lines = f.readlines()

        self.instructions = []
        for line in raw_lines:
            # remove comentários (tudo que vem depois de //)
            clean = line.split('//')[0].strip()
            # remove espaços internos (ex: "D = M" -> "D=M")
            clean = clean.replace(' ', '').replace('\t', '')
            if clean:  # ignora linhas vazias
                self.instructions.append(clean)

        self.current_index = -1
        self.current_instruction = None

    def hasMoreInstructions(self):
        """Retorna True se ainda existe instrução a ser lida."""
        return self.current_index < len(self.instructions) - 1

    def advance(self):
        """Avança para a próxima instrução, tornando-a a instrução atual."""
        self.current_index += 1
        self.current_instruction = self.instructions[self.current_index]

    def instructionType(self):
        instr = self.current_instruction
        if instr.startswith('@'):
            return self.A_INSTRUCTION
        elif instr.startswith('(') and instr.endswith(')'):
            return self.L_INSTRUCTION
        else:
            return self.C_INSTRUCTION

    def symbol(self):
        """Usado apenas quando instructionType() é A_INSTRUCTION ou L_INSTRUCTION."""
        instr = self.current_instruction
        if self.instructionType() == self.A_INSTRUCTION:
            return instr[1:]
        elif self.instructionType() == self.L_INSTRUCTION:
            return instr[1:-1]
        raise ValueError('symbol() só pode ser chamado em A_INSTRUCTION ou L_INSTRUCTION')

    def dest(self):
        """Usado apenas quando instructionType() é C_INSTRUCTION."""
        instr = self.current_instruction
        if '=' in instr:
            return instr.split('=')[0]
        return ''

    def comp(self):
        """Usado apenas quando instructionType() é C_INSTRUCTION."""
        instr = self.current_instruction
        body = instr.split('=')[-1] if '=' in instr else instr
        body = body.split(';')[0]
        return body

    def jump(self):
        """Usado apenas quando instructionType() é C_INSTRUCTION."""
        instr = self.current_instruction
        if ';' in instr:
            return instr.split(';')[1]
        return ''

    def reset(self):
        """Volta o ponteiro para o início (usado para a segunda passagem)."""
        self.current_index = -1
        self.current_instruction = None
