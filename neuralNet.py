import numpy as np

n_x = 7
n_h = 9
n_h2 = 15
n_y = 3
W1_shape = (9, 7)
W2_shape = (15, 9)
W3_shape = (3, 15)
b1_shape = (9, 1)
b2_shape = (15, 1)
b3_shape = (3,1)



def getWeights(weights):
    W1 = weights[0:W1_shape[0]*W1_shape[1]]
    W2 = weights[W1_shape[0]*W1_shape[1]: W2_shape[0]*W2_shape[1] + W1_shape[0]*W1_shape[1]]
    W3 = weights[W2_shape[0]*W2_shape[1] + W1_shape[0]*W1_shape[1]:]
    return W1.reshape(W1_shape[0],W1_shape[1]), W2.reshape(W2_shape[0],W2_shape[1]), W3.reshape(W3_shape[0],W3_shape[1])   


def softmax(Z):
    return np.exp(Z)/np.sum(np.exp(Z))

def forwardPropagation(input ,weights):
    W1, W2, W3 = getWeights(weights)
    assert(W1.shape == W1_shape)
    assert(W2.shape == W2_shape)
    assert(W3.shape == W3_shape)

    Z1 = np.dot(W1, input.T)
    A1 = np.tanh(Z1)
    Z2 = np.dot(W2, A1)
    A2 = np.tanh(Z2)
    Z3 = np.dot(W3, A2)
    A3 = softmax(Z3)
    # print("A3", np.array(A3))
    return np.array(A3)
