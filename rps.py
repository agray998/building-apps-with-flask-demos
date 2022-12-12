from flask import Flask
from random import choice

app = Flask(__name__)

@app.route("/play/<move>")
def play(move):
    moves = ["rock", "paper", "scissors"]
    comp_move = choice(moves)
    winning_combs = {"rock":"paper", "paper":"scissors", "scissors":"rock"}
    
    if comp_move == winning_combs.get(move.lower(), "invalid"):
        winner = "computer"
    elif move.lower() == winning_combs.get(comp_move, "invalid"):
        winner = "player"
    else:
        winner = "none"
    
    return {"Player move": move, "Computer move": comp_move, "Winner": winner}

if __name__ == '__main__':
    app.run(debug = True)
