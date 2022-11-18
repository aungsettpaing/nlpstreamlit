import streamlit as st 

# App title
st.title("Text Segmentation ")

radio_method = st.radio("Category", ["Syllable", "Word"], index=0, horizontal=True)

# line divider
st.write("***")

if radio_method == "Syllable":
    text_input = st.text_area("Enter Text")
    syllabification_input = st.radio("Choose Segmentation Type", ["Orthographically", "Phonetically"], horizontal=True)

    # line divider
    st.write("***")

    # result placeholder
    result_placeholder = st.empty()
    result_placeholder.text_area("Here's the result", disabled=True)

    if st.button("Segment"):
        # Segment
        text = text_input.title()

        # show the result
        result_placeholder.text_area("Here's the result", "RESULT", disabled=True)
else:
    text_input_word = st.text_area("Enter Text")

    # line divider
    st.write("***")

    # result placeholder
    result_placeholder = st.empty()
    result_placeholder.text_area("Here's the result", disabled=True)

    if st.button("Segment"):
        # Segment
        text = text_input_word.title()

        # show the result
        result_placeholder.text_area("Here's the result", "RESULT", disabled=True)
    