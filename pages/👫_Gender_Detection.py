import streamlit as st 
from audio_recorder_streamlit import audio_recorder
from utilities.genderization import nameGenderDetect

# tabs
# name_tab, audio_tab = st.tabs(["📝 By Name", "🗣️ By Voice"])

# gender detection with name
#with name_tab:
# App title
st.title("Gender Detection (By Name)")

# Input area
name = st.text_input("Enter Burmese Name", placeholder="Ello")
need_help = st.checkbox("Need help for Burmese names ?")
if need_help:
    col1, col2 = st.columns(2)
    with col1:
        st.code("♂️ Male Sample Names:\nစိုင်းဝေယံ\nမောင်မောင်ဌေးလွင်")
    with col2:
        st.code("♀️ Female Sample Names:\nလှယဉ်\nဟန်နီနွေဦး")

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
    result = nameGenderDetect.predict_gender(name_value)

    # Replace the placeholder with some text:
    gender_index = 0 if result[1] == "male" else 1
    placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], index=gender_index, horizontal=True)
    st.write("Predicted with ", result[0], " confidence!")

    sorry = """
    We sincerely apologize if our prediction was incorrect. 
    Our gender prediction model is based on patterns in data and may not always capture the uniqueness of every individual. 
    We deeply respect and celebrate the diversity of all identities. 
    hank you for your understanding and feedback as we strive to improve!
    """
    st.write(sorry)

# # gender detection with voice
# with audio_tab:
#     # App title
#     st.title("Gender Detection (By Voice)")

#     st.write("Under construction")

    # # input area
    # audio_bytes = audio_recorder()
    # predict_button_voice = st.button("Predict", key="predict_button_voice")

    # # line divider
    # st.write("***")

    # # show result
    # placeholder = st.empty()
    # placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], \
    #     index=0, horizontal=True, disabled=True, key="gender_voice")

    # if predict_button_voice:
    #     # show the input audio
    #     if audio_bytes:
    #         st.audio(audio_bytes, format="audio/wav")

    #     # predict gender by name;

    #     # Replace the placeholder with some text:
    #     placeholder.radio("Predicted Gender", ["Male", "Female", "Decide Later"], index=1, horizontal=True)
