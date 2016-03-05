import re
Chin ={'di':"\u7b2c",    # ordinal
        'hui':"\u56de",   # chapter
       'period':"\u3002", 
       'question':"\?\uff1f",
       'exclamation':"!\uff01",
       'beginquote':"\u300c",
       'endquote':"\u300d",
       'space':"\u3000",
       'interpunct':"\u00b7",
       'comma':",\uff0c",
       'open_title_caret':"\u300a",   #《
       'close_title_caret':"\u300b",   #》
       'circle_empty':'\u25ef',
       'circle_top_filled':'\u25d3',
       'circle_bot_filled':'\u25d2',
       'circle_filled':'\u25cf'
       }
Chin['quote']=Chin['beginquote']+Chin['endquote']
Chin['end']=Chin['period']+Chin['exclamation']+Chin['question']
Chin['spaces']=Chin['space']+"\x20"
Chin['punctuation']=Chin['end']+Chin['comma']
Chin['tones']={'A':Chin['circle_empty'],'B':Chin['circle_top_filled'],'C':Chin['circle_bot_filled'],'D':Chin['circle_filled']}
Chin['scansion'] = ["◎","○","●","⊙"]
Numbers=["\u96f6","\u4e00","\u4e8c","\u4e09","\u56db","\u4e94","\u516d","\u4e03","\u516b","\u4e5d","\u5341"] # 0 1 2 3 4 5 6 7 8 9 10
NumberRegex="[{0}]".format(''.join(Numbers))
PunctRegex="[{0}]".format(''.join(Chin['punctuation']))
NonNumber = re.compile("[^%s]"%(''.join(Numbers)))

def FillTones(S):
    return ''.join([Chin['tones'][x] if x in "ABCD" else x for x in S])

def RomToChin(Num):
    num = int(Num)
    if num % 10 == 0 and num > 10:
        result = Numbers[int(num/10)]+Numbers[10]
    elif num > 10:
        result = RomToChin(Num[0]+'0')+Numbers[int(Num[1])]
    else:
        result = Numbers[num]
    return result

def ChiNumToInt(ChiNum):
    ChiNum = list(ChiNum)
    num = 0
    if ChiNum[0] == "\u5341":     # workaround for allowed absence of "yi1" for nums between 10 and 20 ex "shi2jiu3" not "yi1shi2jiu3"
        ChiNum.insert(0,"\u4e00")
    while ChiNum:
        a = Numbers.index(ChiNum.pop(0))
        b = Numbers.index(ChiNum.pop(0)) if len(ChiNum) > 0 else 0
        num += a*b if b > 0 else a
    return(num)

def ChiBookSort(ChiNumList):
    # sort based on list of Chinese-style book ordinals. Get rid of characters like \u7b2c \u56de \u5377, calculate the integer value\n",
    # if it is supplemental volume i.e. contains \"\u88dc\" separate into separate list, perform same sort and append to primary list \n",
    Main = {}
    Supplement = {}
    for x in ChiNumList:
        if x.find("\u88dc") > -1:    # bu3 meaning supplemental.  put them at the end of the list
            Supplement[x] = ChiNumToInt(NonNumber.sub("",x))
        else:
            Main[x] = ChiNumToInt(NonNumber.sub("",x))
    return sorted(Main,key=lambda x:Main[x])+sorted(Supplement,key=lambda y:Supplement[y])

def FindTone(Char,Dataset):
    tones = []
    for buf in Dataset.created_content(">{0}</a>".format(Char),ReturnList=True):
        Tone = re.search('span class="comment">(.)声<',-buf,re.DOTALL|re.MULTILINE).group(1)
        tones += Tone if Tone not in tones else [] 
    if len(tones) > 0:
        final = "{0}".format(tones[0]) if len(tones) == 1 else "({0})".format("|".join(tones))
        return final
    return Char

