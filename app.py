import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from transformers import pipeline

classifier = pipeline("zero-shot-classification",
                    model="facebook/bart-large-mnli")

labels = ["offensive", "non offensive", "neutral"]

stt_button = Button(label="Speak", width=100)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    text = result.get("GET_TEXT")
    if "GET_TEXT" in result:
        st.write(text)

    result = classifier(text, labels)
    if result['scores'][0] > result['scores'][1]:
        text = result['labels'][0]
    else:
        text = result['labels'][1]

    # text = st.text_input("Say what ?")
    # text = '. '.join(text.split())

    tts_button = Button(label="Speak", width=100)

    tts_button.js_on_event("button_click", CustomJS(code=f"""
        var u = new SpeechSynthesisUtterance();
        u.text = "{text}";
        u.lang = 'en-UK';

        speechSynthesis.speak(u);
        """))

    st.bokeh_chart(tts_button)