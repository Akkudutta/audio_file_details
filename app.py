import streamlit as st
import soundfile as sf


st.set_page_config(page_title="Audio File Information", page_icon='🎛')

# Function to get sample rate and bit depth for audio files
def get_file_info(file_contents, file_extension):
    # Save the uploaded file in a temporary location
    with st.spinner("Analyzing audio file..."):
        with open("temp_audio.wav", "wb") as f:
            f.write(file_contents)

    with sf.SoundFile("temp_audio.wav") as audio_file:
        sample_rate = audio_file.samplerate
        bit_depth = audio_file.subtype
        channels = audio_file.channels

    if file_extension == "mp3":
        bit_depth = "16-bit"  # Set bit depth to 16-bit for mp3 files

    return sample_rate, bit_depth, channels

# Streamlit web app
st.title("Audio File Information Finder")

uploaded_file = st.file_uploader("Upload an audio file (WAV or MP3)", type=["wav", "mp3"], key="audio_file")

if uploaded_file is not None:
    # Check the file format and display the sample rate and bit depth
    file_extension = uploaded_file.name.split(".")[-1].lower()
    file_name = uploaded_file.name

    sample_rate, bit_depth, channels = get_file_info(uploaded_file.read(), file_extension)

    if file_extension not in ["wav", "mp3"]:
        st.error("Unsupported file format. Please upload a WAV or MP3 file.")
    else:
        # Create a data dictionary with "File Name," "Sample Rate," "Bit Depth," and "No of Channels"
        data = {
            "Attribute": ["File Name", "Sample Rate", "Bit Depth", "No of Channels"],
            "Value": [file_name, f"{sample_rate/1000} kHz", bit_depth[4:], channels],
        }
        # Display the table without row and column labels using CSS
        st.markdown(
            """
            <style>
                .dataframe {text-align: left;}
                th {display: none;}
                th, td:first-child {display: none;}
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.table(data)
