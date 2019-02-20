from flask import Flask, render_template, redirect, request
import util
import data_manager
import connection
import csv
from datetime import datetime

app = Flask(__name__)

generated_ids = []


@app.route('/')
def home_page():
    all_questions = data_manager.get_questions()

    return render_template('home.html', questions=all_questions)

@app.route('/add-question', methods=['GET' , 'POST'])
def add_question():
    message = request.form.get('message')
    title = request.form.get('title')
    image = request.form.get('image')
    if request.method == 'POST':
        data_manager.new_question(title, message, image)

        return redirect('/')

    return render_template('add-question.html', message=message, title=title, image=image)


@app.route('/question/<int:question_id>/new-answer')
def question_page(question_id):

    my_q = data_manager.get_q_by_id(question_id)
    my_a = data_manager.get_answer_by_q(question_id)


    return render_template('q-and-a.html', question=my_q, answer=my_a)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
