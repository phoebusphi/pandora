import os
import time
import base64
import streamlit as st
from optimization_distribution import GAtelco
from create_gif import create_gif
from getpass import getpass

def func(generations,mu,eta,p1_num,p2_num,p3_num,bw_total):
    genetico = GAtelco(generations=generations, mu=mu, eta=eta).GA()
    p1=p1_num
    p2=p2_num
    p3=p3_num
    bw=bw_total
    pos, latency = genetico["dominio"][-1], genetico["imagen"][-1]
    print(pos)
    print(latency)
    create_gif('./images_gif/', 'output.gif')

#func()

st.set_page_config(
    page_title="PANDORA",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("P.A.N.D.O.R.A.")

col1, col2 = st.columns(2)
description = '''Genetic algorithms make use of the following parameters:
    
***Number of Generations***: Represents the number of cycles or generations defined for the algorithm. *(default value: 3000)* 

***Crossover***: Recombination is the main genetic operator, it represents sexual reproduction, it operates on two chromosomes at a time to generate two descendants where the characteristics of both parent chromosomes are combined. *(default value: 0.75)* 

***Mutation***: Randomly modifies part of the chromosome of individuals, and allows reaching areas of the search space that were not covered by the individuals of the current population. *(default value: 0.22)*

Below you can configure the parameters explained above.
    
'''

planning = '''Bellow set the parameters regarding Network Planning.

As user you are required to filled the estimated number of users for each priority and total Bandwidth capacity.

Currently PANDORA considers 3 kind of priorities or use cases:

***Priority 1***: VoIP and real-time applications

***Priority 2***: Video streaming applications

***Priority 3***: Web browsing and Non-critical applications

***Total Bandwidth***: Total Bandwidth capacity provided by Core ISP in Gbps.

'''

with col1:
    st.markdown(description)

    generations = st.number_input("Insert number of generations", min_value=1000, max_value=20000) # 3000
    cross = st.number_input("Insert Cross", min_value=0.00, max_value=1.00) # 0.75
    mutation = st.number_input("Insert Mutation", min_value=0.00, max_value=1.00) # 0.22

    st.markdown(planning)

    p1_num = st.number_input("Insert number of users for Priority 1", min_value=10, max_value=5000)
    p2_num = st.number_input("Insert number of users for Priority 2", min_value=10, max_value=5000)
    p3_num = st.number_input("Insert number of users for Priority 3", min_value=10, max_value=5000)

    total_bandwidth = st.number_input("Total Bandwidth capacity provided by Core ISP in Gbps", min_value=100, max_value=200000)
    st.button("Submit", on_click=func, args=[generations,cross,mutation,p1_num,p2_num,p3_num,total_bandwidth], type="primary")

with col2:
    st.image("optimal.jpg", caption="Sunrise by the mountains")

    while not os.path.exists("./output.gif"):
        print(f"El archivo output.gif no existe. Esperando...")
        time.sleep(2)
    file_ = open("./output.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="optimal position router gif">',
        unsafe_allow_html=True,
    )


# import os
# import json
# import openai
# #
# client = openai.OpenAI(
#     base_url="https://api.aimlapi.com/v1",
#     api_key='',
# )

# tools = [
#   {
#     "type": "function",
#     "function": {
#       "name": "get_current_weather",
#       "description": "Get the current weather in a given location",
#       "parameters": {
#         "type": "object",
#         "properties": {
#           "location": {
#             "type": "string",
#             "description": "The city and state, e.g. San Francisco, CA"
#           },
#           "unit": {
#             "type": "string",
#             "enum": [
#               "celsius",
#               "fahrenheit"
#             ]
#           }
#         }
#       }
#     }
#   }
# ]

# messages = [
#     {"role": "system", "content": "You are a helpful assistant that can access external functions. The responses from these function calls will be appended to this dialogue. Please provide responses based on the information from these function calls."},
#     {"role": "user", "content": "What is the current temperature of New York, San Francisco, and Chicago?"}
# ]

# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=messages,
#     tools=tools,
#     tool_choice="auto",
# )

# print(json.dumps(response.choices[0].message.model_dump()['tool_calls'], indent=2))
