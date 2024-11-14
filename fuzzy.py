import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from textblob import TextBlob

# Function to read the latest feedback from Excel
def read_latest_feedback_from_excel(file_path):
    try:
        feedback_df = pd.read_excel(file_path)
        latest_feedback = feedback_df.iloc[-1]['Feedback']
    except FileNotFoundError:
        latest_feedback = ""
    return latest_feedback

# Read feedback from Excel
try:
    feedback_df = pd.read_excel('feedback.xlsx')
    feedback = feedback_df['Feedback'].tolist()
except FileNotFoundError:
    feedback = []

# Perform sentiment analysis
sentiment_scores = [TextBlob(fb).sentiment.polarity for fb in feedback]
positive_count = sum(1 for score in sentiment_scores if score > 0)
negative_count = sum(1 for score in sentiment_scores if score < 0)
neutral_count = sum(1 for score in sentiment_scores if score == 0)

# Define fuzzy variables for sentiment scores and sentiment levels
sentiment_score_var = ctrl.Antecedent(np.arange(-1, 1.1, 0.1), 'sentiment_score')
sentiment_level = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'sentiment_level')

# Define membership functions for sentiment scores
sentiment_score_var['negative'] = fuzz.trimf(sentiment_score_var.universe, [-1, -1, 0])
sentiment_score_var['neutral'] = fuzz.trimf(sentiment_score_var.universe, [-0.5, 0, 0.5])
sentiment_score_var['positive'] = fuzz.trimf(sentiment_score_var.universe, [0, 1, 1])

# Define membership functions for sentiment levels
sentiment_level['low'] = fuzz.trimf(sentiment_level.universe, [0, 0, 0.5])
sentiment_level['medium'] = fuzz.trimf(sentiment_level.universe, [0.25, 0.5, 0.75])
sentiment_level['high'] = fuzz.trimf(sentiment_level.universe, [0.5, 1, 1])

# Define rules
rule1 = ctrl.Rule(sentiment_score_var['negative'], sentiment_level['low'])
rule2 = ctrl.Rule(sentiment_score_var['neutral'], sentiment_level['medium'])
rule3 = ctrl.Rule(sentiment_score_var['positive'], sentiment_level['high'])

# Create control system
sentiment_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

# Perform control system simulation for each sentiment count
positive_sim = ctrl.ControlSystemSimulation(sentiment_ctrl)
positive_sim.input['sentiment_score'] = 1
positive_sim.compute()
positive_level = positive_sim.output['sentiment_level']

negative_sim = ctrl.ControlSystemSimulation(sentiment_ctrl)
negative_sim.input['sentiment_score'] = -1
negative_sim.compute()
negative_level = negative_sim.output['sentiment_level']

neutral_sim = ctrl.ControlSystemSimulation(sentiment_ctrl)
neutral_sim.input['sentiment_score'] = 0
neutral_sim.compute()
neutral_level = neutral_sim.output['sentiment_level']

# Plot the fuzzy logic output for each sentiment count

plt.bar(['Positive', 'Negative', 'Neutral'], [positive_level, negative_level, neutral_level])
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Sentiment Level')

# Read the latest feedback from Excel
latest_feedback = read_latest_feedback_from_excel('feedback.xlsx')

# Perform sentiment analysis
overall_sentiment_score = TextBlob(latest_feedback).sentiment.polarity

# Define fuzzy variables
sentiment_score_var = ctrl.Antecedent(np.arange(-1, 1.1, 0.1), 'sentiment_score')
sentiment_level = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'sentiment_level')

# Define membership functions for sentiment_score
sentiment_score_var['negative'] = fuzz.trimf(sentiment_score_var.universe, [-1, -1, 0])
sentiment_score_var['neutral'] = fuzz.trimf(sentiment_score_var.universe, [-0.5, 0, 0.5])
sentiment_score_var['positive'] = fuzz.trimf(sentiment_score_var.universe, [0, 1, 1])

# Define membership functions for sentiment_level
sentiment_level['low'] = fuzz.trimf(sentiment_level.universe, [0, 0, 0.5])
sentiment_level['medium'] = fuzz.trimf(sentiment_level.universe, [0.25, 0.5, 0.75])
sentiment_level['high'] = fuzz.trimf(sentiment_level.universe, [0.5, 1, 1])

# Define rules
rule1 = ctrl.Rule(sentiment_score_var['negative'], sentiment_level['low'])
rule2 = ctrl.Rule(sentiment_score_var['neutral'], sentiment_level['medium'])
rule3 = ctrl.Rule(sentiment_score_var['positive'], sentiment_level['high'])

# Create control system
sentiment_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
sentiment_eval = ctrl.ControlSystemSimulation(sentiment_ctrl)

# Pass sentiment score and compute sentiment level
sentiment_eval.input['sentiment_score'] = overall_sentiment_score
sentiment_eval.compute()

sentiment_level.view(sim=sentiment_eval)
plt.title('Fuzzy Logic Sentiment')
plt.tight_layout()
plt.show()
