# !/usr/bin/python
"""
libs.database
~~~~~~~~~~~~~~~~~~~~

This class contains database related functions

"""

import logging
import traceback

import pymysql.cursors


logger = logging.getLogger(__name__)

DB_SERVER = "localhost"
DB_USER = "guesswhouser"
DB_PASSWORD = "Infoserver123"


class Database:

    def __init__(self):
        """
        initialize the database class
        """
        self.db = None
        self.cursor = None

    @property
    def is_connected(self):
        return self.db and self.db.open

    # connect to mysql database
    def connect_to_database(self, host=DB_SERVER,
                            username=DB_USER, password=DB_PASSWORD,
                            db_name=""):
        """
        :func:`connect_to_database` this function connect to database using provided credentials

        :param host: (optional)   database server host details
        :param username: (optional)   database username
        :param password: (optional)   database password
        :param db_name: (optional)   database name

        :rtype: `object` returns database object
        """
        try:
            if not db_name:
                self.db = pymysql.connect(
                    host=host,
                    user=username,
                    password=password,
                    cursorclass=pymysql.cursors.DictCursor)
            else:
                self.db = pymysql.connect(
                    host=host,
                    user=username,
                    password=password,
                    db=db_name,
                    cursorclass=pymysql.cursors.DictCursor)

            self.cursor = self.db.cursor()
            return self.db
        except BaseException as e:
            logger.debug("connection to database failed ")
            logger.info("error occurs: %s , with details:\n %s",
                        e, traceback.format_exc())

            raise

    def select_data(self, tbl, field='*', where_field=None, where_val=None, st_limit=None, offset=None,
                    custom_query_append=None):
        """
        :func:`select_data` this function prepare dynamic query and fetch data from database using select query
        based on different input params

        :param tbl:  database table name
        :param field: (optional)   specify name of columns that need to be fetch
        :param where_field: (optional)   different column names (in list format) required in where clause
        :param where_val: (optional)   where_field respective column values (in list format)
        :param st_limit: (optional) starting limit offset
        :param offset: number of records that needs to be fetch from st_limit
        e.g. limit 10, 50 means get record from 10 to next 50 element, so here st_limit = 10 and offset = 50
        :param custom_query_append: append custom query to automatically generate query using provided input data

        :rtype: `dict` returns select query result in dict format
        """

        where_field = where_field or []
        where_val = where_val or []

        sql = "SELECT " + field + " FROM " + tbl + " WHERE {where_clause} {custom_query} {limit}"

        if where_field and where_val:
            where_clause = "1 "
            for i in range(0, len(where_field)):
                where_clause += " AND {} = '{}'".format(where_field[i], where_val[i])
        else:
            where_clause = "1 "

        custom_query = ''
        if custom_query_append:
            custom_query = custom_query_append

        limit = ''
        if st_limit and offset:
            limit = " order by rand() limit " + str(st_limit) + ", " + str(offset)

        sql = sql.format(where_clause=where_clause, custom_query=custom_query, limit=limit)

        logger.debug("The sql statement is: {}".format(sql))
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except BaseException:
            logger.debug("Failed to get data from table {}".format(sql))
            raise

    def db_select_query(self, query):
        """
        :func:`db_select_query` this function will fire/execute provided query on db and return result
        :param query:  custom mysql query
        :rtype: `dict` returns query fetch data
        """

        try:
            logger.debug("The sql statement is: {}".format(query))
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            logger.info("error occurs: %s , with details:\n %s",
                        e, traceback.format_exc())
            logger.debug("Failed to execute query {}".format(query))
            raise

    def db_commit_query(self, query):
        """
        :func:`db_commit_query` this func will execute provided insert/update/delete query on db and return result
        :param query:  custom mysql insert/update/delete  query
        :rtype: `boolean` return True on success else raise exception on exceptional issue
        """
        try:
            self.cursor.execute(query)
            logger.debug("The commit statement is: {}".format(query))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            logger.info("error occurs: %s , with details:\n %s",
                        e, traceback.format_exc())
            logger.debug("Failed to execute query {}".format(query))
            raise

    def __del__(self):
        """
        :func:__del__ destructor will close the db connection object
        """
        self.cursor.close()
        self.db._force_close()
