#!/usr/bin/env python

__author__ = "Stephanie McCumsey"
__credits__ = ["https://raw.githubusercontent.com/actions-on-google/apiai-number-genie-nodejs/master/app.js"]

import os
import time
import math
from random import random
from slackclient import SlackClient

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

class BotAssistant:

        def __init__(self):
            # starterbot's ID as an environment variable
            self.BOT_ID = os.environ.get("BOT_ID")

            # constants
            self.AT_BOT = "<@" + self.BOT_ID + ">"
            self.EXAMPLE_COMMAND = "play"

            # game constants
            self.MIN = 0
            self.MAX = 100

            # bot response constants
            self.HIGHER_HINT = 'higher'
            self.LOWER_HINT = 'lower'
            self.NO_HINT = 'none'

            self.SSML_SPEAK_START = ''#'<speak>'
            self.SSML_SPEAK_END = '' #'</speak>'
            self.COLD_WIND_AUDIO = '' #'<audio src="https://xxx/NumberGenieEarcon_ColdWind.wav">cold wind sound</audio>'
            self.STEAM_ONLY_AUDIO = '' #'<audio src="https://xxx/NumberGenieEarcon_SteamOnly.wav">steam sound</audio>'
            self.STEAM_AUDIO = '' #'<audio src="https://xxx/NumberGenieEarcons_Steam.wav">steam sound</audio>'
            self.YOU_WIN_AUDIO = '' #'<audio src="https://xxx/NumberGenieEarcons_YouWin.wav">winning sound</audio>'

            self.ANOTHER_GUESS_PROMPT = ['What\'s your next guess?', 'Have another guess?', 'Try another.']
            self.LOW_PROMPTS = ['It\'s lower than %s.']
            self.HIGH_PROMPTS = ['It\'s higher than %s.']
            self.LOW_CLOSE_PROMPTS = ['Close, but not quite!']
            self.HIGH_CLOSE_PROMPTS = ['Close, but not quite!']
            self.LOWER_PROMPTS = ['You\'re getting warm.    It\'s lower than %s. Have another guess?',
            'Warmer. Take another guess that\'s lower than %s.', 'Close, but it\'s lower than %s.']
            self.HIGHER_PROMPTS = ['You\'re getting warm. It\'s higher than %s. Have another guess?',
            'Warmer. It\'s also higher than %s. Take another guess.', 'Close, but it\'s higher than %s.']
            self.LOWEST_PROMPTS = ['You\'re piping hot! But it\'s still lower.',
            'You\'re hot as lava! Go lower.', 'Almost there! A bit lower.']
            self.HIGHEST_PROMPTS = ['You\'re piping hot! But it\'s still higher.',
            'You\'re hot as lava! Go higher.', 'Almost there! A bit higher.']

            self.CORRECT_GUESS_PROMPTS = ['Well done! It is indeed %s.', 'Congratulations, that\'s it! I was thinking of %s.',
            'You got it! It\'s %s.' ]
            self.PLAY_AGAIN_QUESTION_PROMPTS = ['Wanna play again?', 'Want to try again?', 'Hey, should we do that again?']

            self.QUIT_REVEAL_PROMPTS = ['Ok, I was thinking of %s.', 'Sure, I\'ll tell you the number anyway. It was %s.']
            self.QUIT_REVEAL_BYE = ['Bye.', 'Good bye.', 'See you later.']
            self.QUIT_PROMPTS = ['Alright, talk to you later then.', 'OK, till next time. Bye!',
            'See you later.', 'OK, I\'m already thinking of a number for next time. Bye.']

            self.GREETING_PROMPTS = ['Let\'s play Number Genie!', 'Welcome to Number Genie!']
            self.INVOCATION_PROMPT = ['I\'m thinking of a number from %s to %s. What\'s your first guess?']
            self.RE_PROMPT = ['Great!', 'Awesome!', 'Cool!', 'Okay, let\'s play again.', 'Okay, here we go again',
            'Alright, one more time with feeling.']
            self.RE_INVOCATION_PROMPT = ['I\'m thinking of a new number from %s to %s. What\'s your guess?']

            self.WRONG_DIRECTION_LOWER_PROMPTS = ['Clever, but no. It\'s still lower than %s.',
            'Nice try, but it\'s still lower than %s.']

            self.REALLY_COLD_LOW_PROMPTS = ['You\'re ice cold. It\'s way lower than %s.',
            'You\'re freezing cold. It\'s a lot lower than %s.']
            self.REALLY_COLD_HIGH_PROMPTS = ['You\'re ice cold. It’s way higher than %s.',
            'You\'re freezing cold. It\'s a lot higher than %.']
            self.REALLY_HOT_LOW_PROMPTS = ['Keep going.', 'So close, you\'re almost there.']
            self.REALLY_HOT_HIGH_PROMPTS = ['Keep going.', 'So close, you\'re almost there.']

            self.SAME_GUESS_PROMPTS_1 = ['It\'s still not %s. Guess %s.']
            self.SAME_GUESS_PROMPTS_2 = ['Maybe it\'ll be %s the next time. Let’s play again soon.']

            self.MIN_PROMPTS = ['I see what you did there. But no, it\'s higher than %s.']
            self.MAX_PROMPTS = ['Oh, good strategy. Start at the top. But no, it’s lower than a %s.']

            self.MANY_TRIES_PROMPTS = ['Yes! It\'s %s. Nice job!    How about one more round?']

            self.FALLBACK_PROMPT_1 = ['Are you done playing Number Genie?']
            self.FALLBACK_PROMPT_2 = ['Since I\'m still having trouble, so I\'ll stop here. Let’s play again soon.']

            self.DEEPLINK_PROMPT_1 = ['%s has %s letters. It\'s higher than %s.', '%s has %s letters, but the number is higher than %s.']
            self.DEEPLINK_PROMPT_2 = ['%s has %s letters. It\'s lower than %s.', '%s has %s letters, but the number is lower than %s.']
            self.DEEPLINK_PROMPT_3 = ['%s has %s letters. Wow! The number I was thinking of was %s!', '%s has %s letters. Amazing! The number I was thinking of was %s!']

            self.NO_INPUT_PROMPTS = ['I didn\'t hear a number', 'If you\'re still there, what\'s your guess?', 'We can stop here. Let\'s play again soon.']

        #random number for guessing game
        @staticmethod
        def getRandomNumber(min, max):
            return math.floor(random() * (max - min + 1)) + min

        # Utility function to pick prompts
        @staticmethod
        def getRandomPrompt(array):
            return array[math.floor(random() * len(array))]

        def generateAnswer(self):
            print('generateAnswer')
            answer = BotAssistant.getRandomNumber(self.MIN,self.MAX)
            self.answer = answer
            self.guessData = []
            self.guessCount = 0
            self.duplicateCount = 0
            self.fallbackCount = 0
            return BotAssistant.getRandomPrompt(self.GREETING_PROMPTS) + ' ' + \
                        BotAssistant.getRandomPrompt(self.INVOCATION_PROMPT) % (self.MIN, self.MAX)

        def checkGuess(self, guess):
            print('checkGuess')
            guess = int(guess)
            answer = self.answer
            diff = abs(answer - guess)
            self.guessCount += 1
            self.fallbackCount = 0
            # Check for duplicate guesses
            if hasattr(BotAssistant, 'previousGuess'):
                if self.previousGuess == guess:
                    self.duplicateCount += 1
                    if self.duplicateCount == 1:
                        return BotAssistant.getRandomPrompt(self.SAME_GUESS_PROMPTS_1) % (guess, self.hint)
                    elif self.duplicateCount == 2:
                        return getRandomPrompt(SAME_GUESS_PROMPTS_2) % (guess)
            self.duplicateCount = 0
            # Check if user isn't following hints
            if hasattr(BotAssistant, 'hint'):
                if self.hint == self.HIGHER_HINT and guess <= self.previousGuess:
                    return getRandomPrompt(self.WRONG_DIRECTION_HIGHER_PROMPTS) % (self.previousGuess)
                elif self.hint == self.LOWER_HINT and guess >= self.previousGuess:
                    return getRandomPrompt(self.WRONG_DIRECTION_LOWER_PROMPTS) % (self.previousGuess)
            # Handle boundaries with special prompts
            if answer != guess:
                if guess == self.MIN:
                    self.hint = self.HIGHER_HINT
                    self.previousGuess = guess
                    return getRandomPrompt(self.MIN_PROMPTS) % (self.MIN)
                elif guess == self.MAX:
                    self.hint = self.LOWER_HINT
                    self.previousGuess(guess)
                    return getRandomPrompt(self.MAX_PROMPTS) % (self.MAX)
            # Give different responses based on distance from number
            if diff > 75:
                # Guess is far away from number
                if answer > guess:
                    self.hint = HIGHER_HINT
                    self.previousGuess = guess
                    return self.SSML_SPEAK_START + self.COLD_WIND_AUDIO + \
                        BotAssistant.getRandomPrompt(self.REALLY_COLD_HIGH_PROMPTS) % (guess) + self.SSML_SPEAK_END

                elif answer < guess:
                    self.hint = self.LOWER_HINT
                    self.previousGuess = guess
                    return self.SSML_SPEAK_START + self.COLD_WIND_AUDIO + \
                        BotAssistant.getRandomPrompt(self.REALLY_COLD_LOW_PROMPTS) % (guess) + self.SSML_SPEAK_END

            elif diff == 4:
                # Guess is getting closer
                if answer > guess:
                    self.hint = self.NO_HINT
                    self.previousGuess = guess
                    return BotAssistant.getRandomPrompt(self.HIGH_CLOSE_PROMPTS)
                elif answer < guess:
                    self.hint = self.NO_HINT
                    self.previousGuess = guess
                    return BotAssistant.getRandomPrompt(self.LOW_CLOSE_PROMPTS)
            elif diff == 3:
                # Guess is even closer
                if answer > guess:
                    self.hint = self.HIGHER_HINT
                    self.previousGuess = guess
                    return self.SSML_SPEAK_START + self.STEAM_ONLY_AUDIO + BotAssistant.getRandomPrompt(self.HIGHEST_PROMPTS) + self.SSML_SPEAK_END
                elif answer < guess:
                    self.hint = self.LOWER_HINT
                    self.previousGuess = guess
                    return self.SSML_SPEAK_START + self.STEAM_ONLY_AUDIO + BotAssistant.getRandomPrompt(self.LOWEST_PROMPTS) + self.SSML_SPEAK_END
            elif diff <= 10 and diff > 4:
                # Guess is nearby number
                if answer > guess:
                    self.hint = self.HIGHER_HINT
                    self.previousGuess = guess
                    return BotAssistant.getRandomPrompt(self.HIGHER_PROMPTS) % (guess),
                elif answer < guess:
                    self.hint = self.LOWER_HINT
                    self.previousGuess = guess
                    return BotAssistant.getRandomPrompt(self.LOWER_PROMPTS) % (guess)
            # Give hints on which direction to go
            if answer > guess:
                if hasattr(self, "hint"):
                    previousHint = self.hint
                self.hint = self.HIGHER_HINT
                self.previousGuess = guess
                if 'previousHint' in locals():
                    if previousHint == self.HIGHER_HINT and diff <= 2:
                        # Very close to number
                        return self.SSML_SPEAK_START + self.STEAM_AUDIO + \
                            BotAssistant.getRandomPrompt(self.REALLY_HOT_HIGH_PROMPTS) + self.SSML_SPEAK_END
                    else:
                        return BotAssistant.getRandomPrompt(self.HIGH_PROMPTS) % (guess) + ' ' + \
                            BotAssistant.getRandomPrompt(self.ANOTHER_GUESS_PROMPT)
            elif answer < guess:
                if hasattr(self, "hint"):
                    previousHint = self.hint
                self.hint = self.LOWER_HINT
                self.previousGuess = guess
                if 'previousHint' in locals():
                    if previousHint == self.LOWER_HINT and diff <= 2:
                        # Very close to number
                        return self.SSML_SPEAK_START + self.STEAM_AUDIO + \
                            BotAssistant.getRandomPrompt(self.REALLY_HOT_LOW_PROMPTS) + self.SSML_SPEAK_END
                    else:
                        return self.getRandomPrompt(self.LOW_PROMPTS) % (guess) + ' ' + \
                            BotAssistant.getRandomPrompt(self.ANOTHER_GUESS_PROMPT)
            else:
                # Guess is same as number
                guessCount = self.guessCount
                self.hint = self.NO_HINT
                self.previousGuess = -1
                #self.setContext(self.YES_NO_CONTEXT)
                self.guessCount = 0
                if guessCount >= 10:
                    return self.SSML_SPEAK_START + self.YOU_WIN_AUDIO + \
                        BotAssistant.getRandomPrompt(self.MANY_TRIES_PROMPTS) % (answer) + self.SSML_SPEAK_END
                else:
                    return self.SSML_SPEAK_START + self.YOU_WIN_AUDIO + \
                        BotAssistant.getRandomPrompt(self.CORRECT_GUESS_PROMPTS) % (answer) + ' ' + \
                        BotAssistant.getRandomPrompt(self.PLAY_AGAIN_QUESTION_PROMPTS) + self.SSML_SPEAK_END

        def handle_command(self, command, channel):
                """
                        Receives commands directed at the bot and determines if they
                        are valid commands. If so, then acts on the commands. If not,
                        returns back what it needs for clarification.
                """
                response = "Not sure what you mean. Use the *" + self.EXAMPLE_COMMAND + \
                                     "* command to get started."
                #response = self.NO_INPUT_PROMPTS
                print("ATTR: ", hasattr(self, 'guessCount'))
                if command.startswith(self.EXAMPLE_COMMAND):
                        if not hasattr(BotAssistant, 'guessCount'):
                                response = self.generateAnswer()
                elif hasattr(self, 'guessCount'):
                        if command.isnumeric():
                                if self.guessCount >= 0:
                                        response = self.checkGuess(command)
                slack_client.api_call("chat.postMessage", channel=channel,
                                                            text=response, as_user=True)


        def parse_slack_output(self, slack_rtm_output):
                """
                        The Slack Real Time Messaging API is an events firehose.
                        this parsing function returns None unless a message is
                        directed at the Bot, based on its ID.
                """
                output_list = slack_rtm_output
                if output_list and len(output_list) > 0:
                        for output in output_list:
                                if output and 'text' in output and self.AT_BOT in output['text']:
                                        # return text after the @ mention, whitespace removed
                                        return output['text'].split(self.AT_BOT)[1].strip().lower(), \
                                                     output['channel']
                return None, None


if __name__ == "__main__":
        READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
        my_bot = BotAssistant()
        if slack_client.rtm_connect():
                print("StarterBot connected and running!")
                while True:
                        command, channel = my_bot.parse_slack_output(slack_client.rtm_read())
                        if command and channel:
                                my_bot.handle_command(command, channel)
                                if hasattr(my_bot, 'answer'):
                                        print("CHECK: ", command, my_bot.answer)
                        time.sleep(READ_WEBSOCKET_DELAY)
        else:
                print("Connection failed. Invalid Slack token or bot ID?")
