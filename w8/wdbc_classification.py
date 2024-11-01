import numpy as np
import matplotlib.pyplot as plt
from sklearn import (datasets, svm, metrics)
from matplotlib.lines import Line2D # For the custom legend

def load_wdbc_data(filename):
    class WDBCData:
        data          = [] # Shape: (569, 30)
        target        = [] # Shape: (569, )
        target_names  = ['malignant', 'benign']
        feature_names = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension',
                         'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error',
                         'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension']
    wdbc = WDBCData()
    with open(filename) as f:
        for line in f.readlines():
            items = line.split(',')
            wdbc.target.append(0 if items[1]=='M' else 1)       # Add the true label: 0 for M, 1 for others
            wdbc.data.append([float(num) for num in items[2:]]) # Append 30 attributes as floating-point numbers
        wdbc.data = np.array(wdbc.data)
    return wdbc

if __name__ == '__main__':
    # Load a dataset
    wdbc = load_wdbc_data('data/wdbc.data')

    # Train a model
    model = svm.SVC(kernel='rbf', gamma=0.001)                 # Find a better classifier (SVC accuracy: 0.902) -> (rbf SVC accuracy: 0.987)
    model.fit(wdbc.data, wdbc.target)

    # Test the model
    predict = model.predict(wdbc.data)
    accuracy = metrics.balanced_accuracy_score(wdbc.target, predict)
    
    # Make dictionary for preparing visualization
    cm_dict = {'gtm': 0, 'gtb': 0, 'pm': 0, 'pb': 0}
    
    # Modify each value with interating both list
    for p, gt in zip(predict, wdbc.target):
        if gt == 0:
                cm_dict['gtm'] += 1
        else:
                cm_dict['gtb'] += 1
        if p == 0:
                cm_dict['pm'] += 1
        else:
                cm_dict['pb'] += 1
    
    print(cm_dict['gtm'])
    print(cm_dict['gtb'])
    print(cm_dict['pm'])
    print(cm_dict['pb'])
    
    # Set values of Ground Truth and its Prediction
    y_true = [False] * cm_dict['gtm'] + [True] * cm_dict['gtb'] # True labels
    y_pred = [False] * cm_dict['pm'] + [True] * cm_dict['pb']   # Predicted labels
    
    # TODO #3) Visualize the confusion matrix
    conf_matx = metrics.confusion_matrix(y_true, y_pred)
    conf_disp = metrics.ConfusionMatrixDisplay(conf_matx, display_labels=['malignant', 'benign'])
    conf_disp.plot()
    plt.savefig('wdbc_classification_matrix.png')
    
    # Visualize testing results
    cmap = np.array([(1, 0, 0), (0, 1, 0)])
    clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]
    for (x, y) in [(0, 1)]: # Not mandatory, but try [(i, i+1) for i in range(0, 30, 2)]
        plt.figure()
        plt.title(f'My Classifier (Accuracy: {accuracy:.3f})')
        plt.scatter(wdbc.data[:,x], wdbc.data[:,y], c=cmap[wdbc.target], edgecolors=cmap[predict])
        plt.xlabel(wdbc.feature_names[x])
        plt.ylabel(wdbc.feature_names[y])
        plt.legend(handles=clabel, framealpha=0.5)
    plt.savefig('wdbc_classification_scatter.png')
    plt.show()