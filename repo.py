from psycopg2 import connect

class Repo:

    def __init__(self):
        self.__db_name = 'postgres'
        self.__conn = connect(
            dbname = self.__db_name,
            user = 'postgres',
            host = 'db',
            password = 'postgres'
        )
        self.__cursor = self.__conn.cursor()
        
    def get_top_repos(self):
        insert_query = f'''
            INSERT INTO TOP_REPOS(repo_name, repo_url, star_count, forks_count)
            VALUES
                ('3', '3', 3, 3),
                ('2', '2', 2, 2);
        '''
        #self.__cursor.execute(insert_query)
        self.__cursor.execute(f"SELECT COUNT(*) FROM top_repos;")
        return self.__cursor.fetchone()
        
