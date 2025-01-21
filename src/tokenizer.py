import regex as re
class Tokenizer:
    def __init__(self, verbose=0):
        self.max_token = 255
        self.verbose = verbose
        self.vocabulary = {i : chr(i) for i in range(256)}
        self.tokens = None
        self.words = None
        self.GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
    
    #! Bug in encode: if tokenizer hasn't been traiend yet
    #! and you try to encode text, it breaks
    
    #! Optimize encoder, for now it takes more than a minute to encode 
    #! the text once, but in reality we'll have to do it many times each training
    #! Possible sollutions:
    #! 1. Do not encode each epoch and only update the saved version
    #! 1.1 maybe keep a list of indexes to recreate words out of merged tokens 

    #TODO: Rewrite all funcs in tokenizer to work with 
    #TODO: word chunks instead of independent utf-8 bytes
    def get_stats(self, text=None):
        if text:
            text = re.findall(self.GPT4_SPLIT_PATTERN, text)
            self.words = tuple(tuple(map(int, word.encode('utf-8'))) for word in text)
            # self.words = tuple(self.encode(word) for word in text)
            # self.tokens = list(int(token) for token in text.encode('utf-8'))
        
        pairs = {}
        max_pair = None
        max_pair_value = 0
        for word in self.words:
            if len(word) < 2:
                continue
            for i in range(len(word)-1):
                pair = (word[i], word[i+1])
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
        self.vocabulary[self.max_token] = self.vocabulary[pair[0]] + self.vocabulary[pair[1]]
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

        if self.words is None:
            text = re.findall(self.GPT4_SPLIT_PATTERN, text)
            self.words = tuple(tuple(map(int, word.encode('utf-8'))) for word in text)
            # self.words = tuple(self.encode(word) for word in text)

        if self.verbose==1:
            len_before = len(self.tokens)
            vocab_size_before = self.max_token + 1
            print('-'*100, f'length before: {len_before}, vocab size before: {vocab_size_before}', sep='\n')

        for _ in range(merges):
            pair = self.get_stats()
            self.merge(pair)
            # self.words = tuple(self.encode(word) for word in text)
        
        if self.verbose==1:
            len_after = len(self.tokens)
            vocab_size_after = self.max_token + 1
            print('-'*20,(f'length after: {len_after}, vocab size after: {vocab_size_after},\n' 
                  f'length decrease: {len_before-len_after}, vocab size increase: {vocab_size_after - vocab_size_before}\n'
                  f'length decrease: {len_before/len_after:.2f}x, ' 
                  f'vocab size increase: {vocab_size_after/vocab_size_before:.2f}x'), sep='\n')

        return self.tokens
    
    def decode(self, tokens:list[int]):
        output = ''
        for token in tokens:
            output+= self.vocabulary[token]
        
        return output
    
    def encode(self, text:str):
        vocabulary = self.vocabulary.copy()
        vocabulary = dict(list(vocabulary.items())[::-1])
        text_bytes = bytes(text.encode('utf-8'))
        tokens = []
        i = 0
        while i<len(text_bytes):
            for token, translation in vocabulary.items():
                if text_bytes[i:].startswith(bytes(translation.encode('utf-8'))):
                    tokens.append(token)
                    i+=len(translation)
                    break
            else:
                raise ValueError(f"Couldn't find a translation for {text[i:]} \nCurrent vocab: {self.vocabulary}")
        return tokens
                
# Tests

if __name__ == '__main__':
    # text = open('src/data/unicode_diverse.txt').read()
    
    # tokenizer = Tokenizer(verbose=1)
    # tokens = tokenizer.train(text, 700)

    # print(tokenizer.decode(tokens))
    
    text = open('src/data/TinyShakespeare.txt').read()
    tokenizer = Tokenizer(verbose=1)
    # pair = tokenizer.get_stats(text)
    # merged_tokens = tokenizer.merge(pair, text)
    # print(merged_tokens[:100])
    # tokens = tokenizer.train(text, 1)
    tokens = tokenizer.encode(text)
    print(tokens)
    print(tokenizer.decode(tokens))
    # print(tokenizer.decode(tokens)[:1000])
    # print(tokenizer.encode(text[:1000]))

