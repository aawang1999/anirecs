from flask import Flask, render_template, request, redirect, url_for, session
from anime import setup, get_recommendation

app = Flask(__name__)
app.secret_key = 'secret_key'

genre_ids, anime_id_at, ultimate_binary_list = setup()


@app.route('/', methods=['GET', 'POST'])
def show_home():
    if request.method == 'POST':
        if request.form.get('search_by_card'):
            anime_title = request.form.get('search_by_card')
        else:
            anime_title = request.form['anime_title']
        recommend_list = get_recommendation(
            anime_title, genre_ids, anime_id_at, ultimate_binary_list)
        session.clear()
        session['recommend_list'] = recommend_list

        if len(recommend_list) == 0:
            return redirect(url_for('error', anime_title=anime_title))

        return redirect(url_for('result', anime_title=anime_title))

    return render_template('home.html', title="Home")


@app.route('/result/<anime_title>')
def result(anime_title):
    recommend_list = session['recommend_list']
    return render_template("result.html", title="Result", anime_title=anime_title, input=anime_title, recommend_list=recommend_list)


@app.route('/error/<anime_title>')
def error(anime_title):
    return render_template("error.html", title="Error", anime_title=anime_title)


if __name__ == '__main__':
    app.run(debug=True)
