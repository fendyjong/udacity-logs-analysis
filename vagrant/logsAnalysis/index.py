from flask import Flask, request, redirect, url_for, render_template, send_file

from appDb import get_answer, download_answer_as_text

app = Flask(__name__)


@app.route('/')
def main():
    """Main page"""
    html = render_template('layout.html', answer1=get_answer(1), answer2=get_answer(2),
                           answer3=get_answer(3))
    return html


@app.route('/download/<question>')
def download(question):
    filename = download_answer_as_text(question)
    return send_file(filename, as_attachment=True, cache_timeout=1)
