from flask import Flask, request, jsonify
from flask_restful import reqparse
import json

app = Flask(__name__)
users_seen = {}
@app.route('/api/user/GetUserService/<limit>', methods=['POST','GET'])
def get_user_service(limit):

   response_object = """
   [
      {
        "UserEmailID": "monika.agrawal@infobeans.com",
        "UserToken": "12345",
        "RewardPoints": 90,
        "TestDate": "datetime.datetime(2019, 2, 19, 0, 0)",
        "TestDuration": 60,
        "QuestionsCount": 10,
        "CorrectAnswersCount": 9,
        "InCorrectAnswersCount": 1
      }, 
      {
        "UserEmailID": "monika.agrawal@infobeans.com",
        "UserToken": "fG0vxD2+uKn2+EeDIpDruHMMavDa/245N",
        "RewardPoints": 60,
        "TestDate": "datetime.datetime(2019, 2, 19, 0, 0)",
        "TestDuration": 60,
        "QuestionsCount": 10,
        "CorrectAnswersCount": 6,
        "InCorrectAnswersCount": 4
      }, 
      {
        "UserEmailID": "monika.agrawal@infobeans.com",
        "UserToken": "fG0vxD2+uKn2+EeDIpDruHMMavDa/245N",
        "RewardPoints": 40,
        "TestDate": "datetime.datetime(2019, 2, 19, 0, 0)",
        "TestDuration": 60,
        "QuestionsCount": 10,
        "CorrectAnswersCount": 4,
        "InCorrectAnswersCount": 1
      }
    ]
   """

   parser = reqparse.RequestParser()
   parser.add_argument('UserEmailID')
   parser.add_argument('UserToken')
   parser.add_argument('NumberOfRecords')
   args = parser.parse_args()

   # Transform json input to python objects
   input_dict = json.loads(response_object)

   # Transform python object back into json
   output_json = jsonify(input_dict)

   # Show json
   return output_json

# http://172.16.20.87:5000/AddUserResult/
@app.route('/api/user/AddUserScore/', methods=['POST'])
def add_user_score():
    parser = reqparse.RequestParser()
    parser.add_argument('UserEmailID')
    #parser.add_argument('UserToken', type=str)
    parser.add_argument('TestDuration', type=str)
    parser.add_argument('QuestionsCount', type=str)
    parser.add_argument('RewardPoints', type=str)
    parser.add_argument('TestDate', type=str)
    parser.add_argument('CorrectAnswersCount', type=str)
    parser.add_argument('InCorrectAnswersCount', type=str)
    args = parser.parse_args()
    my_dict = {
        'status': True,
        'message': 'success'
    }
    return jsonify(my_dict)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)