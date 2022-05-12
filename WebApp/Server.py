from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def intro_page():
    return render_template('intro_page.html')


@app.route('/element_selector')
def element_selector():
    return render_template('Element_Selector.html')


if __name__ == '__main__':
    app.run(debug=True)
