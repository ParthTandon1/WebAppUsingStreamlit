import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.title('Simple Iris Flower Prediction')

st.write('This app predicts the Iris flower type!')

st.sidebar.header('User Input Parameters')

def user_input_features():
    sepal_length = st.sidebar.slider('sepal length',4.3,7.9,5.4)
    sepal_width= st.sidebar.slider('sepal width',2.0,4.4,3.4)
    petal_length = st.sidebar.slider('petal length',1.0,6.9,1.3)
    petal_width = st.sidebar.slider('petal width',0.1,2.5,0.2)
    data = {
        'sepal length':sepal_length,
        'sepal width':sepal_width,
        'petal length':petal_length,
        'petal width':petal_width
    }
    features = pd.DataFrame(data,index=[0])
    return features

df = user_input_features()

st.header('User Input Papameters')
st.write(df)

iris = datasets.load_iris()
X = iris.data
Y = iris.target

clf = RandomForestClassifier()
clf.fit(X,Y)

prediction = clf.predict(df)
prediction_prob = clf.predict_proba(df)

st.subheader('Class labels and their corresponding index number.')
st.write(iris.target_names)

st.subheader('Prediciton')
st.write(iris.target_names[prediction])

st.subheader('Prediction Probability')
st.write(prediction_prob)




