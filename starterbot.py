import os
import time
import math
from slackclient import SlackClient


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# game constants
MIN = 0
MAX = 100

# bot response constants
ANOTHER_GUESS_PROMPT = ['What\'s your next guess?', 'Have another guess?', 'Try another.']
LOW_PROMPTS = ['It\'s lower than %s.']
HIGH_PROMPTS = ['It\'s higher than %s.']
LOW_CLOSE_PROMPTS = ['Close, but not quite!']
HIGH_CLOSE_PROMPTS = ['Close, but not quite!']
LOWER_PROMPTS = ['You\'re getting warm.  It\'s lower than %s. Have another guess?',
'Warmer. Take another guess that\'s lower than %s.', 'Close, but it\'s lower than %s.']
HIGHER_PROMPTS = ['You\'re getting warm. It\'s higher than %s. Have another guess?',
'Warmer. It\'s also higher than %s. Take another guess.', 'Close, but it\'s higher than %s.']
LOWEST_PROMPTS = ['You\'re piping hot! But it\'s still lower.',
'You\'re hot as lava! Go lower.', 'Almost there! A bit lower.']
HIGHEST_PROMPTS = ['You\'re piping hot! But it\'s still higher.',
'You\'re hot as lava! Go higher.', 'Almost there! A bit higher.']

CORRECT_GUESS_PROMPTS = ['Well done! It is indeed %s.', 'Congratulations, that\'s it! I was thinking of %s.',
'You got it! It\'s %s.' ]
PLAY_AGAIN_QUESTION_PROMPTS = ['Wanna play again?', 'Want to try again?', 'Hey, should we do that again?']

QUIT_REVEAL_PROMPTS = ['Ok, I was thinking of %s.', 'Sure, I\'ll tell you the number anyway. It was %s.']
QUIT_REVEAL_BYE = ['Bye.', 'Good bye.', 'See you later.']
QUIT_PROMPTS = ['Alright, talk to you later then.', 'OK, till next time. Bye!',
'See you later.', 'OK, I\'m already thinking of a number for next time. Bye.']

GREETING_PROMPTS = ['Let\'s play Number Genie!', 'Welcome to Number Genie!']
INVOCATION_PROMPT = ['I\'m thinking of a number from %s to %s. What\'s your first guess?']
RE_PROMPT = ['Great!', 'Awesome!', 'Cool!', 'Okay, let\'s play again.', 'Okay, here we go again',
'Alright, one more time with feeling.']
RE_INVOCATION_PROMPT = ['I\'m thinking of a new number from %s to %s. What\'s your guess?']

WRONG_DIRECTION_LOWER_PROMPTS = ['Clever, but no. It\'s still lower than %s.',
'Nice try, but it\'s still lower than %s.']
WRONG_DIRECTION_HIGHER_PROMPTS = ['Clever, but no. It\'s still higher than %s.',
'Nice try, but it\'s still higher than %s.']

REALLY_COLD_LOW_PROMPTS = ['You\'re ice cold. It\'s way lower than %s.',
'You\'re freezing cold. It\'s a lot lower than %s.']
REALLY_COLD_HIGH_PROMPTS = ['You\'re ice cold. It’s way higher than %s.',
'You\'re freezing cold. It\'s a lot higher than %.']
REALLY_HOT_LOW_PROMPTS = ['Keep going.', 'So close, you\'re almost there.']
REALLY_HOT_HIGH_PROMPTS = ['Keep going.', 'So close, you\'re almost there.']

SAME_GUESS_PROMPTS_1 = ['It\'s still not %s. Guess %s.']
SAME_GUESS_PROMPTS_2 = ['Maybe it\'ll be %s the next time. Let’s play again soon.']

MIN_PROMPTS = ['I see what you did there. But no, it\'s higher than %s.']
MAX_PROMPTS = ['Oh, good strategy. Start at the top. But no, it’s lower than a %s.']

MANY_TRIES_PROMPTS = ['Yes! It\'s %s. Nice job!  How about one more round?']

FALLBACK_PROMPT_1 = ['Are you done playing Number Genie?']
FALLBACK_PROMPT_2 = ['Since I\'m still having trouble, so I\'ll stop here. Let’s play again soon.']

DEEPLINK_PROMPT_1 = ['%s has %s letters. It\'s higher than %s.', '%s has %s letters, but the number is higher than %s.']
const DEEPLINK_PROMPT_2 = ['%s has %s letters. It\'s lower than %s.', '%s has %s letters, but the number is lower than %s.']
DEEPLINK_PROMPT_3 = ['%s has %s letters. Wow! The number I was thinking of was %s!', '%s has %s letters. Amazing! The number I was thinking of was %s!']

NO_INPUT_PROMPTS = ['I didn\'t hear a number', 'If you\'re still there, what\'s your guess?', 'We can stop here. Let\'s play again soon.']

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

#random number for guessing game
def getRandomNumber(min, max):
    return math.floor(math.random() * (max - min + 1)) + min

# Utility function to pick prompts
def getRandomPrompt(array):
    return array[math.floor(math.random() * length(array))]

def generateAnswer(bot):
    answer = getRandomNumber(MIN,MAX)
    bot['answer'] = answer
    bot['guessCount'] = 0
    bot['fallbackCount'] = 0
    bot['ask'] = getRandomPrompt(GREETING_PROMPTS)) + ' ' + \
          getRandomPrompt(INVOCATION_PROMPT), MIN, MAX), NO_INPUT_PROMPTS)
    return bot


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
