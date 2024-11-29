import streamlit as st
from PIL import Image
import pyttsx3
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

GEMINI_API_KEY = ''  # write your key
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

image = Image.open(r"image file path")

st.image(image, use_column_width=True)
engine = pyttsx3.init()
st.markdown(
    """
    <style>
     .main-title { font-size: 48px; font-weight: bold; text-align: center; color: #4A90E2; margin-top: 50px; }
     .subtitle { font-size: 20px; color: #7D7D7D; text-align: center; margin-bottom: 40px; }
     .feature-header { font-size: 26px; color: #333; font-weight: bold; text-transform: uppercase; margin-top: 30px; }
     .stButton>button { background-color: #4A90E2; color: white; font-size: 16px; font-weight: bold; border-radius: 8px; padding: 10px 20px; border: none; transition: background-color 0.3s; }
     .stButton>button:hover { background-color: #357ABD; }
     footer { font-size: 14px; text-align: center; color: #A0A0A0; padding: 20px 0; background-color: #f1f1f1; }
     hr { border-top: 1px solid #ddd; margin: 30px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)



st.markdown('<div class="main-title">VisioTech</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Empowering lives with AI: Image descriptions and voice guidance!</div>', unsafe_allow_html=True)


image = Image.open(r"image file path")


st.sidebar.image(image,use_column_width=True)
st.sidebar.title("ℹ️ About VisioTech")
st.sidebar.markdown(
    """
    📌 **Features**
    - 🔍 **Describe Scene**: AI insights about the image, including objects and suggestions.  
    - 🔊 **Text-to-Speech**: Hear the extracted text aloud.  

    💡 **How it helps**:
    Assists visually impaired users by providing scene descriptions and speech guidance.

    🤖 **Powered by**:
    - **Google Gemini API** for scene understanding.  
    - **pyttsx3** for text-to-speech.
    """
)


st.sidebar.text_area("📜 Instructions", "1. Upload an image. 2. Choose a feature: Describe Scene or Listen to Text.") 



def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")


st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)


st.markdown("<h3 class='feature-header'>⚙️ Features</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

scene_button = col1.button("🔍 Describe Scene")
tts_button = col2.button("🔊 Text-to-Speech")


input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
4.check the image carefully ,give a short and simple description
"""

if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Generating scene description..."):
            response = generate_scene_description(input_prompt, image_data)
            st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
            st.write(response)

    if tts_button:
        with st.spinner("Converting text to speech..."):
            text = generate_scene_description(input_prompt, image_data)
            if text.strip():
                text_to_speech(text)
                st.success("✅ Text-to-Speech Conversion Completed!")
            else:
                st.warning("No text found to convert.")




