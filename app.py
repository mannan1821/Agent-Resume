# ========== LOAD MODULES ==========

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient

import streamlit as st
import os


# ========== STREAMLIT CONFIG ==========

st.set_page_config(layout="wide")

st.title("AI RESUME GENERATION")

st.write(
"""
This app helps user to build customized professional Resume
with Latest Job apply links
"""
)


if os.path.exists("bg.png"):
    st.image("bg.png")


# ========== API KEYS ==========

TAVILY_API_KEY = "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"
GOOGLE_API_KEY = "AQ.Ab8RN6JWAS9vcT6ZtC2ESg_rNIZeGqWYdsVFLhUTgJ3htX3LuA"



# ========== GEMINI MODEL ==========

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)


# Test Gemini connection

try:
    test = model.invoke("Hello")
    st.success("Gemini Connected Successfully")

except Exception as e:
    st.error(e)



# ========== TAVILY TOOL ==========

@tool
def search_latest_news_jobs(query: str):
    """
    Search latest jobs/news using Tavily
    """

    client = TavilyClient(
        api_key=TAVILY_API_KEY
    )

    response = client.search(query)

    return response



# ========== CREATE AGENT ==========

agent = create_agent(
    model=model,
    tools=[search_latest_news_jobs]
)



# ========== MAIN RESUME AGENT ==========

def main_agent(agent, query):


    prompt = """
You are an AI professional Resume generator.

Your task:
Create detailed professional resumes.

Requirements:
- Modern professional UI
- Advanced CSS design
- Responsive HTML
- Student and professional resume support
- Output HTML only
- No markdown
"""


    response = agent.invoke(
        {
            "messages":
            [
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        }
    )


    detailed_prompt = response["messages"][-1].content


    with open("prompt.txt","w") as f:
        f.write(detailed_prompt)



    user_details = f"""

Generate Resume based on user details.

If details are missing:
Use default profile:
Python Developer


User Details:

{query}

"""


    final_prompt = (
        prompt +
        detailed_prompt +
        user_details
    )


    response = agent.invoke(
        {
            "messages":
            [
                {
                    "role":"user",
                    "content":final_prompt
                }
            ]
        }
    )


    code = response["messages"][-1].content


    return code




# ========== JOB SEARCH AGENT ==========

def get_jobs(agent):


    prompt = """

Find latest DevOps Engineer jobs.

Show results in HTML format.

Include:
- Job Profile
- Company Name
- Location
- Salary
- Apply Link


Create professional job cards UI.

"""


    response = agent.invoke(
        {
            "messages":
            [
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        }
    )


    code = response["messages"][-1].content


    return code




# ========== STREAMLIT UI ==========


user_input = st.text_area(
    "Enter your details"
)



if st.button("Generate Resume"):

    if user_input:

        with st.spinner("Generating Resume..."):

            code = main_agent(
                agent,
                user_input
            )


        st.components.v1.html(
            code,
            height=1200,
            scrolling=True
        )


    else:

        st.warning(
            "Please enter user details"
        )




if st.button("Find Jobs"):

    with st.spinner("Finding Latest Jobs..."):

        jobs = get_jobs(agent)


    st.components.v1.html(
        jobs,
        height=1200,
        scrolling=True
    )
