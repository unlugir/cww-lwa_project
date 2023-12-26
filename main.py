import word
import words_model
import random
import lwa
import numpy as np
import streamlit as st
import pandas as pd

def write_data(name, res1, res2):
    data = {"Name" : [name],
            "TextEv": [res1],
            "NumEv": [res2]}
    df = pd.DataFrame(data)
    df.to_csv("data.csv", mode='a', header=False)
    return

def draw_data():
    df = pd.read_csv("data.csv")
    df2 = df.drop(df.columns[0], axis=1)
    st.table(df2)
    pass

def draw():
    st.header("Інтерфейс оцінки співробітника колегами")
    st.subheader("Ввід оцінки співробітниками")
    user_name = st.text_input("Ім'я співпобітника", "Ім'я")
    model = words_model.words_9
    grades = []
    for word2 in model["words"].keys():
        counts = int(st.text_input(f"Кількість людей які вибрали {word2} ", "1"))
        grades += [word2] * counts
    W = []
    for item in model["words"]:
        W.append(grades.count(item))

    h = min(item["lmf"][-1] for item in model["words"].values())
    m = 50
    intervals_umf = lwa.alpha_cuts_intervals(m)
    intervals_lmf = lwa.alpha_cuts_intervals(m, h)

    res_lmf = lwa.y_lmf(intervals_lmf, model, W)
    res_umf = lwa.y_umf(intervals_umf, model, W)
    res = lwa.construct_dit2fs(
        np.arange(*model["x"]), intervals_lmf, res_lmf, intervals_umf, res_umf
    )


    sm = []
    #model = words_model.words_11
    model = words_model.words_14

    for title, fou in model["words"].items():
        sm.append(
            (
                title,
                res.similarity_measure(word.Word(None, model["x"], fou["lmf"], fou["umf"])),
                word.Word(title, model["x"], fou["lmf"], fou["umf"]),
            ),
        )
    res_word = max(sm, key=lambda item: item[1])
    print(res_word)
    #st.markdown("Value and confidents")
    st.header("Спільне рішення")
    st.write(str(res_word[0]) )
    st.write(str(res_word[1]))

    if (st.button("Створити запис",type="primary")):
        write_data(user_name,str(res_word[0]),str(res_word[1]))
    draw_data()
    #st.markdown(res_word[:2])

    st.subheader("Графіки для 9 слів (зліва) і для 14 слів (справа)")
    left_column, right_column = st.columns(2)
    with left_column:
        res.plot(color='blue')
    with right_column:
        res_word[2].plot(color='yellow')


draw()