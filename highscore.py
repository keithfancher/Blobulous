import pickle


class HighScoreTable:
    """Use Pickle to read/write scores to a file"""

    max_length = 10 # 10 top scores max
    file_name = "highscore.dat"
    scores = [] # a list of tuples (name, score)

    def __init__(self):
        self.clear()

    def add_score(self, name, score): # TODO: add date?
        """adds score to table and re-sorts"""
        self.scores.append((name, score));
        self.sort()

    def read_from_file(self):
        pass

    def write_to_file(self):
        pass

    def sort(self):
        """sort by high score, descending"""
        self.scores = sorted(self.scores, key=lambda score: score[1],
                             reverse=True)

    def print_scores(self):
        """just print to console"""
        print self.scores

    def clear(self):
        """empty the high score table"""
        self.scores = []

    def is_empty(self):
        if not self.scores:
            return True
        else:
            return False
