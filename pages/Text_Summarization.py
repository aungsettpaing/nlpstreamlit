import streamlit as st

# tabs
supervised_tab, unsupervised_tab = st.tabs(["🤖 By Supervised", "🦸 By Unsupervised"])

# text summarization with the supervised method
with supervised_tab:
    # App title
    st.title("Text Summarization (Supervised)")

    title_input = st.text_input("Enter News Title", key="input_title_supervised")
    body_input = st.text_area("Enter News Body", key="input_body_supervised")
    button_supervised = st.button("Summarize", key="button_supervised")

    # line divider
    st.write("***")

    # result placeholder
    result_placeholder = st.empty()
    result_placeholder.text_area("Here is the result", key="output_summary_supervised", disabled=True)

    if button_supervised:
        # summarize
        title = title_input.title()
        body = body_input.title()

        # show the result
        result_placeholder.text_area("Here is the result", "Summarized paragraphs", disabled=True)

# text summarization with the unsupervised method
with unsupervised_tab:
    # App title
    st.title("Text Summarization (Unsupervised)")

    title_input = st.text_input("Enter News Title", key="input_title_unsupervised")
    body_input = st.text_area("Enter News Body", key="input_body_unsupervised")
    button_unsupervised = st.button("Summarize", key="button_unsupervised")

    # line divider
    st.write("***")

    # result cluster placeholder
    cluster_placeholder = st.empty()
    cluster_placeholder.selectbox("Choose Cluster", ["Overall"], disabled=True)

    # result placeholder
    result_placeholder = st.empty()
    result_placeholder.text_area("Here is the result", key="output_summary_unsupervised", disabled=True)

    if button_unsupervised:
        # summarize
        title = title_input.title()
        body = body_input.title()

        # show the result
        res = cluster_placeholder.selectbox("Choose Cluster", ["Overall", "Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4"])
        result_placeholder.text_area("Here is the result", "Summarized paragraphs", disabled=True)

