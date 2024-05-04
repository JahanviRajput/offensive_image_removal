# -*- coding: utf-8 -*-

# pip install -q -U google-generativeai

"""### Import packages

Import the necessary packages.
"""
import time

# Record the current time before the code execution
start_time = time.time()

import pathlib
import textwrap

import google.generativeai as genai
from google.generativeai.types.generation_types import BlockedPromptException
from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY='AIzaSyCIU_780eWIZShAQpYU5snCEeWvFTOUAZI'

genai.configure(api_key=GOOGLE_API_KEY)

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel('gemini-pro')

"""## Generate text from image and text inputs

Gemini provides a multimodal model (`gemini-pro-vision`) that accepts both text and images and inputs. The `GenerativeModel.generate_content` API is designed to handle multimodal prompts and returns a text output.

Let's include an image:
"""

# import PIL.Image

# img = PIL.Image.open('fashion.jpeg')
# img

"""Use the `gemini-pro-vision` model and pass the image to the model with `generate_content`."""

model = genai.GenerativeModel('gemini-pro-vision')

# !unzip /content/image.zip
# !unzip /content/combined_images.zip

import os
# import pandas as pd
import PIL.Image

# Create an empty DataFrame with columns 'safety_rating' and 'file_name'
# df = pd.DataFrame(columns=['safety_rating', 'file_name'])

def massage_of_image(item_path,msg):
    for root, dirs, files in os.walk(item_path):
            for file_name in files:
                if file_name.endswith(('.jpg')) or file_name.endswith(('.jpeg')) or file_name.endswith(('.png')) :
                  try:
                    file_full_path = os.path.join(item_path, file_name)
                    print('\n',file_name,'\n')
                    img = PIL.Image.open(file_full_path)
                    response = model.generate_content([msg, img], stream=True)
                    response.resolve()
                    print(response.text)
                  except BlockedPromptException as e:
                          # Remove the image file
                          os.remove(file_full_path)
                          print(f"\n ________________________________________________Image {file_name} removed____________________________'\n")
                  except:
                    safety_ratings = response.candidates[0].safety_ratings
                    print('\n',safety_ratings,'\n')
                    # Check if any safety rating is not negligible
                    remove_image = any(safety_rating.probability != 'NEGLIGIBLE' for safety_rating in safety_ratings)
                    # Remove image if any safety rating is not negligible
                    if remove_image:
                        # Your code to remove the image goes here
                        os.remove(file_full_path)
                        print(f"\n ________________________________________________Image {file_name} removed____________________________'\n")
                        # print("Image removed.")
                    else:
                        print("Image not removed.")


