from flask import Flask, render_template, request # Flask is a application
# used to run/serve our application
# request is used to access the file which is uploaded by the user in out application
# render_template is used for rendering the html pages
import pickle # pickle is used for serializing and de-serializing Python object structures
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "VW27KsF0GYLCJVFLrl2S-qpnt17wyaCs_x9TFXtQWyW5"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

#response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e928a1c1-ea25-45ab-ac2f-c98478924c6d/predictions?version=2022-03-06', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())

app=Flask(__name__) # our flask app

@app.route('/') # rendering the html template
def home():
    return render_template('h.html')
@app.route('/predict') # rendering the html template
def index() :
    return render_template("index.html")

@app.route('/data_predict', methods=['GET','POST']) # route for our prediction
def predict():
    
    # loading model which we saved
    model = pickle.load(open('wineQuality_new.pkl', 'rb'))
 
    data = [[x for x in request.form.values()]]    
    
    pred= model.predict(data)[0]
    print(pred)
    if pred==0:
        prediction="Bad"
    else:
        prediction="Good"
    
    return render_template('pred.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)