from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

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
    app.run(debug=True)
    
'''
creating an environment folder
python -m venv env 
env\Scripts\activate
'''

