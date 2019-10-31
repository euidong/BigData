# Copyright 2013 University of Washington eScience Institute
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import json
class MapReduce:
    def __init__(self):
        self.intermediate = {}
        self.result = []
    def emit_intermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)
    def emit(self, value):
        self.result.append(value) 
    def execute(self, data, mapper, reducer):
        for line in data:
            record = json.loads(line)
            mapper(record)
        for key in self.intermediate:
            reducer(key, self.intermediate[key])
        #jenc = json.JSONEncoder(encoding='latin-1')
        jenc = json.JSONEncoder()
        for item in self.result:
            print(jenc.encode(item))