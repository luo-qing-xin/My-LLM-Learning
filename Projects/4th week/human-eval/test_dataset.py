#这是一个调试脚本，用来验证数据集是否正确加载，以及查看问题的格式和内容。
from human_eval.data import read_problems

problems = read_problems()

print(len(problems))

for task_id, problem in list(problems.items())[:1]:
    print(task_id)
    print(problem["prompt"])