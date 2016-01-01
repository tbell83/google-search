from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from google import google

app = Flask(__name__)
api = Api(app)


def googleTextSearch(query):
    query = query.replace('+', ' ')
    try:
        try:
            search_results = google.search(query)
        except:
            search_results = google.search(query+' j')

        if len(search_results) > 0:
            result = search_results[0].description
            result_url = search_results[0].link
            results = {'query_status': True, 'search_query': query, 'search_result': result, 'result_url': result_url}
        else:
            results = {'query_status': False}
    except:
        results = {'query_status': False}

    return results


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Search(Resource):
    def get(self, query):
        return googleTextSearch(query)

class Farts(Resource):
    def get(self, query):
        return {'fart': 'braaappppp'}

api.add_resource(HelloWorld, '/')
api.add_resource(Farts, '/farts/<string:query>')
api.add_resource(Search, '/search/<string:query>')

if __name__ == '__main__':
    app.run(debug=True)
