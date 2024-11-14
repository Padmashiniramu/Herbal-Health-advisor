import os
import pandas as pd
from gtts import gTTS
import speech_recognition as sr
from translate import Translator
from flask import Flask, render_template, request

app = Flask(__name__)

class TraditionalMedicineRecommendationSystem:
    def __init__(self, database):
        self.database = database

    def recommend_plants(self, symptoms):
        recommended_plants = []
        for plant in self.database:
            plant_symptoms = plant['SYMPTOM'].lower().split(',')
            if all(symptom.strip().lower() in plant_symptoms for symptom in symptoms):
                recommended_plants.append(plant)
        return recommended_plants

def text_to_speech(text, language, filename='output.mp3'):
     tts = gTTS(text=text, lang=language)
     audio_path = os.path.join(app.root_path, 'static', 'output.mp3')
     tts.save(audio_path)
     return audio_path
 
def speech_to_text(language):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing speech...")
        # Pass language parameter based on output language choice
        user_input = recognizer.recognize_google(audio, language='en-US' if language == '2' else 'ta-IN')
        print("Speech recognized:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand your audio input. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
def save_feedback_to_excel(feedback):
    print("Saving feedback:", feedback)
    try:
        file_path = 'feedback.xlsx'
        if os.path.isfile(file_path):
            feedback_df = pd.read_excel(file_path)
            new_feedback_df = pd.DataFrame({'Feedback': [feedback]})
            updated_feedback_df = pd.concat([feedback_df, new_feedback_df], ignore_index=True)
            updated_feedback_df.to_excel(file_path, index=False)
            print("Feedback added successfully.")
        else:
            new_feedback_df = pd.DataFrame({'Feedback': [feedback]})
            new_feedback_df.to_excel(file_path, index=False)
            print("Created a new feedback file.")
    except PermissionError:
        print("Permission denied: Unable to write to feedback.xlsx. Please check file permissions.")
    except Exception as e:
        print(f"Error occurred while adding feedback: {e}")

@app.route('/', methods=['GET', 'POST'])
def content():
    recommended_plants = []  # Initialize recommended_plants here
    symptoms=[]

    if request.method == 'POST':
        output_language = request.form['language']
        mode = request.form['mode']
        symptom = request.form['symptom']

        def preprocess_input(input_text, language):
            if language == '1':
                # Translate symptoms from Tamil to English
                translator = Translator(to_lang="en", from_lang="ta")
                translated_text = translator.translate(input_text)
                symptoms = translated_text.split(',')
            else:
                symptoms = input_text.split(',')
            return symptoms

        def read_medicinal_plants_data_from_excel(file_path):
            df = pd.read_excel(file_path)
            return df.to_dict('records')

        if output_language not in ['1', '2']:
            print("Invalid language selection.")
            return

        if mode not in ['1', '2']:
            print("Invalid input mode selection.")
            return

        file_path = 'data.xlsx'
        database = read_medicinal_plants_data_from_excel(file_path)
        recommendation_system = TraditionalMedicineRecommendationSystem(database)

        if mode == "1":
            symptoms = preprocess_input(symptom, '1')
        elif mode == "2":
            symptom = speech_to_text(output_language)
            symptoms = preprocess_input(symptom, output_language)
        else:
            print("Invalid input mode selection.")
            return

        if symptoms:
            print("Your Symptoms:", symptoms)
            print("Processing...")
            recommended_plants = recommendation_system.recommend_plants(symptoms)
            if recommended_plants:
                print("Recommended Medicinal Plants:")
                for plant in recommended_plants:
                    translator = Translator(to_lang="ta" if output_language == '1' else "en", from_lang="en")
                    common_name_translation = translator.translate(plant['COMMON NAME'])
                    botanical_name_translation = translator.translate(plant['BOTANICAL NAME'])
                    description_translation = translator.translate(plant['DESCRIPTION'])
                    how_to_use_translation = translator.translate(plant['HOW TO USE'])

                    if output_language == '1':
                        plant['TAMIL_NAME'] = plant.pop('TAMIL NAME')
                        plant['COMMON_NAME'] = common_name_translation
                        plant['BOTANICAL_NAME'] = botanical_name_translation
                        plant['DESCRIPTION'] = description_translation
                        plant['HOW_TO_USE'] = how_to_use_translation

                        audio_choice = request.form.get('audio')
                        if audio_choice == "yes":
                            text_to_speech(plant['DESCRIPTION'], 'ta', f"output_{plant['TAMIL_NAME']}.mp3")
                            plant['AUDIO_PATH'] = f"output_{plant['TAMIL_NAME']}.mp3"

                    else:
                        plant['TAMIL_NAME'] = plant.pop('TAMIL NAME')
                        plant['COMMON_NAME'] = plant.pop('COMMON NAME')
                        plant['BOTANICAL_NAME'] = plant.pop('BOTANICAL NAME')
                        plant['DESCRIPTION'] = plant.pop('DESCRIPTION')
                        plant['HOW_TO_USE'] = plant.pop('HOW TO USE')

                        audio_choice = request.form.get('audio')
                        if audio_choice == "yes":
                            text_to_speech(plant['DESCRIPTION'], 'en', f"output_{plant['COMMON_NAME']}.mp3")
                            plant['AUDIO_PATH'] = f"output_{plant['COMMON_NAME']}.mp3"

                    print("Image Link:", plant['LINK'], "\n")

    return render_template('content.html',symptoms=symptoms, recommended_plants=recommended_plants)

    
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        feedback = request.form['feedback']
        save_feedback_to_excel(feedback)
    return render_template('feed.html') 
if __name__ == "__main__":
    app.run(debug=True)
