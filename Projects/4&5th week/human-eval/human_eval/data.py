#这个代码是 HumanEval 数据集的读写工具模块，
# 提供了读取和写入 JSONL 格式数据的函数。它支持处理 gzip 压缩的文件，并且可以将数据以字典的形式返回，方便后续使用。
from typing import Iterable, Dict
import gzip
import json
import os


ROOT = os.path.dirname(os.path.abspath(__file__))
HUMAN_EVAL = os.path.join(ROOT, "..", "data", "HumanEval.jsonl.gz")


def read_problems(evalset_file: str = HUMAN_EVAL) -> Dict[str, Dict]:
    return {task["task_id"]: task for task in stream_jsonl(evalset_file)}


def stream_jsonl(filename: str) -> Iterable[Dict]:
    """
    Parses each jsonl line and yields it as a dictionary
    """
    if filename.endswith(".gz"):
        with open(filename, "rb") as gzfp:
            with gzip.open(gzfp, 'rt', encoding='utf-8', errors='replace') as fp:
                for line in fp:
                    if any(not x.isspace() for x in line):
                        yield json.loads(line)
    else:
        with open(filename, "r", encoding="utf-8") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)


def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        with open(filename, mode) as fp:
            with gzip.GzipFile(fileobj=fp, mode='wb') as gzfp:
                for x in data:
                    gzfp.write((json.dumps(x, ensure_ascii=False) + "\n").encode('utf-8'))
    else:
        with open(filename, mode) as fp:
            for x in data:
                fp.write((json.dumps(x, ensure_ascii=False) + "\n").encode('utf-8'))
