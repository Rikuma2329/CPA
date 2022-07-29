import os
import numpy as np
import FFT
import matplotlib.pyplot as plt

def pearson(power, HD, pearson):
    pearson.append(np.corrcoef(power, HD)[0][1])      #ピアソンの相関係数を算出

def key_correlation(data, HD, correlation):
    for i in range(len(data[0])):
        Ins_power = []
        for j in range(len(data)):
            Ins_power.append(data[j][i])
        for k in range(256):
            key_HD = []
            for l in range(len(HD)):
                key_HD.append(HD[l][k])             #配列key_HD = [鍵値kのときの暗号文0~nまでのHD]
            pearson(Ins_power, key_HD, correlation)


def byte_corr(corr, corr_coef):
    for i in range(256):
        corr_coef.append(np.mean(corr[i::256]))


def byte_op(data, HD_distance):
    HD = []
    for line in HD_distance:
        line = line.rstrip(',\n')
        HD.append(line.split(','))          #配列HD = [[暗号文0のときのラウンド鍵が0~255までのHD], [暗号文1のときのラウンド鍵が0~255までのHD], ... , [暗号文nのときのラウンド鍵が0~255までのHD]]
    
    for i in range(len(HD)):
        for j in range(len(HD[i])):
            HD[i][j] = int(HD[i][j])
    
    corr_coef = [0] * 256
    for i in range(1, 501):     #15000波形まで試す
        corr = []
        key_correlation(data[: 30*i], HD[: 30*i], corr)
        byte_corr(corr, corr_coef)
        print(len(corr_coef))

    graph(corr_coef)


def data_import(import_data, data):
    for line in import_data:
        line = line.rstrip() 
        data.append(line.split(','))

def power_cut(data):
    for i in range(len(data)):
        del data[i][2119: ]
        del data[i][ :2069]

def graph(corr_coef):
    x = range(0, 15001, 30)
    plt.xlabel('No. of Plaintexts', fontsize=14)
    plt.ylabel('correlation Coefficient', fontsize=14)
    plt.xlim(0, 15000)
    plt.ylim(0, 0.15)
    plt.xticks([0, 3000, 6000, 9000, 12000, 15000])
    plt.yticks([0, 0.03, 0.06, 0.09, 0.12, 0.15])
    for i in range(256):
        if(i == 201):
            plt.plot(x, corr_coef[i::256], c="r", linewidth=1)
        else:
            plt.plot(x, corr_coef[i::256], c="k", linewidth=1)
    plt.show()


def main():
    wave1 = open(os.path.dirname(__file__) + '/week2/aes_tv_0000001-0005000_power.csv', "r", encoding="utf_8")
    wave2 = open(os.path.dirname(__file__) + '/week2/aes_tv_0005001-0010000_power.csv', "r", encoding="utf_8")
    wave3 = open(os.path.dirname(__file__) + '/week2/aes_tv_0010001-0015000_power.csv', "r", encoding="utf_8")
    HD_distance = open(os.path.dirname(__file__) + '/week2/byte_no1.txt', "r", encoding="utf_8")

    data = []
    data_import(wave1, data)
    data_import(wave2, data)
    data_import(wave3, data)

    offset = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
        offset.append(sum(data[i]) / len(data[i]))          #配列offset = 波形ごとの直流成分の電圧値を格納
    
    #dataをFFTする
    for i in range(len(data)):
        data[i] = FFT.FFT(data[i], offset[i])

    power_cut(data)

    byte_op(data, HD_distance)

    wave1.close()
    wave2.close()
    wave3.close()
    HD_distance.close()

if __name__ == '__main__':
    main()