def explore_folder(folder_path, non_offensive_categories):
    value = []
    items = os.listdir(folder_path)
    print('items',items)
    # Loop through each item
    for item in items:
        # Create the full path of the item
        item_path = os.path.join(folder_path, item)
        if item not in non_offensive_categories:
          print("_____________________________",item.upper(),"_____________________________")
          if item.lower() == 'actor':
              msg = "Please assess the following image for potentially offensive content. \
                                    Consider various aspects of potential offensiveness and provide your evaluation using the \
                                    following categories:\
                                      Violence: [No, Unlikely, Likely],\
                                      Adult Content: [No, Unlikely, Likely],\
                                      Nudity: [No, Unlikely, Likely],\
                                      Cultural Insensitivity: [No, Unlikely, Likely],\
                                      Child Abuse: [No, Unlikely, Likely]\
                                    If you observe nudity in the image, consider whether it is presented in a non-offensive manner,\
                                    such as in an artistic or non-sexual context. In such cases, you may categorize it as adult content.\
                                    Ensure your evaluation encompasses cultural, societal. Please note any other forms of offensiveness not \
                                    covered by the provided categories."
          elif item.lower() == 'dance':
              msg = "Please assess the following image for potentially offensive content. \
                                    Consider various aspects of potential offensiveness and provide your evaluation using the \
                                    following categories:\
                                      Violence: [No, Unlikely, Likely],\
                                      Adult Content: [No, Unlikely, Likely],\
                                      Nudity: [No, Unlikely, Likely],\
                                      Hate Speech: [No, Unlikely, Likely],\
                                      Cultural Insensitivity: [No, Unlikely, Likely],\
                                      Child Abuse: [No, Unlikely, Likely]\
                                    If you observe nudity in the image, consider whether it is presented in a non-offensive manner,\
                                    such as in an artistic or non-sexual context. In such cases, you may categorize it as adult content.\
                                    Ensure your evaluation encompasses cultural, societal. Please note any other forms of offensiveness not \
                                    covered by the provided categories."
          elif item.lower() == 'fashion':
            msg = "Please assess the following image for potentially offensive content. \
                                    Consider various aspects of potential offensiveness and provide your evaluation using the \
                                    following categories:\
                                      Adult Content: [No, Unlikely, Likely],\
                                      Nudity: [No, Unlikely, Likely],\
                                      Hate Speech: [No, Unlikely, Likely],\
                                      Cultural Insensitivity: [No, Unlikely, Likely],\
                                    If you observe nudity in the image, consider whether it is presented in a non-offensive manner,\
                                    such as in an artistic or non-sexual context. In such cases, you may categorize it as adult content.\
                                    Ensure your evaluation encompasses cultural, societal. Please note any other forms of offensiveness not \
                                    covered by the provided categories."
          elif item.lower() == 'painting':
            msg = "Please assess the following image for potentially offensive content. \
                                    Consider various aspects of potential offensiveness and provide your evaluation using the \
                                    following categories:\
                                      Violence: [No, Unlikely, Likely],\
                                      Adult Content: [No, Unlikely, Likely],\
                                      Nudity: [No, Unlikely, Likely],\
                                      Hate Speech: [No, Unlikely, Likely],\
                                      Cultural Insensitivity: [No, Unlikely, Likely],\
                                      Child Abuse: [No, Unlikely, Likely]\
                                    If voilence is present in religious way then it can be \
                                    considered into non offensive category. Please note any other forms of offensiveness not \
                                    covered by the provided categories."
          elif item.lower() == 'temples':
            msg = "Please assess the following image for potentially offensive content. \
                                    Consider various aspects of potential offensiveness and provide your evaluation using the \
                                    following categories:\
                                      Child Abuse: [No, Unlikely, Likely]\
                                      Cultural Insensitivity: [No, Unlikely, Likely],\
                                    Ensure your evaluation encompasses cultural, societal.\
                                    Please note any other forms of offensiveness not \
                                    covered by the provided categories."
          elif item.lower() == 'handicrafts':
            msg = "Please assess the following image for potentially offensive content. \
                                    Consider various aspects of potential offensiveness and provide your evaluation using the \
                                    following categories:\
                                      Violence: [No, Unlikely, Likely],\
                                      Adult Content: [No, Unlikely, Likely],\
                                      Nudity: [No, Unlikely, Likely],\
                                      Hate Speech: [No, Unlikely, Likely],\
                                      Cultural Insensitivity: [No, Unlikely, Likely],\
                                      Child Abuse: [No, Unlikely, Likely]\
                                    If you observe nudity in the image, consider whether it is presented in a non-offensive manner,\
                                    such as in an artistic or non-sexual context. In such cases, you may categorize it as adult content.\
                                    If voilence is present in religious way then it can be \
                                    considered into non offensive category. Please note any other forms of offensiveness not \
                                    covered by the provided categories."
          elif item.lower() == 'governance and politics':
            msg = "Please assess the following image for potentially offensive content. \
                                    Consider various aspects of potential offensiveness and provide your evaluation using the \
                                    following categories:\
                                      Violence: [No, Unlikely, Likely],\
                                      Adult Content: [No, Unlikely, Likely],\
                                      Hate Speech: [No, Unlikely, Likely],\
                                      Cultural Insensitivity: [No, Unlikely, Likely],\
                                    If you observe nudity in the image, consider whether it is presented in a non-offensive manner,\
                                    such as in an artistic or non-sexual context. In such cases, you may categorize it as adult content.\
                                    If voilence is present in religious way then it can be \
                                    considered into non offensive category. Please note any other forms of offensiveness not \
                                    covered by the provided categories."
          elif item.lower() == 'education eystem and institutions':
              msg = "Please assess the following image for potentially offensive content. \
                                      Consider various aspects of potential offensiveness and provide your evaluation using the \
                                      following categories:\
                                        Violence: [No, Unlikely, Likely],\
                                        Adult Content: [No, Unlikely, Likely],\
                                        Nudity: [No, Unlikely, Likely],\
                                        Hate Speech: [No, Unlikely, Likely],\
                                        Cultural Insensitivity: [No, Unlikely, Likely],\
                                        Child Abuse: [No, Unlikely, Likely]\
                                      If voilence is present in religious way then it can be \
                                      considered into non offensive category. Please note any other forms of offensiveness not \
                                      covered by the provided categories."
          elif item.lower() == 'education eystem and institutions':
              msg = "Please assess the following image for potentially offensive content. \
                                      Consider various aspects of potential offensiveness and provide your evaluation using the \
                                      following categories:\
                                        Adult Content: [No, Unlikely, Likely],\
                                        Nudity: [No, Unlikely, Likely],\
                                        Child Abuse: [No, Unlikely, Likely]\
                                      If voilence is present in religious way then it can be \
                                      considered into non offensive category. Please note any other forms of offensiveness not \
                                      covered by the provided categories."
          elif item.lower() == 'tribal culture':
              msg = "Please assess the following image for potentially offensive content. \
                                      Consider various aspects of potential offensiveness and provide your evaluation using the \
                                      following categories:\
                                        Violence: [No, Unlikely, Likely],\
                                        Adult Content: [No, Unlikely, Likely],\
                                        Nudity: [No, Unlikely, Likely],\
                                        Hate Speech: [No, Unlikely, Likely],\
                                        Cultural Insensitivity: [No, Unlikely, Likely],\
                                        Child Abuse: [No, Unlikely, Likely]\
                                      If voilence is present in religious way then it can be \
                                      considered into non offensive category. Please note any other forms of offensiveness not \
                                      covered by the provided categories."
          else:
            print("Invalid Category")
            exit()
          massage_of_image(item_path, msg)


# Usage for all the images:
# folder_path = "/content/chosen_images"
folder_path = '/Users/jahanvirajput/Downloads/chosen_images'
non_offensive_categories = ['.DS_Store' ,'coin', 'food', 'monument', 'vehicles', 'musical_instruments', 'religion', 'sports', 'yoga and meditation' ]
# Start exploring from the current directory
explore_folder(folder_path, non_offensive_categories)

end_time = time.time()

# Calculate the time taken by subtracting start time from end time
elapsed_time = end_time - start_time

print("Time taken:", elapsed_time, "seconds")

