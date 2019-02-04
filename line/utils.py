from janome.tokenizer import Tokenizer


def morphological_analysis(text):
    T = Tokenizer()
    tokens = T.tokenize(text)
    list = []
    for i in range(len(tokens)):
        word = tokens[i].base_form
        part_of_speech = tokens[i].part_of_speech.split(',')[0]
        list.append(f'{word} {part_of_speech}')
    return list


if __name__ == '__main__':
    text = '今日はいい天気です'
    result = morphological_analysis(text)
    response = ''
    for item in result:
        response += item + '\n'
    print(response)