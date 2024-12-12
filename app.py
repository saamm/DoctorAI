import streamlit as st
from pathlib import Path
import google.generativeai as genai
from click import prompt
import os

#print(os.environ.get("API_KEY", "API_KEY not found"))
from api_key import api_key

if api_key in os.environ:
    print("API key found in environment variables.")
else:
    print("API key not found. Please set it using `export API_KEY=<your_key>`.")

#export API_KEY=AIzaSyAyJRQpRrEX28pxegj8t8dEaVxQGJGYfdA
#configure GenAI
genai.configure(api_key=os.environ["API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

#Apply Safety Settings
safety_settings = [
    {
        "category" : "HARM_CATEGORY_HARASSMENT",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category" : "HARM_CATEGORY_HATE_SPEECH",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital.
Your expertist is crucial in identifying any anomalies, diseases, or health issues that may be present in the image.

Your responsibilities incluse:

1. Detailed Analysis : Thoroughly analyze each image, focusing on identifying an abnormal findings.
2. Findings Report : Document all observed anomalies or signs of diseases. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps : Based on your analysis, suggest potential nexr steps, including further tests or treatments as applicable.
4. Treatment Suggestions : If appropriate, recommend possible treatment options or intervention.

Important Notes :
1. Scope of Response : Only respond if the image pertains to human health issues.
2. Clarity of image : In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer : Accompany your analysis with the disclaimer : "Consult with a Doctor before making any decisions".
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis adhering to the structured approach outlined above 
"""
#model configuration
model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  safety_settings=safety_settings
)
#set page configuration
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

#set title
st.title("👩‍⚕️ Vital ❤️ Image 📷 Analytics 📊")

#set subtitles
st.subheader("An Application that can help users identify medical images")
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=['png', 'jpg', 'jpg'])

submit_button = st.button("Generate the Analysis")

if submit_button:
    # process uploaded image
    if not uploaded_file:
        st.write("Please upload image")
    image_data = uploaded_file.getvalue()

    #making our image ready
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]
    #making out prompt ready
    prompt_parts = [
        image_parts[0],
        system_prompt
    ]
    #Generate response
    response = model.generate_content(prompt_parts)
    st.write(response.text)






