"""Terminal chatbot using Django initialization and ChatterBot."""
import os
import sys

import django
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


def setup_django():
    """Initialize Django before running the chatbot."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
    django.setup()


def create_chatbot():
    """Build and train the conversational chatbot."""
    bot = ChatBot(
        'StudentChatBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///chatbot_database.sqlite3',
        read_only=False,
    )
    trainer = ListTrainer(bot)
    conversations = [
        ['Hello', 'Hi! How can I help you today?'],
        ['Good morning!', 'Good morning! How are you doing?'],
        ['How are you?', 'I am doing very well, thank you for asking.'],
        ['What is your name?', 'My name is StudentChatBot.'],
        ['What can you do?', 'I can answer questions and have conversations.'],
        ['Do you like hats?', 'Yes, hats can be very stylish!'],
        ['Thank you', "You're welcome!"],
        ['Goodbye', 'Goodbye! Have a wonderful day!'],
    ]
    for conversation in conversations:
        trainer.train(conversation)
    return bot


def start_chat(bot):
    """Accept terminal messages until the user exits."""
    print('=' * 50)
    print('WELCOME TO THE DJANGO CHATTERBOT APPLICATION')
    print('=' * 50)
    print("Type 'exit' to end the conversation.\n")
    while True:
        try:
            message = input('User: ').strip()
            if not message:
                print('Bot: Please enter a message.')
                continue
            if message.lower() in {'exit', 'quit', 'bye'}:
                print('Bot: Goodbye! Have a great day!')
                break
            print(f'Bot: {bot.get_response(message)}')
        except (KeyboardInterrupt, EOFError):
            print('\nBot: Conversation ended.')
            break
        except Exception as exc:
            print(f'Error: {exc}')
            print('Bot: Sorry, I could not process that.')


def main():
    """Set up the application and start the conversation."""
    try:
        setup_django()
        start_chat(create_chatbot())
    except Exception as exc:
        print(f'Application error: {exc}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
