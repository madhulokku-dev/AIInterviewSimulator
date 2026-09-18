from flask import Flask, render_template, request
import random

app = Flask(__name__)


# ---------------- QUESTION BANK ----------------

question_bank = {

    "Python Developer": {
        "Easy": [
            "What is Python?",
            "What is the difference between a list and a tuple?",
            "What are variables in Python?",
            "What is a function in Python?",
            "What is the use of indentation in Python?"
        ],

        "Medium": [
            "What is the difference between shallow copy and deep copy?",
            "What are decorators in Python?",
            "Explain exception handling in Python.",
            "What is the difference between a list, tuple, set and dictionary?",
            "What is object-oriented programming in Python?"
        ],

        "Hard": [
            "Explain Python memory management and garbage collection.",
            "What are generators and why are they useful?",
            "Explain multithreading and multiprocessing in Python.",
            "What are Python metaclasses?",
            "How would you optimize a slow Python application?"
        ]
    },

    "Java Developer": {
        "Easy": [
            "What is Java?",
            "What is the difference between JDK, JRE and JVM?",
            "What is a class in Java?",
            "What is an object?",
            "What is inheritance?"
        ],

        "Medium": [
            "Explain method overloading and method overriding.",
            "What is exception handling in Java?",
            "What is the difference between ArrayList and LinkedList?",
            "What is an interface in Java?",
            "Explain encapsulation, inheritance, polymorphism and abstraction."
        ],

        "Hard": [
            "Explain Java memory management.",
            "How does garbage collection work in Java?",
            "What is multithreading in Java?",
            "Explain synchronization in Java.",
            "How would you improve the performance of a Java application?"
        ]
    },

    "Data Analyst": {
        "Easy": [
            "What is data analysis?",
            "What is the difference between data and information?",
            "What is Excel used for in data analysis?",
            "What is a database?",
            "What is data visualization?"
        ],

        "Medium": [
            "What is data cleaning?",
            "Explain the difference between INNER JOIN and LEFT JOIN.",
            "What is a pivot table?",
            "What is the purpose of Power BI?",
            "How would you handle missing values in a dataset?"
        ],

        "Hard": [
            "How would you identify outliers in a dataset?",
            "Explain the difference between correlation and causation.",
            "How would you design a dashboard for business decision-making?",
            "How would you analyze a dataset containing millions of records?",
            "How would you communicate complex analytical results to a non-technical manager?"
        ]
    },

    "Frontend Developer": {
        "Easy": [
            "What is HTML?",
            "What is CSS?",
            "What is JavaScript?",
            "What is the difference between HTML and CSS?",
            "What is responsive web design?"
        ],

        "Medium": [
            "What is the DOM?",
            "What is the difference between let, var and const?",
            "What are JavaScript promises?",
            "What is React?",
            "What are React components?"
        ],

        "Hard": [
            "Explain React state management.",
            "How would you optimize a slow website?",
            "What is virtual DOM?",
            "Explain asynchronous JavaScript.",
            "How would you improve the performance of a large React application?"
        ]
    },

    "Backend Developer": {
        "Easy": [
            "What is backend development?",
            "What is an API?",
            "What is HTTP?",
            "What is a database?",
            "What is REST API?"
        ],

        "Medium": [
            "What is the difference between GET and POST?",
            "What is authentication?",
            "What is authorization?",
            "What is middleware?",
            "What is the difference between SQL and NoSQL databases?"
        ],

        "Hard": [
            "How would you design a scalable backend system?",
            "Explain database indexing and its advantages.",
            "How would you secure a REST API?",
            "What is caching and why is it useful?",
            "How would you handle thousands of simultaneous requests?"
        ]
    }
}


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SETUP ----------------

@app.route("/setup")
def setup():
    return render_template("setup.html")


# ---------------- INTERVIEW ----------------

@app.route("/interview", methods=["POST"])
def interview():

    name = request.form["name"]
    role = request.form["role"]
    difficulty = request.form["difficulty"]

    questions_count = int(request.form["questions"])

    if role not in question_bank:
        role = "Python Developer"

    available_questions = question_bank[role][difficulty]

    questions_count = min(
        questions_count,
        len(available_questions)
    )

    selected_questions = random.sample(
        available_questions,
        questions_count
    )

    return render_template(
        "interview.html",
        name=name,
        role=role,
        difficulty=difficulty,
        questions=selected_questions
    )


# ---------------- RESULT ----------------

@app.route("/result", methods=["POST"])
def result():

    # Get questions and answers from the interview page
    questions = request.form.getlist("questions")
    answers = request.form.getlist("answers")

    total_score = 0
    answer_scores = []

    for question, answer in zip(questions, answers):

        answer = answer.strip()

        # Basic scoring
        if not answer:
            score = 0

        else:
            words = answer.split()
            word_count = len(words)

            # Score based on answer length
            if word_count >= 40:
                score = 90
            elif word_count >= 25:
                score = 75
            elif word_count >= 15:
                score = 60
            elif word_count >= 8:
                score = 40
            else:
                score = 20

        answer_scores.append(score)
        total_score += score


    # Calculate overall score
    if answer_scores:
        overall_score = round(
            total_score / len(answer_scores)
        )
    else:
        overall_score = 0


    # Feedback based on score
    if overall_score >= 80:

        feedback = (
            "Your answers were detailed and showed "
            "good effort. Keep improving your examples "
            "and technical explanations."
        )

    elif overall_score >= 60:

        feedback = (
            "Your answers showed a basic understanding. "
            "Try to explain concepts with more detail "
            "and practical examples."
        )

    else:

        feedback = (
            "Your answers were quite brief. "
            "Try to explain your ideas clearly and "
            "include examples where possible."
        )


    return render_template(
        "result.html",
        overall_score=overall_score,
        answer_scores=answer_scores,
        feedback=feedback
    )


if __name__ == "__main__":
    app.run(debug=True)