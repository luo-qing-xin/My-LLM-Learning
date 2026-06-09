from human_eval.evaluation import evaluate_functional_correctness
import glob

if __name__ == "__main__":

    # 找到所有 samples 文件
    files = glob.glob("samples_*.jsonl")

    for file in files:
        print(f"\n开始评测: {file}")

        result = evaluate_functional_correctness(
            file,
            k=[1,10,100],
            n_workers=4
        )

        print(f"{file} 结果:")
        print(result)

'''from human_eval.evaluation import evaluate_functional_correctness

if __name__ == "__main__":
    result=evaluate_functional_correctness(
        "samples.jsonl",
        k=[1,10,100],
        n_workers=4
        )
    print(result)

    from human_eval.evaluation import evaluate_functional_correctness
import glob

if __name__ == "__main__":

    # 找到所有 samples 文件
    files = glob.glob("samples_*.jsonl")

    for file in files:
        print(f"\n开始评测: {file}")

        result = evaluate_functional_correctness(
            file,
            k=[1,10,100],
            n_workers=4
        )

        print(f"{file} 结果:")
        print(result)'''