import random
from src.text.paragraphs import help_message, commands_message


def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == 'hello':
        return "Hello peasant"

    if p_message.startswith("roll"):
        try:
            _, user_number = p_message.split(" ")
            user_number = int(user_number)
            if user_number <= 1000000:
                return str(random.randint(1, user_number))
            else:
                return "Number must be between 1 and 1'000'000 "
        except ValueError:
            return "Invalid number"
        except IndexError:
            return "Please provide a number after 'roll'"

    if p_message == "help":
        return help_message

    if p_message == "commands":
        return commands_message





