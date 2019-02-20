import connection

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
    cursor.execute('''
    INSERT INTO question (view_number, vote_number, title, message, image)
    VALUES (%(view_number)s, %(vote_number)s, %(title)s, %(message)s,%(image)s);''',
    {'view_number':0, 'vote_number':0, 'title':title, 'message':message, 'image':image})

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
    {'q_id':q_id})

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

