# README

> 这是专利《一种自动化DeFi安全事件提前感知的方法》的代码复现包，本专利基于Discord社区讨论实现了DeFi事件提前感知与止损功能，避免了由于信息滞后所导致的经济损失的扩大。
>
> This code replication package pertains to the patent "A Method for Early Detection of Automated DeFi Security Incidents." The patent leverages discussions within the Discord community to achieve early detection and mitigation of DeFi events thus preventing the escalation of economic losses due to delayed information.



#### 文件架构

```
/disentanglement      ------ 该文件夹储存对话解纠缠部分代码，用于收集Discord上社区讨论内容并解纠缠为独立对话
/classification       ------ 该文件夹储存DeFi讨论识别部分代码，用于判断解纠缠后的代码是否与DeFi讨论相关
		/data             		------ 该文件夹储存解纠缠后的训练集与测试集，分别为train.txt, test.txt
		/out              		------ 该文件夹储存训练后的模型
		config.json           ------ 训练配置文件
		frminer_model.py      ------ 对话分类网络架构
		frminer_reader.py     ------ 网络数据加载
		preprocess.py         ------ 对话预处理
		...                   ------ 其他训练相关文件
/matching							------ 该文件夹包含DeFi事件数据集，并储存匹配对话是否为基于现有DeFi事件讨论部分代码
	  /all-attack.csv       ------ DeFi事件数据集，包含攻击对象，简介，攻击方式，损失，事件时间字段
	  /flashbots.txt        ------ Flashbots解纠缠后对话
	  ...                   ------ 事件匹配相关代码
readme.md             ------ 本文件
```



#### 复现步骤

##### i. 解纠缠

解纠缠步骤请查看该仓库以获取详情 https://github.com/LuriiWang/Discord_Communication



##### ii. 分类

###### Step1: Preparation

考虑到依赖包兼容性问题，本专利采用Python版本为3.6，可采用如下指令创建对应环境。

```
conda create -n DeFiDiscussion python=3.6.2
conda activate DeFiDiscussion
```

在完成python文件配置后，进行依赖包配置。

```
pip install allennlp==0.8.4
pip install overrides==3.1.0
pip install scikit-learn==0.22.2 
```

完成依赖包配置后，下载词向量文件  `glove.6B.50d.txt`，访问该链接进行下载[Glove](https://nlp.stanford.edu/projects/glove/)，并将该文件放置于指定目录下`/classification/data`。



###### Step2: Data Process

我们已经提供了处理好后的train.txt与test.txt，`preprocess.py`用于将txt格式的对话转化为模型需要的json格式。

```
python classification/data/preprocess.py
```



###### Step3: Train

后续步骤在项目根目录进行操作，首先指定训练集与测试机，修改`classification/config.json`中train_data_path与validation_data_path为指定的测试集与训练集，如现有DeFi相关讨论识别任务中采用的`classification/data/train.txt` , `classification/data/test.txt`，在项目根目录运行以下指令进行训练。

如需采用GPU进行训练，则修改config.json中的cuda_device参数以指定GPU设备，默认采用CPU进行训练，`"cuda_device": -1`。使用GPU进行训练时，采用单张NVIDIA GeForce RTX 3090进行训练，训练用时1-2小时。

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



###### Step4: Test

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



##### iii. 事件识别

将代识别对话存放于matching/dialog.txt目录下，运行 `python matching/match.py`查看相关DeFi事件，本专利按照Description字段识别与该对话最相关的10个DeFi事件，运行后输出如下，从输出中可得本项目与Curve Finance等事件相关。

```
----------------------------------------------------------------------
Discussion is:
<goobygg> Curve Finance front end is compromised  samczref in #offtopic<0x7ec> or join us in #general<eyaleponym> Meaning bundles arrive / pass simulation too late to be included?<goobygg> I don't check gen chat too often <goobygg> Let me hop in there<vagabond2971> someone should send some tornado eth to the wethusdc uni pool no?<__reece__> That would be interesting<0x7ec> it would be a revert? no fallback or receive<0x7ec> maybe with some extra steps<ani9040> could tornado in some usdc<arianonwastaken> nothing a good ol selfdestruct can't solve<ani9040> or did they already blacklist the tornado addresses?<arianonwastaken> they did<bertcmiller> yes<eyaleponym> Thanks Is there a good way to check for this? The time stamp on the block seems largely irrelevant<rjected> implementing simple tx exchange w/ akula might not be that hard if u really want to use it
----------------------------------------------------------------------

Best matched related DeFi Discussions are: ['Alchemix', 'Curve Finance ', 'DEP/USDT,  LEV/USDC', 'CS Token', 'Harvest Finance', 'UvToken', 'Shido', 'MISO', 'Deus Finance', 'FriesDAO']
```
