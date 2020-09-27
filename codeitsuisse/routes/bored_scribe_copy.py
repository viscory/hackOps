import logging
import json
from wordsegment import load, segment

from flask import request, jsonify;

from codeitsuisse import app;
import wordninja

from random import randrange
import string
import math

logger = logging.getLogger(__name__)

class CaesarCipher(object):
    def __init__(self, message=None, encode=False, decode=False, offset=False,
                 crack=None, verbose=None, alphabet=None):
        """
        A class that encodes, decodes and cracks strings using the Caesar shift
        cipher.
        Accepts messages in a string and encodes or decodes by shifting the
        value of the letter by an arbitrary integer to a different letter in
        the alphabet provided.
        http://en.wikipedia.org/wiki/Caesar_cipher
        Do not ever use this for real communication, but definitely use it for
        fun events like the Hacker Olympics.
        Attributes:
            message: The string you wish to encode.
            encode: A boolean indicating desire to encode the string, used as
                command line script flag.
            decoded: A boolean indicating desire to decode the string, used as
                command line script flag.
            cracked: A boolean indicating to desire to crack the string, used
                as command line script flag.
            verbose: A boolean indicating the desire to turn on debug output,
                use as command line script flag.
            offset: Integer by which you want to shift the value of a letter.
            alphabet: A tuple containing the ASCII alphabet in uppercase.
        Examples:
            Encode a string with a random letter offset.
            >>> cipher = CaesarCipher('I want to encode this string.')
            >>> cipher.encoded
            'W kobh hc sbqcrs hvwg ghfwbu.'
            Encode a string with a specific letter offset.
            >>> cipher = CaesarCipher('I want to encode this string.',
            ...     offset=14)
            >>> cipher.encoded
            'W kobh hc sbqcrs hvwg ghfwbu.'
            Decode a string with a specific letter offset.
            >>> cipher = CaesarCipher('W kobh hc sbqcrs hvwg ghfwbu.',
            ...    offset=14)
            >>> cipher.decoded
            'I want to encode this string.'
            Crack a string of ciphertext without knowing the letter offset.
            >>> cipher = CaesarCipher('W kobh hc sbqcrs hvwg ghfwbu.')
            >>> cipher.cracked
            'I want to encode this string.'
        """
        self.message = message
        self.encode = encode
        self.decode = decode
        self.offset = offset
        self.verbose = verbose
        self.crack = crack
        self.alphabet = alphabet

        # Frequency of letters used in English, taken from Wikipedia.
        # http://en.wikipedia.org/wiki/Letter_frequency
        self.frequency = {
            'a': 0.08167,
            'b': 0.01492,
            'c': 0.02782,
            'd': 0.04253,
            'e': 0.130001,
            'f': 0.02228,
            'g': 0.02015,
            'h': 0.06094,
            'i': 0.06966,
            'j': 0.00153,
            'k': 0.00772,
            'l': 0.04025,
            'm': 0.02406,
            'n': 0.06749,
            'o': 0.07507,
            'p': 0.01929,
            'q': 0.00095,
            'r': 0.05987,
            's': 0.06327,
            't': 0.09056,
            'u': 0.02758,
            'v': 0.00978,
            'w': 0.02360,
            'x': 0.00150,
            'y': 0.01974,
            'z': 0.00074}

        # Get ASCII alphabet if one is not provided by the user.
        if alphabet is None:
            self.alphabet = tuple(string.ascii_lowercase)

    def cipher(self):
        """Applies the Caesar shift cipher.
        Based on the attributes of the object, applies the Caesar shift cipher
        to the message attribute. Accepts positive and negative integers as
        offsets.
        Required attributes:
            message
            offset
        Returns:
            String with cipher applied.
        """
        # If no offset is selected, pick random one with sufficient distance
        # from original.
        if self.offset is False:
            self.offset = randrange(5, 25)

        # Cipher
        ciphered_message_list = list(self.message)
        for i, letter in enumerate(ciphered_message_list):
            if letter.isalpha():
                # Use default upper and lower case characters if alphabet
                # not supplied by user.
                if letter.isupper():
                    alphabet = [character.upper()
                                for character in self.alphabet]
                else:
                    alphabet = self.alphabet

                value = alphabet.index(letter)
                cipher_value = value + self.offset
                if cipher_value > 25 or cipher_value < 0:
                    cipher_value = cipher_value % 26
                ciphered_message_list[i] = alphabet[cipher_value]
        self.message = ''.join(ciphered_message_list)
        return self.message

    def calculate_entropy(self, entropy_string):
        """Calculates the entropy of a string based on known frequency of
        English letters.
        Args:
            entropy_string: A str representing the string to calculate.
        Returns:
            A negative float with the total entropy of the string (higher
            is better).
        """
        total = 0
        for char in entropy_string:
            if char.isalpha():
                prob = self.frequency[char.lower()]
                total += - math.log(prob) / math.log(2)
        return total

    @property
    def cracked(self):
        """Attempts to crack ciphertext using frequency of letters in English.
        Returns:
            String of most likely message.
        """
        entropy_values = {}
        attempt_cache = {}
        message = self.message
        for i in range(25):
            self.message = message
            self.offset = i * -1
            test_cipher = self.cipher()
            entropy_values[i] = self.calculate_entropy(test_cipher)
            attempt_cache[i] = test_cipher

        sorted_by_entropy = sorted(entropy_values, key=entropy_values.get)
        self.offset = sorted_by_entropy[0] * -1
        cracked_text = attempt_cache[sorted_by_entropy[0]]
        self.message = cracked_text


        return cracked_text

    @property
    def encoded(self):
        """Encodes message using Caesar shift cipher
        Returns:
            String encoded with cipher.
        """
        return self.cipher()

    @property
    def decoded(self):
        """Decodes message using Caesar shift cipher
        Inverse operation of encoding, applies negative offset to Caesar shift
        cipher.
        Returns:
            String decoded with cipher.
        """
        self.offset = self.offset * -1
        return self.cipher()

