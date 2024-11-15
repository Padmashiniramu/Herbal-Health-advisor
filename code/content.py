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

def text_to_speech(text, language):
    tts = gTTS(text=text, lang=language)
    audio_file = "static/output.mp3"
    tts.save(audio_file)
    return audio_file


@app.route('/', methods=['GET', 'POST'])
def content():
    recommended_plants = []  
    symptoms = []
    
    if request.method == 'POST':
        audio_file = None
        output_language = request.form['language']
        mode = request.form['mode']
        symptom = request.form['symptom']

        def preprocess_input(input_text, language):
            if language == '1':
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
            return render_template('content.html')  # Return a valid response here

        if mode not in ['1', '2']:
            print("Invalid input mode selection.")
            return render_template('content.html')  # Return a valid response here

        file_path = 'data.xlsx'
        database = read_medicinal_plants_data_from_excel(file_path)
        recommendation_system = TraditionalMedicineRecommendationSystem(database)

        if mode == "1":
            symptoms = preprocess_input(symptom, '1')
        else:
            print("Invalid input mode selection.")
            return render_template('content.html')  # Return a valid response here

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
                    else:
                        plant['TAMIL_NAME'] = plant.pop('TAMIL NAME')
                        plant['COMMON_NAME'] = plant.pop('COMMON NAME')
                        plant['BOTANICAL_NAME'] = plant.pop('BOTANICAL NAME')
                        plant['DESCRIPTION'] = plant.pop('DESCRIPTION')
                        plant['HOW_TO_USE'] = plant.pop('HOW TO USE')
                    print("Image Link:", plant['LINK'], "\n")
                    if 'audio' in request.form :
                        print("Generating audio file...")
                        if output_language == '1':
                            output_text_tamil = f"Tamil Name: {plant['TAMIL NAME']}\n" \
                                            f"Common Name: {common_name_translation}\n" \
                                            f"Botanical Name: {botanical_name_translation}\n" \
                                            f"Description: {description_translation}\n" \
                                            f"How to Use: {how_to_use_translation}\n"
                            audio_file = text_to_speech(output_text_tamil, 'ta')
                            print(output_text_tamil)
                        else:
                            output_text = f"Tamil Name: {plant['TAMIL NAME']}\n" \
                                           f"Common Name: {plant['COMMON NAME']}\n" \
                                           f"Botanical Name: {plant['BOTANICAL NAME']}\n" \
                                           f"Description: {plant['DESCRIPTION']}\n" \
                                           f"How to Use: {plant['HOW TO USE']}\n"
                            audio_file = text_to_speech(output_text, 'en')
                            print(output_text)
                        return render_template('content.html', symptoms=symptoms, recommended_plants=recommended_plants, audio_file=audio_file)

                
    return render_template('content.html', symptoms=symptoms, recommended_plants=recommended_plants)

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
    
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        feedback = request.form['feedback']
        save_feedback_to_excel(feedback)
    return render_template('feed.html') 

if __name__ == "__main__":
    app.run(debug=True)
