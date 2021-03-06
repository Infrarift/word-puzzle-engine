class Bucket:

    MAX_WORDS = 10  # Beyond this and the score will suffer.

    def __init__(self, key):
        self.key = key
        self.count = len(key)
        self.words = []
        self.hidden_words = []
        self.sub_buckets = []
        self.active = True
        self.tier_scores = [0] * 10
        self.word_counts = [0] * 10

    def n_min_score(self, n_min=0):

        penalty = 0

        excess = self.word_counts[n_min] - self.MAX_WORDS
        if excess > 0:
            penalty = int(2 ** (len(self.key) - 2) * excess * 1.5)

        # Hack: If no non-hidden words, penalize the score heavily.
        if len(self.words) == 0:
            penalty += 50

        return self.tier_scores[n_min] - penalty

    def sort_score(self, n_min=0):
        key_score = 10 * len(self.key)
        return key_score + len(self.get_word_values(n_min))

    def add_word(self, word):
        self.words.append(word)
        self._add_word_score(word)

    def add_hidden_word(self, word):
        self.hidden_words.append(word)

    def add_sub_bucket(self, sub_bucket):
        if sub_bucket not in self.sub_buckets:
            self.sub_buckets.append(sub_bucket)
            for word in sub_bucket.words:
                self._add_word_score(word)

    def _add_word_score(self, word):
        n_letters = len(word.literal)
        score = 2 ** (n_letters - 2)

        # Add a cumulative score for each tier.
        for i in range(0, n_letters + 1):
            self.tier_scores[i] += score
            self.word_counts[i] += 1

    def get_word_values(self, n_min=0):
        out_words = []
        for s_bucket in self.sub_buckets:
            if n_min == 0 or len(s_bucket.key) >= n_min:
                for word in s_bucket.words:
                    out_words.append(word.literal)

        for word in self.words:
            out_words.append(word.literal)

        out_words.sort(key=lambda item: (len(item), item))
        return out_words

    def get_hidden_word_values(self, n_min=0):
        out_words = []
        for s_bucket in self.sub_buckets:
            if n_min == 0 or len(s_bucket.key) >= n_min:
                for word in s_bucket.hidden_words:
                    out_words.append(word.literal)

        for word in self.hidden_words:
            out_words.append(word.literal)

        out_words.sort(key=lambda item: (len(item), item))
        return out_words

    def reset(self):
        self.active = True

