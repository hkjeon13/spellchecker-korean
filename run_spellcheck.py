import os
import ast
import logging
import argparse
import requests
from tqdm import tqdm
from itertools import chain
from functools import partial
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count


parser = argparse.ArgumentParser()

parser.add_argument('--input_dir', default=None, metavar='DIRECTORY', required=True, help='path for the directory of '
                                                                                          'inputs.')
parser.add_argument('--output_dir', default=None, metavar='DIRECTORY', required=True, help='path for the directory of '
                                                                                           'outputs.')

parser.add_argument('--prefix', default='corrected_', metavar='DIRECTORY', help='flag for distinguishing the '
                                                                                     'outputs.' )

parser.add_argument('--num_cores', type=int, default=None, metavar='N',help='the number of cpu cores.')

parser.add_argument('--delimiter', default='\n', metavar='delimiter', help='delimiter for splitting the text in the '
                                                                           'input file.')


def text_concatenating(corpus, max_seq_len=490, sep_flag='[SEP]'):
    concated_corpus = ['']
    for c in corpus:
        c = c.strip()
        if len(concated_corpus[-1])+len(c)+len(sep_flag) > max_seq_len:
            concated_corpus.append(c)
        else:
            concated_corpus[-1]+=(sep_flag+c)
    return concated_corpus, sep_flag


def spell_check(content, req):
    try:
        base_url= 'https://m.search.naver.com/p/csearch/ocontent/spellchecker.nhn'
        header = {
            'referer': 'https://search.naver.com/',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/57.0.2987.133 Safari/537.36 '
            }
        payload = {
            '_callback':'window.__jindo2_callback._spellingCheck_0', 'q': content}
        original_text = req.get(base_url, params=payload, headers = header).text
        corrected = correct(original_text)['html']
        return corrected
    except Exception as e:
        logging.info(e)
        return content


def correct(content):
    _from = content.index('(')+1
    _to = len(content) - (content[::-1].index(')')) - 1
    result = ast.literal_eval(content[_from:_to])['message']['result']
    new_data = {}
    for key, value in result.items():
        if type(value)==str:
            value = BeautifulSoup(value, "lxml").text
        new_data[key] = value
    return new_data


def run_imap_multiprocessing(func, argument_list, num_processes):

    pool = Pool(processes=num_processes)

    result_list_tqdm = []
    for result in tqdm(pool.imap(func=func, iterable=argument_list), total=len(argument_list)):
        result_list_tqdm.append(result)

    return result_list_tqdm


def load_text(path, return_lines=True, deli='\n'):
    with open(path, 'r', encoding='utf-8') as r:
        content = r.read()
    if return_lines:
        return content.split(deli)
    return content


def save_text(path, content):
    with open(path, 'w', encoding='utf-8') as w:
        w.write(content)
    logging.info(f"Successfully saved in {path}")


if __name__=='__main__':
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    num_cores = args.num_cores if args.num_cores else cpu_count()
    logging.info(f'the number of cpu cores: {num_cores}')
    input_files = [os.path.join(args.input_dir, f) for f in os.listdir(args.input_dir)]
    input_lines = [load_text(inp, return_lines=True, deli=args.delimiter) for inp in input_files]

    for lines, fpath in zip(input_lines, input_files):
        logging.info(f'[input_file]:{fpath}')
        req = requests.Session()
        concated_texts, sep_flag = text_concatenating(lines)
        spell_chk = partial(spell_check, req=req)
        concated_texts = run_imap_multiprocessing(spell_chk, concated_texts, num_cores)
        concated_texts = list(chain(*[c.split(sep_flag) for c in concated_texts if isinstance(c, str)]))
        concated_texts = [c.strip() for c in concated_texts]
        path_out = os.path.join(args.output_dir, args.prefix+os.path.basename(fpath))
        save_contents =args.delimiter.join(concated_texts)
        save_text(path_out, save_contents)