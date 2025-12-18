import streamlit as st
import requests
import PIL
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import google.generativeai as genai
import json

import google.generativeai
print(google.generativeai.__version__)

GOOGLE_API_KEY='AIzaSyBN0GFHKyhNVcT4LLCFxz1ZfiOvsZsbepo'
genai.configure(api_key=GOOGLE_API_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')


st.title("Chat with Graphs")
st.subheader("Ask questions about your image")
# Set page configuration

# Function to fetch image from URL
@st.cache_data
def fetch_image(image_url):
    result = requests.get(image_url)
    try:
        image = PIL.Image.open(BytesIO(result.content))
        return image
    except PIL.UnidentifiedImageError:
        st.error("Error: Unidentified image format.")
        return None

# Function to save the questions, answers, and image URL
def save_interaction(image_url, question, answer, filename="saved_data.json"):
    data = {"image_url": image_url, "question": question, "answer": answer}
   
    # Load existing data if the file exists
    try:
        with open(filename, "r") as file:
            saved_data = json.load(file)
    except FileNotFoundError:
        saved_data = []
 
    # Append new interaction
    saved_data.append(data)
 
    # Save back to file
    with open(filename, "w") as file:
        json.dump(saved_data, file, indent=4)



# Main function for the Streamlit app
def main():
    # Input field for Image URL
    st.sidebar.subheader("Enter Image URL:")
    image_url = st.sidebar.text_input("")

    # Fetch and display image if URL is provided
    if image_url:
        image = fetch_image(image_url)
        if image:
            st.sidebar.image(image, caption='Image', use_container_width=True)

            # Vision model processing
            
            st.write("Ask any query about the image:")

            # Input field for user query
            user_input = st.text_input("Your Query:")

            # Submit button for user query
            if st.button("Submit"):
                if user_input:
                    # Generate response from vision model
                    response = vision_model.generate_content([user_input, image])
                    st.text_area("Model's Response:", value=response.text, height=150, max_chars=None)






if __name__ == "__main__":
    main()