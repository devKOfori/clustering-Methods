class DataPoint:
    def __init__(self, features: list):
        self.features = features
    
    def __repr__(self) -> str:
        features_str = [str(i) for i in self.features]
        return f"({", ".join(features_str)})"
    
    def __add__(self, other):
        addition_list = []
        if len(self.features) != len(other.features):
            raise Exception("The two points must have the same dimension")
        for i in range(len(self.features)):
            result = self.features[i] + other.features[i]
            addition_list.append(result)
        return addition_list
    
    def __sub__(self, other):
        substraction_list = []
        if len(self.features) != len(other.features):
            raise Exception("The two points must have the same dimension")
        for i in range(len(self.features)):
            result = self.features[i] - other.features[i]
            substraction_list.append(result)
        return substraction_list