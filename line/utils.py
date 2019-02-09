from janome.tokenizer import Tokenizer


def morphological_analysis(text):
    T = Tokenizer()
    tokens = T.tokenize(text.replace('\n', ''))
    list = []
    for i in range(len(tokens)):
        word = tokens[i].base_form
        part_of_speech = tokens[i].part_of_speech.split(',')[0]
        list.append(f'{word} {part_of_speech}')
    return list


def list_to_string_with_line_feed(list):
    string = ''
    for item in list:
        string += item + '\n'
    string = string.rstrip('\n')
    return string


if __name__ == '__main__':
    text = '今日はいい天気です'
    print(list_to_string_with_line_feed(morphological_analysis(text)))
    '''
    今日 名詞
    は 助詞
    いい 形容詞
    天気 名詞
    です 助動詞
    '''
