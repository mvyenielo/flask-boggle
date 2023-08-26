from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}

@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId":game_id, "board":game.board})
# jsonify(gameId= game_id, board= game.board)


@app.post("/api/score-word")
def score_word():
    """Check if a word is on the board and is a valid word"""
    # game = request.json
    # game_id = game["gameId"]
    # word = game["word"].upper()
    # current_game = games.get(game_id)

    word = request.json["word"].upper()
    game_id = request.json["gameId"]
    game = games[game_id]


    word_in_list = game.is_word_in_word_list(word)
    word_on_board = game.check_word_on_board(word)

    if word_in_list is False:
        return jsonify({"result": "not-word"})

    if word_on_board is False:
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})

