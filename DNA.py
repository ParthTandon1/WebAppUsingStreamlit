import pandas as pd
import streamlit as st
import altair as alt
import os
#from PIL import Image

st.image(os.path.join(os.getcwd(),"static","dna-logo.jpg"),width = 1000)
#image = Image.open('dna-logo.jpg')
#.image(image,use_column_width = True)

st.title('DNA Nucleotide Count Web App')
st.subheader('This app counts the nucleotide composition of query DNA!')
st.header('Enter DNA sequence')

sequence_input ='''>DNA Query\nGACTACGT TACGTACGAT GCTTGACCGT AAGGCATCTA GCATCGGATC TAGTTACCGT
\nGCAATGCCG TTACGATGCT AGTTCCGATA CGATTGACGC TAAGCTAGTC GATCGTTAAC
\nGCTAGCTAGT TGACCGTATC GAATGCTAGT ACCGATCGTT AAGCTAGCTT GACCGTAACG
\nTTGACTGATC GTACGTTAGC TAA'''
sequence = st.text_area('Sequence input',sequence_input,height = 250)
sequence = sequence.splitlines()
sequence = sequence[1:]
sequence = ''.join(sequence)

st.write('''
***
         ''')

st.header('INPUT (DNA Query)')
sequence

st.header('OUTPUT (DNA Nucleotide Count)')

# 1 method to display
st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
    d = dict([
        ('A',seq.count('A')),
        ('T',seq.count('T')),
        ('G',seq.count('G')),
        ('C',seq.count('C'))
    ])
    return d
X = DNA_nucleotide_count(sequence)
X
#2 method to display
st.subheader('2. Print Text')
st.write('There are ' + str(X['A'])+'Adenine (A)')
st.write('There are ' + str(X['A'])+'Thymine (T)')
st.write('There are ' + str(X['A'])+'Guanine (G)')
st.write('There are ' + str(X['A'])+'Cytosine (C)')
#3 method
st.subheader('3. Display DataFrame')
df = pd.DataFrame.from_dict(X,orient ='index')
df = df.rename({0:'count'},axis='columns')
df.reset_index(inplace = True)
df = df.rename(columns = {'index':'nucleotide'})
st.write(df)
# 4 method
st.subheader('4. Display Bar Chart')
p = alt.Chart(df).mark_bar().encode(
    x = 'nucleotide',y = 'count'
)
p = p.properties(
    width = alt.Step(80)
)
st.write(p)


