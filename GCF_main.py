
import json
import requests
import re
import ast

def create(request):
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

    try:
        storymap = request.args.get('url')
        URL2="https://www.arcgis.com/sharing/rest/content/items/" + storymap + "/data"
        publicURL="https://storymaps.arcgis.com/stories/" + storymap
        # get storymap json
        resp = requests.get(URL2)
        mytext = resp.content
    except:
        return 'url or request error'

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

    # calculate fk
    fk = (.39 * (words / sentences)) + (11.8 * (syllables / words)) -15.59
    final_fk = round(fk, 1)
    with open('lexile.txt') as f:
        data = f.read()
        lexiledata = ast.literal_eval(data)
    for key in lexiledata:
        if str(key) == str(final_fk):
            lexileoutput='<br>Estimated Lexile reading score: ' + str(lexiledata[key]) + 'L'
    output='Title: ' + title + '<br>URL: <a target="new" href="' + publicURL + '">' + publicURL + '</a><br>Approximate Flesch-Kincaid reading grade level: ' + str(round(fk, 1)) + lexileoutput
    #print(str(round(fk, 1)))
    sentences = 0
    words = 0
    syllables = 0
    return output