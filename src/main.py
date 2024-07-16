from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

from Config import *
from CheckInSystem import *

def create_app():
    template_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'templates')
    app = Flask(__name__, template_folder=template_dir) 
    app.system = CheckInSystem(debug_level=DEBUG_LEVEL, db_name=DB_NAME, should_run_thread=True)
    CORS(app)
    

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        reservation_number = data.get('reservationNumber')
        date = data.get('date')
        time_zone = data.get('timeZone')
        print(date, end='\n')
        print(time_zone, end='\n')
        # date_str = data.get('date') # MM/DD/YYYY
        # time = data.get('time') # HH:MM
        # time_zone = data.get('time_zone') #  HAST AKST PST MST CST EST
        if len(reservation_number) != 6:
            print(f'Supplied reservation number: {reservation_number} is not 6 chars long')
            return jsonify({"message": "Incorrect confirmation number"}), 400
    
        print(f'Received reservation: {first_name} {last_name}, Number: {reservation_number}')
        error_code = app.system.add_reservation(first_name, last_name, reservation_number)
        if  error_code != ErrorCode.SUCCESS:
            print(f'Supplied reservation number: {reservation_number} failed with error: {error_code.value}')
            return jsonify({"message": "Unable to add reservation"}), 400
    
        return jsonify({"message": "Reservation received"}), 201
    
    @app.route('/remove', methods=['POST'])
    def delete_reservation():
        data = request.json
        reservation_number = data.get('reservationNumber')
        if len(reservation_number) != 6:
            print(f'Supplied reservation number: {reservation_number} is not 6 chars long')
            return jsonify({"message": "Confirmation number does not exist"}), 400
    
        print(f'Attempting to delete reservation number: {reservation_number}')
        error_code = app.system.delete_reservation_by_name(reservation_number)
        if  error_code != ErrorCode.SUCCESS:
            print(f'Supplied reservation number: {reservation_number} was unable to be deleted with\
                  error: {error_code.value}')
            return jsonify({"message": "Unable to delete reservation"}), 400
    
        return jsonify({"message": "Reservation deleted"}), 201
    
    @app.route('/', methods=['GET'])
    def page():
        return render_template('page.html')

    return app
   
if __name__ == "__main__": 
    app = create_app()
    app.run(debug=False) 
