from bottle import Bottle, run

app = Bottle()

@app.route('/')
def index():
    return "MASAI SCHOOL"

run(app, host='localhost', port=8080)