def solve(data):
    res = []
    load()
    for dic in data:
        ans = {}
        i,s = dic['id'],dic['encryptedText']
        ans['id']=i
        cip = CaesarCipher(s)
        ori = cip.cracked
        nn,cnt,l,ind = 0,0,0,0
        for x in range(len(s)-1):
            for y in range(x+1,len(s)):
                tmp=ori[x:y+1]
                cur=y-x+1
                if tmp==tmp[::-1]:
                    if cur>l:
                        ind,l=x,cur
                    nn+=1
        has=[]
        for c in ori[ind:ind+l]:
            has.append(ord(c))
        ans['encryptionCount'] = 0
        tar=ord(s[0])
        cnt=ord(ori[0])
        #dont know why
        if l==0:
            for t in range(100):
                if cnt==tar:
                    ans['encryptionCount'] = t
                    break
                cnt+=cnt
                if cnt>122:
                    cnt=(cnt-123)%26+97
        else:
            for t in range(100):
                if cnt==tar:
                    ans['encryptionCount'] = t
                    break
                tmp=sum(has)+nn
                for i in range(len(has)):
                    has[i]+=tmp
                    if has[i]>122:
                        has[i]=(has[i]-123)%26+97
                cnt+=tmp
                if cnt>122:
                    cnt=(cnt-123)%26+97
        #s=' '.join(wordninja.split(ori))
        s = ' '.join(segment(ori))
        tmp = s.split(' ')
        s=tmp[0]
        for i in range(1,len(tmp)):
            if tmp[i]=='s' or tmp[i]=='i' and tmp[i-1]=='a':
                s+=tmp[i]
            else:
                s+=' '+tmp[i]

        '''
        p=0
        if 'palindrome' in tmp:
            if 'is' in tmp:
                iss=tmp.index('is')
                if tmp.index('palindrome')>iss:
                    for i in range(iss):
                        ttmp=''.join(tmp[i:iss])
                        if ttmp==ttmp[::-1]:
                            s=''
                            if i!=0:
                                s=' '.join(tmp[:i])+' '
                            s+=ttmp+' '+' '.join(tmp[iss:])
                            break
        '''
        ans['originalText'] = s
        res.append(ans)
    return res
@app.route('/bored-scribe', methods=['POST'])
def bored_scribe():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result=solve(data)
    logging.info("My result :{}".format(result))
    return jsonify(result);
'''
data=[ { "id": 1, "encryptedText": "bbdef" } ]
print(solve(data))
'''
