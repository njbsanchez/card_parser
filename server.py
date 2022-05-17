from flask.helpers import send_from_directory
import roadmap_card_inventory as roadmap
from jinja2 import StrictUndefined
from flask import Flask
import json

app = Flask(__name__)
app.secret_key = "DEV"
app.jinja_env.undefined = StrictUndefined

if __name__ == "__main__":

    url = roadmap.get_url(input)
    file_name = roadmap.file_name_creator()

    container = roadmap.get_container(url)
    cards_dictionary = roadmap.get_cards_dict(container)

    roadmap.create_json(cards_dictionary,file_name)
    roadmap.create_csv(cards_dictionary,file_name)
    
    app.run(debug=True, use_reloader=True, use_debugger=True)

