from flask import Flask, render_template, request, redirect, url_for, flash
import requests

URL="https://cafe-api-nzxp.onrender.com"
# URL=" http://127.0.0.1:5001"
app = Flask(__name__)
app.secret_key = "hbjdhd643hg48hf7"



@app.route('/', methods=['GET', 'POST'])
def home():
 
    if request.method=='POST':
        loc = request.form.get('location')
        response = requests.get(f'{URL}/search', params={"loc":loc.title()})
        # response.raise_for_status()
        if response.status_code == 404:
            flash("Sorry, we don't have the cafe at this location")
            return redirect(url_for('home'))
        data = response.json()
        print(data)
       
        all_cafe = data['cafes']
        # return redirect(url_for('home'))
        return render_template('index.html', cafes = all_cafe, location = loc)

    
    response = requests.get(f'{URL}/all')
    response.raise_for_status()
    data = response.json()
    all_cafe = data['cafes']

    return render_template('index.html', cafes = all_cafe)

@app.route('/new-cafe', methods=['GET', 'POST'])
def new_cafe():
    if request.method == 'POST':
        parameters ={
            "name": request.form.get('cafe_name').title(),
            "map_url": request.form.get('map_url'),
            "img_url": request.form.get('image_url'),
            "loc": request.form.get('location').title(),
            "seats": request.form.get('seats'),
            "price": request.form.get('price'),
            "toilet":request.form.get('toilet'),
            "wifi": request.form.get('wifi'),
            "sockets": request.form.get('sockets'),
            "calls": request.form.get('calls')
        }
        # print(params)
        response = requests.post(f'{URL}/add', params=parameters)
        data = response.json()
        if data['response']:
            flash("Cafe added successfully")
            return redirect(url_for('new_cafe'))
        else:
            flash("Error adding cafe")
            return redirect(url_for('new_cafe'))

    return render_template('add_cafe.html')


@app.route('/edit_price/<int:id>/<name>', methods=['GET', 'POST'])
def edit_price(id, name):
    if request.method == 'POST':
        new_price = request.form.get('price')
        response = requests.patch(f'{URL}/update-price/{id}', params={'price':new_price})
        response.raise_for_status()
        data = response.json()
        print(data)
        if data['response']:
            flash("Price updated successfully")
            return redirect(url_for('home'))
        else:
            flash("Error updating price")
            return redirect(url_for('home'))

    
    return render_template('edit_price.html', name=name, id=id)

@app.route('/delete/<int:id>/<name>', methods=['GET', 'POST'])
def delete_cafe(id, name):
    if request.method=='POST':
        api_key = request.form.get('api-key')
        response = requests.delete(f'{URL}/report-closed/{id}', params={'api-key': api_key})
        response.raise_for_status()
        data = response.json()
        if data['response']:
            flash('Cafe deleted successfully')
            return redirect(url_for('home'))
        else:
            flash('Error deleting cafe')
            return redirect(url_for('home'))
    return render_template('delete_cafe.html', id=id, name=name)

if __name__ == '__main__':
    app.run(debug=True)
