from flask import Flask, render_template, request, session, json
app = Flask(__name__)
app.secret_key = 'SUPERSEKRETKEY'

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/quiz/")
def quiz():
    with open('data/cosmere_questions.json', 'r') as file:
        qa = json.load(file)
    
    try:
        q = int(session['question'])  # Current question number
    except KeyError:
        q = 1

    answer = request.args.get('answer', None)  # User answer
    
    # If the user has provided an answer
    if answer is not None:
        correct = qa.get(str(q)).get('answer')
        if str(answer) == str(correct):
            session['correct'] += 1  # Increase correct count
        else:
            session['incorrect'] += 1  # Increase incorrect count

        q += 1  # Move to the next question
        session['question'] = q

    # Check if the quiz is complete
    if q > len(qa):
        score = session['correct']
        incorrect = session['incorrect']
        return render_template('success.html', score=score, incorrect=incorrect)

    # Continue
    return render_template('quiz.html', text=qa[str(q)]["text"], answers=qa[str(q)]["answers"], number=q)

@app.route("/success/")
def success():
    return render_template('success.html')

@app.route("/startQuiz/")
def startQuiz():
    # Reset variables for a new quiz
    session['question'] = 1
    session['correct'] = 0
    session['incorrect'] = 0
    quiz()
    return()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
