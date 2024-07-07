# README

> 这是专利《一种自动化DeFi安全事件提前感知的方法》的代码复现包，本专利基于Discord社区讨论实现了DeFi事件提前感知与止损功能，避免了由于信息滞后所导致的经济损失的扩大。
>
> This code replication package pertains to the patent "A Method for Early Detection of Automated DeFi Security Incidents." The patent leverages discussions within the Discord community to achieve early detection and mitigation of DeFi events thus preventing the escalation of economic losses due to delayed information.



1. 文件架构

   ```
   /disentanglement      ------ 该文件夹储存对话解纠缠部分代码，用于收集Discord上社区讨论内容并解纠缠为独立对话
   /classification       ------ 该文件夹储存DeFi讨论识别部分代码，用于判断解纠缠后的代码是否与DeFi讨论相关
   		/data             ------ 该文件夹储存解纠缠后的训练集与测试集，分别为train.txt, test.txt
   		/out              ------ 该文件夹储存训练后的模型
   		...               ------ 一些模型训练的文件
   readme.md             ------ 本文件
   ```

   

2. 复现步骤

i. 解纠缠



ii. 分类

###### Preparation

```
pip install allennlp==0.8.4
pip install overrides==3.1.0
pip install scikit-learn==0.22.2 
```

Download  `glove.6B.50d.txt`: Pretrained word2vec file, and you need to download this file at [Glove](https://nlp.stanford.edu/projects/glove/), then put it into folder `/classification/data`.



###### Data Process

我们已经提供了处理好后的train.txt与test.txt，`preprocess.py`用于将txt格式的对话转化为模型需要的json格式。

```
python classification/data/preprocess.py
```



###### Train

修改config.json中train_data_path与validation_data_path为指定的测试集与训练集，在项目根目录运行以下指令进行训练，修改config.json中的cuda_device参数以指定GPU设备。

```
allennlp train classification/config.json -s classification/out/ -f --include-package classification
```

训练结束后输出如下

```
"training_start_epoch": 0,
"training_epochs": 9,
"epoch": 9,
"training_accuracy": 0.8915311653116531,
"training_precision": 0.8915842175483704,
"training_recall": 0.8914633989334106,
"training_fscore": 0.8915237784385681,
"training_s_precision": 0.8676018371799951,
"training_s_recall": 0.8905947775509001,
"training_s_fmeasure": 0.8789474615506568,
"training_loss": 0.35417075519695945,
"training_cpu_memory_MB": 6192.416,
"training_gpu_0_memory_MB": 71824,
"training_gpu_1_memory_MB": 71612,
"training_gpu_2_memory_MB": 71772,
"training_gpu_3_memory_MB": 71650,
"training_gpu_4_memory_MB": 26282,
"training_gpu_5_memory_MB": 45188,
"training_gpu_6_memory_MB": 46106,
"training_gpu_7_memory_MB": 76496,
"validation_accuracy": 0.8611111111111112,
"validation_precision": 0.8714285492897034,
"validation_recall": 0.8472222089767456,
"validation_fscore": 0.8591549396514893,
"validation_s_precision": 0.8675861167283145,
"validation_s_recall": 0.8905797101329768,
"validation_s_fmeasure": 0.878932056442736,
"validation_loss": 0.468152379989624,
"best_validation_accuracy": 0.8611111111111112,
"best_validation_precision": 0.8714285492897034,
"best_validation_recall": 0.8472222089767456,
"best_validation_fscore": 0.8591549396514893,
```



###### Test

```
allennlp evaluate classification/out/model.tar.gz classification/data/test.txt  --include-package classification
```

运行后测试输出如下

```
2024-07-06 06:28:20,846 - INFO - allennlp.training.util - Iterating over dataset
accuracy: 0.87, precision: 0.87, recall: 0.86, fscore: 0.87, s_precision: 0.86, s_recall: 0.87, s_fmeasure: 0.87, loss: 0.46 ||: 100%|█|
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - Finished evaluating.
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - Metrics:
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - accuracy: 0.8680555555555556
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - precision: 0.8732394576072693
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - recall: 0.8611111044883728
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - fscore: 0.867132842540741
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - s_precision: 0.8630136868080317
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - s_recall: 0.8749999878472224
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - s_fmeasure: 0.8689650052797171
2024-07-06 06:28:24,235 - INFO - allennlp.commands.evaluate - loss: 0.46207918524742125
```

