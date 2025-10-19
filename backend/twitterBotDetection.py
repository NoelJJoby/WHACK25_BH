import joblib
from sklearn.preprocessing import PolynomialFeatures


def query_bot_detector(user_data):

    model_filename = 'backend/TwitterBotDetector.joblib'
    model = joblib.load(model_filename)
    input_values = [
            user_data['Retweet Count'],
            user_data['Mention Count'],
            user_data['Follower Count'],
            user_data['Verified']
    ] 
    poly = PolynomialFeatures(degree=2, include_bias=True)
   
    
    transformed_features = poly.fit_transform([input_values])
        
    



    prediction_score = model.predict(transformed_features)

   
    bot_probability = prediction_score[0]

    return bot_probability






if __name__ == "__main__":

    new_user_to_check = {
        'Retweet Count': 0,
        'Mention Count': 0,
        'Follower Count': 142,
        'Verified': 1  # 0 for False
    }


    probability = query_bot_detector(new_user_to_check)



    print("\n--- Prediction Result ---")
    print(f"The bot score is: {probability:.2f}")


  