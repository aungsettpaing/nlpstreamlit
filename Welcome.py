import streamlit as st 

# App config
st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
    initial_sidebar_state="expanded"
)

# App title
st.markdown("# Hello world 👋")
st.write()

st.markdown(
        """
        Here is a single source of my NLP works. Please explore them and give valuable comments!! If you find that we share the same interests, reach out to [me](https://www.linkedin.com/in/aungsettpaing/) so we can learn together.

        👈 **Choose an interactive application** from the sidebar to see how it works!

        #### Applications 👇

        ##### 1. Arsenal - Analysis and Interactive Dashboard Project
        I love watching football (I also love to play but I can't 😩) and now you must know which team I am a fan of. This idea of bite-sized project came out while I was learning google data analytics from Coursera. It includes Arsenal's last 4 years performance and it explains that Mike Dean, one of the referees, is not that biased against us!
        
        ##### 2. Gender Detection
        I was just wondering what if our gender can be guessed when registering to some sites right after adding our names. This, however, only covers for the Burmese names. Plus, there is another option for detecting gender - our voice!
        

        ##### 3. Text Summarization
        This is actually my thesis work that Buddha can only know when I will finish 😄. I did focus on the extractive text summarization using both supervised and unsupervised approach. Again, it is for Burmese news summarization.

        ##### 4. Text Segmentation
        Segmenting texts into different levels of units are challenging tasks for Burmese language. They are my first NLP works. Despite rule-based segmentations, I am proud to list them - syllabification especially.
    """
    )
