import dictionary
import sentence
import Circuit
import Optimizer




if __name__ == '__main__':
    myDict = dictionary.QuantumDict(["big", "dog", "eating", "small","cat","bark","at"])
    mySentence = sentence.Sentence("dog barking at cat", myDict, 1, label=0)
    wired=[]
    mySentence.getqbitcontractions()
    myCircBuilder = Circuit.circuitBuilder()
    mySentence.setsentenceparameters(mySentence)
    print(mySentence.contractions)
    myCircBuilder.createcircuit(mySentence)
    myCircBuilder.executecircuit()
    probs = []
    for sample in myCircBuilder.result:
        state = sample.state.bitstring
        postselectedqubits = ''.join(state[x] for x in range(len(state)) if x != mySentence.sentencequbit)
        if postselectedqubits == '0'*(myCircBuilder.qlmprogram.qbit_count-1):
            probs.append(sample.probability)
            print("State %s: probability %s, amplitude %s" % (sample.state, sample.probability, sample.amplitude))
    params=mySentence.getparameters()
    flat_params0 = [item for sublist in params for item in sublist]
    print('0: ', probs[0]/sum(probs))
    print('1: ', probs[1]/sum(probs))
    myOptimizer=Optimizer.ClassicalOptimizer()

    print(myOptimizer.cost(flat_params0, mySentence))
    resultparams=myOptimizer.optimizesentence(mySentence)
    resultreshaped = myOptimizer.reshapeparams(resultparams.x, mySentence)
    print('original params:', params)
    print('best params:', resultreshaped)


    myCircBuilderifnal = Circuit.circuitBuilder()
    mySentence.setsentenceparameters(randompar=False, params=resultreshaped)
    myCircBuilderifnal.createcircuit(mySentence)
    myCircBuilderifnal.executecircuit()

    probs=[]
    for sample in myCircBuilderifnal.result:
        state = sample.state.bitstring
        postselectedqubits = ''.join(state[x] for x in range(len(state)) if x != mySentence.sentencequbit)
        if postselectedqubits == '0'*(myCircBuilderifnal.qlmprogram.qbit_count-1):
            probs.append(sample.probability)
            #print("State %s: probability %s, amplitude %s" % (sample.state, sample.probability, sample.amplitude))
    print('-----------------')
    print('0: ', probs[0]/sum(probs))
    print('1: ', probs[1]/sum(probs))




