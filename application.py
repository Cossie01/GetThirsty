from flask import Flask, jsonify, abort, request, render_template, redirect, url_for, session
from voteDAO import voteDAO
import requests
from flask_limiter import Limiter
import json

app = Flask(__name__, static_url_path='', static_folder='static')

app.secret_key = 'someSecretKey'

#Limiter
def get_remote_address():
    return request.remote_addr

limiter = Limiter(app)
limiter.key_func = get_remote_address

teas = [
    {'name':'Barrys'},
    {'name':'Lyons'},
    {'name':'PG Tips'},
    {'name':'Tetleys'},
    ]
#External Api
@app.route('/external-teas', methods=['GET'])
def getExternalTeas():
    try:
        api_url = 'https://boonakitea.cyclic.app/api/teas'
        response = requests.get(api_url)
        response.raise_for_status()  
        teas = response.json()
        return render_template('externalApi.html', teas=teas)
    except requests.exceptions.RequestException as e:
        abort(500, f"An error occurred while retrieving teas from the external API: {e}")




#Internal Api
@app.route('/tea', methods = ['GET'])
@limiter.limit("10/minute") #limit usage
def getAllTeas():
    return jsonify(teas)

@app.route('/vote/<teaname>', methods = ['POST'])
@limiter.limit("1/minute")
def voteforTeas(teaname):
    ip_address = request.remote_addr
    data = (teaname, ip_address)
    newid= voteDAO.create(data)
    
    return jsonify({'id':newid})

@app.route('/vote/<teaname>', methods = ['GET'])
def getCountForTeas(teaname):
    count =voteDAO.countvotes(teaname)
    return jsonify({teaname:count})

@app.route('/vote-count', methods = ['GET'])
def getAllCountForTeas():
    allcounts =[]
    for tea in teas:
        teaname=tea['name']
        count = voteDAO.countvotes(teaname)
        allcounts.append({teaname:count})
    return jsonify(allcounts)

@app.route('/vote/all', methods = ['DELETE'])
def deleteAllVotes():
    return jsonify({'done':True})

@app.route('/tea/<teaname>', methods = ['PUT']) 
def updateTea(teaname):
    new_tea_name = request.json.get('new_tea_name')

    for tea in teas:
        if tea['name'] == teaname:
            tea['name'] = new_tea_name
            return jsonify(tea)
    
    abort(404, f"Tea with name {teaname} not found")

#LoginServer
def validate_credentials(email, password):
    return True

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('loginPage'))


@app.route('/vote')
def vote():
    if 'username' not in session:
        return redirect(url_for('loginPage'))

    return render_template('vote.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/results')
def results():
    return render_template('results.html')


#debug
@app.route('/loginPage', methods=['GET', 'POST'])
def loginPage():
    session.clear()  

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Email: {email}")  
        print(f"Password: {password}")  

        if validate_credentials(email, password):
            session['username'] = email  
            return redirect(url_for('vote'))
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('loginPage.html', error=error_message)

    return render_template('loginPage.html')


if __name__ == '__main__':
    app.run(debug=True)
