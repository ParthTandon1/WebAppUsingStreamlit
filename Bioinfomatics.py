import streamlit as st
import pandas as pd
import numpy as np
import pickle
from rdkit import Chem
from rdkit.Chem import Descriptors
import os

# Display logo
st.image(os.path.join(os.getcwd(), "static", "solubility-logo.jpg"), width=1000)

# ---------- Descriptor Functions ----------
def Aromaticproportion(m):
    try:
        aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
        AromaticAtom = sum(1 for is_aromatic in aromatic_atoms if is_aromatic)
        HeavyAtom = Descriptors.HeavyAtomCount(m)
        if HeavyAtom == 0:
            return 0.0
        return AromaticAtom / HeavyAtom
    except Exception as e:
        return np.nan

def generate(smiles_list, verbose=False):
    descriptors_list = []
    valid_smiles = []

    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            st.warning(f"⚠️ Invalid SMILES skipped: {smiles}")
            continue

        try:
            desc_MolLogP = float(Descriptors.MolLogP(mol))
            desc_MolWt = float(Descriptors.MolWt(mol))
            desc_NumRotatableBonds = float(Descriptors.NumRotatableBonds(mol))
            desc_AromaticProportion = float(Aromaticproportion(mol))

            # Skip any row with NaN
            if any(pd.isna([desc_MolLogP, desc_MolWt, desc_NumRotatableBonds, desc_AromaticProportion])):
                st.warning(f"⚠️ Descriptor NaN detected and skipped for: {smiles}")
                continue

            row = [desc_MolLogP, desc_MolWt, desc_NumRotatableBonds, desc_AromaticProportion]
            descriptors_list.append(row)
            valid_smiles.append(smiles)

        except Exception as e:
            st.warning(f"⚠️ Error processing {smiles}: {e}")
            continue

    columnNames = ['MolLogP', 'MolWt', 'NumRotatableBonds', 'AromaticProportion']
    descriptors_df = pd.DataFrame(descriptors_list, columns=columnNames)
    descriptors_df = descriptors_df.astype(float)

    return descriptors_df, valid_smiles

# ---------- App Title ----------
st.write('''
# 🧪 Molecular Solubility Prediction Web App
This app predicts the **Solubility (LogS)** values of molecules!

Data obtained from John S. Delaney:  
[ESOL: Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x)  
*J. Chem. Inf. Comput. Sci. 2004, 44, 3, 1000–1005.*
''')    

# ---------- Sidebar ----------
st.sidebar.header('User Input Features')

default_SMILES = 'NCCCC\nCCC\nCN'
SMILES_input = st.sidebar.text_area('SMILES input (one per line):', default_SMILES)

# Preprocess SMILES input
SMILES = SMILES_input.strip().split('\n')
SMILES = [s for s in SMILES if s.strip()]  # Remove empty lines

# ---------- Descriptor Generation ----------
st.header('📥 Input SMILES')
st.write(SMILES)

st.header('🧬 Computed Molecular Descriptors')
X, valid_smiles = generate(SMILES)
st.write(X)

# ---------- Load Model ----------
try:
    load_model = pickle.load(open('solubility_model.pkl', 'rb'))
except FileNotFoundError:
    st.error("❌ Trained model file `solubility_model.pkl` not found!")
    st.stop()

# ---------- Predict ----------
if X.empty:
    st.error("❌ No valid descriptors could be calculated. Please check your SMILES input.")
else:
    try:
        prediction = load_model.predict(X)

        st.header('🔮 Predicted LogS Values')
        st.write(pd.DataFrame({
            'SMILES': valid_smiles,
            'Predicted LogS': prediction
        }))

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")








