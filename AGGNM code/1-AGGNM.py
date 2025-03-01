"""
  构建模型：（带GNM动态特征）
    Note: 欠采样cutoff = 6，GNM的mod = 60
    测试结果保存在：./result/AutoGLGNM.txt中
"""
import pickle
import warnings
import numpy as np
from autogluon.tabular import TabularDataset, TabularPredictor

# turn off warnings
warnings.filterwarnings('ignore')

time = 2
file_dir = './result/'
save_path = 'aggnm' # 模型保存路径

x_train = pickle.load(open("./data/train_nma_all_features.pkl", "rb"))
y_train = pickle.load(open("./data/train_nma_all_labels.pkl", "rb"))
x_val= pickle.load(open("./data/valid_nma_all_features.pkl", "rb"))
y_val = pickle.load(open("./data/valid_nma_all_labels.pkl", "rb"))
x_test1 = pickle.load(open("./data/test1_nma_all_features.pkl", "rb"))
y_test1 = pickle.load(open("./data/test1_nma_all_labels.pkl", "rb"))
x_test2 = pickle.load(open("./data/test2_nma_all_features.pkl", "rb"))
y_test2 = pickle.load(open("./data/test2_nma_all_labels.pkl", "rb"))


colName = [ # 特征名称列
  'Score',
  'Druggability Score',
  'Number of Alpha Spheres',
  'Total SASA',
  'Polar SASA',
  'Apolar SASA',
  'Volume',
  'Mean local hydrophobic density',
  'Mean alpha sphere radius',
  'Mean alp. sph. solvent access',
  'Apolar alpha sphere proportion',
  'Hydrophobicity score',
  'Volume score',
  'Polarity score',
  'Charge score',
  'Proportion of polar atoms',
  'Alpha sphere density',
  'Cent. of mass - Alpha Sphere max dist',
  'Flexibility',
  'gnm60',
  'isAllo' # 是否是变构口袋
]

# 1 生成测试数据
train_data = np.concatenate(([it[1:] for it in x_train], y_train.reshape(-1, 1)), axis=1)
valid_data = np.concatenate(([it[1:] for it in x_val], y_val.reshape(-1, 1)), axis=1)
test1_data = np.concatenate(([it[1:] for it in x_test1], y_test1.reshape(-1, 1)), axis=1)
test2_data = np.concatenate(([it[1:] for it in x_test2], y_test2.reshape(-1, 1)), axis=1)
train_data = TabularDataset(train_data)
valid_data = TabularDataset(valid_data)
test1_data = TabularDataset(test1_data)
test2_data = TabularDataset(test2_data)
# 3 合并数据 + 数据列
train_data.columns = colName # 添加列名称
valid_data.columns = colName
test1_data.columns = colName
test2_data.columns = colName
# 4 训练模型
predictor = TabularPredictor(label="isAllo", eval_metric='f1',path=save_path).fit( # 这里使用路径
    train_data, time_limit=60*time, tuning_data=valid_data
)
# testing results
y_test1_label = test1_data['isAllo']
y_test1_nolab = test1_data.drop(columns=['isAllo'])
y_pred_test1 = predictor.predict(y_test1_nolab)
perf_test1 = predictor.evaluate_predictions(
    y_true=y_test1_label, y_pred=y_pred_test1, auxiliary_metrics=True)

y_test2_label = test2_data['isAllo']
y_test2_nolab = test2_data.drop(columns=['isAllo'])
y_pred_test2 = predictor.predict(y_test2_nolab)
perf_test2 = predictor.evaluate_predictions(
    y_true=y_test2_label, y_pred=y_pred_test2, auxiliary_metrics=True)
# 6 记录每次的结果
ret = open(file_dir +  "AGGNM.txt", "a")
ret.write("================== " 
              + str(" AGGNM result ") 
              + "==================\n")
metrics = ['f1', 'accuracy', 'precision', 'recall']

# write testing results
ret.write("test1 results:\n")
for key in metrics:
    val = perf_test1[key]
    ret.write(str(key) + ' > ' + str(val) + '\n')
ret.write("\n")

ret.write("test2 results:\n")
for key in metrics:
    val = perf_test2[key]
    ret.write(str(key) + ' > ' + str(val) + '\n')
ret.write("\n")
ret.close()
