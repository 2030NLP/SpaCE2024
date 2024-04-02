# !/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import json
import traceback

tgt_format = ['A', 'B', 'C', 'D']

# 计算准确率
def acc_count(correct, total):
    return correct / total


def main(params):
    answers = {}
    with open(params['answer_path'], 'r', encoding='utf-8') as fin:
        for line in fin:
            js = json.loads(line)
            answers[js['qid']] = js

    predictions = {}
    with open(params['prediction_path'], 'r', encoding='utf-8') as fin:
        for line in fin:
            js = json.loads(line)
            if ('qid' in js):
                predictions[js['qid']] = js

    # single指答案唯一的单选题，multiple指答案不唯一的多选题
    single_correct, multiple_correct, single_num, multiple_num = 0, 0, 0, 0
    for qid in answers:
        x = answers[qid]
        x_gold = set(g.strip() for g in x['answer'] if g.strip() in tgt_format)
        multiple_trigger = False
        if len(x_gold) == 1:
            single_num += 1
        else:
            multiple_num += 1
            multiple_trigger = True
        if qid in predictions:
            y = predictions[qid]
            y_predict = set()
            if not isinstance(y['answer'], list):
                print(f"{qid}的答案格式必须是一个列表，请检查!")
                continue
            for p in y['answer']:
                p = p.strip()
                if p not in tgt_format:
                    print(f"{qid}的答案形式可能不规范，请检查!")
                y_predict.add(p)
            if x_gold == y_predict:
                if not multiple_trigger:
                    single_correct += 1
                else:
                    multiple_correct += 1

    # 单选题数量和多选题数量之和=所有题目的数量
    correct = single_correct + multiple_correct
    total = single_num + multiple_num
    status = 'Accepted'

    total_score = acc_count(correct, total)
    single_score = acc_count(single_correct, single_num)
    multiple_score = acc_count(multiple_correct, multiple_num)

    # total_Accuracy是所有题目的准确率，single_Accuracy是单选题的准确率，multiple_Accuracy是多选题的准确率
    print(status)
    print('total_Accuracy: %d/%d = %f' % (correct, total, total_score))
    print('single_Accuracy: %d/%d = %f' % (single_correct, single_num, single_score))
    print('multiple_Accuracy: %d/%d = %f' % (multiple_correct, multiple_num, multiple_score))

    # total_Accuracy是赛事的排名指标，single_Accuracy和multiple_Accuracy不作为赛事的排名依据！
    final_result = {
        'correct': correct,
        'total': total,
        'accuracy': total_score,
    }

    return status, final_result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # data paths
    parser.add_argument('--answer_path', type=str, default='../data/gold.jsonl')
    parser.add_argument('--prediction_path', type=str, default='../output/prediction.jsonl')

    args = parser.parse_args()
    params = args.__dict__
    print(params)

    try:
        status, final_result = main(params)
        print(json.dumps(final_result, indent=2))
    except:
        traceback.print_exc()
        status, final_result = 'Error in execution', None