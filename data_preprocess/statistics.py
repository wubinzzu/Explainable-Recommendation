# Usage: python statistics.py data-dir

import sys
import os
import json

def get_statistics(file):
    user_dict = {}
    product_dict = {}
    reviews_count = 0;
    with open(file) as data_file:
        for line in data_file:
            reviews_count += 1
            json_data = json.loads(line)
            user_id = json_data["reviewerID"]
            product_id = json_data["asin"]
            if user_id not in user_dict:
                user_dict[user_id] = 0
            if product_id not in product_dict:
                product_dict[product_id] = 0

    print "%-20s   %-10d    %-10d    %-10d    %-10f" %(os.path.basename(file), len(user_dict), len(product_dict), reviews_count, (reviews_count/len(user_dict)))



if len(sys.argv) < 2:
    sys.exit('Usage: %s data-dir' % sys.argv[0])
data_dir = sys.argv[1]

files = os.listdir(data_dir)
print "%-20s   %-10s    %-10s    %-10s    %-10s" %("Dataset", "#users", "#items", "#reviews", "#reviews/#users")
for file in files:
    if os.path.splitext(file)[1] == '.json':
        get_statistics(os.path.join(data_dir, file))
