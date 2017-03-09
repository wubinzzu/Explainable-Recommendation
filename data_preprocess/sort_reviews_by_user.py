# Usage: Run in console with arguments of data dir and output dir.

import sys
import os
import json

def processCategory(file, outputDir):
    dict = {}
    with open(file) as data_file:
        for line in data_file:
            json_data = json.loads(line)
            userID = json_data["reviewerID"]
            if userID not in dict:
                dict[userID] = []
            dict[userID].append(json_data)
        for k, v in dict.items():
            v = sorted(v, key=lambda k: k['unixReviewTime'], reverse=True)
            filename = os.path.join(outputDir, k + '.json')
            with open(filename, 'a') as file:
                for jsonRecord in v:
                    file.write(json.dumps(jsonRecord) + '\n')




if len(sys.argv) < 3:
    sys.exit('Usage: %s data-dir output-dir' % sys.argv[0])
outputPath = sys.argv[2]
dataDir = sys.argv[1]



files = os.listdir(dataDir)
for file in files:
    if os.path.splitext(file)[1] == '.json':
        outputDir = os.path.join(outputPath, os.path.splitext(file)[0])
        isExists = os.path.exists(outputDir)
        if not isExists:
            os.makedirs(outputDir)
        processCategory(os.path.join(dataDir, file), outputDir)

