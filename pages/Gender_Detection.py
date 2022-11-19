import streamlit as st 
from audio_recorder_streamlit import audio_recorder

# tabs
name_tab, audio_tab = st.tabs(["📝 By Name", "🗣️ By Voice"])

# gender detection with name
with name_tab:
    # App title
    st.title("Gender Detection (By Name)")

    # Input area
    name = st.text_input("Enter Burmese Name", placeholder="Ello")
    predict_button_name = st.button("Predict", key="predict_button_name")

    # line divider
    st.write("***")

    # show result
    placeholder = st.empty()
    placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], \
        index=0, horizontal=True, disabled=True, key="gender_name")


    if predict_button_name:
        # predict gender by name;
        name_value = name.title()

        # Replace the placeholder with some text:
        placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], index=1, horizontal=True)

# gender detection with voice
with audio_tab:
    # App title
    st.title("Gender Detection (By Voice)")

    # input area
    audio_bytes = audio_recorder()
    predict_button_voice = st.button("Predict", key="predict_button_voice")

    # line divider
    st.write("***")

    # show result
    placeholder = st.empty()
    placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], \
        index=0, horizontal=True, disabled=True, key="gender_voice")

    if predict_button_voice:
        # show the input audio
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")

        # predict gender by name;

        # Replace the placeholder with some text:
        placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], index=1, horizontal=True)
