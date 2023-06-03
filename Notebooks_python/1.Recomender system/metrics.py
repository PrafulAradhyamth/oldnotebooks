import numpy as np

def confusion_matrix(y_true, y_pred,normalize=None):
    """Computes the confusion matrix from predictions and labels.

    The matrix columns represent the real labels and the rows represent the
    prediction labels. The confusion matrix is always a 2-D array of shape `[n_labels, n_labels]`,
    where `n_labels` is the number of valid labels for a given classification task. Both
    prediction and labels must be 1-D arrays of the same shape in order for this
    function to work.

    Parameters:
        y_true: 1-D array of real labels for the classification task.
        y_pred: 1-D array of predictions for a given classification.
        normalize: One of ['true', 'pred', 'all', None], corresponding to column sum, row sum, matrix sum, or no
                   normalization.

    Returns:
        A 2-D array with shape `[n_labels, n_labels]` representing the confusion
        matrix, where `n` is the number of possible labels in the classification
        task.
    """
    x = y_true
    y = y_pred
    N_ele = np.unique(x)
    N_Len = len(N_ele)
    cm = np.zeros((N_Len,1))
    
    for i in range(N_Len):
        temp = y[x==N_ele[i]]
        emt_hist = np.zeros((N_Len,1))
        Hist = np.asarray(np.unique(temp, return_counts=True)).T
        temp_hist_r1 = Hist[:,0].reshape((len(Hist[:,0]), 1))
        temp_hist_r2 = Hist[:,1].reshape((len(Hist[:,0]), 1))
        emt_hist[temp_hist_r1[:,0]] = temp_hist_r2
        emt_hist = emt_hist.reshape((len(emt_hist), 1))
        cm = np.hstack((cm, emt_hist))

    cm = np.delete(cm, 0, axis=1)
    cm = np.transpose(cm)

    if normalize not in ['true', 'pred', 'all', None]:
        raise ValueError("normalize must be one of {'true', 'pred', 'all', None}")

    if normalize == 'true':
        cm = cm / cm.sum(axis=1, keepdims=True)
    elif normalize == 'pred':
        cm = cm / cm.sum(axis=0, keepdims=True)
    elif normalize == 'all':
        cm = cm / cm.sum()
        # TODO (TASK 1)

    return cm


def precision(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred,normalize='pred')
    p = cm.diagonal()
    return p
    # TODO (TASK 2)


def recall(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred,normalize='true')
    r = cm.diagonal()
    return r
    # TODO (TASK 2)

def false_alarm_rate(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred,normalize='all')
    
    FP = cm.sum(axis=0) - np.diag(cm)  
    #FN = cm.sum(axis=1) - np.diag(cm)
    TP = np.diag(cm)
    #TN = cm.sum() - (FP + FN + TP)
    
    FAR = FP/(TP+FP)
    return FP/(TP+FP)
