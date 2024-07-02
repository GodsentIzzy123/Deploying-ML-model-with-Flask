import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from flask import Flask, request, render_template
import requests
from io import StringIO

app = Flask(__name__)

@app.route("/")
def loadPage():
    return render_template("home.html", query="")

@app.route("/", methods=["POST"])
def IrisPrediction():
    data_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

    # Get the data using requests with SSL verification disabled
    response = requests.get(data_url, verify=False)
    df = pd.read_csv(StringIO(response.text))

    inputQuery1 = float(request.form['query1'])
    inputQuery2 = float(request.form['query2'])
    inputQuery3 = float(request.form['query3'])
    inputQuery4 = float(request.form['query4'])

    df['species'] = df['species'].map({'setosa': 0, 'versicolor': 1, 'virginica': 2})

    train, test = train_test_split(df, test_size=0.1)

    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

    train_X = train[features]
    train_y = train.species

    test_X = test[features]
    test_y = test.species

    model = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    model.fit(train_X, train_y)

    prediction = model.predict(test_X)
    accuracy = metrics.accuracy_score(prediction, test_y)

    data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4]]
    new_df = pd.DataFrame(data, columns=features)

    single = model.predict(new_df)[0]
    probabilities = model.predict_proba(new_df)[0]

    if single == 0:
        o1 = "This Flower species is Setosa"
        o2 = f"Confidence: {probabilities[single] * 100:.2f}%"
    elif single == 1:
        o1 = "This Flower species is Versicolor"
        o2 = f"Confidence: {probabilities[single] * 100:.2f}%"
    else:
        o1 = "This Flower species is Virginica"
        o2 = f"Confidence: {probabilities[single] * 100:.2f}%"

    return render_template("home.html", output1=o1, output2=o2, query1=inputQuery1, query2=inputQuery2, query3=inputQuery3, query4=inputQuery4)

if __name__ == "__main__":
    app.run(debug=True)
