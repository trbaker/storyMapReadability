import requests
import json
import pprint
import re
import ast

# vars
syllables=0
syllables1=0
syllables2=0
syllables3=0
syllables4=0
syllables5 = 0
sentences=0
words=0
wordcounterr1=0
wordcounterr2=0
wordcounterr3=0

storymaplist=['d51f8ab5d4b84a8d8208a369fad5f520', '0a718288bcb44cbe9f5cf439179b719d','12ba699e36d549daa5f0f27a63c2ebe0','445fdebc91e9409bb5f88fbf74801d75','c47ed912c6f44cb0adc35cb17115f1e9']

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
            syllables6 = myvar.count('y')
            syllables = syllables + syllables1 + syllables2 + syllables3 + syllables4 + syllables5 + syllables6
            # remove common diphthongs and trailing e to improve syllable count
            trailingE = myvar.count('e ')
            dipthongs = ['ae', 'ai', 'au', 'ay', 'ea', 'ee', 'ei', 'ey' 'ie', 'oa', 'oo', 'ou', 'ey', 'oy', 'uy']
            # dipthongs = ['ou', 'oy', 'oi']
            diptotal=0
            dip=0
            for dip in dipthongs:
                temp = myvar.count(dip)
                diptotal = diptotal + temp
            syllables = syllables - trailingE - diptotal
            words = words + myvar.count(' ') + 1  # the added 1 accounts for the last word in each block.
            # clean up some word count issues
            wordcounterr1 = myvar.count(' - ')
            wordcounterr2 = myvar.count('0 ')   # number w trailing space should keep from counting single or multi digits numbers
            wordcounterr3 = myvar.count('1 ')
            wordcounterr4 = myvar.count('2 ')
            wordcounterr5 = myvar.count('3 ')
            wordcounterr6 = myvar.count('4 ')
            wordcounterr7 = myvar.count('5 ')
            words = words - wordcounterr1 - wordcounterr2 - wordcounterr3 - wordcounterr4 - wordcounterr5 - wordcounterr6 - wordcounterr7
            sentences = sentences + myvar.count('.') + myvar.count('?') + myvar.count('!') - myvar.count('.0') - myvar.count('http') * 3 - myvar.count('...') * 3       # using a 2 multiplier to account for the multiple periods and potential question mark in a URL
            # print(syllables, words, sentences)
            #print(myvar)

    print(syllables, words, sentences)
    # calculate fk
    print('Title: ' + title)
    print('URL: ' + publicURL)
    fk = (.39 * (words / sentences)) + (11.8 * (syllables / words)) -15.59
    # estimate Lexile Reader Measure
    # table: http://www.evers.cps.edu/What%20is%20A%20Lexile%20and%20How%20Does%20it%20Compare%20to%20My%20RIT%20Score.html
    # table: https://www.lexialearning.com/blog/more-number-what-is-lexile-measure
    final_fk = round(fk, 1)
    with open('lexile.txt') as f:
        data = f.read()
        lexiledata = ast.literal_eval(data)
    for key in lexiledata:
        if str(key) == str(final_fk):
            print('Lexile-approximate: ' + str(lexiledata[key]-10) + 'L - ' + str(lexiledata[key]+10) + 'L')
    print('Flesch-Kincaid grade level score: ', final_fk)
    print('  ')
    #rest for next pass
    sentences = 0
    words = 0
    syllables = 0