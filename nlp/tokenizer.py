import nltk
from nltk.tokenize import word_tokenize

CACHE_DIR = '.nltk-data/'

nltk.download('punkt', download_dir=CACHE_DIR)

class Tokenizer:
    def __init__(self):
        self.tokenize = word_tokenize
