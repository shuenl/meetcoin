# Bitcoin punishment system for showing up late for meetings with friends
import requests
import datetime
import time
import re
import json
import threading
import signal


# Telegram bot credentials
bot_token = ''
bot_url = 'https://api.telegram.org/bot%s/' %(bot_token)


# Send message function
def send_message(response_text, chat_id):
	sendmessage_url = bot_url+'sendMessage'
	payload = {'chat_id':chat_id,'text':response_text}
	r = requests.get(sendmessage_url,params=payload)


# Check text based message for keywords
def text_check(message_text, message_userid, sender_name):
	if re.search('teststring', message_text):
		send_message('hi there', message_userid)
	elif re.search('/ipadd', message_text):
		pi_ip = requests.get('http://httpbin.org/ip').json()['origin']
		send_message(pi_ip, message_userid)
	elif re.search('remind me|message me in|text me in|.remind', message_text):
		remind_me(message_text, message_userid)


# Long polling for message updates, this is how new messages are read by the bot
def message_check():
	offset = 0
	while True:
		update_url = bot_url+'getUpdates'
		payload = {'timeout':'30','offset':offset}
		# Get the message JSON object and decode the JSON
		try:
			r = requests.get(update_url,params=payload).json()
			print(r)
		except:
			print('Error with requests')
			pass
		try:
			# Get each piece of information from the Updates
			offset = r['result'][0]['update_id'] +1
			key_list = r['result'][0]['message'].keys()
			message_userid = r['result'][0]['message']['chat']['id']
			sender_name = r['result'][0]['message']['from']['first_name']
			message_time = int(r['result'][0]['message']['date'])
			curr_time = int(time.time())

			# Response for text, and only respond if the message read was sent <10 sec ago
			if 'text' in key_list and (message_time + 10) > curr_time:
				message_text = r['result'][0]['message']['text']
				# Make the whole message lower case so I can compare strings
				message_text = message_text.lower()
				print (message_text)
				print (message_userid)
				text_check(message_text, message_userid, sender_name)

		# Bugfixing, ignore this for now
		except IndexError:
			pass
		except ValueError:
			print ("Got a ValueError")
			pass
		except KeyError:
			pass


def main():
	message_check()

main()
