import MapReduce
import sys
mr = MapReduce.MapReduce()
# =============================
# Do not modify above this line
def mapper(record):
    # TODO: implement this class
    if (record[0] == 'a'):
        for i in range(5):
           mr.emit_intermediate((record[1],i), record)
    else:
        for i in range(5):
            mr.emit_intermediate((i,record[2]), record)

    
def reducer(key, list_of_values):
    # TODO: implement this class
    result = 0
    a_array = [0,0,0,0,0]
    b_array = [0,0,0,0,0]
    for value in list_of_values:
        if value[0] == 'a':
            a_array[value[2]] += value[3]
        else :
            b_array[value[1]] += value[3]
    for i in range(5):
        result += a_array[i] * b_array[i]
    mr.emit([key[0], key[1], result])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)