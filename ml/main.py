import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
import sklearn.datasets as dt
from sklearn.metrics import r2_score, silhouette_score, recall_score, accuracy_score, f1_score, roc_auc_score
from sklearn.metrics import mean_squared_error as MSE
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.datasets import load_breast_cancer, load_iris, load_wine, load_boston
from sklearn.decomposition import PCA
from sklearn.svm import SVC, SVR
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


def getWoe(cut, tar):
    gb = tar.value_counts()  # 整个样本中正反例样本数量
    gi = pd.crosstab(cut, tar)  # 每组中正反例样本数量
    gbi = (gi[1] / gi[0]) / (gb[1] / gb[0])
    woe = np.log(gbi)
    return woe


def getIv(cut, tar):
    gb = tar.value_counts()  # 整个样本中正反例样本数量
    gi = pd.crosstab(cut, tar)  # 每组中正反例样本数量
    gbi = (gi[1] / gi[0]) / (gb[1] / gb[0])
    woe = np.log(gbi)
    # iv = (py-pn)*woe中的py一组中正例样本和整个样本集中正例样本的比例
    iv = ((gi[1] / gb[1]) - (gi[0] / gb[0])) * woe
    return iv


def mae(y_true, y_pred):
    return np.mean(abs(y_true - y_pred))


def missing_values_table(df):
    # 计算每一列缺失值的个数和百分比，返回每列信息(DataFrame)
    mis_val = df.isnull().sum(axis=0)  # 缺失值的个数
    mis_val_percent = 100 * df.isnull().sum(axis=0) / data.shape[0]  # 每列缺失值占该列总数据的百分比
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)  # 将每一列缺失值的数量和缺失值的百分比级联到一起,形成一个新的表格
    mis_val_table_ren_columns = mis_val_table.rename(columns={0: '缺失个数', 1: '缺失占比'})  # 重新给上步表格的列命名
    # 将百分比不为0的行数据根据百分比进行降序排序
    mis_val_table_ren_columns = mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        '缺失占比', ascending=False).round(1)
    # 打印概述
    print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
                                                              "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")
    return mis_val_table_ren_columns


def erase_missing_cols(df, percent):
    # 设置阈值将缺失比例超过百分之percent的列删除
    # 找出超过阈值的列
    missing_df = missing_values_table(df)
    missing_columns = list(missing_df.loc[missing_df['缺失占比'] > percent].index)
    print('We will remove %d columns.' % len(missing_columns))
    df.drop(columns=list(missing_columns), inplace=True)


def statistic(df):
    # 通过 describe 和 matplotlib 可视化查看数据的相关统计量（柱状图）
    # 正常：后5柱直线递增   不正常：方差（第2柱）很小，后5柱都很大（方差小无意义）/max（最后1柱）很大，其他很小（异常值）
    data_desc = df.describe()
    cols = data_desc.columns
    index = data_desc.index[1:]  # 去除count行
    plt.figure(figsize=(30, 30))
    for i in range(len(cols)):
        ax = plt.subplot(5, 6, i + 1)
        ax.set_title(cols[i])
        for j in range(len(index)):
            plt.bar(index[j], data_desc.loc[index[j], cols[i]])
    plt.show()


def data_mean(df):
    # 中位数填充 返回DataFrame格式
    tmp = df.copy()
    for col in tmp.columns:
        if tmp[col].isnull().sum() > 0:  # tmp[col]有空值
            tmp[col].fillna(value=np.median(tmp[col][tmp[col].notnull()]),
                            inplace=True)  # [col][tmp[col].notnull()] == [tmp[col].notnull(),col]
            # print(np.median( tmp[col][tmp[col].notnull()] ),col)   #填充内容
    return tmp.copy()


def data_avg(df):
    # 均值填充 返回DataFrame格式
    tmp = df.copy()
    for col in tmp.columns:
        if tmp[col].isnull().sum() > 0:  # tmp[col]有空值
            tmp[col].fillna(value=tmp[col].mean(), inplace=True)  # 取当列的平均数（不包括nan的值）填充
    return tmp.copy()


def unusual_index(df, col):
    # 离群点数据过滤  （或者log变换）   返回异常值的行的索引
    q1 = df[col].describe()['25%']
    q3 = df[col].describe()['75%']
    iq = q3 - q1
    return df[(df[col] < (q1 - 3 * iq)) | (df[col] > (q3 + 3 * iq))]


def depend_index(df):
    # 显示相关性强的列  返回n行3列
    cols = df.columns  # 获取列的名称
    corr_list = []
    size = df.shape[1]
    high_corr_fea = []  # 存储相关系数大于0.5的特征名称
    features_corr = df.corr()
    for i in range(0, size):
        for j in range(i + 1, size):
            if (abs(features_corr.iloc[i, j]) >= 0.5):
                corr_list.append([features_corr.iloc[i, j], i, j])  # features_corr.iloc[i,j]：按位置选取数据

    sorted_corr_list = sorted(corr_list, key=lambda xx: -abs(xx[0]))
    for v, i, j in sorted_corr_list:
        high_corr_fea.append(cols[i])
        print("%s and %s = %.2f" % (cols[i], cols[j], v))  # cols: 列名
    return sorted_corr_list


def build(feature, target):
    # 全体建模
    x_train, x_test, y_train, y_test = train_test_split(feature, target, test_size=0.1, random_state=2020)
    line = LinearRegression().fit(x_train, y_train)
    logi = LogisticRegression().fit(x_train, y_train)
    svr = SVR().fit(x_train, y_train)
    svc = SVC().fit(x_train, y_train)
    dtree_gini = DecisionTreeClassifier(criterion='gini').fit(x_train, y_train)
    dtree_entropy = DecisionTreeClassifier(criterion='entropy').fit(x_train, y_train)
    forest = RandomForestRegressor().fit(x_train, y_train)
    knn = KNeighborsClassifier().fit(x_train, y_train)
    rid = Ridge(alpha=0.9).fit(x_train, y_train)
    gauss = GaussianNB().fit(x_train, y_train)
    multi = MultinomialNB().fit(x_train, y_train)


title = 'date,hour,pm2.5,DEWP,TEMP,PRES,Iws,Is,Ir,cbwd_NE,cbwd_NW,cbwd_SE,cbwd_cv'.split(',')

# print(len('2010-01-02,0,129.0,-16,-4.0,1020.0,1.79,0,0,0,0,1,0'.split(',')))

train = pd.read_csv('pm25_train.csv', header=None, names=title)
test = pd.read_csv('pm25_test.csv', header=None)  # ,names=title)
print(test.head())
print('----------------------------------')
print(train)
print('----------------------------------')
print(train.info())
# statistic(train)

hit = ['hour', 'DEWP', "TEMP", "pm2.5"]
dropper = []
for i in title:
    if i not in hit:
        dropper.append(i)
print(dropper)

data = train.drop(columns=dropper)
print(data.shape)
# statistic(data)
# print(depend_index(data))


def myscore(y_true, y_pred):
    return MSE(y_true, y_pred)


feature = data.iloc[:, 2:]
target = data.iloc[:, 1]
print(feature)
print('////////////////////////////////')
print(target)
x_train, x_test, y_train, y_test = train_test_split(feature, target, test_size=0.2)
line = LinearRegression().fit(x_train, y_train)
svr_line = SVR(kernel='linear').fit(x_train, y_train)
print(myscore(y_test, svr_line.predict(x_test)))
