## **eval_latest.py**
评分文件，指标采用accuracy。
**all_accuracy是赛事的唯一排名指标**，是所有题目的准确率。
<br>
以下指标均不作为赛事的排名依据：
- 单选题_accuracy是答案唯一类题目的准确率；
- 多选题_accuracy是多个答案类题目的准确率；
- 实体识别_accuracy是实体识别类题目的准确率； # 新增
- 角色识别_accuracy是角色识别类题目的准确率； # 新增
- 异常识别_accuracy是异常识别类题目的准确率； # 新增
- 空间推理_accuracy是空间推理类题目的准确率； # 新增
- 同义识别_accuracy是同义识别类题目的准确率； # 新增

【参数说明】
--answer_path 后为答案的文件路径。
--prediction_path 后为预测结果的文件路径。

【报错预警】
#### xxx的答案格式必须是一个列表，请检查!
答案和预测结果均采用列表装填答案。评分前请对预测结果做预处理。

#### xxx的答案形式可能不规范，请检查!
答案和预测结果均采用字母形式，仅支持'A', 'B', 'C', 'D'四个字母。评分前请对预测结果做预处理。