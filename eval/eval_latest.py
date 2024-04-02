# !/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import json
import traceback

tgt_format = ['A', 'B', 'C', 'D']
category_name = {'1': '实体识别',
                 '2': '角色识别',
                 '3': '异常识别',
                 '4': '空间推理',
                 '5': '同义识别',
                 's': '单选题',
                 'm': '多选题'}

# 计算准确率
def acc_count(category):
    for k, v in category.items():
        correct, total = v
        name = category_name[k]
        try:
            score = correct / total
            print(name+'_Accuracy: %d/%d = %f' % (correct, total, score))
        except:
            print(name+'_Accuracy: %d/%d = %f' % (correct, total, 0))


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

    # 1指实体识别任务，2指角色识别任务，3指异常识别任务，4指空间推理任务，5指同义识别任务
    task_category = {str(i): [0, 0] for i in range(1, 6)}
    # s指答案唯一的单选题，m指答案不唯一的多选题
    answer_category = {'s': [0, 0], 'm': [0, 0]}
    correct, total = 0, 0
    for qid in answers:
        x = answers[qid]
        task_id, _, anum_id, _ = qid.split('-')
        x_gold = set(g.strip() for g in x['answer'] if g.strip() in tgt_format)
        task_category[task_id][1] += 1
        answer_category[anum_id][1] += 1
        total += 1
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
                task_category[task_id][0] += 1
                answer_category[anum_id][0] += 1
                correct += 1

    status = 'Accepted'
    total_score = correct / total
    print('\n【整体得分】')
    print('all_Accuracy: %d/%d = %f' % (correct, total, total_score))
    print('-'*35)
    print('【能力得分】')
    acc_count(task_category)
    print('-'*35)
    print('【题型得分】')
    acc_count(answer_category)
    print('-'*35)

    # all_Accuracy是赛事的排名指标，其他Accuracy不作为赛事的排名依据！
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