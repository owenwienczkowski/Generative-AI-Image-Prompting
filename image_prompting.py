# this program uses generative AI for image prompting to identify and categorize contents of a vending machine.

import google.generativeai as genai
from PIL import Image
from keys import key
import json

# key hidden for privacy reasons
genai.configure(api_key=key)

# import latest version of gemini-1.5-pro
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# create system prompt
system_prompt = "You are a generative AI assistant who specializes in analyzing images and producing desired details"

# Open the images
image_path_1 = 'vending-machine-1.jpg'
vending_machine_image_1 = Image.open(image_path_1)

image_path_2 = 'vending-machine-2.jpg'
vending_machine_image_2 = Image.open(image_path_2)

# create the user prompt
text_prompt = "List all the items inside the vending machines and help me organize them into categories."

prompt = [text_prompt, vending_machine_image_1, vending_machine_image_2]

# begin list to store conversation history (only necessary for continuing conversation)
system_data = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": text_prompt, "attachments": (image_path_1, image_path_2)}
]

# generate AI response
response = model.generate_content(prompt)

# store AI response in chat history
system_data.append({"role": "assistant", "content": response})

# format response text as string
response_text = response.text

# print response
print("Assistant: " + response_text)


# Function to parse the response text and create a dictionary
def parse_response(text):
    data = {}
    current_machine = None
    current_category = None

    for line in text.split('\n'):
        line = line.strip()
        if line.startswith("**Vending Machine"):
            current_machine = line.strip('*: ')
            data[current_machine] = {}
        elif line.startswith("* **"):
            current_category = line.strip('*: ')
            data[current_machine][current_category] = []
        elif line.startswith("* "):
            item = line.strip('*: ')
            data[current_machine][current_category].append(item)
        elif line.startswith("**General Categories"):
            current_machine = "General Categories"
            data[current_machine] = {}
        elif line.startswith("* "):
            category = line.strip('*: ')
            data[current_machine][category] = []

    return data


# Parse the response text
parsed_data = parse_response(response_text)

# Writing to vending_machines.json
with open("vending_machines.json", "w") as outfile:
    json.dump(parsed_data, outfile, indent=4)

print("Data has been written to vending_machines.json\n")

