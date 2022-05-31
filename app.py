from flask import Flask, jsonify, request
import requests, json
import repo

app = Flask(__name__)
psql_repo = repo.Repo()

@app.route('/')
def index():
    return f'<a href="/topRepos">peak top github repos{psql_repo.get_top_repos()}</a>'

base_url = 'https://api.github.com'
@app.route('/topRepos')
def get_top_repos():
    url = f'{base_url}/search/repositories?q=stars:>0&sort=stars&order=desc'
    limit = request.args.get("repo_count", type=int, default=3)
    response = requests.get(url).json()
    top_repos = response['items'][0:limit]
    return jsonify(list(
        map(
            lambda repo: 
                {
                    "repo_name": repo['name'], 
                    "repo_url": repo['html_url'],
                    "star_count": repo['stargazers_count'],
                    "forks_count": repo['forks_count']
                }
        , top_repos)
    ))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
'''
creating an environment folder
python -m venv env 
to activate: env\Scripts\activate
'''

