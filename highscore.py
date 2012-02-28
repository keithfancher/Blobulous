import pickle


class HighScoreTable:
    """Use Pickle to read/write scores to a file"""

    max_length = 5 # 5 top scores max
    file_name = "highscore.pkl"
    scores = [] # a list of tuples (name, score)

    def __init__(self):
        self.clear()

    def add_score(self, name, score): # TODO: add date?
        """adds score to table and re-sorts"""
        # if score is lower than lowest score and table is full, don't bother
        if self.query(score):
            self.scores.append((name, score));
            self.sort()
            # if we ever add more than one score at a time, this will have to be
            # changed to accomodate that
            if len(self.scores) > self.max_length:
                del self.scores[self.max_length]

    def read_from_file(self):
        """if the file exists, read from it; if it doesn't exist, just init an
        empty table"""
        # if the file doesn't exist, clear the table and return
        try:
            score_file = open(self.file_name, 'rb')
        except IOError as e:
            self.clear()
            return

        # otherwise load the data and close the file
        self.scores = pickle.load(score_file)
        score_file.close()

    def write_to_file(self):
        """dump high scores to file using pickle module"""
        if self.scores:
            # TODO: error checking, etc.
            score_file = open(self.file_name, 'wb')
            pickle.dump(self.scores, score_file)
            score_file.close()

    def sort(self):
        """sort by high score, descending"""
        self.scores = sorted(self.scores, key=lambda score: score[1],
                             reverse=True)

    def query(self, score):
        """returns true if given score is high enough to get in the table"""
        # empty table means any score is good enough
        if self.is_empty():
            return True
        # non-full table means any score is good enough
        elif len(self.scores) < self.max_length:
            return True
        # score is greater than lowest score (if there's a tie the one already
        # in the table has precedence)
        elif score > self.scores[-1][1]:
            return True
        # no good!
        else:
            return False

    def get_table_with_names(self):
        pass

    def get_table_without_names(self):
        """returns a string of the high score table with just the scores, not
        assicated with names"""
        return "Testing\nfuck\nyou"

    def clear(self):
        """empty the high score table"""
        self.scores = []

    def is_empty(self):
        if not self.scores:
            return True
        else:
            return False
