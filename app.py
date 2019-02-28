from flask import Flask, request, jsonify
from flask_restful import reqparse
import random
import json
import datetime as dt

from libs import user_ops

app = Flask(__name__)
users_seen = {}


@app.route('/api/user/GetUserResults<limit>', methods=['POST'])
def get_user_controller(limit):
    req_obj = request.get_json()
    print(req_obj)

    if not 'UserEmailID' in req_obj:
        empty_user_email = {
            'status': False,
            'message': 'User Email-Id Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_user_email)
    elif not 'UserToken' in req_obj:
        empty_user_token = {
            'status': False,
            'message': 'Token Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_user_token)
    if not 'NumberOfRecords' in req_obj:
        empty_limit = {
            'status': False,
            'message': 'Limit Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_limit)
    user_email_id = req_obj['UserEmailID']
    user_token = req_obj['UserToken']
    number_of_records = limit

    if user_email_id == "" or user_email_id is None:
        empty_user_email = {
            'status': False,
            'message': 'User Email-Id Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_user_email)
    elif user_token == "" or user_token is None:
        empty_user_token = {
            'status': False,
            'message': 'Token Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_user_token)
    elif number_of_records == "" or number_of_records is None:
        empty_limit = {
            'status': False,
            'message': 'Limit of records is  Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_limit)

    error_dict = {"status": "success", "message": "No matching records"}

    # Database connection and data according to Query
    db_obj = user_ops.get_db_obj()
    query = "SELECT * FROM score_db.`user_score` where UserEmailId = '%s' LIMIT "+limit
    query = query %user_email_id
    results = db_obj.db_select_query(query)

    for i in results:
        dt.datetime.strftime(results[0]['TestDate'], "%Y-%m-%dT%H:%M:%S")

    if not results:
        return jsonify(error_dict)

    # Show json
    return jsonify(results)


# http://172.16.20.87:5000/AddUserResult/
@app.route('/api/user/AddUserScore', methods=['POST'])
def add_user_score_controller():
    req_obj = request.get_json()
    print(req_obj)

    user_email_id = req_obj['UserEmailID']
    user_token = req_obj['UserToken']
    test_duration = str(req_obj['TestDuration'])
    question_count = str(req_obj['QuestionsCount'])
    reward_points = str(req_obj['RewardPoints'])
    test_date = req_obj['TestDate']
    correct_answer_count = str(req_obj['CorrectAnswersCount'])
    incorrect_answer_count = str(req_obj['InCorrectAnswersCount'])

    """
    INSERT INTO igw.`usertest`(`UserEmailID`, `RewardPoints`, `TestDate`, `TestDuration`, `QuestionsCount`, `CorrectAnswersCount`, `InCorrectAnswersCount`)
    VALUES ('mangesh.khude@infobeans.com',60,'2019-02-19 00:00:00',60,10,6,4)
    """
    if user_email_id is None:
        empty_user_email = {
            'status': False,
            'message': 'User Email-Id Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_user_email)
    elif user_token is None:
        empty_user_token = {
            'status': False,
            'message': 'Token Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_user_token)
    elif test_duration is None:
        empty_test_duration = {
            'status': False,
            'message': 'Test Duration Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_test_duration)
    elif question_count is None:
        empty_question_count = {
            'status': False,
            'message': 'Total Question Count Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_question_count)
    elif reward_points is None:
        empty_reward_point = {
            'status': False,
            'message': 'Reward point Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_reward_point)
    elif test_date is None:
        empty_test_date = {
            'status': False,
            'message': 'Test Date Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_test_date)
    elif correct_answer_count is None:
        empty_correct_ansewer = {
            'status': False,
            'message': 'Correct answer count Missing ',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_correct_ansewer)
    elif incorrect_answer_count is None:
        empty_incorrect_answer = {
            'status': False,
            'message': 'Incorrect answer count Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_incorrect_answer)

    query = "INSERT INTO score_db.`user_score`(`UserEmailID`, `RewardPoints`, `TestDate`, `TestDuration`, `QuestionsCount`, `CorrectAnswersCount`, `InCorrectAnswersCount`)" \
            "VALUES ('" + user_email_id + "','" + reward_points + "','" + test_date + "'," + test_duration + ","\
            + question_count + "," + correct_answer_count + "," + incorrect_answer_count + ")"
    print(query)
    db_obj = user_ops.get_db_obj()
    is_inserted = db_obj.db_commit_query(query)
    not_inserted_dict = {
        'status': is_inserted,
        'message': 'Data not inserted, Please try again'
    }
    inserted_dict = {
        'status': is_inserted,
        'message': 'Data inserted'
    }
    if not is_inserted:
        return jsonify(not_inserted_dict)

    return jsonify(inserted_dict)


@app.route('/api/user/GetTopScore/', methods=['POST'])
def get_top_score():
    req_obj = request.get_json()
    user_email_id = req_obj['UserEmailID']
    user_token = req_obj['UserToken']
    is_current_score = str(req_obj['IsCurrentScore'])

    """
    1. SELECT `UserEmailID`, `TestID`, `CorrectAnswersCount` FROM mytest.usertest where `UserEmailID`='mangesh.khude@infobeans.com' ORDER BY `CorrectAnswersCount` DESC LIMIT 1
    2. SELECT `UserEmailID`, `TestID`, `CorrectAnswersCount` FROM mytest.usertest where `UserEmailID`='mangesh.khude@infobeans.com' ORDER BY `TestID` DESC LIMIT 1
    """
    best_of_all_query = "SELECT `UserEmailID`, `TestID`, `CorrectAnswersCount` FROM score_db.`user_score` " \
                        "where `UserEmailID`= '" + user_email_id + "' ORDER BY `CorrectAnswersCount` DESC LIMIT 1"
    current_score_query = "SELECT `UserEmailID`, `TestID`, `CorrectAnswersCount` FROM score_db.`user_score` " \
                          "where `UserEmailID`= '" + user_email_id + "' ORDER BY `TestID` DESC LIMIT 1"
    if is_current_score == 'true':
        db_obj = user_ops.get_db_obj()
        best_of_all = db_obj.db_select_query(best_of_all_query)
        current_score = db_obj.db_select_query(current_score_query)
        best_of_all[0]['Status'] = "Success"
        best_of_all[0]['Message'] = "Top score retrieved Successfully"
        best_of_all[0]['UserToken'] = user_token
        best_of_all[0]['IsCurrentScore'] = is_current_score
        best_of_all[0]['UserScore'] = current_score[0]['CorrectAnswersCount']
        best_of_all[0]['BestScore'] = best_of_all[0]['CorrectAnswersCount']
        result_json = jsonify(best_of_all)
        return result_json
    elif is_current_score == 'false':
        db_obj = user_ops.get_db_obj()
        best_of_all = db_obj.db_select_query(best_of_all_query)
        best_of_all[0]['Status'] = "Success"
        best_of_all[0]['Message'] = "Top score retrieved Successfully"
        best_of_all[0]['UserToken'] = user_token
        best_of_all[0]['IsCurrentScore'] = is_current_score
        best_of_all[0]['BestScore'] = best_of_all[0]['CorrectAnswersCount']
        result_json = jsonify(best_of_all)
        return result_json
    else:
        error_dict = {"Status": "Failure", "Message": "Failed to fetch Top score for the user"}
        return jsonify(error_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
