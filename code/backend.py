import os
import pandas as pd
from gtts import gTTS
import speech_recognition as sr
from translate import Translator

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
    tts.save("output.mp3")
    os.system("start output.mp3")

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

def save_feedback_to_excel(feedback):
    try:
        feedback_df = pd.read_excel('feedback.xlsx')
        new_feedback_df = pd.DataFrame({'Feedback': [feedback]})
        updated_feedback_df = pd.concat([feedback_df, new_feedback_df], ignore_index=True)
        updated_feedback_df.to_excel('feedback.xlsx', index=False)
    except FileNotFoundError:
        new_feedback_df = pd.DataFrame({'Feedback': [feedback]})
        new_feedback_df.to_excel('feedback.xlsx', index=False)

def main():
    print("Please select the language for output:")
    print("1. Tamil")
    print("2. English")
    output_language = input("Enter your choice (1 or 2): ")

    if output_language not in ['1', '2']:
        print("Invalid language selection.")
        return

    print("Please select the input mode:")
    print("1. Text Input")
    print("2. Speech Input")
    mode = input("Enter your choice (1 or 2): ")

    if mode not in ['1', '2']:
        print("Invalid input mode selection.")
        return

    file_path = 'data.xlsx'
    database = read_medicinal_plants_data_from_excel(file_path)
    recommendation_system = TraditionalMedicineRecommendationSystem(database)

    if mode == "1":
        symptoms_tamil = input("Please enter your symptoms separated by commas: ")
        symptoms = preprocess_input(symptoms_tamil, '1')
    elif mode == "2":
        symptoms_tamil = speech_to_text(output_language)
        symptoms = preprocess_input(symptoms_tamil, output_language)
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
                # Translate relevant information to the chosen output language
                translator = Translator(to_lang="ta" if output_language == '1' else "en", from_lang="en")
                common_name_translation = translator.translate(plant['COMMON NAME'])
                botanical_name_translation = translator.translate(plant['BOTANICAL NAME'])
                description_translation = translator.translate(plant['DESCRIPTION'])
                how_to_use_translation = translator.translate(plant['HOW TO USE'])

                if output_language == '1':
                    # Print and ask user if they want to listen to the audio
                    output_text_tamil = f"Tamil Name: {plant['TAMIL NAME']}\n" \
                                        f"Common Name: {common_name_translation}\n" \
                                        f"Botanical Name: {botanical_name_translation}\n" \
                                        f"Description: {description_translation}\n" \
                                        f"How to Use: {how_to_use_translation}\n"    
                    print(output_text_tamil)
                    audio_choice = input("Do you want to listen to the audio? (yes/no): ").strip().lower()
                    if audio_choice == "yes":
                        text_to_speech(output_text_tamil, 'ta')
                else:
                    # Print and ask user if they want to listen to the audio
                    output_text = f"Tamil Name: {plant['TAMIL NAME']}\n" \
                                  f"Common Name: {plant['COMMON NAME']}\n" \
                                  f"Botanical Name: {plant['BOTANICAL NAME']}\n" \
                                  f"Description: {plant['DESCRIPTION']}\n" \
                                  f"How to Use: {plant['HOW TO USE']}\n" 
                                    
                    print(output_text)
                    audio_choice = input("Do you want to listen to the audio? (yes/no): ").strip().lower()
                    if audio_choice == "yes":
                        text_to_speech(output_text, 'en')
                # Wait for the user to press Enter before proceeding to the next recommendation
                print("Image Link:",plant['LINK'],"\n")
                input("Press Enter to continue...")

            # Get feedback and save to Excel
            feedback = input("Please provide feedback on the recommended plants: ")
            save_feedback_to_excel(feedback)

if __name__ == "__main__":
    main()
