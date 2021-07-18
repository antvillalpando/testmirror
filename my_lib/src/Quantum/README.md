An WIP implementation of functorial learning and question answering. The sentence object contains all the information for that sentence to be written as a quantum circuit: the number of qubits per word, the categories assigned to each part of speech, the parameters for the rotations and the qubits that need to be contracted. 
To construct that object a dictionary of word needs to be specified and input the number of qubits for 'noun' and 'sentence' categories. The kind of sentence must be specified too. Currently the algorithm is able to do the contractions for: \
    - Noun+TransitiveVerb+Noun \
    - Adjective+Noun+TransitiveVerb+Adjective+Noun \
    - Noun+IntransitiveVerb+Preposition+Noun \
This should be enough to train the sentences in the dataset, but as sentence structures grow both in number and complexity, we need a way to automatically detect and perform these contractions. NLP libraries like spacy can help, but I found that sometimes it fails to detect the correct part of speech. In my opinion we should discuss this in more detail.
