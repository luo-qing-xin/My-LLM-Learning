# Some Exporation
这次是开学的第一周，还挺忙的，于是...把项目拖到了周末来做：

## 学习使用API的方式调用大模型：

我是使用的[硅基流动 (SiliconFlow)](https://cloud.siliconflow.cn/me/account/ak)的API（因为有16元的代金券）

硅基流动的 API 基础地址（固定值，无需修改）
    base_url="https://api.siliconflow.cn/v1"
   
代码如下：
```
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv() # 加载 .env 文件中的环境变量
api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

response=client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",    
    #这个要去看文档，选择你需要的模型
    messages=[
        {"role": "system", "content": "你是我的人工智能助手，协助我解答问题和提供信息。"},
        {"role": "user", "content": input("请输入你的问题：")}
    #这里本来是固定的，我改成能问答的了
    ],
    max_tokens=500,
    temperature=0.7
)
    #关键字参数，Python 会根据参数名来识别，而不是根据位置。
    print(response.choices[0].message.content)
```
### 探索1：了解API调用大模型的各个[参数含义](https://chat.deepseek.com/share/0nc7ayhpnk9rbipk7t)，可以通过寻找教程、阅读手册等

messages*（现在大部分是messages，还有propmt, [区别](https://chat.deepseek.com/share/w84p1csvyqhdiwfcdn)在此）

model*

temperature,top_p

max_tokens

stream

presence_penalty

frequency_penalty   

stop

### 探索2：设计prompt，在鸢尾花数据集上完成分类，调整prompt查看区别

### 探索3：对比之前鸢尾花分类方法，代码实现逻辑上有何异同
#### （1）异：
  1. 数据方面：有无训练集
  2. 模型是否提供=>库不同，
  3. 输入，一个是输入数据集，另一个将数据嵌在prompt中
  4. 是否需要训练（从有无.pth文件生成就能看出）有无显式训练
  5. 超参数：一个是机器学习的超参数，一个是api调用时的超参数
### 探索4：使用GPT-2模型分类鸢尾花，对比当下先进的LLM（不局限在准确率上，所有的都可以分享）
可能使用到的资源：[https://www.volcengine.com](https://www.volcengine.com)


上周由于时间仓促，没能完成一些任务，故继续研究：
1.api怎么不搞到代码里？——使用环境变量（记得勾选vs code中的设置选项）
