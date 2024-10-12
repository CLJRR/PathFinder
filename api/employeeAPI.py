from flask import Blueprint,request,jsonify, render_template
from firebase_admin import firestore

db = firestore.client()
dbCollection = db.collection("employees")
employeeAPI = Blueprint("employeeAPI",__name__)

@employeeAPI.route('/',methods = ['GET'])
def show_form():
    return render_template('employeeDashboard.html')

@employeeAPI.route('/employee/<name>', methods=['GET'])
def employee_dashboard(name):
    try:
        # Fetch employee personal information from 'employees' collection
        employee_document = dbCollection.document(name).get()

        if employee_document.exists:
            employee_data = employee_document.to_dict()
        else:
            return jsonify({"error": "Employee not found"}), 404

        # Fetch KPI data from the 'kpi' collection
        kpi_ref = db.collection('kpi').document('base')
        kpi_doc = kpi_ref.get()

        if kpi_doc.exists:
            kpi_data = kpi_doc.to_dict()
            kpi_incidents = kpi_data.get('maxIncidents')
        else:
            return jsonify({"error": "KPI base document not found"}), 404

        # Fetch employee-specific KPI data (number of incidents)
        employee_kpi_ref = db.collection('kpi').document(name)
        employee_kpi_doc = employee_kpi_ref.get()

        if employee_kpi_doc.exists:
            employee_kpi_data = employee_kpi_doc.to_dict()
            employee_incidents = employee_kpi_data.get("incidents")
        else:
            return jsonify({"error": "Employee KPI data not found"}), 404

        # Determine risk level based on employee incidents and KPI max incidents
        if employee_incidents >= kpi_incidents:
            risk = "High Risk"
        elif employee_incidents > kpi_incidents / 2:
            risk = "Medium Risk"
        elif employee_incidents > kpi_incidents / 3:
            risk = "Low Risk"
        else:
            risk = "No Risk"

        response_data = {
            "employee_data": employee_data,
            "kpi_data": {
                "maxIncidents": kpi_incidents,
                "employeeIncidents": employee_incidents,
                "risk": risk
            }
        }

        # Return the combined JSON object
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    