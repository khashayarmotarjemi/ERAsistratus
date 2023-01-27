import wikipedia
import re
from nltk.tokenize import word_tokenize
import wikipediaapi
import keyword, difflib

low = 0
high = 2030
span_min = 25
span_max = 100


def getWikiText(keyword):

    wiki_wiki = wikipediaapi.Wikipedia('en')

    page_py = wiki_wiki.page(keyword)

    if(page_py.exists()):
        return page_py.text, page_py.title
    else:
        matches = wikipedia.search(keyword)
        print(matches)
        close_matches = difflib.get_close_matches(keyword, matches)
        print(close_matches)
        if(keyword in close_matches): close_matches.remove(keyword)
        new_page = wiki_wiki.page(close_matches[0])
        return new_page.text, new_page.title


def isBC(words,num): 
    nIndex = words.index(num)
    next_words = words[nIndex:nIndex+8]
    lower_words = [x.lower() for x in next_words]
    return any(x in lower_words for x in ['bc', 'b.c.', 'bce', 'b.c.e.', 'b.c'])
        

def isYear(number):
    return number > low and number < high

def isBirth(pair):
    p0 = int(pair[0])
    p1 = int(pair[1])
    p_span = max(p0, p1) - min(p0, p1)
    return isYear(p0) and isYear(p1) and (p_span < span_max and p_span > span_min)

def yearFinder(text):
    head = text[0:300]
   
    # bad bad bad bad
    head = head.replace('-', ' ')
    head = head.replace('–', ' ')
    head = head.replace('/', ' ')
    head = head.replace('|', ' ')

    # print(head)

    head_tk = word_tokenize(head)

    numbers = re.findall(r'\d+',head)
    # print(numbers)
    print(numbers)

    pairs = [(a, b) for idx, a in enumerate(numbers) for b in numbers[idx + 1:]]
    good_pairs = []
    for p in pairs:
        if(isBirth(p)) :
            good_pairs.append(p)

    if(not good_pairs):
        if(not numbers):
            return "Sorry, couldn't find any numbers in this"
        else:
            print("got here")
            return f'{numbers[0]} {"B.C." if (isBC(head_tk,numbers[0])) else ""}'
    else:    
        first = good_pairs[0]
        
        # print(head_tk)
        
        min_year = min(int(first[0]),int(first[1]))
        max_year = max(int(first[0]),int(first[1]))

        return f'{min_year}-{max_year} {"B.C." if (isBC(head_tk,first[0]) or isBC(head_tk,first[1])) else ""}'


    # if(not numbers):
    #     return "Sorry, couldn't find any numbers in this"
    # elif(len(numbers) == 1):
    #     print("got here")
    #     return f'{numbers[0]} {"B.C." if (isBC(head_tk,numbers[0])) else ""}'
    # else: 
      
    # isBC(head_tk,first)

def getYearByKeyword(word):
    return yearFinder(getWikiText(word))
    
# text = yearFinder(getWikiText("Pythagoras"))
# print(text)
# pt = wikipedia.page("Socrates")
# print(pt.content)
# gp = yearFinder("George Washington (February 22, 1732[b] – December 14, 1799) was an American military officer, statesman, and Founding Father who served as the first president of the United States from 1789 to 1797. Appointed by the Continental Congress as commander of the Continental Army, Washington led Patriot forces to victory in the American Revolutionary War and served as president of the Constitutional Convention of 1787, which created and ratified the Constitution of the United States and the American federal government. Washington has been called the Father of his Country for his ")
# print(gp)
# print(yearFinder(pt.content))