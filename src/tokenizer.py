class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.max_token = 256
        self.byte_tokens, self.int_tokens, self.vocabulary = self.get_vocab(text)

    def get_vocab(self, text):
        toks_b = []
        toks_i = []
        dictionary = {}
        
        for c in text:
            tok_b = c.encode("utf-8")
            tok_i = tuple(int(byte) for byte in tok_b)

            if len(tok_i) > 1:
                self.max_token += 1
                tok_i = self.max_token
            else:
                tok_i = tok_i[0]
            
            if tok_i not in dictionary:
                dictionary[tok_i] = tok_b

            toks_b.append(tok_b)
            toks_i.append(tok_i)
        
        return toks_b, toks_i, dictionary

    def byte_pair_step_get(self):
        sequences = {}
        pairs_found = set()

        for i, token in enumerate(self.int_tokens):
            if token not in sequences:
                sequences[token] = [i]
            else:
                sequences[token].append(i)

        print(sequences)

        for token, ids in sequences.items():
            if len(ids) <= 1:
                continue

            pairs = {}
            pair_found = False

            for i in ids:
                if i + 1 == len(self.int_tokens):
                    continue

                pair = (self.int_tokens[i], self.int_tokens[i + 1])
                if pair in pairs:
                    pairs[pair] += 1
                    pair_found = True
                else:
                    pairs[pair] = 1

            if pair_found:
                best_pair = sorted(pairs.items(), key=lambda x: x[1], reverse=True)[0]
                pairs_found.add(best_pair)

        if pairs_found:
            pairs_found = sorted(list(pairs_found), key=lambda x: x[-1], reverse=True)
            return pairs_found
        else:
            return None

    @staticmethod
    def print_info(func):
        def wrapper(self, *args, **kwargs):
            print(f"Vocabulary before: {self.vocabulary}")
            print(f"Length before: {len(self.int_tokens)}")
            result = func(self, *args, **kwargs)
            print(f"Vocabulary after: {self.vocabulary}")
            print(f"Length after: {len(self.int_tokens)}")
            return result
        return wrapper

    @print_info
    def byte_pair_step_set(self, pairs_found):
        pairs_found = [x[0] for x in pairs_found]
        pair_to_token = {}

        for pair in pairs_found:
            self.max_token += 1
            pair_to_token[pair] = self.max_token
        
        new_tokens = []
        i = 0

        while i < len(self.int_tokens):
            if i < len(self.int_tokens) - 1:
                tok1 = self.int_tokens[i]
                tok2 = self.int_tokens[i + 1]
                translation = pair_to_token.get((tok1, tok2))
                if translation is not None:
                    new_tokens.append(translation)
                    self.vocabulary[translation] = (
                        self.vocabulary[tok1] + self.vocabulary[tok2]
                    )
                    i += 2
                    continue

            new_tokens.append(self.int_tokens[i])
            i += 1

        self.int_tokens = new_tokens
        self.byte_tokens = [self.vocabulary[t] for t in self.int_tokens]

        return new_tokens

    def byte_pair_tokenization(self):
        pairs_found = True
        while pairs_found:
            pairs_found = self.byte_pair_step_get()
            prev_len = len(self.int_tokens)

            if pairs_found:
                self.byte_pair_step_set(pairs_found)
            
            if len(self.int_tokens) == prev_len:
                break

tokenizer = Tokenizer(big_text)
tokenizer.byte_pair_tokenization()