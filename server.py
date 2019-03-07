from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)

generated_ids = []


@app.route('/', methods=['GET', 'POST'])
def home_page():
    all_qs = data_manager.get_questions_desc('submission_time')
    search_for = request.form.get('search')

    return render_template('home.html', questions=all_qs, search_for=search_for)


@app.route('/ordered-home/<how>/desc')
def order_home_desc(how):
    all_qs = data_manager.get_questions_desc(how)

    return render_template('home.html', questions=all_qs)


@app.route('/ordered-home/<how>/asc')
def order_home_asc(how):
    all_qs = data_manager.get_questions_asc(how)

    return render_template('home.html', questions=all_qs)


@app.route('/search', methods=['GET'])
def search_route():
    search_string = request.args.get('search')
    results = data_manager.search_for_q(search_string)

    return render_template('search.html', results=results, search_for=search_string)


@app.route('/all-questions')
def all_questions():
    all_qs = data_manager.get_questions_desc('submission_time')

    return render_template('allquestions.html', questions=all_qs)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    message = request.form.get('message')
    title = request.form.get('title')
    image = request.form.get('image')
    if request.method == 'POST':
        data_manager.new_question(title, message, image)
        tag = request.form.get( 'tags' )
        data_manager.add_tags( tag )

        return redirect('/')

    return render_template('add-question.html', message=message, title=title, image=image)


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
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

    return render_template("question-comment.html", question_id=question_id, question=my_q, answer=my_a,
                           question_comments=comment)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def give_answer(question_id):
    my_answer = request.form.get('message')
    image = request.form.get('image')

    if request.method == 'POST':
        data_manager.new_answer(question_id, my_answer, image)
        return redirect('/')

    return render_template('answer.html', message=my_answer, image=image, question_id=question_id)


@app.route('/delete-question/<int:question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == "GET":
        data_manager.delete_q(question_id)
        return redirect('/')

    all_qs = data_manager.get_questions_desc('submission_time')

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
        return render_template('q-and-a.html', question=my_q, answer=my_a, question_comments=comment,
                               answer_comment=answer_comments)
    return render_template('answer_comment.html', answer_id)


@app.route('/answer/<int:answer_id>/edit-answer', methods=['GET', 'POST'])
def edit_answer(answer_id):
    comments = data_manager.get_answer_comments(answer_id)
    answer = data_manager.get_the_choosen_answer(answer_id)
    print(comments)
    if request.method == 'POST':
        answer_message = request.form.get('edit-answer')
        data_manager.editing_answer(answer_id, answer_message)
        return redirect('/')
    if comments:
        return render_template('edit_answer.html', answer=answer[0], commentss=comments)
    return render_template('edit_answer.html', answer=answer[0])


@app.route('/answer/<int:answer_id>/edit-answer/new-comment', methods=['GET', 'POST'])
def add_new_answer_comment(answer_id):
    answer = data_manager.get_the_choosen_answer(answer_id)

    if request.method == 'POST':
        new_a_comment = request.form.get('new_answer_comment')
        data_manager.new_comment(answer_id, new_a_comment)
        return redirect('/')
    return render_template('add-answer-comment.html')


@app.route('/question/<int:question_id>/edit-question', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_q_by_id(question_id)
    if request.method == 'POST':
        question_message = request.form.get('edit-question')
        data_manager.editing_question(question_id, question_message)

        return redirect('/')

    return render_template('edit-question.html', question=question[0])

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == "GET":
        data_manager.delete(id)
        return redirect('/')

    return redirect('/')



@app.route('/comment/<int:id>/edit-commit', methods=['GET', 'POST'])
def edit_comment(id):
    initial_comment = data_manager.get_comment(id)
    if request.method == 'POST':
        new_comment = request.form.get('edit-comment')
        data_manager.editing_comment(id, new_comment)
        return redirect('/')
    return render_template('edit-comment.html', initial_comment=initial_comment[0])


@app.route('/add-question', methods=['POST', 'GET'])
def tags():
    if request.method == 'POST':
        tag = request.form.get( 'tags' )
        data_manager.add_tags(tag)


        return redirect('/')

    return render_template('add-question.html')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
