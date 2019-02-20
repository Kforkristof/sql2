import connection
import time
import datetime


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                   """)
    answers = cursor.fetchall()

    return answers


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """)
    questions = cursor.fetchall()

    return questions


@connection.connection_handler
def new_question(cursor, title, message, image):
    realtime = time.time()
    st = datetime.datetime.fromtimestamp(realtime).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s,%(image)s);''',
                   {'submission_time': st, 'view_number': 0, 'vote_number': 0, 'title': title,
                    'message': message, 'image': image})

# SQL generates own ID

    return cursor


@connection.connection_handler
def new_answer(cursor, question_id, message, image):
    cursor.execute('''
    INSERT INTO answer (question_id, vote_number, message, image)
    VALUES (%(question_id)s, %(vote_number)s, %(message)s, %(image)s);''',
    {'question_id':question_id, 'vote_number':0, 'message':message, 'image':image})

    return cursor


@connection.connection_handler
def get_q_by_id(cursor, my_id):
    cursor.execute('''
    SELECT * FROM question
    WHERE id=%(my_id)s
    ;''',
    {'my_id':my_id})

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
                   {'searching_for':searching_for})

    result = cursor.fetchall()
    return result



@connection.connection_handler
def new_q_comment(cursor, comment, question_id):
    realtime = time.time()
    st = datetime.datetime.fromtimestamp(realtime).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
    insert into comment (submission_time, question_id, message, edited_count)
    values (%(submission_time)s, %(question_id)s, %(message)s, %(edited_count)s);""",
                   {'submission_time': st, 'question_is': question_id, 'message': comment, 'edited_count': 0})
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
