from flask import Flask,render_template,request
import pickle
import sklearn
import warnings
warnings.filterwarnings('ignore')
import os

with open('model1.pkl','rb') as my_file:
    unpickler=pickle.Unpickler(my_file)
    model=unpickler.load()
    print(model)

app=Flask(__name__)

@app.route("/",methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/text',methods=['POST'])
def predict_price():
    if request.method=="POST":
        Present_Price=int(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        current_year=2023
        reg_year=int(request.form['reg_year'])
        Owner=int(request.form['Owner'])
        Age=current_year-reg_year
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol=="Petrol":
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif Fuel_Type_Petrol=='Diesel':
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if Seller_Type_Individual=="Individual":
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0

        Transmission_Manual=request.form['Transmission_Manual']
        if Transmission_Manual=="Manual":
            Transmission_Manual=1
        else:
            Transmission_Manual=0
    else:
        return render_template('home.html')


    # fp=open('model1.pkl','rb')
    # model=pickle.load(fp)

    prediction=model.predict([[Present_Price,
                               Kms_Driven,
                               Owner,
                               Age,
                               Fuel_Type_Diesel,
                               Fuel_Type_Petrol,
                               Seller_Type_Individual,
                               Transmission_Manual]])
    output=round(prediction[0],2)

    # if output<0:
    #     return render_template("home.html",prediction_text="Sorry You Cannot Sell this Car")
    # else:
    #     return render_template("home.html",prediction_text="You can sell your car at {}".format(output))
    if output<0:
        return render_template('home.html',prediction_text="Sorry you can not sell this car")
    else:
        return render_template('home.html',prediction_text="you can sell this car at  {}Lakhs of Rupees".format(output))



if  __name__ == "__main__":
    app.run(debug=True)

