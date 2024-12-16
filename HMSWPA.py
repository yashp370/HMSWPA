import mysql.connector
from datetime import date
import pandas as pd 
import matplotlib.pyplot as plt

# Establish database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='mysq001'
)
cursor = db.cursor()


# Add a new patient
def add_patient(name, age, gender, lifestyle_factors, contact_info):
    query = "INSERT INTO patients (name, age, gender, lifestyle_factors, contact_info) VALUES (%s, %s, %s, %s, %s)"
    values = (name, age, gender, lifestyle_factors, contact_info)
    cursor.execute(query, values)
    db.commit()
    print(f"Patient {name} added successfully!")


# Schedule an appointment
def add_appointment(patient_id, doctor_id, appointment_date, appointment_time):
    query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time) VALUES (%s, %s, %s, %s)"
    values = (patient_id, doctor_id, appointment_date, appointment_time)
    cursor.execute(query, values)
    db.commit()
    print("Appointment scheduled successfully!")


# Add medical history for a patient
def add_medical_history(patient_id, diagnosis, treatment, diagnosis_date):
    query = "INSERT INTO medical_history (patient_id, diagnosis, treatment, diagnosis_date) VALUES (%s, %s, %s, %s)"
    values = (patient_id, diagnosis, treatment, diagnosis_date)
    cursor.execute(query, values)
    db.commit()
    print("Medical history added successfully!")


# Fetch patient data for health risk prediction
def fetch_patient_data():
    query = "SELECT age, gender, lifestyle_factors FROM patients"
    cursor.execute(query)
    result = cursor.fetchall()
    data = pd.DataFrame(result, columns=['age', 'gender', 'lifestyle_factors'])
    return data

# Predict health risk based on age and lifestyle
def predict_health_risk():
    data = fetch_patient_data()
    risk = []
    
    for i, row in data.iterrows():
        if row['age'] > 50 and 'smoking' in row['lifestyle_factors'].lower():
            risk.append('High')
        else:
            risk.append('Low')
    
    data['risk'] = risk
    print("Health Risk Predictions:")
    print(data[['age', 'gender', 'lifestyle_factors', 'risk']])
    

# Visualize health data without using apply
def visualize_health_data():
    data = fetch_patient_data()
    risk = []
    
    for i, row in data.iterrows():
        if row['age'] > 50 and 'smoking' in row['lifestyle_factors'].lower():
            risk.append('High')
        else:
            risk.append('Low')
    
    data['risk'] = risk
    
    # Simple bar plot for age distribution by risk level
    risk_counts = data['risk'].value_counts()
    risk_counts.plot(kind='bar')
    plt.xlabel('Risk Level')
    plt.ylabel('Count')
    plt.title('Patient Risk Level Distribution')
    plt.show()


# Generate a report on high-risk patients without using apply
def generate_report():
    data = fetch_patient_data()
    high_risk_patients = data[(data['age'] > 50) & (data['lifestyle_factors'].str.contains('smoking', case=False))]
    
    print("High-Risk Patients Report:\n", high_risk_patients)   

# Menu system to interact with the user
def menu():
    while True:
        print("\nHealthcare Management System")
        print("1. Add Patient")
        print("2. Schedule Appointment")
        print("3. Add Medical History")
        print("4. Predict Health Risk")
        print("5. Visualize Health Data")
        print("6. Generate Report")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter patient name: ")
            age = int(input("Enter patient age: "))
            gender = input("Enter patient gender (Male/Female): ")
            lifestyle_factors = input("Enter lifestyle factors (e.g., smoking, diet): ")
            contact_info = input("Enter contact information: ")
            add_patient(name, age, gender, lifestyle_factors, contact_info)

        elif choice == '2':
            patient_id = int(input("Enter patient ID: "))
            doctor_id = int(input("Enter doctor ID: "))
            appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
            appointment_time = input("Enter appointment time (HH:MM): ")
            add_appointment(patient_id, doctor_id, appointment_date, appointment_time)

        elif choice == '3':
            patient_id = int(input("Enter patient ID: "))
            diagnosis = input("Enter diagnosis: ")
            treatment = input("Enter treatment: ")
            diagnosis_date = input("Enter diagnosis date (YYYY-MM-DD): ")
            add_medical_history(patient_id, diagnosis, treatment, diagnosis_date)

        elif choice == '4':
            predict_health_risk()

        elif choice == '5':
            visualize_health_data()

        elif choice == '6':
            generate_report()

        elif choice == '7':
            print("Exiting system...")
            break

        else:
            print("Invalid choice, please try again.")


# Run the menu
menu()
