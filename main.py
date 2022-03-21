from translator import Translator
from glob import glob

t = Translator()


def prepare_line(line):
    for sep in ['. //', '? //', '! //', './/', '?//', '!//']:
        line = line.replace(sep, sep[0] + '\n\n')
    for sep in ['. /', '? /', '! /', './', '?/', '!/']:
        line = line.replace(sep, sep[0] + '\n')
    line = line.replace('/', ' ')
    return line


def translate_file(path):
    global t

    result = ''
    lines = open(path).read().split('\n')[:-1]
    lines = {l.split('\t')[0]: l.split('\t')[1] for l in lines}
    text = [prepare_line(lines[l]) for l in lines if lines[l] != '']
    translation = t.chain_translate(text, runs=3)
    i = 0
    for line in lines:
        result += line + '\t'
        if lines[line] != '':
            result += translation[i]
            i += 1
        result += '\n'
    open(path.replace('original', 'translated'), 'w', encoding="utf-8").write(result)


files_to_translate = glob('original/**/*.tsv', recursive=True)
for file in files_to_translate:
    translate_file(file)
    print(f'File {file} translated!')

