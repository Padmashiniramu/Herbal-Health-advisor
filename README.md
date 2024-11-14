# 🌿 Herbal Health Advisor
## 📝 Overview
The Herbal Health Advisor is a web-based application that provides natural, plant-based remedies based on user-inputted symptoms. Designed with both Tamil and English language support, the platform leverages fuzzy logic and machine learning to analyze user feedback and refine recommendations.
## 🌟Features
- **Symptom Input**: Users can enter symptoms to receive herbal remedy suggestions.
- **Language Support**: Remedies are displayed in both Tamil and English for accessibility.
- **Plant Remedies with Images**: Detailed information on each plant remedy, including 
images, to help users identify and understand treatments.
- **Sentiment Analysis**: Feedback is collected and analyzed using Natural Language 
Processing (NLP) and machine learning to categorize sentiment as positive, negative, or 
neutral.
- **AI and Machine Learning Integration**:
 - Supervised Learning: Uses classification and regression algorithms.
 - Unsupervised Learning: Implements clustering (K-means).
 - Sentiment classification powered by Bayes classification and TextBlob.
 - Prediction module that selects algorithms based on accuracy.
 - Evaluation module using iterative processes for dataset training.
## Project Modules
1. **Data Collection**: Collects user-generated comments from forums, blogs, and social 
networks using APIs.
2. **Data Preprocessing**: Tokenization, stemming, and filtering are applied to prepare data 
for analysis.
3. **Sentiment Classification**: Categorizes user feedback into positive, negative, or neutral 
sentiments.
4. **Machine Learning Algorithms**:
 - **Supervised Learning**: Classification and regression models for accurate predictions.
 - **Unsupervised Learning**: Clustering with K-means to group similar data points.
5. **Prediction and Evaluation**: Optimizes algorithm accuracy and continually improves 
predictions through dataset training.
## ⚙️ Installation
### Prerequisites
**Python 3.x**
**pip (Python package installer)**
1. Clone the repository:
 ```bash
 git clone https://github.com/padmashiniram/herbal-health-advisor.git
 ```
2. Install the required dependencies:
 ```bash
 pip install -r requirements.txt
 ```
3. Set up language support files for Tamil and English.
4. Run the application:
 ```bash
 python app.py
 ```
## 🚀Usage
1. Navigate to the home page.
2. Enter symptoms and select the preferred language (Tamil or English).
3. View recommended herbal remedies with images.
4. Leave feedback on remedies to help improve the recommendation engine.
5. Review sentiment analysis results on the feedback page.
## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Machine Learning**: TextBlob, Naive Bayes Classifier, K-means Clustering
- **Data Collection**: APIs for forums, blogs, social networks
- **Data Preprocessing**: Tokenization, Stemming, Filtering
## 📊 Machine Learning Workflow
-**Data Collection**
Uses APIs to gather user-generated comments from forums, blogs, and social networks.

-**Data Preprocessing**
Includes tokenization, stemming, and filtering to prepare text for sentiment analysis.

-**Algorithms**
*Supervised Learning:* Classification and regression models.
*Unsupervised Learning:* Clustering and K-means algorithms for symptom pattern discovery.
-**Evaluation**
An iterative training process is used to improve the accuracy of predictive models.
  
## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.
## 📜License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for 
details
