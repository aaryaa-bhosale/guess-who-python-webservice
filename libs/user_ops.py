import json
from libs.database import Database


# global database session
db_obj = None


def get_db_obj():
    """
    Used to initialize the DB session
    """
    global db_obj
    if db_obj:
        return db_obj
    db_obj = Database()
    db_obj.connect_to_database(db_name="mytest")
    return db_obj


def load_top_survey_score(st_limit=0, offset=10):
    sql = "select UserEmailID, RewardPoints from usertest order by RewardPoints desc limit {}, {}".format(st_limit, offset)
    user_dict = db_obj.db_select_query(sql)
    response_in_json_format = json.dumps(user_dict)
    return response_in_json_format


def insert_user_data(input_in_json_format=None):

    user_obj = json.loads(input_in_json_format) # convert in dict format

    table_column = ["TestID", "UserEmailID", "UserToken", "RewardPoints",
                    "TestDate", "TestDuration", "QuestionsCount", "CorrectAnswersCount", "InCorrectAnswersCount"]

    if isinstance(user_obj, dict):
        select_field = value_field = ''
        for key, value in user_obj.items():
            if key in table_column:
                select_field += key + ", "
                if isinstance(value, str):
                    value_field += "'" + str(value) + "', "
                else:
                    value_field += str(value) + ", "

        select_field = select_field[:-2]
        value_field = value_field[:-2]
        try:
            query = "insert into usertest (" + select_field + ") values (" + value_field + ")"
            return db_obj.db_commit_query(query)
        except Exception as e:
            print(e)
            return False
    else:
        return False
