#Flask - Python Web Framework
from flask import Flask, render_template, request, redirect

#For getting video transcript using API
from youtube_transcript_api import YouTubeTranscriptApi

#Text Summarization HuggingFace (Seq2Seq Encoding Decoding)
from summarizer import summarize_text

#module call
from pdf_handler import pdf2text

#for getting the pdf files
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

from werkzeug.utils import secure_filename

import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'files'

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload")

#Function to get transcript using video ID
def get_yt_video_id(id):
    transcript = YouTubeTranscriptApi.get_transcript(id, languages=['en'])
    transcript_text = ''

    for text in transcript:
        transcript_text += text['text']

    summary = summarize_text(transcript_text)

    return " ".join(summary)
    #chunks = text_processing(transcript_text)
    #summary = summarize_text(chunks)
    #return summary

@app.route("/", methods = ["GET", "POST"])
@app.route("/home", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        url = str(request.form.get("url"))
        if '=' in url:
            video_id = str(url.split("=")[1])
        else:
            video_id = str(url.split("/")[3])
        text = get_yt_video_id(video_id)
        return text

    return render_template("root.html")


@app.route("/pdf", methods = ["GET", "POST"])
def pdf_text_try():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        text = pdf2text(file)
        summary = summarize_text(text)
        return " ".join(summary)
        #file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
        #                        secure_filename(file.filename)))  # Then save the file
        #return "File has been uploaded."

    return render_template('pdf.html', form = form)


if __name__ == '__main__':
    app.run(debug = True)