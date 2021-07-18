import dictionary
import sentence
import Circuit
import scipy.optimize

class ClassicalOptimizer:

    def __init__(self, optimizer='cobyla', tol=0.1, maxiter=200):
        self.optimizer = optimizer
        self.tol = tol
        self.maxiter = maxiter

    def optimizesentence(self, mySentence):
        params0 = mySentence.getparameters()
        flat_params0 = [item for sublist in params0 for item in sublist]
        result = scipy.optimize.minimize(self.cost, flat_params0,
                                                    args=(mySentence),
                                                    tol=1e-1,
                                                    options={'maxiter':50},
                                                    method="COBYLA")
        return result

    def reshapeparams(self, parameters, mySentence):
        originalparams = mySentence.getparameters()
        shapedparams = []
        iparam=0
        for word in originalparams:
            iwparam=0
            wordparams = []
            while iwparam < len(word):
                wordparams.append(parameters[iparam])
                iparam+=1
                iwparam+=1
            shapedparams.append(wordparams)
        return shapedparams




    def cost(self, parameters, mySentence):
        shapedparams = self.reshapeparams(parameters, mySentence)
        mySentence.setsentenceparameters(randompar=False, params=shapedparams)
        myCircBuilder = Circuit.circuitBuilder()
        myCircBuilder.createcircuit(mySentence)
        myCircBuilder.executecircuit()
        label=mySentence.label
        probs = []
        for sample in myCircBuilder.result:
            state = sample.state.bitstring
            postselectedqubits = ''.join(state[x] for x in range(len(state)) if x != mySentence.sentencequbit)
            if postselectedqubits == '0' * (myCircBuilder.qlmprogram.qbit_count - 1):
                probs.append(sample.probability)
                print("State %s: probability %s, amplitude %s" % (sample.state, sample.probability, sample.amplitude))
        prob0 = probs[0] / sum(probs)
        prob1 = probs[1] / sum(probs)
        if label==0:
            costval = 1-prob0
            print(costval)
        elif label==1:
            costval = 1-prob1
            print(costval)
        return costval

