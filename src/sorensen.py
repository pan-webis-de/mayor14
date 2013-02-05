def sorensen(vec1,vec2,**args):

    d1d2 =  len([ item  for item in vec1 if item in vec2 ])
  
  
    if len(vec1) + len(vec2) == 0:
        return 0.0
  
  
    return float(2.0*d1d2 / (len(vec1) + len(vec2) ) )
  
