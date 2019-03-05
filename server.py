from flask import Flask, render_template, redirect, request
import util
import data_manager
import connection
import csv
from datetime import datetime

app = Flask(__name__)

generated_ids = []


@app.route('/', methods=['GET', 'POST'])
def home_page():
    all_qs = data_manager.get_questions('submission_time')
    search_for = request.form.get('search')

    if request.method == 'POST':
        results = data_manager.search_for_q(search_for)

        return render_template(url_for("search"), results=results, search_for=search_for)


    return render_template('home.html', questions=all_qs)


@app.route('/ordered-home/<how>/desc')
def order_home_desc(how):
    all_qs = data_manager.get_questions(how)

    return render_template('home.html', questions=all_qs)

@app.route('/ordered-home/<how>/asc')
def order_home_asc(how):
    all_qs = data_manager.get_questions_asc(how)

    return render_template('home.html', questions=all_qs)


@app.route('/search/<search_for>')
def search(search_for):
    print(search_for)
    results = data_manager.search_for_q(search_for)
    return render_template('search.html', results=results)


@app.route('/all-questions')
def all_questions():
    all_qs = data_manager.get_questions('submission_time')

    return render_template('allquestions.html', questions=all_qs)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    message = request.form.get('message')
    title = request.form.get('title')
    image = request.form.get('image')
    if request.method == 'POST':
        data_manager.new_question(title, message, image)

        return redirect('/')

    return render_template('add-question.html', message=message, title=title, image=image)


@app.route('/question/<int:question_id>', methods=['GET','POST'])
def question_page(question_id):

    my_q = data_manager.get_q_by_id(question_id)
    my_a = data_manager.get_answer_by_q(question_id)
    question_comment = data_manager.get_q_comments(question_id)
    data_manager.view_number_increase(question_id)


    if request.method == "POST":
        return render_template('question-comment.html', question=my_q)


    return render_template('q-and-a.html', question=my_q, answer=my_a, question_comments=question_comment)


@app.route('/question/<int:question_id>/question-comment', methods=['GET', 'POST'])
def question_comment(question_id):
    comment = request.form.get('comment')
    my_q = data_manager.get_q_by_id(question_id)
    my_a = data_manager.get_answer_by_q(question_id)
    if request.method == "POST":
        data_manager.new_q_comment(comment, question_id)

        return redirect('/')

    return render_template("question-comment.html", question_id=question_id, question=my_q, answer=my_a, question_comments=comment)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def give_answer(question_id):
    my_answer = request.form.get('message')
    image = request.form.get('image')

    if request.method == 'POST':
        data_manager.new_answer(question_id,my_answer,image)
        return redirect('/')

    return render_template('answer.html', message=my_answer, image=image, question_id=question_id)


@app.route('/delete-question/<int:question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == "GET":
        data_manager.delete_q(question_id)
        return redirect('/')

    all_qs = data_manager.get_questions('submission_time')

    return render_template('home.html', questions=all_qs)


@app.route('/question/<int:question_id>/answer-comment')
def answer_comment(answer_id):
    answer_comment = request.form.get('answer-comment')
    if request.method == "POST":
        data_manager.new_a_comment(answer_comment, answer_id)
        my_q = data_manager.get_q_by_id(answer_id)
        my_a = data_manager.get_answer_by_q(answer_id)
        comment = data_manager.get_q_comments(answer_id)
        answer_comments = data_manager.get_a_comments()
        return render_template('q-and-a.html', question=my_q, answer=my_a, question_comments=comment, answer_comment=answer_comments)
    return render_template('answer_comment.html', answer_id)


#@app.route('/answer/<int:answer[0]["question_id"]>/<int:answer[0]["id"]>')
#def selected_answer(question_id, answer_id):
    #    answer = data_manager.get_answer_by_q(question_id)
    #comments = data_manager.get_a_comments(answer_id)
    #return render_template("selected-answer.html", answer=answer, comments=comments)






@app.route('/answer/<int:answer_id>/edit-answer', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_the_choosen_answer(answer_id)
    if request.method == 'POST':
        answer_message = request.form.get('edit-answer')
        data_manager.editing_answer(answer_id, answer_message)
        return redirect('/')
    return render_template('edit_answer.html', answer=answer[0])






if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
