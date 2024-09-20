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

# Function to preprocess the extracted text
def preprocess_text(text):
    # Clean unwanted characters and extra spaces
    clean_text = re.sub(r'[^A-Za-z0-9\s\.\-:]', '', text)
    return clean_text

# Function to extract transaction details using regex
def extract_transaction_details(text):
    date_pattern = r"((Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s+[A-Za-z]+\s+\d{1,2}\s+\d{4})"
    time_pattern = r"(\d{1,2}:\d{2}\s*(AM|PM))"
    amount_pattern = r"GHS\s*[\d\.\-]+"

    dates = re.findall(date_pattern, text)
    times = re.findall(time_pattern, text)
    amounts = re.findall(amount_pattern, text)

    return dates, times, amounts

# Function to ensure equal list lengths for DataFrame creation
def pad_lists(dates, times, amounts):
    max_len = max(len(dates), len(times), len(amounts))
    dates += [None] * (max_len - len(dates))
    times += [None] * (max_len - len(times))
    amounts += [None] * (max_len - len(amounts))
    return dates, times, amounts

# If an image is uploaded
if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Extract text from the image using OCR
    extracted_text = extract_text_from_image(image)
    
    # Show the raw extracted text for debugging
   # st.write("Raw Extracted Text:")
   # st.write(extracted_text)
    
    # Preprocess the extracted text
    preprocessed_text = preprocess_text(extracted_text)
    
    # Show the preprocessed text for debugging
   # st.write("Preprocessed Text:")
    #st.write(preprocessed_text)
    
    # Extract the transaction details
    dates, times, amounts = extract_transaction_details(preprocessed_text)
    
    print(dates, times, amounts)

    # Ensure equal list lengths for DataFrame creation
    dates, times, amounts = pad_lists(dates, times, amounts)
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Time': times,
        'Amount': amounts
    })
    
    st.write("Extracted Transaction Data:")
    st.write(df)
    
    # Convert the DataFrame to a CSV
    csv = df.to_csv(index=False)
    
    # Create a download button for the CSV file
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="transaction_data.csv",
        mime="text/csv"
    )