import connection

from psycopg2 import sql
import util


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer
                    ;
                   """)
    answers = cursor.fetchall()

    return answers


@connection.connection_handler
def get_questions(cursor, base):
    cursor.execute(
        sql.SQL("select * from question ORDER BY {base} DESC").format(base=sql.Identifier(base)))

    questions = cursor.fetchall()

    return questions


@connection.connection_handler
def new_question(cursor, title, message, image):
    st = util.get_submission_time()
    cursor.execute('''
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s,%(image)s);''',
                   {'submission_time': st, 'view_number': 0, 'vote_number': 0, 'title': title,
                    'message': message, 'image': image})

    # SQL generates own ID

    return cursor


@connection.connection_handler
def new_answer(cursor, question_id, message, image):
    submission_time = util.get_submission_time()
    cursor.execute('''
    INSERT INTO answer (question_id, vote_number, message, image, submission_time)
    VALUES (%(question_id)s, %(vote_number)s, %(message)s, %(image)s, %(submission_time)s);''',
                   {'question_id': question_id, 'vote_number': 0, 'message': message, 'image': image,
                    'submission_time': submission_time})

    return cursor


@connection.connection_handler
def get_q_by_id(cursor, my_id):
    cursor.execute('''
    SELECT * FROM question
    WHERE id=%(my_id)s
    ;''',
                   {'my_id': my_id})

    whatiwant = cursor.fetchall()
    return whatiwant


@connection.connection_handler
def get_answer_by_q(cursor, q_id):
    cursor.execute('''
    SELECT * FROM answer
    WHERE question_id = %(q_id)s;
    ''',
                   {'q_id': q_id})

    toreturn = cursor.fetchall()
    return toreturn


@connection.connection_handler
def search(cursor, searching_for):
    cursor.execute('''
    SELECT * FROM question, answer
    WHERE title,message,image LIKE CONCAT('%' + %(searching_for)s + '%')
    ;''',
                   {'searching_for': searching_for})

    result = cursor.fetchall()
    return result


@connection.connection_handler
def new_q_comment(cursor, comment, question_id):
    st = util.get_submission_time()
    cursor.execute("""
    insert into comment (submission_time, question_id, message, edited_count)
    values (%(submission_time)s, %(question_id)s, %(message)s, %(edited_count)s);""",
                   {'submission_time': st, 'question_id': question_id, 'message': comment, 'edited_count': 0})
    return cursor


@connection.connection_handler
def get_q_comments(cursor, question_id):
    cursor.execute("""
    select * from comment
    where question_id = %(q_id)s;
    """,
                   {'q_id': question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def delete_q(cursor, question_id):
    cursor.execute("""
    DELETE FROM comment WHERE question_id=%(q_id)s;
    DELETE FROM answer WHERE question_id=%(q_id)s;
    DELETE FROM question WHERE id=%(q_id)s;
    """,
                   {'q_id': question_id})

    return cursor


# These two scope below for the answer and answer updating
@connection.connection_handler
def get_the_choosen_answer(cursor, answer_id):
    cursor.execute("""
    select * from answer
    where id = %(answer_i)s;
    """,
                   {'answer_i': answer_id})
    answer = cursor.fetchall()
    return answer


@connection.connection_handler
def editing_answer(cursor, answer_id, answer):
    cursor.execute("""
    update answer
    set message = %(ans)s
    where id = %(ans_id)s;
    """,
                   {'ans': answer, 'ans_id': answer_id})
    return cursor
