from flask import Flask, request, render_template
import requests, os
from docx import Document
from werkzeug.utils import secure_filename
app = Flask(__name__)
result = ""
#Rander Home page
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        saved_filename = f.filename
        f.save(saved_filename)
        file_extension = os.path.splitext(saved_filename)[1]
        if(file_extension == ".txt"):
            try:
                with open(saved_filename, 'r', encoding='utf-8') as file:
                    combined_lines = ""
                    for line in file:
                        combined_lines += line.strip()
                    return render_template('index.html', content=combined_lines)
            except FileNotFoundError:
                return 'File not found', 404
            except Exception as e:
                return f'An error occurred: {str(e)}', 500
        if(file_extension ==".docx" or file_extension ==".doc"):
            if saved_filename:
                try:
                    document = Document(saved_filename)
                    full_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
                    return render_template('index.html', content=full_text) # Display content
                except Exception as e:
                    error_message = f"Error reading Word file: {e}"
                    return render_template("error.html", error_message=error_message)
@app.route('/translation', methods=['POST'])
def translate():
    # with open(, 'r') as file:
    #     # Initialize an empty string to store the lines
    #     combined_lines = ""
    #     for line in file:
    #         combined_lines += line.strip()
    #     text = request.form.get("text")
    #     if text == "":
    #         input = combined_lines
    #     else:
    #         input = text

    input = request.form.get("text")
    khmer = ['ក\u200b', 'ខ', 'គ', 'ឃ', 'ង', 'ច', 'ឆ', 'ជ', 'ឈ', 'ញ', 'ដ', 'ឋ', 'ឌ', 'ឍ', 'ណ', 'ត', 'ថ', 'ទ', 'ធ', 'ន', 'ប', 'ផ', 'ព', 'ភ', 'ម', 'យ', 'រ', 'ល', 'វ', 'ស', 'ហ', 'ឡ', 'អ', 'ា', 'ិ', 'ី', 'ឹ', 'ឺ', 'ុ', 'ូ', 'ួ', 'ើ', 'ឿ', 'ៀ', 'េ', 'ែ', 'ៃ', 'ោ', 'ៅ', 'ុំ', 'ំ', 'ាំ', 'ះ', 'ុះ', 'េះ', 'ោះ', 'ែះ', 'ើះ', 'ាះ', 'អ', 'អា', 'ឥ', 'ឦ', 'ឧ', 'ឩ', 'ឪ', 'ឫ', 'ឬ', 'ឭ', 'ឮ', 'ឯ', 'ឰ', 'ឱ', 'ឳ', '៉', '៊', '៍', '់', '័', '៏', '៌', 'ៈ', 'ៗ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩', '។ល។', '។', '>', '<', '?', '!', '=', '-', '៕', '...', 'a\u200b', '{\u200b\u200b', '}', '[', ']', '៖', '√', '×', 'b', 'c', 'd', 'e', 'f', '', '#']
    english = ['g', 'k', ',g', ',k', ']', 'j', '+', ',j', ',+', ',?', 'd', '-)', ',d', '0)', 'n', 't', ')', ',t', ',)', ',n', 'b', 'p', '&', ',p', 'm', ',y', 'r', ',l', 'w', 's', 'h', 'l', 'o', '*', '/', 'e', '[', '5', 'c', '3', '2', '%', 'q', '(', 'f', '<', 'i', ':', '_', '$', 'y', 'z', 'a', 'x', 'u', '!', '<a', '%a', '*a', 'o', 'o*', ',/', 'ea', 'ca', ',3', '\\', ',x', 'xa', '?', '?a', '"', 'fa', ':a', '_c', '@', '-', '0', '9', '>', "'", '7', '^', '1', 'j', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', '=,l=', '=', '$.1', '$"k', '8', '6', '.k', '-', '=,', "'''", 'v', '.(', '.)', '@(', '@)', './', '@>', '/@>', '!', 'u', 'x', '$', 'z', '' , '#']

    dictionary = dict(zip(khmer, english))
    def change_dict_key(d, old_key, new_key, default_value=None):
        d[new_key] = d.pop(old_key, default_value)

    change_dict_key(dictionary,'ក\u200b','ក')
    change_dict_key(dictionary,'a\u200b','a')
    # change_dict_key(dictionary,'១\u200b','១')
    change_dict_key(dictionary,'{\u200b\u200b','{')
    dictionary['\n'] = '\n'
    dictionary['\t'] = '\t'
    dictionary['\r'] = '\r'
    dictionary['\u200b']= ' '
    dictionary[' ']= ' '

    def convertKhToEng(b):
        convertedText = ''
        for character in b:
            if character == "្":
                character="a"
            convertedText += dictionary.get(character, 'default_value')
        return convertedText
    characterUnicodes = {'a': '\u2801', 'b': '\u2803','c': '\u2809', 'd': '\u2819', 'e': '\u2811','f': '\u280B','g': '\u281B','h': '\u2813',
                        'i': '\u280A','j': '\u281A','k': '\u2805', 'l': '\u2807','m': '\u280D', 'n': '\u281D','o': '\u2815','p': '\u280F',
                        'q': '\u281F','r': '\u2817','s': '\u280E','t': '\u281E',  'u': '\u2825', 'v': '\u2827','w': '\u283A','x': '\u282D',
                        'y': '\u283D','z': '\u2835','%':'\u2829','+':'\u282C',"=":"\u283F","'": '\u2804', ',': '\u2820', '-': '\u2824',
                        '/': '\u280C', '!' : '\u282E', '?': '\u2839', '$': '\u282B', ':': '\u2831',';': '\u2830', '(': '\u2837', ')': '\u283E',
                        ' ': '\u2800', '@':'\u2808', '>':'\u281C', '<':'\u2823', '_': '\u2838', '#': '\u283C','[':'\u282A', ']':'\u283B',
                        '"':'\u2810', '&':'\u282F','^':'\u2818','1': '\u2802', '2': '\u2806', '3': '\u2812', '4': '\u2832','5': '\u2822', '6': '\u2816',
                        '7': '\u2836', '8': '\u2826', '9': '\u2814', '0': '\u2834','.':'\u2828','*':'\u2821', '[': '\u282A', ']':'\u283B','\\':'\u2833'}
    escapeCharacters = ['\n', '\r', '\t']
    def convertText(textToConvert):
        if type(textToConvert) is not str:
            raise TypeError("Only strings can be converted")
        return convert(textToConvert)
    def convertNum(Num):
        for i in Num:
            print(i)
            return(i)

    def convert(textToConvert):
        isNumber = False
        convertedText = ''
        for character in textToConvert:
            if character in escapeCharacters:
                convertedText += character
                continue
            else:
            # if isNumber and character not in numberPunctuations:
                isNumber = False
            convertedText += characterUnicodes.get(character)
        return convertedText
    KHCONST = set(u'កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមយរលវឝឞសហឡអឣឤឥឦឧឨឩឪឫឬឭឮឯឰឱឲឳ')
    KHVOWEL = set(u'឴឵ាិីឹឺុូួើឿៀេែៃោៅ\u17c6\u17c7\u17c8')
    ENGCONST = set(u'abcdefghijklmnopqrstuvwxyz')
    # subscript, diacritics
    KHSUB = set(u'្')
    KHDIAC = set(u"\u17c9\u17ca\u17cb\u17cc\u17cd\u17ce\u17cf\u17d0") #MUUSIKATOAN, TRIISAP, BANTOC,ROBAT,
    KHSYM = set('៕។៛ៗ៚៙៘,.? ') # add space
    KHNUMBER = set(u'០១២៣៤៥៦៧៨៩0123456789') # remove 0123456789
    # lunar date:  U+19E0 to U+19FF ᧠...᧿
    KHLUNAR = set('᧠᧡᧢᧣᧤᧥᧦᧧᧨᧩᧪᧫᧬᧭᧮᧯᧰᧱᧲᧳᧴᧵᧶᧷᧸᧹᧺᧻᧼᧽᧾᧿')
    def is_khmer_char(ch):
        if ('\u0041' <= ch <= '\u007A') or ('\u1780' <= ch <= '\u17FF'): return True
        if ch in KHSYM: return True
        if ch in KHLUNAR: return True
        return False

    def is_start_of_kcc(ch):
        if is_khmer_char(ch):
            if ch in KHCONST: return True
            if ch in KHSYM: return True
            if ch in KHNUMBER: return True
            if ch in KHLUNAR: return True
            if ch in ENGCONST: return True
            return False
        return True

    # kcc base - must surround space with \u200b using cleanupstr()
    def seg_kcc(str_sentence):
        segs = []
        cur = ""
        sentence = str_sentence
        #for phr in str_sentence.split(): #no longer split by space, use 200b
        #    print("phr: '", phr,"'")
        for word in sentence.split('\u200b'):
        #print("PHR:[%s] len:%d" %(phr, len(phr)))
            for i,c in enumerate(word):
                #print(i," c:", c)
                cur += c
                nextchar = word[i+1] if (i+1 < len(word)) else ""

                # cluster non-khmer chars together
                if not is_khmer_char(c) and nextchar != " " and nextchar != "" and not is_khmer_char(nextchar):
                    continue
                # cluster number together
                if c in KHNUMBER and nextchar in KHNUMBER:
                    continue

                # cluster non-khmer together
                # non-khmer character has no cluster
                if not is_khmer_char(c) or nextchar==" " or nextchar=="":
                    segs.append(cur)
                    cur=""
                elif is_start_of_kcc(nextchar) and not (c in KHSUB):
                    segs.append(cur)
                    cur=""
                # add space back after split
                #segs.append(" ")
        return segs # [:-1] # trim last space

    # testing some text
    # text1 = []
    # text = []
    def Khmer_to_Braille(Khmer_sentence):
        KCC_Sengmentation = seg_kcc(Khmer_sentence)
        # print(KCC_Sengmentation)
        text1 = ''
        text = []
        # print the KCC segmentation
        # print(KCC_Sengmentation)
        for i in KCC_Sengmentation:
            totalWord = []
            if (i.isnumeric()):
                # print(i)
                i = "#" + i
                # print(i)
                text.append(i)
                continue
            for y in i:
                totalWord.append(y)
                lenTotalWord = len(totalWord)
            #Speacail case for Braille character and Segmentation
                word1 = ['ៃ','ែ', 'េ']
                word2 = '្'
                word3 = 'រ'
                w1 = 'ោ'
                w2 = 'ះ'
                r1 = 'ុ'
                r2 = 'ះ'
                s1 = 'េ'
                s2 = 'ះ'
                d1 = 'ំ'
                d2 = 'ុ'
                l1 = 'ា'
                l2 = 'ំ'
                if(w1 in totalWord and w2 in totalWord):
                    totalWord.remove(w2)
                    totalWord.remove(w1)
                    totalWord.insert(lenTotalWord-1, 'b')
                if(r1 in totalWord and r2 in totalWord):
                    totalWord.remove(r1)
                    totalWord.remove(r2)
                    totalWord.insert(lenTotalWord-1, 'd')
                if(s1 in totalWord and s2 in totalWord):
                    totalWord.remove(s1)
                    totalWord.remove(s2)
                    totalWord.insert(lenTotalWord-1, 'c')
                if(d1 in totalWord and d2 in totalWord):
                    totalWord.remove(d1)
                    totalWord.remove(d2)
                    totalWord.insert(lenTotalWord-1, 'e')
                if(l1 in totalWord and l2 in totalWord):
                    totalWord.remove(l1)
                    totalWord.remove(l2)
                    totalWord.insert(lenTotalWord-1, 'f')
                if(word2 in totalWord and word3 in totalWord):
                    # print(totalWord)
                    totalWord.remove(word2)
                    totalWord.remove(word3)
                    totalWord.insert(0, word2)
                    totalWord.insert(1, word3)
                for n in word1:
                    if(n in totalWord):
                    # print(totalWord)
                        totalWord.remove(n)
                        totalWord.insert(0, n)
                    elif(word2 in totalWord and word3 in totalWord and n in totalWord):
                    # print(totalWord)
                        totalWord.remove(n)
                        totalWord.remove(word2)
                        totalWord.remove(word3)
                        totalWord.insert(0, n)
                        totalWord.insert(1, word2)
                        totalWord.insert(2, word3)
                    else:
                        continue
            #Get all KCC segmentation of sentence store in array
            # print(totalWord)
            text.append(totalWord)
            # print(totalWord)
        for n in text:
            # print(n)
            for j in n:
            #Convert each element of array to braille character and print it out
                braille = convertText(convertKhToEng(j))
                text1+=braille
                print(j)
                print(braille)
                # braille
        print(text1)
        return (text1)
    # print(Khmer_to_Braille("ហេតុការណ៍អគ្គិភ័យនេះកើតឡើងនាយប់ថ្ងៃទី១ ខែមករា ឆ្នាំ២០២៤ បណ្ដាលមកពីភ្លើងចង្រ្កាន នៅចំណុចភូមិខ្មែរ ឃុំងន ស្រុកសណ្ដាន់ ខេត្តកំពង់ធំ នារសៀលថ្ងៃទី២ ខែមករា ឆ្នាំ២០២៤។ "))
    
    b = (Khmer_to_Braille(input))
    return render_template('index.html', result = b, input = input)

if __name__ == '__main__':
    app.run(debug=True)
