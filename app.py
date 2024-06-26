from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = 'hF3ZM0PYodqDhBcZ6DnjF9luNe4qnJMQN52bJKDn'  # Replace with your actual API key

def get_movies_by_genre(genre, max_runtime, streaming_services):
    url = f'https://api.watchmode.com/v1/search/?apiKey={API_KEY}'
    params = {
        'search_field': 'genre',
        'search_value': genre
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        movies = response.json().get('titles', [])

        print(f"Received {len(movies)} movies from Watchmode API.")  # Debug print

        filtered_movies = []
        for movie in movies:
            if movie['runtime'] <= max_runtime and any(service in movie['sources'] for service in streaming_services):
                filtered_movies.append({
                    'title': movie['title'],
                    'user_rating': movie['user_rating'],
                    'runtime': movie['runtime']
                })
        
        filtered_movies.sort(key=lambda x: x['user_rating'], reverse=True)
        print(f"Filtered to {len(filtered_movies)} movies based on criteria.")  # Debug print
        return filtered_movies[:10]
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    req_data = request.get_json()
    print(f"Received request data: {req_data}")  # Debug print

    genre = req_data.get('genre')
    max_runtime = int(req_data.get('max_runtime'))
    streaming_services = req_data.get('streaming_services', [])

    recommendations = get_movies_by_genre(genre, max_runtime, streaming_services)
    print(f"Returning {len(recommendations)} recommendations.")  # Debug print
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)