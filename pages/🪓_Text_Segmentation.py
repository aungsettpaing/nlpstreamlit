import streamlit as st
from utilities.segmentation import syllable_segmentation, wordSegmentation

# tabs
syllable_tab, word_tab = st.tabs(["🐛 Syllable", "🦋 Word"])

# syllable segmentation
with syllable_tab:
    # title
    st.title("Text Segmentation (Syllable)")

    # input text area
    text_input = st.text_area("Enter Text", key="text_area_1")
    need_help = st.checkbox("Need help for Burmese texts ?", key="help_checkbox_1")
    if need_help:
        st.code("Sampel Texts:\nမင်္ဂလာပါနော်\nအင်္ဂါဗုဒ္ဓဟူးဂျိုးကလေးတကူကူး")

    # segmentation method
    syllabification_option = st.radio("Choose Segmentation Type", ["Orthographically", "Phonetically"], horizontal=True)
    syllable_button = st.button("Segment", key="syllable_segment")

    # line divider
    st.write("***")

    # result placeholder
    result_placeholder = st.empty()
    result_placeholder.text_area("Here's the result", key="syllable_output", disabled=True)

    if syllable_button:
        # Segment
        text = text_input.title()
        result = syllable_segmentation.syllable_break(text, syllabification_option)

        # show the result
        result_placeholder.text_area("Here's the result", result, disabled=True)

# word segmentation
with word_tab:
    # title
    st.title("Text Segmentation (Word)")

    text_input_word = st.text_area("Enter Text", key="text_area_2")
    need_help = st.checkbox("Need help for Burmese texts ?", key="help_checkbox_2")
    if need_help:
        st.code("Sampel Texts:\nအရှေ့အရပ်ကနေဝန်းထွက်သည့်ပမာ\nတချို့အဆင်းလှတချို့အဆင်းမလှ")
    word_button = st.button("Segment", key="word_segment")

    # line divider
    st.write("***")

    # result placeholder
    result_placeholder = st.empty()
    result_placeholder.text_area("Here's the result", key="word_output", disabled=True)

    if word_button:
        # Segment
        text = text_input_word.title()
        result = wordSegmentation.work_break(text)

        # show the result
        result_placeholder.text_area("Here's the result", result, disabled=True)