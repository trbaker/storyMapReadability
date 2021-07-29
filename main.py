import requests
import json
import pprint
import re

# vars
syllables=0
syllables1=0
syllables2=0
syllables3=0
syllables4=0
syllables5 = 0
sentences=0
words=0

storymaplist=['d51f8ab5d4b84a8d8208a369fad5f520', '0a718288bcb44cbe9f5cf439179b719d','12ba699e36d549daa5f0f27a63c2ebe0']

for i in range(0, len(storymaplist)):
    storymap=storymaplist[i]
    URL2="https://www.arcgis.com/sharing/rest/content/items/" + storymap + "/data"
    publicURL="https://storymaps.arcgis.com/stories/" + storymap

    # get storymap json
    resp = requests.get(URL2)
    mytext = resp.content

    # pprint.pprint(jtext)

    # convert json to python dictionary
    jtext = json.loads(mytext)

    # loop over nodes and check for data-text
    for i, entry in enumerate(jtext['nodes']):
        try:
            summary = jtext['nodes'][entry]["data"]["summary"]
            if len(summary) != 0:
                title = jtext['nodes'][entry]["data"]["title"]
        except:
            dummyload=1

        try:
            myvar = jtext['nodes'][entry]["data"]["text"]
        except:
            myvar=''

        myvar=re.sub('<[^<]+?>', '', myvar)
        # output to screen for testing
        #print(myvar)
        if len(myvar) != 0:
            syllables1 = myvar.count('a')
            syllables2 = myvar.count('e')
            syllables3 = myvar.count('i')
            syllables4 = myvar.count('o')
            syllables5 = myvar.count('u')
            syllables = syllables + syllables1 + syllables2 + syllables3 + syllables4 + syllables5
            # remove common diphthongs and trailing e to improve syllable count
            trailingE = myvar.count('e ')
            #dip1 = myvar.count('ea')
            dip1 = 0    # set to zero to align better with MS Words FK results
            syllables = syllables - trailingE - dip1
            words = words + myvar.count(' ') +1
            sentences = sentences + myvar.count('.') +1
            #print(syllables, words, sentences)

    # calculate fk
    fk = (.39 * (words / sentences)) + (11.8 * (syllables / words)) -15.59
    print('Title: ' + title)
    print('URL: ' + publicURL)
    print('Approximate Flesch-Kincaid reading grade level: ', round(fk, 1))
    print('  ')
