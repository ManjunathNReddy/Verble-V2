# Create verb files to be used by the game

import json
from operator import itemgetter
from constants import CORPUS_VERBS, FREQUENT_VERBS, VERBLE_CORPUS, VERBLE_FREQUENT, NUM_LETTERS

verb_list = []
with open(CORPUS_VERBS, "r") as all_verbs:
    # Filter out verbs that are not of the specified length or contain dashes or apostrophes 
    verb_list = filter(
        lambda v: len(v) == NUM_LETTERS and '-' not in v and "'" not in v,
        map(str.strip, all_verbs)
    )
    verb_list = list(verb_list)

# Save the list to txt file
with open(VERBLE_CORPUS, "w") as verbs_file:
    verbs_file.write('\n'.join(verb_list))

freq_verbs = {}
with open(FREQUENT_VERBS, "r") as frequent_verbs:
    freq_verbs = json.load(frequent_verbs)

# Get common words
common_words = list(set(freq_verbs.keys()) & set(verb_list))

# Save top 500 common words sorted by frequencies to a file
common_word_dict = dict((k, freq_verbs[k]) for k in common_words if k in freq_verbs)
common_word_dict = dict(sorted(common_word_dict.items(), key=itemgetter(1), reverse=True)[:500])

with open(VERBLE_FREQUENT, "w") as common_words_file:
    json.dump(common_word_dict, common_words_file)
