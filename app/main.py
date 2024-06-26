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
        flash(f"The number is lower than your guess.")
        attempts += 1

    else:
        flash(f"The number is higher than your guess.")
        attempts += 1

#Runs when the user chooses to play again, resets all vars and picks a new number
def reset():
    global playing, pick, attempts, guesses
    playing = True
    pick = randint(1, 100)
    attempts = 1
    guesses = ""

#Saves the statistics from the previous game to stats.txt
def save_stats():
    try:
        stats_file = open("stats.txt", "a")
        stats_file.write(f"The number was {pick}.\tNumber of attempts was: {attempts}\tThe guesses the user made were: {guesses}\n")
        stats_file.close()
    except PermissionError:
        print("Could not access the stats.txt file\n")

# Flask init
app = Flask(__name__)
app.secret_key = "iwrfjoiwfioweflp"

@app.route('/', methods=["POST", "GET"])
def main():
    global guesses
    message = None

    ###########ChatGPT#########
    if request.method == "POST":
        if 'input' in request.form: #If the user presses the "Submit" button
            guess = request.form["input"] #Get the input from the user
            guesses = guesses + guess + ', '
            guess = int(guess)

            message = logic(guess) #Depending on the guess flash a different message on screen

        elif 'reset' in request.form: #If the user presses the "Play Again" button
            reset()
            return redirect(url_for('main')) 
        
    return render_template("index.html", message=message, playing=playing) #Give the parameters message and playing to index.html
    ############################

if __name__ == "__main__":
    app.run(debug=True)