import requests
from psycopg2 import connect
class Repo:

    def __init__(self):
        #connecting to psql
        self.__db_name = 'postgres'
        self.__conn = connect(
            dbname = self.__db_name,
            user = 'postgres',
            host = 'db',
            password = 'postgres'
        )
        self.__cursor = self.__conn.cursor()
        
        #creating table
        self.__create_top_repos_table()
        
    def get_top_repos(self, count=10):
        #getting x top repos
        self.__cursor.execute(f"SELECT * FROM TOP_REPOS LIMIT {count};")
        return self.__cursor.fetchall()
    
    def get_repo_count(self):
        self.__cursor.execute(f"SELECT COUNT(*) FROM TOP_REPOS;")
        return self.__cursor.fetchone()
    
    def __create_top_repos_table(self):
        #creates relation if it doesn't exist
        query = '''
            CREATE TABLE IF NOT EXISTS TOP_REPOS (
                repo_name  VARCHAR ( 60 ) PRIMARY KEY,
                repo_url VARCHAR ( 1000 ) NOT NULL,
                star_count INT NOT NULL,
                forks_count INT NOT NULL
            );
        '''
        self.__cursor.execute(query)
        
        #populates table from github api if table is empty
        if self.__is_empty_table('TOP_REPOS'):            
            self.__populate_top_repos()
            
        self.__conn.commit()
        
    def __is_empty_table(self, tabel_name):
        self.__cursor.execute(f"SELECT COUNT(*) FROM (SELECT 1 FROM {tabel_name} LIMIT 1) AS t;")
        return not self.__cursor.fetchone()[0]
    
    def __populate_top_repos(self):
        url = 'https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc'
        response = requests.get(url).json()['items']
        
        #turning all repos into tuples then to strings
        values_tuples = list(
            map(
                lambda repo: str(
                    (
                        repo['name'], 
                        repo['html_url'],
                        repo['stargazers_count'],
                        repo['forks_count']
                    )
                )
            , response)
        )
        #separating each value tuple with a ','
        values = ','.join(values_tuples)
        insert_query = f'''
            INSERT INTO TOP_REPOS(repo_name, repo_url, star_count, forks_count)
            VALUES {values}
        '''
        self.__cursor.execute(insert_query)
