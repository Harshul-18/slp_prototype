import streamlit as st
import soundfile as sf
import io
import numpy as np

# Use Streamlit to get the audio input from the user
audio_input = st.audio_input("Record audio")

# Check if the user has started recording
if audio_input is not None:
    # Convert the audio input to a numpy array
    audio_array = np.frombuffer(audio_input, dtype=np.int16)

    # Save the audio as a .wav file
    with io.BytesIO() as buffer:
        sf.write(buffer, audio_array, samplerate=44100)
        st.audio(buffer.getvalue(), format='audio/wav')
        with open('recorded_audio.wav', 'wb') as f:
            f.write(buffer.getvalue())