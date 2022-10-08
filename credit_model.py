# -*- coding: utf-8 -*-
"""credit_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NTBVsSJNePigTHJQ4B7h9WLHEThFdPgc
"""

# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pickle

# Read database
df=pd.read_csv('/content/train_u6lujuX_CVtuZ9i.csv')
df

# show all database
pd.set_option('display.max_rows',df.shape[0]+1)
df

# Show only 10 rows (First 5 rows and last 5 rows)
pd.set_option('display.max_rows',10)
df

# see missing values
df.info()

# sum and sort and classification missing values
df.isnull().sum().sort_values(ascending=False)

# show statistic of numeric values
df.describe()

# show statistic of categorical values
df.describe(include='O')

# Fill in missing values (Renseigner les valeurs manquantes)
# split the DB into two a digital DB and another categorical
cat_data=[]
num_data=[]
for i,c in enumerate(df.dtypes):
  if c==object:
    cat_data.append(df.iloc[:,i])
  else:
    num_data.append(df.iloc[:,i])
cat_data=pd.DataFrame(cat_data).transpose()
num_data=pd.DataFrame(num_data).transpose()

num_data

cat_data

# for categorical variables we will replace the missing values ​​by the values ​​that are repeated the most
# pour les variables catégoriques on va remplacer les valeurs manquantes par les précedente de la mêmê colonne
cat_data=cat_data.apply(lambda x:x.fillna(x.value_counts().index[0]))
# check that there are no missing values
cat_data.isnull().sum().any()

# Explique le code => cat_data=cat_data.apply(lambda x:x.fillna(x.value_counts().index[0]))
print(cat_data['Education'].value_counts())
print ('--------------------')
print(cat_data['Education'].value_counts().index[0])

# for numerical variables we will replace the missing values ​​by the previous ones of the same column
# pour les variables numérique on va remplacer les valeurs manquantes par les précedvente de la mêmê colonne
num_data.fillna(method='bfill',inplace=True)
num_data.isnull().sum().any()

# Method 1
# transform targett column 
target_value={'Y':1, 'N':0}
target=cat_data['Loan_Status']
cat_data.drop('Loan_Status',axis=1,inplace=True)
target=target.map(target_value)
target

cat_data

# Method 2
# Remplacer les valeurs catégoriques par des valeurs numérique 0,1,2,...
le = LabelEncoder()
for i in cat_data:
  cat_data[i]=le.fit_transform(cat_data[i])
cat_data

# delete Loan_ID
cat_data.drop('Loan_ID',axis=1, inplace=True)

# Concatenate cat_data and num_data and specify target column
# X for decision and Y for result
X=pd.concat([cat_data,num_data],axis=1)
Y=target

Y

# will start with the target variable
target.value_counts()

# the database used for EDA
df=pd.concat([cat_data,num_data,target],axis=1)

"""**relation entre deux attribut**




"""

# visualize a categorical variable
plt.figure(figsize=(8,6))
sns.countplot(target)
yes=target.value_counts()[0]/len(target)
no=target.value_counts()[1]/len(target)
print(f'le pourcentage des crédits accordés est: {yes}')
print(f'le pourcentage des crédits non accordés est: {no}')

# credit history
grid=sns.FacetGrid(df,col='Loan_Status',size=3.2,aspect=1.6)
grid.map(sns.countplot,'Credit_History')

# Gender
grid=sns.FacetGrid(df,col='Loan_Status',size=3.2,aspect=1.6)
grid.map(sns.countplot,'Gender')

# Married
grid=sns.FacetGrid(df,col='Loan_Status',size=3.2,aspect=1.6)
grid.map(sns.countplot,'Married')

# Education
grid=sns.FacetGrid(df,col='Loan_Status',size=3.2,aspect=1.6)
grid.map(sns.countplot,'Education')

# revenu de demandeur (claimant income)
plt.scatter(df['ApplicantIncome'],df['Loan_Status'])

plt.scatter(df['CoapplicantIncome'],df['Loan_Status'])

df.groupby('Loan_Status').median()

"""**4: Réalisation du modèle**


"""

# split the database into a test and training database
# diviser la base de données en une base de données test et d'entrainement
 ## 20% pour le test
sss=StratifiedShuffleSplit(n_splits=1, test_size=0.2,random_state=42)
for train,test in sss.split(X,Y):
  X_train,X_test=X.iloc[train],X.iloc[test]
  y_train,y_test=Y.iloc[train],Y.iloc[test]

print("X_train shape: ", X_train.shape)
print("X_test shape: ", X_test.shape)
print("y_train shape: ", y_train.shape)
print("y_test shape: ", y_test.shape)

"""# *the best algorithm is logistic Regression for our problem*"""

# we will apply three algorithms logitic Regression, KNN, DecisionTree
# on va appliquer trois algorithmes logitic Regression, KNN, DecisionTree 

models={
    'LogisticRegression': LogisticRegression(random_state=42),
    'KNeighborsClassifier': KNeighborsClassifier(),
    'DecisionTreeClassifier': DecisionTreeClassifier(max_depth=1, random_state=42)
}
# the precision function
def accu(y_true,y_pred,retu=False):
  acc=accuracy_score(y_true,y_pred)
  if retu:
    return acc
  else:
    print(f'la precision du modéle est: {acc}')
# la fonction d'application des modèles
def train_test_eval(models, X_train, y_train, X_test, y_test):
  for name,model in models.items():
    print(name,':')
    model.fit(X_train,y_train)
    accu(y_test,model.predict(X_test))
    print('-'*30)

train_test_eval(models,X_train,y_train,X_test,y_test)

"""# Create new DB"""

# choose specific features to improve our model
# choisir des featur spécifique pour améliorer notre modèl 
X_2=X[['Credit_History','Married','CoapplicantIncome','ApplicantIncome']]

# split the database into a test and training database
# diviser la base de données en une base de données test et d'entrainement
 ## 20% pour le test
sss=StratifiedShuffleSplit(n_splits=1, test_size=0.2,random_state=42)
for train,test in sss.split(X_2,Y):
  X_train,X_test=X_2.iloc[train],X_2.iloc[test]
  y_train,y_test=Y.iloc[train],Y.iloc[test]

print("X_train shape: ", X_train.shape)
print("X_test shape: ", X_test.shape)
print("y_train shape: ", y_train.shape)
print("y_test shape: ", y_test.shape)

train_test_eval(models,X_train,y_train,X_test,y_test)