import connection

@connection.connection_handler
def get_answers(cursor, city):
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

