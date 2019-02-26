from flask import Flask, request, jsonify
from flask_restful import reqparse
import random
import json

from libs import user_ops

app = Flask(__name__)
users_seen = {}


@app.route('/GetUserService/<limit>', methods=['POST'])
def get_user_service(limit):
    error_dict = {"status": "success", "message": "No matching records"}

    parser = reqparse.RequestParser()
    parser.add_argument('UserEmailID')
    parser.add_argument('UserToken')
    parser.add_argument('NumberOfRecords')
    args = parser.parse_args()

    # Database connection and data according to Query
    db_obj = user_ops.get_db_obj()
    query = "SELECT * FROM mytest.usertest where UserEmailId = '%s'" % args['UserEmailID']
    results = db_obj.db_select_query(query)

    # Transform python object back into json
    output_json = json.dumps(results, default=str)

    if not results:
        return jsonify(error_dict)

    # Show json
    return jsonify(output_json)


# http://172.16.20.87:5000/AddUserResult/
@app.route('/AddUserScore/', methods=['POST'])
def add_user_score():
    parser = reqparse.RequestParser()
    parser.add_argument('UserEmailID')
    parser.add_argument('UserToken', type=str)
    parser.add_argument('TestDuration', type=str)
    parser.add_argument('QuestionsCount', type=str)
    parser.add_argument('RewardPoints', type=str)
    parser.add_argument('TestDate', type=str)
    parser.add_argument('CorrectAnswersCount', type=str)
    parser.add_argument('InCorrectAnswersCount', type=str)

    args = parser.parse_args()
    # """
    # INSERT INTO mytest.`usertest`(`UserEmailID`, `RewardPoints`, `TestDate`, `TestDuration`, `QuestionsCount`, `CorrectAnswersCount`, `InCorrectAnswersCount`)
    # VALUES ('vaibhav.gade@infobeans.com',60,'2019-02-19 00:00:00',60,10,6,4)
    # """
    if args['UserEmailID'] is None:
        empty_user_email = {
            'status': False,
            'message': 'User Email-Id Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_user_email)
    elif args['UserToken'] is None:
        empty_user_token = {
            'status': False,
            'message': 'Token Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_user_token)
    elif args['TestDuration'] is None:
        empty_test_duration = {
            'status': False,
            'message': 'Test Duration Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_test_duration)
    elif args['QuestionsCount'] is None:
        empty_question_count = {
            'status': False,
            'message': 'Total Question Count Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_question_count)
    elif args['RewardPoints'] is None:
        empty_reward_point = {
            'status': False,
            'message': 'Reward point Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_reward_point)
    elif args['TestDate'] is None:
        empty_test_date = {
            'status': False,
            'message': 'Test Date Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_test_date)
    elif args['CorrectAnswersCount'] is None:
        empty_correct_ansewer = {
            'status': False,
            'message': 'Correct answer count Missing ',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_correct_ansewer)
    elif args['InCorrectAnswersCount'] is None:
        empty_incorrect_answer = {
            'status': False,
            'message': 'Incorrect answer count Missing',
            'db-message': 'Data not inserted'
        }
        return jsonify(empty_incorrect_answer)

    query = "INSERT INTO mytest.`usertest`(`UserEmailID`, `RewardPoints`, `TestDate`, `TestDuration`, `QuestionsCount`, `CorrectAnswersCount`, `InCorrectAnswersCount`)" \
            "VALUES ('" + args['UserEmailID'] + "','" + args['RewardPoints'] + "','" + args['TestDate'] + "'," + args[
                'TestDuration'] + "," + args['QuestionsCount'] + "," + args['CorrectAnswersCount'] + "," + args[
                'InCorrectAnswersCount'] + ")"
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
