class Tokenizer:
    def __init__(self, verbose=0):
        self.max_token = 255
        self.verbose = verbose
        self.tokens = None

    def get_stats(self, text=None):
        if text:
            self.tokens = list(int(token) for token in text.encode('utf-8'))
        
        pairs = {}
        max_pair = None
        max_pair_value = 0

        for i in range(len(self.tokens)-1):
            pair = (self.tokens[i], self.tokens[i+1])
            pair_value = pairs.get(pair, 0) + 1
            pairs[pair] = pair_value

            # Keeping track of the most frequently occurring pair
            if pair_value > max_pair_value:
                max_pair = pair
                max_pair_value = pair_value
        
        return max_pair

    def merge(self, pair, text=None):
        if text:
            self.tokens = list(int(token) for token in text.encode('utf-8'))
        merged_tokens = []
        i = 0
        self.max_token+=1
        
        while i < len(self.tokens) - 1:
            
            if pair == (self.tokens[i], self.tokens[i+1]):   
                merged_tokens.append(self.max_token)
                i+=2
            else:
                merged_tokens.append(self.tokens[i])
                i+=1
        self.tokens = merged_tokens
        return merged_tokens

    def train(self, text:str, merges:int):
        if self.tokens is None:
            self.tokens = list(int(token) for token in text.encode('utf-8'))
        
        if self.verbose==1:
            len_before = len(self.tokens)
            vocab_size_before = self.max_token + 1
            print('-'*100, f'length before: {len_before}, vocab size before: {vocab_size_before}', sep='\n')

        for _ in range(merges):
            pair = self.get_stats()
            self.merge(pair)
        
        if self.verbose==1:
            len_after = len(self.tokens)
            vocab_size_after = self.max_token + 1
            print('-'*20,(f'length after: {len_after}, vocab size after: {vocab_size_after},\n' 
                  f'length decrease: {len_before-len_after}, vocab size increase: {vocab_size_after - vocab_size_before}\n'
                  f'length decrease: {len_before/len_after:.2f}x, ' 
                  f'vocab size increase: {vocab_size_after/vocab_size_before:.2f}x'), sep='\n')

        return self.tokens

# Tests

if __name__ == '__main__':
    text = open('src/data/unicode_diverse.txt').read()
    
    tokenizer = Tokenizer(verbose=1)
    tokenizer.train(text, 100)
    
    text = open('src/data/TinyShakespeare.txt').read()
    tokenizer = Tokenizer(verbose=1)
    tokenizer.train(text, 200)
