import pandas as pd
from levenshtein_distance import cer
from levenshtein_distance import wer

GT = 'GT.xlsx'
check = 'check.xlsx'

gt_data = pd.read_excel(GT)
check_data = pd.read_excel(check)
debug = 1
num = 0

def print_detail(gt_word,check_word,c_error,w_error):
    print(f"REF: {gt_word}\n"
        f"HYP: {check_word}\n"
        f"cer: {c_error}\n"
        f"wer: {w_error}\n\n")

for col in gt_data.columns: 
    gt_col = gt_data[col]
    check_col = check_data[col]
    if gt_col.size != check_col.size:
        print('size not same')
        break
    words = 0
    chars = 0
    word_error = 0
    cha_error = 0
    print(f"{col}:\n")
    for i in range(gt_col.size):
        gt_word = gt_col[i]
        check_word = check_col[i]
        if pd.isna(gt_word) and pd.isna(check_word):
            continue
        elif pd.isna(gt_word):
            c_error += len(check_word.replace(' ',''))
            w_error += len(check_word.split())
            cha_error += c_error
            word_error += w_error
            words += w_error
            chars += c_error
            if debug:
                print_detail(gt_word,check_word,c_error,w_error)
        elif pd.isna(check_word):
            cha_error += len(gt_word.replace(' ',''))
            word_error += len(gt_word.split())
            if debug:
                print_detail(gt_word,check_word,c_error,w_error)
        else:
            gt_word_list = gt_word.split()
            check_word_list = check_word.split()

            gt_word_ns = gt_word.replace(' ','')
            check_word_ns = check_word.replace(' ','')

            c_error = cer(gt_word_ns,check_word_ns)
            w_error = wer(gt_word_list,check_word_list)
            word_error += w_error
            cha_error += c_error
            words += len(gt_word_list)
            chars += len(gt_word)

            if w_error and debug:
                print_detail(gt_word,check_word,c_error,w_error)

    print(
        f"character Accuracy: {(chars-cha_error)/chars}\n"
        f"Word Accuracy: {(words-word_error)/words}\n\n"
        )
