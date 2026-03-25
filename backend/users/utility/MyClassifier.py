import os
from django.conf import settings

# Global variables for lazy initialization
_DATA_INITIALIZED = False
X_train = None
X_test = None
y_train = None
y_test = None
X_train_norm = None
X_test_norm = None
minmax_scale = None
df_global = None

def _initialize_data():
    global _DATA_INITIALIZED, X_train, X_test, y_train, y_test, X_train_norm, X_test_norm, minmax_scale, df_global
    
    if _DATA_INITIALIZED:
        return
        
    try:
        import pandas as pd
        from sklearn import preprocessing
        from sklearn.model_selection import train_test_split
        
        filepath = os.path.join(settings.MEDIA_ROOT, 'stress_data.xlsx')

        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found. KNN classifier will not work correctly.")
            return

        df = pd.read_excel(filepath, header=None)
        df.columns = ['Target', 'ECG(mV)', 'EMG(mV)', 'Foot GSR(mV)', 'Hand GSR(mV)', 'HR(bpm)', 'RESP(mV)']
        df_global = df
        
        X = df[['ECG(mV)', 'EMG(mV)', 'Foot GSR(mV)', 'Hand GSR(mV)', 'HR(bpm)', 'RESP(mV)']]
        y = df['Target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=12345)
        
        minmax_scale = preprocessing.MinMaxScaler().fit(X)
        df_minmax = minmax_scale.transform(X)
        
        X_train_norm, X_test_norm, _, _ = train_test_split(df_minmax, y, test_size=0.30, random_state=12345)
        
        _DATA_INITIALIZED = True
        print("KNN Classifier data initialized successfully.")
    except Exception as e:
        print(f"Error initializing KNN data: {e}")

class KNNclassifier:
    def getKnnResults(self):
        _initialize_data()
        
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn import metrics
        
        if not _DATA_INITIALIZED:

            raise RuntimeError("KNN classifier data was not initialized correctly. Check if stress_data.xlsx exists.")
            
        print("Started KNN classification")
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_train, y_train)

        knn_norm = KNeighborsClassifier(n_neighbors=5)
        knn_norm.fit(X_train_norm, y_train)

        pred_test = knn.predict(X_test)
        pred_test_norm = knn_norm.predict(X_test_norm)

        confusion = metrics.confusion_matrix(y_test, pred_test_norm)
        TP = confusion[1, 1]
        TN = confusion[0, 0]
        FP = confusion[0, 1]
        FN = confusion[1, 0]

        accuracy = metrics.accuracy_score(y_test, pred_test_norm)
        classificationerror = 1 - accuracy
        sensitivity = metrics.recall_score(y_test, pred_test_norm)
        Specificity = TN / float(TN + FP) if (TN + FP) > 0 else 0
        fsp = FP / float(TN + FP) if (TN + FP) > 0 else 0
        precision = metrics.precision_score(y_test, pred_test_norm)

        return df_global, accuracy, classificationerror, sensitivity, Specificity, fsp, precision