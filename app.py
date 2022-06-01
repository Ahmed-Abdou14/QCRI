from flask import Flask, jsonify, request
from repo import Repo

app = Flask(__name__)
psql_repo = Repo()

@app.route('/')
def index():
    return f'<a href="/topRepos">peak top github repos #{psql_repo.get_repo_count()}</a>'

base_url = 'https://api.github.com'
@app.route('/topRepos')
def get_top_repos():
    limit = request.args.get("repo_count", type=int, default=10)
    top_repos = psql_repo.get_top_repos(limit)
    return jsonify(
        [
            dict(
                (['repo_name', 'repo_url', 'star_count', 'forks_count'][i], value) for i, value in enumerate(row)
            ) for row in top_repos
        ]
    )
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
'''
creating an environment folder
python -m venv env 
to activate: env\Scripts\activate
'''

