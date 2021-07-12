import random
import math
from qat.lang.AQASM import Program, H, CNOT, RX, RY, RZ
from qat.qpus import get_default_qpu


class circuitBuilder:

    def __init__(self, layers=1, parameterization='Simple', random = True, *kwargs):
        self.layers = layers
        self.parameterization = parameterization

        if not random:
            pass  # load vocabulary parameters
        elif random:
            self.random = True

    def setwordparameters(self, myword, mysentence):
        wordposition = mysentence.dictionary.dictionary[myword].pos
        wordqubits = mysentence.qubitsarray[wordposition]
        gates = []
        if self.random:
            if self.parameterization == 'Simple':  # Two rotations + C-NOT gate per layer
                for layer in range(self.layers):
                    for qubit in wordqubits:
                        ry = 2 * math.pi * random.random()
                        rz = 2 * math.pi * random.random()
                        gates.append(dict({'Gate': 'RY', 'Angle': ry, 'Qubit': qubit}))
                        gates.append(dict({'Gate': 'RZ', 'Angle': rz, 'Qubit': qubit}))
                    for qubit in wordqubits[:-1]:
                        gates.append(dict({'Gate': 'CX', 'Qubit': [qubit, qubit + 1]}))
                mysentence.dictionary.dictionary[myword].gateset = gates

        elif not self.random:
            pass  # load vocabulary parameters

    def setsentenceparameters(self, mysentence):
        for word, qword in mysentence.dictionary.dictionary.items():
            self.setwordparameters(word, mysentence)

    def executecircuit(self):
        quantumcircuit = self.qlmprogram.to_circ()
        job = quantumcircuit.to_job()
        qpu = get_default_qpu()
        result = qpu.submit(job)
        self.result = result
        for sample in result:
            pass

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


    def createcircuit2(self, sentence):
        totqubits = sentence.qubitsarray[-1][-1] + 1
        my_program = Program()
        my_program.qalloc(totqubits)
        my_program.calloc(totqubits)
        my_program = self.preparewords(sentence,my_program)
        my_program = self.contractqubits(sentence,my_program)
        self.qlmprogram = my_program