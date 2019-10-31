import MapReduce
import sys
mr = MapReduce.MapReduce()
# =============================
# Do not modify above this line
def mapper(record):
    # TODO: implement this class
    mr.emit_intermediate(record[1], record)
def reducer(key, list_of_values):
    # TODO: implement this class
    if key == '32':
        mr.emit(list_of_values)
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)