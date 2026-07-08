// Computa R2 = max(R0, R1)  (R0, R1, R2 são RAM[0], RAM[1], RAM[2])

   @R0
   D=M              // D = primeiro número
   @R1
   D=D-M            // D = primeiro - segundo
   @OUTPUT_FIRST
   D;JGT            // se D>0, primeiro é maior: pula para OUTPUT_FIRST
   @R1
   D=M              // D = segundo número
   @OUTPUT_D
   0;JMP            // pula para OUTPUT_D
(OUTPUT_FIRST)
   @R0
   D=M              // D = primeiro número
(OUTPUT_D)
   @R2
   M=D              // RAM[2] = maior valor
(INFINITE_LOOP)
   @INFINITE_LOOP
   0;JMP            // loop infinito (fim do programa)
