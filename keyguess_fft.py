import os
import numpy as np
import FFT

#ピアソンの相関係数を算出
def pearson(power, HD, pearson):
    pearson.append(np.corrcoef(power, HD)[0][1])      


def data_import(import_data, data):
    for line in import_data:
        line = line.rstrip() 
        data.append(line.split(','))


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

def key_guess(correlation):
    #10ラウンド目周辺50点の相関係数の平均が最も大きい推定鍵値を算出
    correlation_mean = []
    for i in range(256):
        correlation_mean.append(np.mean(correlation[i::256]))
    
    key = correlation_mean.index(max(correlation_mean))

    with open(os.path.dirname(__file__) + '/week2/key_guess.txt', mode='a', encoding='utf-8') as key_guess:
        key_guess.write(hex(key) + '\n')
    
    print(hex(key))
    print(correlation_mean[key])

#10ラウンド目周辺50点を切り出す
def power_cut(data):
    for i in range(len(data)):
        del data[i][2119: ]
        del data[i][ :2069]


def byte_op(data, HD_distance):
    HD = []
    for line in HD_distance:
        line = line.rstrip(',\n')
        HD.append(line.split(','))          #配列HD = [[暗号文0のときのラウンド鍵が0~255までのHD], [暗号文1のときのラウンド鍵が0~255までのHD], ... , [暗号文nのときのラウンド鍵が0~255までのHD]]
    
    for i in range(len(HD)):
        for j in range(len(HD[i])):
            HD[i][j] = int(HD[i][j])
    
    correlation = []
    key_correlation(data, HD[:(len(data))], correlation)

    key_guess(np.array(correlation))


def main():
    wave1 = open(os.path.dirname(__file__) + '/week2/aes_tv_0000001-0005000_power.csv', "r", encoding="utf_8")
    wave2 = open(os.path.dirname(__file__) + '/week2/aes_tv_0005001-0010000_power.csv', "r", encoding="utf_8")
    wave3 = open(os.path.dirname(__file__) + '/week2/aes_tv_0010001-0015000_power.csv', "r", encoding="utf_8")
    wave4 = open(os.path.dirname(__file__) + '/week2/aes_tv_0015001-0020000_power.csv', "r", encoding="utf_8")
    wave5 = open(os.path.dirname(__file__) + '/week2/aes_tv_0020001-0025000_power.csv', "r", encoding="utf_8")
    wave6 = open(os.path.dirname(__file__) + '/week2/aes_tv_0025001-0030000_power.csv', "r", encoding="utf_8")
    HD_distance0 = open(os.path.dirname(__file__) + '/week2/byte_no0.txt', "r", encoding="utf_8")
    HD_distance1 = open(os.path.dirname(__file__) + '/week2/byte_no1.txt', "r", encoding="utf_8")
    HD_distance2 = open(os.path.dirname(__file__) + '/week2/byte_no2.txt', "r", encoding="utf_8")
    HD_distance3 = open(os.path.dirname(__file__) + '/week2/byte_no3.txt', "r", encoding="utf_8")
    HD_distance4 = open(os.path.dirname(__file__) + '/week2/byte_no4.txt', "r", encoding="utf_8")
    HD_distance5 = open(os.path.dirname(__file__) + '/week2/byte_no5.txt', "r", encoding="utf_8")
    HD_distance6 = open(os.path.dirname(__file__) + '/week2/byte_no6.txt', "r", encoding="utf_8")
    HD_distance7 = open(os.path.dirname(__file__) + '/week2/byte_no7.txt', "r", encoding="utf_8")
    HD_distance8 = open(os.path.dirname(__file__) + '/week2/byte_no8.txt', "r", encoding="utf_8")
    HD_distance9 = open(os.path.dirname(__file__) + '/week2/byte_no9.txt', "r", encoding="utf_8")
    HD_distance10 = open(os.path.dirname(__file__) + '/week2/byte_no10.txt', "r", encoding="utf_8")
    HD_distance11 = open(os.path.dirname(__file__) + '/week2/byte_no11.txt', "r", encoding="utf_8")
    HD_distance12 = open(os.path.dirname(__file__) + '/week2/byte_no12.txt', "r", encoding="utf_8")
    HD_distance13 = open(os.path.dirname(__file__) + '/week2/byte_no13.txt', "r", encoding="utf_8")
    HD_distance14 = open(os.path.dirname(__file__) + '/week2/byte_no14.txt', "r", encoding="utf_8")
    HD_distance15 = open(os.path.dirname(__file__) + '/week2/byte_no15.txt', "r", encoding="utf_8")

    data = []
    data_import(wave1, data)
    data_import(wave2, data)
    data_import(wave3, data)
    data_import(wave4, data)
    data_import(wave5, data)
    data_import(wave6, data)

    offset = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
        offset.append(sum(data[i]) / len(data[i]))          #配列offset = 波形ごとの直流成分の電圧値を格納
    
    #dataをFFTする
    for i in range(len(data)):
        data[i] = FFT.FFT(data[i], offset[i])
    
    #10ラウンド目の周辺50データを抜き出す
    power_cut(data)

    #バイトごと鍵値推定
    byte_op(data, HD_distance0)
    byte_op(data, HD_distance1)
    byte_op(data, HD_distance2)
    byte_op(data, HD_distance3)
    byte_op(data, HD_distance4)
    byte_op(data, HD_distance5)
    byte_op(data, HD_distance6)
    byte_op(data, HD_distance7)
    byte_op(data, HD_distance8)
    byte_op(data, HD_distance9)
    byte_op(data, HD_distance10)
    byte_op(data, HD_distance11)
    byte_op(data, HD_distance12)
    byte_op(data, HD_distance13)
    byte_op(data, HD_distance14)
    byte_op(data, HD_distance15)

    wave1.close()
    wave2.close()
    wave3.close()
    wave4.close()
    wave5.close()
    wave6.close()
    HD_distance0.close()
    HD_distance1.close()
    HD_distance2.close()
    HD_distance3.close()
    HD_distance4.close()
    HD_distance5.close()
    HD_distance6.close()
    HD_distance7.close()
    HD_distance8.close()
    HD_distance9.close()
    HD_distance10.close()
    HD_distance11.close()
    HD_distance12.close()
    HD_distance13.close()
    HD_distance14.close()
    HD_distance15.close()

if __name__ == '__main__':
    main()