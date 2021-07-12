import dictionary
import sentence
import Circuit



if __name__ == '__main__':
    myDict = dictionary.QuantumDict(["big", "dog", "eating", "small","cat","bark","at"])
    mySentence = sentence.Sentence("dog barking at cat", myDict,1)
    wired=[]
    mySentence.getqbitcontractions()
    myCircBuilder = Circuit.circuitBuilder()
    myCircBuilder.setsentenceparameters(mySentence)
    print(mySentence.contractions)
    myCircBuilder.createcircuit2(mySentence)
    myCircBuilder.executecircuit()
    probs = []
    for sample in myCircBuilder.result:
        state = sample.state.bitstring
        postselectedqubits = ''.join(state[x] for x in range(len(state)) if x != mySentence.sentencequbit)
        if postselectedqubits == '0'*(myCircBuilder.qlmprogram.qbit_count-1):
            probs.append(sample.probability)
            print("State %s: probability %s, amplitude %s" % (sample.state, sample.probability, sample.amplitude))
    print('0: ', probs[0]/sum(probs))
    print('1: ', probs[1]/sum(probs))





