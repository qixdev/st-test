import cohere
import streamlit as st
COHERE_API_KEY = "HYtK23kvuUwiyHapMuY85d5NuKWZV22AvK8gYKbY"
co = cohere.Client(COHERE_API_KEY)

def generate_idea(industry, temperature):
    prompt = f"""
    Generate a startup idea given the industry.

    # Examples
    Industry: Workplace
    Startup Idea: A platform that generates slide deck contents automatically based on a given outline

    Industry: Home Decor
    Startup Idea: An app that calculates the best position of your indoor plants for your apartment

    Industry: Healthcare
    Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week

    Industry: Education
    Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals

    Industry: {industry}"""

    response = co.chat(
        model='command-r',
        message=prompt,
        preamble="",
        temperature=temperature,
    )
    return response.text.replace("Startup Idea: ", "")


def generate_name(idea):
    prompt= f"""
    Generate a startup name and name given the startup idea.

    # Examples
    Startup Idea: A platform that generates slide deck contents automatically based on a given outline
    Startup Name: Deckerize

    Startup Idea: An app that calculates the best position of your indoor plants for your apartment
    Startup Name: Planteasy

    Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week
    Startup Name: Hearspan

    Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals
    Startup Name: Prime Age

    Startup Idea: {idea}"""
    response = co.chat(
        model='command-r',
        message=prompt,
        preamble="",
    )
    return response.text.replace("Startup Name: ", "")

st.title("🚀 Startup Idea Generator")
form = st.form(key="user-settings")
with form:
    col1, col2 = st.columns(2)
    industry_input = st.text_input("Industry", key="industry_input")
    with col1:
        num_input = st.slider("Number of ideas", value = 3, key = "num_input", min_value=1, max_value=10)
    with col2:
        creativity_input = st.slider("Creativity", value = 0.5, key = "creativity_input", min_value=0.1, max_value=0.9)
    generate_button = form.form_submit_button("Generate Idea")
    if generate_button and industry_input:
        bar = st.progress(0.05)
        st.subheader("Startup ideas")
        for i in range(num_input):
            startup_idea = generate_idea(industry=industry_input, temperature=creativity_input)
            startup_name = generate_name(idea=startup_idea)
            st.markdown("#### %s"%startup_name)
            st.write(startup_idea)
            bar.progress((i+1)/num_input)
