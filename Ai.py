import speech_recognition as sr
import pyttsx3
import datetime
import json
import sqlite3
import requests
import random
from dataclasses import dataclass
from typing import List, Dict, Any
import threading
import schedule
import time

class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure voice settings
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id)  # Female voice
        self.tts_engine.setProperty('rate', 180)
        
        # Initialize database
        self.init_database()
        
        # Load assistant modules
        self.study_assistant = StudyAssistant()
        self.wellness_assistant = WellnessAssistant()
        self.productivity_assistant = ProductivityAssistant()
        self.support_chatbot = SupportChatbot()
        self.finance_assistant = FinanceAssistant()
        self.meal_planner = MealPlanner()
        self.tech_troubleshooter = TechTroubleshooter()
        self.language_buddy = LanguageBuddy()
        
        self.is_listening = False
        
    def init_database(self):
        """Initialize SQLite database for storing user data"""
        self.conn = sqlite3.connect('assistant_data.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create tables for different modules
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT,
                priority TEXT,
                due_date TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                amount REAL,
                category TEXT,
                description TEXT,
                date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY,
                meal_name TEXT,
                meal_type TEXT,
                calories INTEGER,
                ingredients TEXT,
                date TEXT
            )
        ''')
        
        self.conn.commit()
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        """Listen for voice input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5)
                
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
            
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Sorry, there was an error with the speech recognition service."
        except sr.WaitTimeoutError:
            return "timeout"
    
    def process_command(self, command):
        """Process voice commands and route to appropriate module"""
        if any(word in command for word in ['math', 'science', 'history', 'study', 'homework']):
            return self.study_assistant.handle_query(command)
            
        elif any(word in command for word in ['mindfulness', 'meditation', 'stress', 'wellness', 'relax']):
            return self.wellness_assistant.handle_request(command)
            
        elif any(word in command for word in ['task', 'reminder', 'todo', 'schedule', 'productivity']):
            return self.productivity_assistant.handle_task(command)
            
        elif any(word in command for word in ['support', 'help', 'problem', 'issue']):
            return self.support_chatbot.handle_support(command)
            
        elif any(word in command for word in ['money', 'budget', 'expense', 'finance', 'spend']):
            return self.finance_assistant.handle_finance(command)
            
        elif any(word in command for word in ['meal', 'food', 'nutrition', 'recipe', 'diet']):
            return self.meal_planner.handle_meal_request(command)
            
        elif any(word in command for word in ['tech', 'computer', 'wifi', 'troubleshoot', 'fix']):
            return self.tech_troubleshooter.handle_tech_issue(command)
            
        elif any(word in command for word in ['language', 'translate', 'learn', 'practice']):
            return self.language_buddy.handle_language_request(command)
            
        elif 'stop' in command or 'quit' in command or 'exit' in command:
            return "stop"
            
        else:
            return "I'm not sure how to help with that. Try asking about studies, wellness, tasks, support, finance, meals, tech issues, or language learning."
    
    def run(self):
        """Main loop for the voice assistant"""
        self.speak("Hello! I'm your personal AI assistant. I can help you with studies, wellness, productivity, support, finance, meals, tech issues, and language learning. How can I assist you today?")
        
        self.is_listening = True
        
        while self.is_listening:
            command = self.listen()
            
            if command == "timeout":
                continue
            elif "Sorry" in command:
                self.speak(command)
                continue
                
            response = self.process_command(command)
            
            if response == "stop":
                self.speak("Goodbye! Have a great day!")
                self.is_listening = False
            else:
                self.speak(response)

# Study Assistant Module
class StudyAssistant:
    def __init__(self):
        self.math_topics = {
            'algebra': 'Algebra involves working with variables and equations. Key concepts include solving for x, factoring, and working with polynomials.',
            'geometry': 'Geometry deals with shapes, angles, and spatial relationships. Important concepts include area, perimeter, and the Pythagorean theorem.',
            'calculus': 'Calculus involves derivatives and integrals. It helps us understand rates of change and areas under curves.'
        }
        
        self.science_topics = {
            'physics': 'Physics studies matter, energy, and their interactions. Key areas include mechanics, thermodynamics, and electromagnetism.',
            'chemistry': 'Chemistry focuses on atoms, molecules, and chemical reactions. Important concepts include the periodic table and chemical bonding.',
            'biology': 'Biology is the study of living organisms. It covers topics like cells, genetics, evolution, and ecosystems.'
        }
        
        self.history_topics = {
            'world war': 'World War 1 occurred from 1914-1918, and World War 2 from 1939-1945. These conflicts reshaped global politics and society.',
            'ancient rome': 'Ancient Rome was a powerful civilization that lasted from 753 BC to 476 AD, known for its military, law, and engineering.',
            'renaissance': 'The Renaissance was a period of cultural rebirth in Europe from the 14th to 17th centuries, marked by advances in art and science.'
        }
    
    def handle_query(self, query):
        """Handle study-related queries"""
        query = query.lower()
        
        # Check for math topics
        for topic, explanation in self.math_topics.items():
            if topic in query:
                return f"Here's what I know about {topic}: {explanation}"
        
        # Check for science topics
        for topic, explanation in self.science_topics.items():
            if topic in query:
                return f"Here's what I know about {topic}: {explanation}"
        
        # Check for history topics
        for topic, explanation in self.history_topics.items():
            if topic in query:
                return f"Here's what I know about {topic}: {explanation}"
        
        # Math problem solving
        if 'solve' in query and any(op in query for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            return "I can help with basic math problems. For complex calculations, I recommend breaking them down into smaller steps."
        
        return "I can help with math, science, and history topics. What specific subject would you like to learn about?"

# Mental Wellness Assistant Module
class WellnessAssistant:
    def __init__(self):
        self.breathing_exercises = [
            "Let's do a 4-7-8 breathing exercise. Breathe in for 4 counts, hold for 7, then exhale for 8. Ready? Breathe in... 1, 2, 3, 4. Hold... 1, 2, 3, 4, 5, 6, 7. Exhale... 1, 2, 3, 4, 5, 6, 7, 8.",
            "Try box breathing. Breathe in for 4, hold for 4, exhale for 4, hold for 4. Let's begin: In... 1, 2, 3, 4. Hold... 1, 2, 3, 4. Out... 1, 2, 3, 4. Hold... 1, 2, 3, 4."
        ]
        
        self.meditation_guides = [
            "Find a comfortable position. Close your eyes and focus on your breath. Notice the air entering and leaving your nostrils. When your mind wanders, gently bring attention back to your breath.",
            "Let's do a body scan meditation. Start by relaxing your toes, then your feet, ankles, calves. Work your way up through your entire body, releasing tension as you go."
        ]
        
        self.affirmations = [
            "You are capable of handling whatever comes your way today.",
            "You deserve peace, happiness, and success.",
            "Every challenge is an opportunity to grow stronger.",
            "You are worthy of love and respect, especially from yourself."
        ]
    
    def handle_request(self, request):
        """Handle wellness-related requests"""
        request = request.lower()
        
        if 'breathing' in request or 'breathe' in request:
            return random.choice(self.breathing_exercises)
        
        elif 'meditation' in request or 'meditate' in request:
            return random.choice(self.meditation_guides)
        
        elif 'affirmation' in request or 'positive' in request:
            return f"Here's a positive affirmation for you: {random.choice(self.affirmations)}"
        
        elif 'stress' in request:
            return "When feeling stressed, try the 5-4-3-2-1 grounding technique: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste."
        
        elif 'anxious' in request or 'anxiety' in request:
            return "For anxiety, try progressive muscle relaxation. Tense and then relax each muscle group, starting with your toes and working up to your head."
        
        return "I can guide you through breathing exercises, meditation, provide affirmations, or help with stress and anxiety techniques. What would you like to try?"

# Productivity Assistant Module
class ProductivityAssistant:
    def __init__(self):
        self.tasks = []
    
    def handle_task(self, command):
        """Handle productivity and task management"""
        command = command.lower()
        
        if 'add task' in command or 'new task' in command:
            return "What task would you like to add? Please tell me the task description."
        
        elif 'list tasks' in command or 'show tasks' in command:
            if not self.tasks:
                return "You have no tasks scheduled."
            
            task_list = "Here are your current tasks: "
            for i, task in enumerate(self.tasks, 1):
                task_list += f"{i}. {task['description']} - Priority: {task['priority']}. "
            return task_list
        
        elif 'complete task' in command:
            return "Which task number would you like to mark as complete?"
        
        elif 'reminder' in command:
            return "I can set reminders for you. What would you like to be reminded about and when?"
        
        elif 'schedule' in command:
            return "I can help you manage your schedule. Would you like to add an appointment or view your calendar?"
        
        return "I can help you add tasks, set reminders, manage your schedule, and boost productivity. What would you like to do?"
    
    def add_task(self, description, priority="medium"):
        """Add a new task"""
        task = {
            'description': description,
            'priority': priority,
            'completed': False,
            'created_at': datetime.datetime.now()
        }
        self.tasks.append(task)
        return f"Task added: {description} with {priority} priority."

# Customer Support Chatbot Module
class SupportChatbot:
    def __init__(self):
        self.faq = {
            'account': 'For account issues, please check your login credentials and ensure your internet connection is stable.',
            'password': 'To reset your password, go to the login page and click "Forgot Password". Follow the instructions sent to your email.',
            'billing': 'For billing questions, please check your account dashboard or contact our billing department.',
            'technical': 'For technical issues, try restarting the application or clearing your browser cache.',
            'refund': 'Refund requests can be processed within 30 days of purchase. Please provide your order number.'
        }
    
    def handle_support(self, query):
        """Handle customer support queries"""
        query = query.lower()
        
        for keyword, response in self.faq.items():
            if keyword in query:
                return response
        
        if 'help' in query:
            return "I can help with account issues, password resets, billing questions, technical problems, and refund requests. What specific issue are you experiencing?"
        
        return "I understand you need support. Can you please describe your specific issue? I can help with accounts, passwords, billing, technical issues, or refunds."

# Finance & Budget Assistant Module
class FinanceAssistant:
    def __init__(self):
        self.expenses = []
        self.budget_categories = {
            'food': 500,
            'transportation': 200,
            'entertainment': 150,
            'utilities': 300,
            'shopping': 200
        }
    
    def handle_finance(self, command):
        """Handle finance and budget queries"""
        command = command.lower()
        
        if 'add expense' in command or 'spent' in command:
            return "I can help you track that expense. What did you spend money on and how much?"
        
        elif 'budget' in command:
            budget_info = "Here's your monthly budget: "
            for category, amount in self.budget_categories.items():
                budget_info += f"{category.title()}: ${amount}. "
            return budget_info
        
        elif 'expenses' in command or 'spending' in command:
            if not self.expenses:
                return "You haven't recorded any expenses yet."
            
            total = sum(expense['amount'] for expense in self.expenses)
            return f"Your total recorded expenses are ${total:.2f}."
        
        elif 'save money' in command or 'saving tips' in command:
            tips = [
                "Try the 50-30-20 rule: 50% needs, 30% wants, 20% savings.",
                "Track your daily expenses to identify spending patterns.",
                "Consider cooking at home more often to save on food costs.",
                "Look for subscription services you're not using and cancel them."
            ]
            return random.choice(tips)
        
        return "I can help you track expenses, manage your budget, and provide money-saving tips. What would you like to know about your finances?"

# Meal Planner & Nutrition Assistant Module
class MealPlanner:
    def __init__(self):
        self.recipes = {
            'breakfast': [
                {'name': 'Oatmeal with berries', 'calories': 300, 'prep_time': '5 minutes'},
                {'name': 'Greek yogurt parfait', 'calories': 250, 'prep_time': '3 minutes'},
                {'name': 'Avocado toast', 'calories': 350, 'prep_time': '5 minutes'}
            ],
            'lunch': [
                {'name': 'Grilled chicken salad', 'calories': 400, 'prep_time': '15 minutes'},
                {'name': 'Quinoa bowl', 'calories': 450, 'prep_time': '20 minutes'},
                {'name': 'Turkey sandwich', 'calories': 380, 'prep_time': '5 minutes'}
            ],
            'dinner': [
                {'name': 'Baked salmon with vegetables', 'calories': 500, 'prep_time': '25 minutes'},
                {'name': 'Chicken stir-fry', 'calories': 450, 'prep_time': '20 minutes'},
                {'name': 'Vegetarian pasta', 'calories': 400, 'prep_time': '15 minutes'}
            ]
        }
    
    def handle_meal_request(self, request):
        """Handle meal planning and nutrition requests"""
        request = request.lower()
        
        if 'breakfast' in request:
            meal = random.choice(self.recipes['breakfast'])
            return f"For breakfast, I suggest {meal['name']}. It has {meal['calories']} calories and takes {meal['prep_time']} to prepare."
        
        elif 'lunch' in request:
            meal = random.choice(self.recipes['lunch'])
            return f"For lunch, try {meal['name']}. It has {meal['calories']} calories and takes {meal['prep_time']} to prepare."
        
        elif 'dinner' in request:
            meal = random.choice(self.recipes['dinner'])
            return f"For dinner, I recommend {meal['name']}. It has {meal['calories']} calories and takes {meal['prep_time']} to prepare."
        
        elif 'meal plan' in request:
            breakfast = random.choice(self.recipes['breakfast'])
            lunch = random.choice(self.recipes['lunch'])
            dinner = random.choice(self.recipes['dinner'])
            
            return f"Here's your daily meal plan: Breakfast - {breakfast['name']}, Lunch - {lunch['name']}, Dinner - {dinner['name']}. Total calories: approximately {breakfast['calories'] + lunch['calories'] + dinner['calories']}."
        
        elif 'calories' in request:
            return "The average daily calorie needs are about 2000 for women and 2500 for men, but this varies based on age, activity level, and other factors."
        
        elif 'nutrition' in request:
            tips = [
                "Aim for 5 servings of fruits and vegetables daily.",
                "Include lean proteins in every meal.",
                "Choose whole grains over refined grains.",
                "Stay hydrated with 8 glasses of water daily."
            ]
            return random.choice(tips)
        
        return "I can help you plan meals, suggest recipes, provide nutrition information, and give healthy eating tips. What would you like to know?"

# DIY Tech Troubleshooter Module
class TechTroubleshooter:
    def __init__(self):
        self.solutions = {
            'wifi': [
                "Try restarting your router by unplugging it for 30 seconds, then plugging it back in.",
                "Check if other devices can connect to the same network.",
                "Move closer to the router to improve signal strength.",
                "Forget and reconnect to the WiFi network in your device settings."
            ],
            'computer slow': [
                "Restart your computer to clear temporary files and refresh memory.",
                "Check for running programs in Task Manager and close unnecessary ones.",
                "Run a disk cleanup to free up storage space.",
                "Check for malware using your antivirus software."
            ],
            'phone': [
                "Try restarting your phone by holding the power button.",
                "Check if you have enough storage space available.",
                "Update your apps and operating system.",
                "Clear the cache for problematic apps."
            ],
            'printer': [
                "Check that the printer is connected and powered on.",
                "Ensure there's paper in the tray and ink in the cartridges.",
                "Try printing a test page from the printer's menu.",
                "Restart both your computer and printer."
            ]
        }
    
    def handle_tech_issue(self, issue):
        """Handle tech troubleshooting requests"""
        issue = issue.lower()
        
        for problem, solutions in self.solutions.items():
            if problem in issue:
                return f"Here's how to fix your {problem} issue: {random.choice(solutions)}"
        
        if 'internet' in issue or 'connection' in issue:
            return random.choice(self.solutions['wifi'])
        
        elif 'slow' in issue:
            return random.choice(self.solutions['computer slow'])
        
        elif any(device in issue for device in ['laptop', 'computer', 'pc']):
            return random.choice(self.solutions['computer slow'])
        
        return "I can help troubleshoot WiFi, slow computers, phone issues, printer problems, and internet connectivity. What specific tech issue are you experiencing?"

# Language Learning Buddy Module
class LanguageBuddy:
    def __init__(self):
        self.languages = {
            'spanish': {
                'greetings': {'hello': 'hola', 'goodbye': 'adiós', 'thank you': 'gracias'},
                'numbers': {'one': 'uno', 'two': 'dos', 'three': 'tres'},
                'colors': {'red': 'rojo', 'blue': 'azul', 'green': 'verde'}
            },
            'french': {
                'greetings': {'hello': 'bonjour', 'goodbye': 'au revoir', 'thank you': 'merci'},
                'numbers': {'one': 'un', 'two': 'deux', 'three': 'trois'},
                'colors': {'red': 'rouge', 'blue': 'bleu', 'green': 'vert'}
            },
            'german': {
                'greetings': {'hello': 'hallo', 'goodbye': 'auf wiedersehen', 'thank you': 'danke'},
                'numbers': {'one': 'eins', 'two': 'zwei', 'three': 'drei'},
                'colors': {'red': 'rot', 'blue': 'blau', 'green': 'grün'}
            }
        }
        
        self.learning_tips = [
            "Practice speaking out loud, even if you're alone.",
            "Try to think in the language you're learning.",
            "Watch movies or TV shows with subtitles in your target language.",
            "Use flashcards for vocabulary building.",
            "Practice a little bit every day rather than long sessions occasionally."
        ]
    
    def handle_language_request(self, request):
        """Handle language learning requests"""
        request = request.lower()
        
        # Check for specific languages
        for lang in self.languages.keys():
            if lang in request:
                if 'greeting' in request:
                    greetings = self.languages[lang]['greetings']
                    greeting_list = ", ".join([f"{eng} is {foreign}" for eng, foreign in greetings.items()])
                    return f"Here are some {lang} greetings: {greeting_list}"
                
                elif 'number' in request:
                    numbers = self.languages[lang]['numbers']
                    number_list = ", ".join([f"{eng} is {foreign}" for eng, foreign in numbers.items()])
                    return f"Here are some {lang} numbers: {number_list}"
                
                elif 'color' in request:
                    colors = self.languages[lang]['colors']
                    color_list = ", ".join([f"{eng} is {foreign}" for eng, foreign in colors.items()])
                    return f"Here are some {lang} colors: {color_list}"
        
        if 'translate' in request:
            return "I can help with basic translations for Spanish, French, and German. What would you like to translate?"
        
        elif 'practice' in request:
            return "Let's practice! I can help you with greetings, numbers, and colors in Spanish, French, or German. Which language interests you?"
        
        elif 'tip' in request or 'advice' in request:
            return f"Here's a language learning tip: {random.choice(self.learning_tips)}"
        
        return "I can help you learn Spanish, French, or German. I can teach greetings, numbers, colors, provide translations, and give learning tips. What would you like to learn?"

# Main execution
if __name__ == "__main__":
    # Create and run the voice assistant
    assistant = VoiceAssistant()
    
    print("Starting Voice Assistant...")
    print("Available modules:")
    print("- Study Assistant (math, science, history)")
    print("- Mental Wellness (mindfulness, meditation)")
    print("- Productivity (tasks, reminders)")
    print("- Customer Support")
    print("- Finance & Budget")
    print("- Meal Planner & Nutrition")
    print("- Tech Troubleshooter")
    print("- Language Learning")
    print("\nSay 'stop', 'quit', or 'exit' to end the session.\n")
    
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nAssistant stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        assistant.conn.close()
