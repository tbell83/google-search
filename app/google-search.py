from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from google import google
import requests
import json

app = Flask(__name__)
api = Api(app)
slack_token = 'poops'

def googleTextSearch(query):
    query = query.replace('+', ' ')
    try:
        try:
            search_results = google.search(query)
        except:
            search_results = google.search(query+' j')

        if len(search_results) > 0:
            return search_results
        else:
            return False

    except:
        return False

class Search(Resource):
    def get(self):
        token = request.args.get('token')
        print token

        if token == slack_token:
            print 'Token checks out'
            query = request.args.get('text')
            print 'Query is {0}'.format(query)
            result = googleTextSearch(query)
            print result[0].description
            print result[0].link
            if result is not None:
                print 'Getting some info...'
                print '{0} {1}'.format(result[0].description, result[0].link)
                attachment = {"attachments":[{"fallback":query,"pretext":query,"color":"#FFF","fields": [{"title":query,"value":'{0}\n{1}'.format(result[0].description, result[0].link)}],"image_url": url}]}
                print "\n\n\n{0}\n{1}\n\n\n".format(url, attachment)
                data = json.dumps(attachment)
                post = requests.post(response_url, data=data)
                resp = Response(status=200)
            else:
                resp = Response(status=404)
            return resp
        else:
            return 'Unauthorized'

api.add_resource(Search, '/')

if __name__ == '__main__':
    app.run(debug=True)
