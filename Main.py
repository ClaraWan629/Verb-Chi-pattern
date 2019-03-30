# sort the target sentences by collocation of the verb
# 2019-Feb-9
# Clara WAN

import sys
import glob
import nltk
from nltk import FreqDist

# goal: sort by post-verbal word class collocation e.g. 吃 *N

## 1. extract all the sentences that contain 吃 as a verb

### read the files under one directory
path = 'E:\\TaggedGiga_all\\*'
files = glob.glob(path)

mylist = []
for file in files:
    f = open(file, 'r', encoding='utf-8')
    text = f.readlines()
    temp_string = ""
    sent_status = 0

    for line in text:
        if line.find("<P>") >= 0:
            sent_status = 1
        elif line.find("</P>") >= 0:
            sent_status = 0
            mylist.append(temp_string)

            temp_string = ""
        elif sent_status == 1:
            temp_string += line.strip('\n')

    f.close()

#### locate 吃(V
mylist_special = []
for line in mylist:
    if line.find(" 吃(V") >= 0:
        mylist_special.append(line)

# identify the post verbal N collocation of the verb
mylist_Noun = []
mark_list = []
for line in mylist_special:
    mark = ""

    word_tag = line.split(' ')

    for i in range(len(word_tag)):

        if word_tag[i].find('吃')>=0:
            if len(word_tag) == i+1:
                mark = '吃(a'
            elif word_tag[i + 1].find('(P') >= 0 or word_tag[i + 1].find('(C')>= 0: #接标点符号
                mark = '吃(1'
            elif len(word_tag) == i + 2:
                if word_tag[i + 1].find('(N') >= 0:
                    mark = '吃' + word_tag[i + 1]

                else: mark = '吃(2'
            elif len(word_tag) == i + 3:
                if word_tag[i + 1].find('(N') >= 0:
                    mark = '吃' + word_tag[i + 1]
                elif word_tag[i + 2].find('(N') >= 0:
                    mark = '吃' + word_tag[i + 2]
                else:
                    mark = '吃(3'
            elif len(word_tag) > i + 3:
                if word_tag[i + 1].find('(N') >= 0:
                    mark = '吃' + word_tag[i + 1]
                elif word_tag[i + 2].find('(N') >= 0:
                    mark = '吃' + word_tag[i + 2]
                elif word_tag[i + 3].find('(N') >= 0:
                    mark = '吃' + word_tag[i + 3]
                else:
                    mark = '吃(0'

            else: mark = '吃' + word_tag[i + 1]
            break

    newline = mark + '\t' + ' '.join(w_t.split('(')[0] for w_t in word_tag)
    mylist_Noun.append(newline)
    '''
        if mark.find('(')== -1:
            newline = mark + '\t' + ' '.join(w_t.split('(')[0] for w_t in word_tag)
        else: newline = mark.split('(')[1] + '\t' + ' '.join(w_t.split('(')[0] for w_t in word_tag)
    '''
    mark_list.append(mark)

fd = nltk.FreqDist(line.split('(')[1] for line in mark_list)
feature_frequency = fd.most_common()


def mark(s):
    a = s.split('\t')[0]
    b = a.split('(')[1]

    return b

mynewlist = sorted(mylist_Noun, key = mark)

# write the extracted verb file to the output file
outfile = open('E:\\GigaExtractOutputFiles\\Chi_sorted_by_Post-Noun.txt', 'w', encoding='utf-8')
for sentence in mynewlist:
    outfile.write(sentence+'\n')
outfile.close()

print('The Chi_sorted_by_Post-Noun.txt file is successfully created.')

# write the frequency distribution of 2grams to the output file
outfile2 = open('E:\\GigaExtractOutputFiles\\mark_fd_chi.txt', 'w', encoding='utf-8')
for m,freq in feature_frequency:
    outfile2.write(m + '\t' + str(freq) + '\n')
outfile2.close()


print('The mark_fd_chi.txt file is successfully created.')


'''
# n-gram collocation

# read one file
f = open("D:\\GigaExtractOutputFiles\\放-shuffle400.txt", 'r', encoding='utf-8')
text = f.readlines()
f.close()

# identify the collocation-2gram of the verb fang
mylist = []
mark_list = []
for line in text:
    temp_list = []
    mark = ""

    for word in line:
        temp_list.append(word)

    for i in range(len(temp_list)):
        if temp_list[i] == '放':
            mark = '放' + temp_list[i+1]
            break

    newline = mark + '\t' + line
    mylist.append(newline)
    mark_list.append(mark)

fd = nltk.FreqDist(line for line in mark_list)
feature_frequency = fd.most_common()

def secondchar(s):
    return s[1]
mynewlist = sorted(mylist, key = secondchar)

# write the extracted verb file to the output file
outfile = open('D:\\GigaExtractOutputFiles\\Fang-sorted_shuffle400.txt', 'w', encoding='utf-8')
for sentence in mynewlist:
    outfile.write(sentence)
outfile.close()

# write the frequency distribution of 2grams to the output file
outfile2 = open('D:\\GigaExtractOutputFiles\\mark_fd_shuffle400.txt.txt', 'w', encoding='utf-8')
for m,freq in feature_frequency:
    outfile2.write(m + '\t' + str(freq) + '\n')
outfile2.close()
print('The Fang-sorted.txt file and the fd of 2 grams are created.')

'''




