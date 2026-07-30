from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("AI RESUME GENERATION")
st.write("""This app helps user to build customized professional Resume
with Latest Job apply links""")

st.image("bg.png")
st.sidebar.title("Fill Important Details")
st.sidebar.image("bg.png")

TAVILY_API_KEY = "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"
GOOGLE_API_KEY = "AQ.Ab8RN6JWAS9vcT6ZtC2ESg_rNIZeGqWYdsVFLhUTgJ3htX3LuA"
GROQ_API_KEY =  "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"

model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)

# response = model.invoke("Hello Buddy!")
# response.content[-1]["text"]


def search_latest_news_jobs(query):
  """This function helps to fetch lastest
  news or jobs related article using
  tavily"""

  client = TavilyClient(
      api_key  = TAVILY_API_KEY)

  response = client.search(query)
  return response

  # Agent Creation
agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs])
# agent


def main_agent(agent, query):
  """This is the main agent, or leader agent
  orchestrate sub agents"""

  # Giving prompt to create detailed prompt
  # for code generation
  prompt = """You are AI assistant and
  below given is prompt, your
  task is to give detailed prompt for
  this.
  You are a professional Resume generator
  where user will give their personal info,
  you have to create detailed Resume
  for students or professional one,
  it must be with dynamic UI and UX and,
  with advanced CSS Professional Designing
  Make sure to give output in HTML format only
  no markdowns allowed
  """

  response = agent.invoke({"messages":[{'role':'user',
                                        'content':prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']

  # SAVE PROMPT using File Handling

  with open("prompt.txt",'w') as f:
    f.write(detailed_prompt)

  user_details = f"""Below Given is a user details
  generate Resume based on that, if not
  given keep: Default Resume: Python Developer
  user details: {query}"""

  final_prompt = prompt + detailed_prompt + user_details

  # CODE GENERATION

  response = agent.invoke({"messages":[{'role':'user',
                                        'content':final_prompt}]})

  code = response['messages'][-1].content[-1]['text']

  return code


# code = main_agent(agent,"MANNAN LAMBA, AI DEVOPS EXPERT")
# from IPython import display as DISPLAY
# DISPLAY.HTML(code)


# Fetch Latest Domain related Jobs using Tavily

def get_jobs(agent,Location = "Noida,Delhi",Profile = "Junior Devops Engineer"):
  Location = "Noida,Delhi"
  Profile = "Junior Devops Engineer"
  prompt = f"""Based on user given Job profile,
  fetch latest jobs or job apply article
  using Naukri, Linkedin, Indeed, or all popular
  Job applyplatforms, Show Results with
  JOB PROFILE NAME, LOCATION, SALARY, COMPANY NAME,
  SHOW jobs only related to given
  {Location} and {Profile}, output must be in
  Professional HTML Naukri theme cards with Dynamic Design
  Show atleast Top 10-20 results with dir"""

  response = agent.invoke({"messages":[{'role':'user',
                                          'content':prompt}]})

  code = response['messages'][-1].content[-1]['text']

  return code

# code = get_jobs(agent,"Agra,Delhi,Noida","Devops engineer")
# DISPLAY.HTML(code) 
