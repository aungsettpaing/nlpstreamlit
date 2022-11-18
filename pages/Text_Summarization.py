import streamlit as st 

# App title
st.title("Text Summarization ")

radio_method = st.radio("Methods", ["By Supervised", "By Unsupervised"], index=0, horizontal=True)

# line divider
st.write("***")

if radio_method == "By Supervised":
    title_input = st.text_input("Enter News Title")
    body_input = st.text_area("Enter News Body")

    # line divider
    st.write("***")

    # result placeholder
    result_placeholder = st.empty()
    result_placeholder.text_area("Here is the result", disabled=True)

    if st.button("Summarize"):
        # summarize
        title = title_input.title()
        body = body_input.title()

        # show the result
        result_placeholder.text_area("Here is the result", "Summarized paragraphs", disabled=True)
else:
    title_input = st.text_input("Enter News Title")
    body_input = st.text_area("Enter News Body")

    # line divider
    st.write("***")

    # result cluster placeholder
    cluster_placeholder = st.empty()
    cluster_placeholder.selectbox("Choose Cluster", ["Overall"], disabled=True)

    # result placeholder
    result_placeholder = st.empty()
    result_placeholder.text_area("Here is the result", disabled=True)

    if st.button("Summarize 2"):
        # summarize
        title = title_input.title()
        body = body_input.title()

        # show the result
        res = cluster_placeholder.selectbox("Choose Cluster", ["Overall", "Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4"])
        result_placeholder.text_area("Here is the result", "Summarized paragraphs", disabled=True)
