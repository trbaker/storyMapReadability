
import json
import requests
import re

def create(request):
    syllables=0
    syllables1=0
    syllables2=0
    syllables3=0
    syllables4=0
    syllables5 = 0
    sentences=0
    words=0

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
            syllables = syllables + syllables1 + syllables2 + syllables3 + syllables4 + syllables5
            # remove common diphthongs and trailing e to improve syllable count
            trailingE = myvar.count('e ')
            #dip1 = myvar.count('ea')
            dip1 = 0    # set to zero to align better with MS Words FK results
            syllables = syllables - trailingE - dip1
            words = words + myvar.count(' ') +1
            sentences = sentences + myvar.count('.') + myvar.count('?')+ myvar.count('!') + .45  # the final constant is intended to help ofset title lines that don't contain punctuation. this number can be adjusted (prob .2 to 1.0).
            #print(syllables, words, sentences)

    # calculate fk
    fk = (.39 * (words / sentences)) + (11.8 * (syllables / words)) -15.59
    output='Title: ' + title + '<br>URL: <a target="new" href="' + publicURL + '">' + publicURL + '</a><br>Approximate Flesch-Kincaid reading grade level: ' + str(round(fk, 1))
    print(str(round(fk, 1)))

    return output