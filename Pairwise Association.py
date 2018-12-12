#creates file to be read
def on_vocareum():
    import os
    return os.path.exists('.voc')

def download(file, local_dir="", url_base=None, checksum=None):
    import os, requests, hashlib, io
    local_file = "{}{}".format(local_dir, file)
    if not os.path.exists(local_file):
        if url_base is None:
            url_base = "https://cse6040.gatech.edu/datasets/"
        url = "{}{}".format(url_base, file)
        print("Downloading: {} ...".format(url))
        r = requests.get(url)
        with open(local_file, 'wb') as f:
            f.write(r.content)            
    if checksum is not None:
        with io.open(local_file, 'rb') as f:
            body = f.read()
            body_checksum = hashlib.md5(body).hexdigest()
            assert body_checksum == checksum, \
                "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_file,
                                                                                           body_checksum,
                                                                                           checksum)
    print("'{}' is ready!".format(file))


# seprates different sets  
def get_lists (s):
    assert type (s) is str
    return s.split('\n')

def make_itemsets(lists):
    item_set = set()
    return [food_list for food_list in lists if food_list not in item_set]


# update dicts
from collections import defaultdict
from itertools import permutations

def update_pair_counts (pair_counts, itemset):
    assert type (pair_counts) is defaultdict
    for pair in permutations(itemset.split(','), 2):
        pair_counts[pair] += 1
        
def update_item_counts(item_counts, itemset):
    for item in itemset.split(','):
        item_counts[item] += 1


def filter_rules (pair_counts, item_counts, threshold, min_count):
    rules = {} # (item_a, item_b) -> conf (item_a => item_b)
    for pair, count in pair_counts.items():
        item_count = item_counts[pair[0]]
        check = count/item_count
        
        if item_count >= min_count and check >= threshold:
            rules[pair] = check
   
    return rules 

def find_assoc_rules_min(receipts, threshold, min_count):
    pair_counts, item_counts = defaultdict(lambda: 0), defaultdict(lambda: 0)
    for r in receipts:
        update_pair_counts(pair_counts, r)
        update_item_counts(item_counts, r)
    
    return filter_rules(pair_counts, item_counts, threshold, min_count)



def main():
    if on_vocareum():
        DATA_PATH = "../resource/asnlib/publicdata/"
    else:
        DATA_PATH = ""
    datasets = {'groceries.csv': '0a3d21c692be5c8ce55c93e59543dcbe'}

    for filename, checksum in datasets.items():
        download(filename, local_dir=DATA_PATH, checksum=checksum)

    with open('{}{}'.format(DATA_PATH, 'groceries.csv')) as fp:
        groceries_file = fp.read()
    print (groceries_file[0:250] + "...\n... (etc.) ...") # Prints the first 250 characters only
    print("\n(All data appears to be ready.)")

    # Confidence threshold
    THRESHOLD = 0.5
    # Only consider rules for items appearing at least `MIN_COUNT` times.
    MIN_COUNT = 10
    grocery_itemset = make_itemsets(get_lists(groceries_file))
    basket_rules = find_assoc_rules_min(grocery_itemset, THRESHOLD, MIN_COUNT)
        
    print("Found {} rules whose confidence exceeds {}.".format(len(basket_rules), THRESHOLD))
    print("Here they are:\n")
    print(basket_rules)



main()