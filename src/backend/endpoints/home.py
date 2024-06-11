import sys
from business import suggestionsBusiness

from flask import Blueprint,request


home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def index():
    return "Welcome to Open Healthcare API"


@home_blueprint.route('/relevantDocs')
def getRelevantTextDocs(payload):
    return ""


@home_blueprint.route('/getsuggestion',methods=["POST"])
def getSuggestion():
    return suggestionsBusiness.getAISuggestions(request.get_json())