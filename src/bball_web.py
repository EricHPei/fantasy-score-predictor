from collections import Counter
from flask import Flask, request, render_template
app = Flask(__name__)


def dict_to_html(d):
    return '<br>'.join('{0}: {1}'.format(k, d[k]) for k in sorted(d))


# Form page to submit text

@app.route('/')
def intro():
    return render_template('index.html')

@app.route('/fanduel')
def fanduel_page():
    return render_template('fanduel.html')

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/my_picks')
def mypicks_page():
    return render_template('my_picks.html')
    #'''
    #    <form action="/word_counter" method='POST' >
    #        <input type="text" name="user_input" />
    #        <input type="submit" />
    #    </form>
    #    '''


# My word counter app
@app.route('/my_picks', methods=['POST'] )
def word_counter():
    text = str(request.form['user_input'])
    word_counts = Counter(text.lower().split())
    page = 'There are {0} words.<br><br>Individual word counts:<br> {1}'
    return page.format(len(word_counts), dict_to_html(word_counts))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)