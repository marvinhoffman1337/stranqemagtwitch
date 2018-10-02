
import requests
import re
import socket
import json
import argparse

# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = "#0_123456789"                               # Channelname = #{Nickname}
NICK = "0_123456789"                         # Nickname = Twitch username
PASS = "oauth:k8f5t0x7a5r0r31nxmofremszmkya4"   # www.twitchapps.com/tmi/ will help to retrieve the required authkey
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))

def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
	if len(msg) >= 1:
		msg = msg.split(' ')
con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
stream_count = 0
for number in range(1, 250):
	response = requests.get('https://api.twitch.tv/kraken/streams?client_id=6arow4uftfxfu50giby5wx15l0r1x2&stream_type=live&offset='+str(number)+"00")
	parsed_json = json.loads(response.text)
	for j in parsed_json['streams']:
		name = str(j["channel"]["name"])
		display_name = str(j["channel"]["display_name"])
		status = str(j["channel"]["status"])
		followers = str(j["channel"]["followers"])
		if len(j["channel"]["name"]) >= 1:
			stream_count += 1
			print(str(stream_count)+" | "+display_name+" | "+followers+" | "+status)
			join_channel("#"+name)
		else:
			pass
data = ""

while True:
    try:
        data = data+con.recv(1024).decode('UTF-8', errors='ignore')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
