import os
import streamlit as st
from getpass import getpass


st.title("P.A.N.D.O.R.A.")

values = st.slider("Select a range of values", 0.0, 1)
st.write("Values:", values)

text = st.text_area(label="Description your problem", value="")
st.button("Send")


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
