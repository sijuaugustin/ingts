import numpy as np
import pickle

class NPNormalizer():

    def __init__(self):
        self.v_min = None
        self.v_max = None
    
    def fit(self, vector):
        vector = np.asanyarray(vector, dtype="double")
        self.v_min = vector.min(axis=0)
        self.v_max = vector.max(axis=0)
        return self
 
    def transform(self, vector):
        vector = np.asanyarray(vector, dtype="double")
        return (vector - self.v_min)/(self.v_max - self.v_min)
        
    def denormalize(self, vector):
        return vector*(self.v_max - self.v_min) + self.v_min
        
    def save(self, target_path):
        pickle.dump(self, open(target_path,"w"))
    
    @staticmethod    
    def load(source_path):
        return pickle.load(open(source_path))
        
if __name__ == "__main__":
    
    x = np.array([[1000,  10,   0.5],
                  [ 765,   5,  0.35],
                  [ 800,   7,  0.09]])

    normalizer = NPNormalizer()
    normalizer.fit(x)
    normalizer.save("normalizer.model")
    x_normed = NPNormalizer.load("normalizer.model").transform(x)
    print(x_normed)
