from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

def save_vehicle(data):
    with open('vehicles.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def load_vehicles():
    vehicles = []
    with open('vehicles.csv', mode='r') as file:
        reader = csv.reader(file)
        vehicles = list(reader)
    return vehicles

def load_vehicle_by_plate(plate):
    vehicles = load_vehicles()
    for vehicle in vehicles:
        if vehicle[3] == plate:
            return vehicle
    return None

def update(plate, updated_data):
    vehicles = load_vehicles()
    for index, vehicle in enumerate(vehicles):
        if vehicle[3] == plate:
            vehicles[index] = updated_data
            break
    with open('vehicles.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(vehicles)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        plate = request.form['plate']
        data = [make, model, year, plate]
        save_vehicle(data)
        return redirect(url_for('list_vehicles'))
    return render_template('register.html')

@app.route('/listar')
def list_vehicles():
    vehicles = load_vehicles()
    return render_template('list.html', vehicles=vehicles)

@app.route('/pesquisar', methods=['GET', 'POST'])
def search_vehicle():
    if request.method == 'POST':
        plate = request.form['plate']
        vehicle = load_vehicle_by_plate(plate)
        if vehicle:
            return redirect(url_for('update_vehicle', plate=plate))
        else:
            return render_template('search.html', error='Veículo não encontrado')
    return render_template('search.html')

@app.route('/atualizar/<plate>', methods=['GET', 'POST'])
def update_vehicle(plate):
    vehicle = load_vehicle_by_plate(plate)
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        updated_data = [make, model, year, plate]
        update(plate, updated_data)
        return redirect(url_for('list_vehicles'))
    return render_template('update.html', vehicle=vehicle, plate=plate)

if __name__ == '__main__':
    app.run(debug=True)
