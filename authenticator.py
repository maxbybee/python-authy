import time
import hmac
import base64
import struct
import hashlib
import os
import json
import re
import curses
from curses import wrapper

# Generate an OTP using the HMAC-based One-Time Password algorithm (HOTP)
def generate_hotp(secret, counter, digits=6):
    key = base64.b32decode(secret, True)
    msg = struct.pack('>Q', counter)
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    o = hmac_hash[19] & 15
    token = (struct.unpack('>I', hmac_hash[o:o+4])[0] & 0x7fffffff) % 10**digits
    return str(token).zfill(digits)

# Generate a TOTP using the Time-Based One-Time Password algorithm (TOTP)
def generate_totp(secret, interval=30, digits=6):
    counter = int(time.time()) // interval
    return generate_hotp(secret, counter, digits)

# Save secrets to a file
def save_secrets(secrets):
    with open('secrets.json', 'w') as f:
        json.dump(secrets, f)

# Load secrets from a file
def load_secrets():
    if os.path.exists('secrets.json'):
        with open('secrets.json', 'r') as f:
            return json.load(f)
    return []

# Normalize secret format
def normalize_secret(secret):
    pattern = r'^(\w{4} ){7}\w{4}$'
    if re.match(pattern, secret):
        return secret.replace(' ', '')
    return secret

# Class to manage the 2FA authenticator
class Authenticator:
    def __init__(self):
        self.codes = load_secrets()

    def add_code(self, secret, nickname):
        normalized_secret = normalize_secret(secret)
        self.codes.append({'secret': normalized_secret, 'nickname': nickname})
        save_secrets(self.codes)

    def delete_code(self, index):
        if 0 <= index < len(self.codes):
            del self.codes[index]
            save_secrets(self.codes)

    def move_code(self, old_index, new_index, new_nickname):
        if 0 <= old_index < len(self.codes) and 0 <= new_index < len(self.codes):
            if new_nickname:
                self.codes[old_index]['nickname'] = new_nickname
            self.codes.insert(new_index, self.codes.pop(old_index))
            save_secrets(self.codes)

    def display_codes(self, stdscr):
        stdscr.clear()
        for i, code in enumerate(self.codes):
            nickname = code.get('nickname', 'Unnamed')
            stdscr.addstr(i, 0, f"{i}. Nickname: {nickname}, TOTP: {generate_totp(code['secret'])}")
        stdscr.refresh()

    def run(self, stdscr):
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True)  # Set getch() to be non-blocking
        while True:
            self.display_codes(stdscr)
            stdscr.addstr(len(self.codes) + 1, 0, "\nOptions:")
            stdscr.addstr(len(self.codes) + 2, 0, "1. Add code")
            stdscr.addstr(len(self.codes) + 3, 0, "2. Delete code")
            stdscr.addstr(len(self.codes) + 4, 0, "3. Move code")
            stdscr.addstr(len(self.codes) + 5, 0, "4. Exit")
            stdscr.addstr(len(self.codes) + 6, 0, "Choose an option: ")

            stdscr.refresh()
            choice = stdscr.getch()

            if choice == ord('1'):
                stdscr.clear()
                stdscr.addstr(0, 0, "Enter the base32 encoded secret: ")
                curses.echo()
                secret = stdscr.getstr(1, 0).decode('utf-8')
                stdscr.addstr(2, 0, "Enter a nickname for this code: ")
                nickname = stdscr.getstr(3, 0).decode('utf-8')
                curses.noecho()
                self.add_code(secret, nickname)
            elif choice == ord('2'):
                stdscr.clear()
                stdscr.addstr(0, 0, "Enter the index of the code to delete: ")
                curses.echo()
                index = int(stdscr.getstr(1, 0).decode('utf-8'))
                curses.noecho()
                self.delete_code(index)
            elif choice == ord('3'):
                stdscr.clear()
                stdscr.addstr(0, 0, "Enter the index of the code to move: ")
                curses.echo()
                old_index = int(stdscr.getstr(1, 0).decode('utf-8'))
                stdscr.addstr(2, 0, "Enter the new index: ")
                new_index = int(stdscr.getstr(3, 0).decode('utf-8'))
                stdscr.addstr(4, 0, "Enter a new nickname for this code (press Enter to keep the current nickname): ")
                new_nickname = stdscr.getstr(5, 0).decode('utf-8')
                curses.noecho()
                self.move_code(old_index, new_index, new_nickname)
            elif choice == ord('4'):
                break
            time.sleep(0.1)  # Sleep briefly to avoid excessive CPU usage

def main(stdscr):
    authenticator = Authenticator()
    authenticator.run(stdscr)

if __name__ == "__main__":
    wrapper(main)
