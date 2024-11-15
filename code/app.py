from flask import Flask, render_template, request
import backend as new1

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')
# Load medicinal plants data from Excel
file_path = 'data.xlsx'
database = new1.read_medicinal_plants_data_from_excel(file_path)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        output_language = request.form['language']
        mode = request.form['mode']
        symptoms = request.form['symptoms']

        if mode == '2':
            # For speech input mode, call speech_to_text function
            symptoms = new1.speech_to_text(output_language)

        # Preprocess input
        symptoms = new1.preprocess_input(symptoms, output_language)

        if symptoms:
            # Initialize recommendation system
            recommendation_system = new1.TraditionalMedicineRecommendationSystem(database)

            # Get recommended plants
            recommended_plants = recommendation_system.recommend_plants(symptoms)

            return render_template('content.html', symptoms=symptoms, recommended_plants=recommended_plants)

    # Render the initial page for GET request or if there's no form submission
    return render_template('content.html')
@app.route('/feed')
def feed():
    return render_template('feed.html')



if __name__ == "__main__":
    app.run(debug=True)
