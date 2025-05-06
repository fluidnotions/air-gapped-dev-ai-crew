from pathlib import Path

import streamlit as st
from crewai import Task, Crew
from crew_agents import architect_agent  # you should define this in crew_agents.py
import whisper
import pyttsx3
import soundfile as sf
import numpy as np
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import streamlit as st
from agent_tools import MCMGitDiffTool

st.set_page_config(page_title="Codebase Assistant with Voice", layout="centered")
st.title("🎙️ Codebase AI Chat Assistant")

# Session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input fallback
user_input = st.text_input("Ask a question about your codebase:")

# Microphone STT
st.markdown("---")
st.subheader("🎤 Or record your voice")
audio_data = None

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.audio_frames.append(audio)
        return frame

webrtc_ctx = webrtc_streamer(
    key="stt", audio_processor_factory=AudioProcessor, media_stream_constraints={"audio": True, "video": False}
)

if st.button("Transcribe Voice") and webrtc_ctx.audio_processor:
    audio_frames = webrtc_ctx.audio_processor.audio_frames
    if audio_frames:
        audio = np.concatenate(audio_frames)
        sf.write("temp.wav", audio, 16000)

        model = whisper.load_model("base")
        result = model.transcribe("temp.wav")
        user_input = result["text"]
        st.success(f"You said: {user_input}")

# Process query if available
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    task = Task(description=user_input, agent=architect_agent)
    crew = Crew(agents=[architect_agent], tasks=[task], verbose=False)
    with st.spinner("Thinking..."):
        response = crew.run()
    st.session_state.chat_history.append(("AI", response))

    # Text-to-speech
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

# Chat history display
st.markdown("---")
st.subheader("📝 Chat History")
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")



    st.set_page_config(page_title="Local AI Crew", layout="wide")
    st.title("🧠 Local AI Assistant")

    # Tabs
    tabs = st.tabs(["Chat", "MCM Diff Viewer"])

    # Tab 1: Chat UI placeholder (to be integrated)
    with tabs[0]:
        st.subheader("Chat with your agents")
        st.info("Voice/chat interface coming soon...")

    # Tab 2: MCM Diff Viewer
    with tabs[1]:
        st.subheader("🧩 MCM Codebase Diff Tool")

        repo_path = Path('/Users/justinrobinson/Documents/hyvemobile/repos/mcm.v3')
        target_branch = st.text_input("Branch to compare:", value="domains/ng.mycontent.mobi")
        reference_branch = st.text_input("Reference branch:", value="default-integration")
        limit = st.slider("Max number of files to diff:", min_value=1, max_value=100, value=20)

        if st.button("🔍 Generate Diff Report"):
            try:
                tool = MCMGitDiffTool(repo_path, reference_branch)
                html = tool.diff_to_html(target_branch, limit=limit)
                st.components.v1.html(html, height=1000, scrolling=True)
            except Exception as e:
                st.error(f"❌ Failed to generate diff: {e}")

