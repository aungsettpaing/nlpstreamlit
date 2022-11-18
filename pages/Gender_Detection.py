import streamlit as st 
from audio_recorder_streamlit import audio_recorder

# App title
st.title("Gender Detection ")

radio_method = st.radio("Methods", ["By Name", "By Voice"], index=0, horizontal=True)

# line divider
st.write("***")

if radio_method == "By Name":
    # Input area
    name = st.text_input("Enter Burmese Name", placeholder="Ello")

    # show result
    placeholder = st.empty()
    placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], index=0, horizontal=True, disabled=True)


    if st.button("Predict"):
        name_value = name.title()

        # predict gender by name; continue;

        # Replace the placeholder with some text:
        placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], index=1, horizontal=True)
else:
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")