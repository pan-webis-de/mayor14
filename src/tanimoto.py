def tanimoto(vec1,vec2,**args):
    
    d1d2 = [item for item in vec1 if item in vec2]
  
    if len(d1d2)  == 0: return 0.0
  
    return float(len(d1d2))/ (len(vec1) + len(vec2) - len(d1d2))
