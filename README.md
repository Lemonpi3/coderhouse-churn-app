# Coderhouse-churn-app
This is one of my Coderhouse proyects, it's not fully finished yet (I'm still doing the final touches), 
the main notebook is in spanish. 

I analized the dataset of a telecomunications company to get insights about how bad, 
which areas and what was causing the churn problem for the company. Then I built 2 models concatenated with each other
to help with their churn problem. 

One that predicts if a client is going to churn or not. And the other, if the 
first model predicts a churn, predicts the churn reason category (Competition, Dissatisfaction, Attitude, Price and Other).

I also made an app that contains the storytelling in a blog style and a canva presentation. 

The models are deployed in a flask api that uses a Sqllite database to store the clients data and the model predictions.
As for the app itself I've made it using the streamlit library.

## Links
* App https://lemonpi3-coderhouse-churn-app-app-oopeoj.streamlit.app/
* Notebook https://colab.research.google.com/drive/1roIA3LR2fZoZzlAq2NSs2g5gWIRLzFKI?usp=sharing
