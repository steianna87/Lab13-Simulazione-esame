from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct year(`datetime`) as y
                    from sighting s 
                    order by y desc"""

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['y'])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAllShape(year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct shape 
                    from sighting s 
                    where year (s.`datetime`) = %s 
                    order by shape  """

        cursor.execute(query, (year, ))
        result = []
        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAllStates():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select *
                    from state s """

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(State(**row))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAllVicini(Map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select state1 , state2 
                    from neighbor n """

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append((Map[row['state1']], Map[row['state2']]))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getPeso(year, shape, s1: State):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select s.state , count(*) as peso
                    from sighting s
                    where year(s.`datetime`) = %s 
                    and s.shape = %s 
                    and s.state = %s"""

        cursor.execute(query, (year, shape, s1.id))
        result = []
        for row in cursor:
            result.append(row['peso'])

        cursor.close()
        cnx.close()
        return result
