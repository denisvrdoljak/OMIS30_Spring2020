from flask import Flask,request

helloYou = """Hello {lastname_field}, {firstname_field}. How are you today?

""".strip()

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Hello World!"



@app.route('/calc_home')
def calculator_landing_page():
    return calc_splashHTML

@app.route('/calc1')
def calc1():
    return calc1HTML

@app.route('/helloYou')
def calc1result():
    lastname = request.args.get('lastname')
    firstname = request.args.get('firstname')
    return helloYou.format(firstname_field=firstname,lastname_field=lastname)




# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
