from flask import Flask, render_template, request, flash, redirect, url_for
from random import randint

#Init vars
playing = True
attempts = 1
guesses = ""
pick = randint(1, 100)

# Game Logic
def logic(guess):
    global playing, attempts
    if guess == pick:
        playing = False
        flash(f"You found it! The number was {pick}")
        save_stats()
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

def save_stats():
    stats_file = open("app/stats.txt", "a")
    stats_file.write(f"The number was {pick}.\tNumber of attempts was: {attempts}\tThe guesses the user made were: {guesses}\n")
    stats_file.close()

# Flask init
app = Flask(__name__)
app.secret_key = "iwrfjoiwfioweflp"

@app.route('/', methods=["POST", "GET"])
def main():
    global guesses
    message = None

    ###########ChatGPT#########
    if request.method == "POST":
        if 'input' in request.form:
            guess = request.form["input"]
            guesses = guesses + guess + ', '
            guess = int(guess)

            message = logic(guess)

        elif 'reset' in request.form:
            reset()
            return redirect(url_for('main'))   
        
    return render_template("index.html", message=message, playing=playing)
    ############################

if __name__ == "__main__":
    app.run(debug=True)