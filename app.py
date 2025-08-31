# app.py
import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="Transcript Extractor", layout="centered")

st.title("Transcript Extractor")
st.caption("Navigate to the lecture recording page and: \n1. Click transcript and ensure it is highlighted blue \n2. Click 'ctrl + shift + I' or 'cmd + option + I' to inspect the page \n3. Right click on the line that says '<html lang='en' class>', click 'copy' and click 'copy element'\n4. Paste the full HTML code below. The app extracts transcript times and texts.")


# Input field
html_content = st.text_area(
    "Paste HTML here:",
    value="",
    height=300,
    placeholder="Paste the website's HTML source here...",
)

# Button to run extraction
if st.button("Extract Transcript", type="primary"):
    if not html_content.strip():
        st.warning("Please paste some HTML first.")
    else:
        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")
        transcript_times = soup.find_all("div", class_="transcript-time")
        transcript_texts = soup.find_all("div", class_="transcript-text")

        times = [t.get_text(strip=True) for t in transcript_times]
        lines = [l.get_text(strip=True) for l in transcript_texts]

        transcript = ""
        for t, l in zip(times, lines):
            transcript += f"{t} {l}\n"

        if transcript:
            st.success(f"Transcript extracted: {len(transcript.splitlines())} lines found.")
            st.text_area("Transcript", value=transcript, height=300)
            st.download_button(
                "Download Transcript",
                data=transcript,
                file_name="transcript.txt",
                mime="text/plain",
            )
        else:
            st.error("No transcript lines found. Check the HTML structure.")
