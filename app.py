import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import re



# Title of the Streamlit app
st.title('Extract Transaction Details from Image and Save to CSV')

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Function to extract text using pytesseract
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)



def preprocess_text(text):
    clean_text = re.sub(r'[^A-Za-z0-9\s\.\-:]', '', text)
    return clean_text


def extract_transaction_details(text):
    date_pattern = r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+[A-Za-z]+\s+\d{1,2}\s+\d{4}"
    time_pattern = r"\d{1,2}:\d{2}\s*(AM|PM)"
    amount_pattern = r"GHS\s*[\d\.\-]+"

    
    dates = re.findall(date_pattern, text)
    times = re.findall(time_pattern, text)
    amounts = re.findall(amount_pattern, text)

    return dates, times, amounts

# Function to pad lists with None for DataFrame creation
def pad_lists(dates, times, amounts):
    max_len = max(len(dates), len(times), len(amounts))
    dates += [None] * (max_len - len(dates))
    times += [None] * (max_len - len(times))
    amounts += [None] * (max_len - len(amounts))
    return dates, times, amounts


if uploaded_file is not None:
    
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
   
    extracted_text = extract_text_from_image(image)
    
    
    st.write("Raw Extracted Text:")
    st.write(extracted_text)
    
    
    preprocessed_text = preprocess_text(extracted_text)
    
    
    st.write("Preprocessed Text:")
    st.write(preprocessed_text)
    
    
    dates, times, amounts = extract_transaction_details(preprocessed_text)
    
    # Pad the lists to ensure equal lengths for DataFrame creation
    dates, times, amounts = pad_lists(dates, times, amounts)
    
    
    df = pd.DataFrame({
        'Date': dates,
        'Time': times,
        'Amount': amounts
    })
    
    st.write("Extracted Transaction Data:")
    st.write(df)
    
    
    csv = df.to_csv(index=False)
    
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="transaction_data.csv",
        mime="text/csv"
    )