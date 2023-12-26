import streamlit as st
import numpy as np
import pandas as pd
import words_model as wm

'''
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
'''
df = pd.DataFrame([wm.words_14])
#st.table(df)
st.dataframe(df)