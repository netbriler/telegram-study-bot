import os
import re

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class ProfanityFilter(object):
    def __init__(self, clean_word='*'):
        self.bad_words = set(line.strip('\n') for line in open(
            os.path.join(__location__, 'bad_words.txt'), encoding='utf-8'))
        self.censor_char = clean_word

    """
    Replaces a bad word in a string with something more PG friendly
    """

    def censor(self, string):
        exp = '(\W|^)(%s)(\W|$)' % '|'.join(self.bad_words)
        r = re.compile(exp, re.IGNORECASE)

        return r.sub(lambda text: self._censor_char(text), string)

    """
    Return True if string line without profanity
    """

    def is_clean(self, string):
        exp = '(\W|^)(%s)(\W|$)' % '|'.join(self.bad_words)
        r = re.compile(exp, re.IGNORECASE)
        return not r.search(string)

    """
    Return True if string with profanity
    """

    def is_profane(self, string):
        exp = '(\W|^)(%s)(\W|$)' % '|'.join(self.bad_words)
        r = re.compile(exp, re.IGNORECASE)
        return r.search(string)

    """
    Replace word with censored characters
    """

    def _censor_char(self, text):
        return len(text.group(0)) * self.censor_char
