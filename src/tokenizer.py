class Tokenizer:
    def __init__(self):
        self.max_token = 255
        self.tokens = []

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

    # @staticmethod
    # def print_info(func):
    #     def wrapper(self, *args, **kwargs):
    #         print(f"Vocabulary before: {self.vocabulary}")
    #         print(f"Length before: {len(self.int_tokens)}")
    #         result = func(self, *args, **kwargs)
    #         print(f"Vocabulary after: {self.vocabulary}")
    #         print(f"Length after: {len(self.int_tokens)}")
    #         return result
    #     return wrapper

    # @print_info

    def merge(self, pair, text=None):
        if text:
            self.tokens = list(int(token) for token in text.encode('utf-8'))
        merged_tokens = []
        i = 0

        while i < len(self.tokens) - 1:
            
            if pair == (self.tokens[i], self.tokens[i+1]):
                self.max_token+=1    
                merged_tokens.append(self.max_token)
                i+=2
            else:
                merged_tokens.append(self.tokens[i])
                i+=1
        self.tokens = merged_tokens
        return merged_tokens

    def train(self, text:str, merges:int):
        self.tokens = list(int(token) for token in text.encode('utf-8'))
        for _ in range(len(merges)):
            pair = self.get_stats()    
            self.merge(pair)    
        
        return self.tokens

tokenizer = Tokenizer()
tokenizer.get_stats(text)