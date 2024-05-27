from flask import Flask, render_template, request, flash, redirect, url_for
from random import randint

# Game Logic
playing = True
attempts = 1
pick = randint(1, 100)

def logic(guess):
    global playing, attempts
    if guess == pick:
        playing = False
        flash(f"You found it! The number was {pick}")
        if attempts == 1:
            flash(f"It took you {attempts} attempt to find it")
        else:
            flash(f"It took you {attempts} attempts to find it")

    elif guess > pick:
        flash(f"The number is lower than your guess. {guess}{pick}")
        attempts += 1

    else:
        flash(f"The number is higher than your guess. {guess}{pick}")
        attempts += 1

def reset():
    global playing, pick, attempts
    playing = True
    pick = randint(1, 100)
    attempts = 1

# Flask init
app = Flask(__name__)
app.secret_key = "iwrfjoiwfioweflp"

@app.route('/', methods=["POST", "GET"])
def main():
    message = None

    ###########ChatGPT#########
    if request.method == "POST":
        if 'input' in request.form:
            guess = int(request.form["input"])
            message = logic(guess)

        elif 'reset' in request.form:
            reset()
            return redirect(url_for('main'))   
        
    return render_template("index.html", message=message, playing=playing)
    ############################

if __name__ == "__main__":
    app.run(debug=True)