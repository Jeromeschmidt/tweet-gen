import random
import re
from dictogram import Dictogram
import string

class MarkovChain(Dictogram):
    def __init__(self, word_list):
        super().__init__()
        self.start_tokens = Dictogram()
        self.stop_tokens = Dictogram()

        word_list[0] = re.sub("[^a-zA-Z]", '', word_list[0])
        self.start_tokens.add_count(word_list[0].lower(), 1)

        for i in range(1, len(word_list)-1, 1):
            if((word_list[i][0].isupper()) and word_list[i-1][len(word_list[i-1])-1] in string.punctuation):
                word_list[i] = re.sub("[^a-zA-Z]", '', word_list[i])
                self.start_tokens.add_count(word_list[i].lower(), 1)
        for i in range(len(word_list)):
            if(word_list[i][len(word_list[i])-1] in string.punctuation):
                word_list[i] = re.sub("[^a-zA-Z]", '', word_list[i])
                # word_list[i] = word_list[i][:len(word_list[i])-1]
                self.stop_tokens.add_count(word_list[i], 1)
        for i in range(len(word_list)-1):
            word_list[i] = re.sub("[^a-zA-Z]", '', word_list[i])
            word_list[i+1] = re.sub("[^a-zA-Z]", '', word_list[i+1])
            if word_list[i] in self:
                self[word_list[i].lower()].add_count(word_list[i+1].lower(), 1)
            else:
                self[word_list[i].lower()] = Dictogram([word_list[i+1].lower()])

    def random_walk(self, length=10):
        sentence = ""
        keys = list(self.keys())
        word = self.start_word()
        sentence += word + " "
        word = word.lower()
        for i in range(length-1):
            word = self[word].sample()
            sentence += word + " "
        sentence = sentence + self.end_word() + ". "
        return sentence

    def start_word(self):
        dart = random.randint(0, len(self.start_tokens)+1)
        fence = 0
        for elm in self.start_tokens:
            for key in self.start_tokens.keys():
                fence += self.start_tokens[key]
                if fence > dart:
                    return elm.capitalize()

    def end_word(self):
        dart = random.randint(0, len(self.stop_tokens)+1)
        fence = 0
        while 1:
            for elm in self.stop_tokens:
                for key in self.stop_tokens.keys():
                    fence += self.stop_tokens[key]
                    if fence >= dart:
                        return elm

if __name__ == '__main__':
    words = "One fish blue fish. Red fish blue fish."
    word_list = words.split()
    print(word_list)
    # word_list = ["Blue", "One.", "fish.", "One", "two","blue", "fish", "two", "red", "fish", "blue", "red", "blue", "fish", "red", "blue", "fish"]
    markovChain = MarkovChain(word_list)
    # print(markovChain)
    print(markovChain.random_walk(20))
