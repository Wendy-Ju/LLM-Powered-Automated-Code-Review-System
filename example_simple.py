def avg(x):
 y = sum(x)/len(x)
 return y

def outlier(data):
  #calculate standard deviation
  import statistics
  stdev = statistics.stdev(data)
  mean = avg(data)
  for i in data:
    if i > mean + 2 * stdev:
     print(i)
