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
def get_questions_desc(cursor, base):
    cursor.execute(
        sql.SQL("select question.*, tag.name "
                "from tag "
                "join question_tag "
                "on tag.id = question_tag.tag_id "
                "right join question"
                " on question_tag.question_id = question.id "
                "ORDER BY {base} DESC").format(base=sql.Identifier(base)))
    questions = cursor.fetchall()

    return questions


@connection.connection_handler
def get_questions_asc(cursor, base):
    cursor.execute(
        sql.SQL("select question.*, tag.name "
                "from tag "
                "join question_tag "
                "on tag.id = question_tag.tag_id "
                "right join question"
                " on question_tag.question_id = question.id "
                "ORDER BY {base} ASC").format(base=sql.Identifier(base)))
    questions = cursor.fetchall()

    return questions


@connection.connection_handler
def new_question(cursor, title, message):
    st = util.get_submission_time()
    cursor.execute('''
    INSERT INTO question (submission_time, view_number, vote_number, title, message)
    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s);''',
                   {'submission_time': st, 'view_number': 0, 'vote_number': 0, 'title': title,
                    'message': message})
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

    question = cursor.fetchall()
    cursor.execute("""
    select tag.name as tagname
    from tag
    join question_tag on tag.id = question_tag.tag_id
    where question_tag.question_id = %(id)s;
    """,
                   {'id': my_id})

    tag = cursor.fetchall()
    return question, tag


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
def search_for_q(cursor, search_for):
    cursor.execute('''
        SELECT
            DISTINCT(question.id), question.submission_time, question.view_number,
            question.vote_number, question.title, question.message, question.image            
        FROM question
        LEFT OUTER JOIN answer ON question.id=answer.question_id
        WHERE question.message ILIKE CONCAT('%%' , %(search_for)s , '%%')
            OR answer.message ILIKE CONCAT('%%' , %(search_for)s , '%%')
            OR question.title ILIKE CONCAT('%%' , %(search_for)s , '%%')
 
    ;''',
                   {'search_for': search_for})

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


@connection.connection_handler
def view_number_increase(cursor, question_id):
    cursor.execute("""
    select view_number
    from question
    where id = %(q_id)s;
    """,
                   {'q_id': question_id})
    initial_view_number = cursor.fetchall()
    current_view_number = initial_view_number[0]['view_number'] + 1
    cursor.execute("""
    update question
    set view_number = view_number + 1
    where id = %(id)s;
    """,
                   {'id': question_id})
    return cursor


@connection.connection_handler
def vote_up(cursor, question_id):
    cursor.execute("""
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = %(question_id)s
    ;""",
                   {'question_id': question_id})


@connection.connection_handler
def vote_down(cursor, question_id):
    cursor.execute("""
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id = %(question_id)s
    ;""",
                   {'question_id': question_id})


@connection.connection_handler
def editing_question(cursor, question_id, quest):
    cursor.execute("""
    update question
    set message = %(quest)s
    where id = %(question_id)s;
    """,
                   {'quest': quest, 'question_id': question_id})
    return cursor


@connection.connection_handler
def get_answer_comments(cursor, answer_id):
    cursor.execute("""
    select comment.submission_time, comment.message, comment.id
    from comment
    where comment.answer_id = %(id)s;
    """,
                   {'id': answer_id})
    answer_comments = cursor.fetchall()
    return answer_comments


@connection.connection_handler
def new_comment(cursor, id, new_a_comment):
    st = util.get_submission_time()
    edited_count = 0
    cursor.execute("""
    select id, question_id
    from answer
    where id = %(a_id)s;
    """,
                   {'a_id': id})
    qid_and_aid = cursor.fetchall()
    ids = qid_and_aid[0]
    cursor.execute("""
    insert into comment(question_id, answer_id, message, submission_time, edited_count)
    values (null, %(ans_id)s, %(message)s, %(submission_t)s, %(edited_c)s);
    """,
                   {'ans_id': ids['id'], 'message': new_a_comment, 'submission_t': st, 'edited_c': edited_count})
    return cursor


@connection.connection_handler
def add_tags(cursor, tag):
    cursor.execute("""INSERT INTO tag(name)
                        VALUES (%(tag)s);""",
                   {'tag': tag})
    return cursor


@connection.connection_handler
def get_latest_tag_id(cursor):
    cursor.execute("""
    SELECT id
    FROM tag
    ORDER BY id DESC
    LIMIT 1""")
    id = cursor.fetchall()
    return  id

@connection.connection_handler
def write_record_to_the_question_tag(cursor, q_id, t_id):
    cursor.execute("""
        INSERT INTO question_tag(question_id, tag_id)
        VALUES (%(qid)s, %(tag_id)s);
        """,
                   {'qid': q_id, 'tag_id': t_id})

@connection.connection_handler
def delete(cursor, id):
    cursor.execute("""
    delete from comment
    where id = %(cid)s;
    """,
                   {'cid': id})
    return cursor

@connection.connection_handler
def delete_a(cursor, aid):
    cursor.execute("""
    DELETE FROM comment WHERE answer_id=%(id)s;
    delete from answer
    where id = %(id)s;
    """,
                   {'id': aid})

@connection.connection_handler
def get_comment(cursor, id):
    cursor.execute("""
    select *
    from comment
    where id = %(comm_id)s;
    """,
                   {'comm_id': id})
    comment = cursor.fetchall()
    return comment


@connection.connection_handler
def editing_comment(cursor, id, comment):
    st = util.get_submission_time()
    cursor.execute("""    

    update comment
    set message = %(mess)s, edited_count = edited_count + 1
    where id = %(c_id)s;
    """,
                   {'mess': comment, 'c_id': id})
    return cursor


@connection.connection_handler
def get_latest_question_id(cursor):
    cursor.execute("""
    select id
    from question
    
    order by id desc
    limit 1""")

    question_id = cursor.fetchall()
    return question_id

@connection.connection_handler
def delete_the_wrong_tags(cursor):
    cursor.execute("""
    delete from tag
    where id = 4 or id = 5 or id = 6 or id = 7 or id = 8 or id = 9""")




@connection.connection_handler
def register(cursor, sess_id, plain_password):
    hashed_pw = util.hash_password(plain_password)
    st = util.get_submission_time()
    cursor.execute("""
    INSERT INTO sessions
    VALUES (%(id)s, %(register_time)s, 0, %(h_pw)s);
    """, {'id': sess_id, 'register_time': st, 'h_pw': hashed_pw})


@connection.connection_handler
def check_existing_username(cursor, username):
    cursor.execute("""
    SELECT * FROM sessions
    WHERE id = %(username)s;
    """,
                   {'username': username})
    result = cursor.fetchall()

    return result
