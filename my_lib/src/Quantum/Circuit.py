import random
import math
from qat.lang.AQASM import Program, H, CNOT, RX, RY, RZ
from qat.qpus import PyLinalg



class circuitBuilder:

    def __init__(self, layers=1, parameterization='Simple', random = True, *kwargs):
        self.layers = layers
        self.parameterization = parameterization

        if not random:
            pass  # load vocabulary parameters
        elif random:
            self.random = True

    def executecircuit(self):
        quantumcircuit = self.qlmprogram.to_circ()
        job = quantumcircuit.to_job()
        qpu = PyLinalg()
        result = qpu.submit(job)
        self.result = result

    def preparewords(self, sentence, my_program):

        qbits_reg = my_program.registers[0]
        for word, qword in sentence.dictionary.dictionary.items():
            for gate in qword.gateset:
                if gate['Gate'] == 'RY':
                    my_program.apply(RY(gate['Angle']), qbits_reg[gate['Qubit']])
                elif gate['Gate'] == 'RZ':
                    my_program.apply(RZ(gate['Angle']), qbits_reg[gate['Qubit']])
                elif gate['Gate'] == 'H':
                    my_program.apply(H, qbits_reg[gate['Qubit']])
                elif gate['Gate'] == 'CX':
                    my_program.apply(CNOT, qbits_reg[gate['Qubit'][0]], qbits_reg[gate['Qubit'][1]])
        return my_program


    def contractqubits(self, sentence, my_program):
        contractions = sentence.contractions
        qbits_reg = my_program.registers[0]
        for contraction in contractions:
            leftqbits = contraction[0]
            rightqbits = contraction[1]
            for i in range(len(leftqbits)):
                my_program.apply(CNOT, qbits_reg[leftqbits[i]], qbits_reg[rightqbits[i]])
                my_program.apply(H, qbits_reg[leftqbits[i]])
        return my_program


    def createcircuit(self, sentence):
        totqubits = sentence.qubitsarray[-1][-1] + 1
        my_program = Program()
        my_program.qalloc(totqubits)
        my_program.calloc(totqubits)
        my_program = self.preparewords(sentence,my_program)
        my_program = self.contractqubits(sentence,my_program)
        self.qlmprogram = my_program