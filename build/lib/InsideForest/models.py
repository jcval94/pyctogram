from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


class models:
  def get_knn_rows(self, df, target_col, criterio_fp=True, min_obs = 5):
    X = df.drop(columns=[target_col]).values
    y = df.loc[:, target_col].values
    for k in range(1,int(len(df))):
      knn = KNeighborsClassifier(n_neighbors=k)
      knn.fit(X, y)
      y_pred = knn.predict(X)
      cm = confusion_matrix(y, y_pred)
      tn, fp, fn, tp = cm.ravel()
      if criterio_fp:
        if fp>min_obs:
          break
      else:
        if fn>min_obs:
          break
    if fn>0:
      false_negatives = (y == 1) & (y_pred == 0)
      return df[false_negatives], df[~false_negatives]
    if fp>0:
      false_positives = (y == 0) & (y_pred == 1)
      return df[false_positives], df[~false_positives]
  
  def get_cvRF(self, X_train, y_train, param_grid):
    rf = RandomForestClassifier(random_state=31416)
    cv = GridSearchCV(rf,param_grid=param_grid,cv=5,n_jobs=-1)
    cv.fit(X_train,y_train)
    return cv

