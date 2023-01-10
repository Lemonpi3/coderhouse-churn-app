# Coderhouse-churn-app
This is one of my Coderhouse proyects, it's not fully finished yet (I'm still doing the final touches), 
the main notebook is in spanish. 

I analized the dataset of a telecomunications company to get insights about how bad, 
which areas and what was causing the churn problem for the company.

To tackle the business problem I made 4 models:
* 2 clasification models:
  - First one is a Binary clasification model: Predicts the churn probability of a user.
  - The second one is a multiclasification model: Predicts the churn type category. Is concatenated to the first model, if it predicts a churn it predicts the probabilities of the categories
* 1 regression model: Predicts the total revenue that the user will yield in the quarter, with the main goal of setting priorities in churn savings efforts (it's not the same to lose a user that just pays the minimum than loosing a whale).
* 1 clustering model: Segmentates the users in 4 clusters with the goal of helping the company to give a more personalized service to the customers and increase tenure.

I also made an app that contains the storytelling in a blog style and a canva presentation. 

The models are deployed in a flask api that uses a Sqllite database to store the clients data and the model predictions.
As for the app itself I've made it using the streamlit library.

## Links
* App https://lemonpi3-coderhouse-churn-app-app-oopeoj.streamlit.app/
* Notebook https://colab.research.google.com/drive/1roIA3LR2fZoZzlAq2NSs2g5gWIRLzFKI?usp=sharing

**For more info about the dataset or models check the app**
