import os
from scipy.spatial import distance
import AES
import copy

#ハミング距離算出
def Hamming_Distance(state, ciphertext, dis):
    for i in range(16):
        c = format(state[i] ^ ciphertext[i], 'b')
        dis.append(int(distance.hamming(list(c), [str(0)] * len(c)) * len(c)))          #C(x, y)とS(x, y)のハミング距離を算出
    
    AES.ShiftRows(dis)          #Inv_ShiftRowsの分を戻す

#HDテーブル出力
def write_data(byte_HD, byte_no, data0, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15):
    if(byte_no == 0):
        for i in range(256):
            data0.write(str(byte_HD[i]))
            data0.write(',')
        data0.write('\n')
    elif(byte_no == 1):
        for i in range(256):
            data1.write(str(byte_HD[i]))
            data1.write(',')
        data1.write('\n')
    elif(byte_no == 2):
        for i in range(256):
            data2.write(str(byte_HD[i]))
            data2.write(',')
        data2.write('\n')
    elif(byte_no == 3):
        for i in range(256):
            data3.write(str(byte_HD[i]))
            data3.write(',')
        data3.write('\n')
    elif(byte_no == 4):
        for i in range(256):
            data4.write(str(byte_HD[i]))
            data4.write(',')
        data4.write('\n')
    elif(byte_no == 5):
        for i in range(256):
            data5.write(str(byte_HD[i]))
            data5.write(',')
        data5.write('\n')
    elif(byte_no == 6):
        for i in range(256):
            data6.write(str(byte_HD[i]))
            data6.write(',')
        data6.write('\n')
    elif(byte_no == 7):
        for i in range(256):
            data7.write(str(byte_HD[i]))
            data7.write(',')
        data7.write('\n')
    elif(byte_no == 8):
        for i in range(256):
            data8.write(str(byte_HD[i]))
            data8.write(',')
        data8.write('\n')
    elif(byte_no == 9):
        for i in range(256):
            data9.write(str(byte_HD[i]))
            data9.write(',')
        data9.write('\n')
    elif(byte_no == 10):
        for i in range(256):
            data10.write(str(byte_HD[i]))
            data10.write(',')
        data10.write('\n')
    elif(byte_no == 11):
        for i in range(256):
            data11.write(str(byte_HD[i]))
            data11.write(',')
        data11.write('\n')
    elif(byte_no == 12):
        for i in range(256):
            data12.write(str(byte_HD[i]))
            data12.write(',')
        data12.write('\n')
    elif(byte_no == 13):
        for i in range(256):
            data13.write(str(byte_HD[i]))
            data13.write(',')
        data13.write('\n')
    elif(byte_no == 14):
        for i in range(256):
            data14.write(str(byte_HD[i]))
            data14.write(',')
        data14.write('\n')
    elif(byte_no == 15):
        for i in range(256):
            data15.write(str(byte_HD[i]))
            data15.write(',')
        data15.write('\n')

def main():
    text = open(os.path.dirname(__file__) + '/week1/CIPHERTEXT10000.txt', "r", encoding="utf_8")
    data0 = open(os.path.dirname(__file__) + '/week1/byte_no0.txt', 'w', encoding="utf_8")
    data1 = open(os.path.dirname(__file__) + '/week1/byte_no1.txt', 'w', encoding="utf_8")
    data2 = open(os.path.dirname(__file__) + '/week1/byte_no2.txt', 'w', encoding="utf_8")
    data3 = open(os.path.dirname(__file__) + '/week1/byte_no3.txt', 'w', encoding="utf_8")
    data4 = open(os.path.dirname(__file__) + '/week1/byte_no4.txt', 'w', encoding="utf_8")
    data5 = open(os.path.dirname(__file__) + '/week1/byte_no5.txt', 'w', encoding="utf_8")
    data6 = open(os.path.dirname(__file__) + '/week1/byte_no6.txt', 'w', encoding="utf_8")
    data7 = open(os.path.dirname(__file__) + '/week1/byte_no7.txt', 'w', encoding="utf_8")
    data8 = open(os.path.dirname(__file__) + '/week1/byte_no8.txt', 'w', encoding="utf_8")
    data9 = open(os.path.dirname(__file__) + '/week1/byte_no9.txt', 'w', encoding="utf_8")
    data10 = open(os.path.dirname(__file__) + '/week1/byte_no10.txt', 'w', encoding="utf_8")
    data11 = open(os.path.dirname(__file__) + '/week1/byte_no11.txt', 'w', encoding="utf_8")
    data12 = open(os.path.dirname(__file__) + '/week1/byte_no12.txt', 'w', encoding="utf_8")
    data13 = open(os.path.dirname(__file__) + '/week1/byte_no13.txt', 'w', encoding="utf_8")
    data14 = open(os.path.dirname(__file__) + '/week1/byte_no14.txt', 'w', encoding="utf_8")
    data15 = open(os.path.dirname(__file__) + '/week1/byte_no15.txt', 'w', encoding="utf_8")
    #cipher_text = '7df76b0c1ab899b33e42f047b91b546f'

    for line in text:           #暗号文の回数繰り返す
        cipher_text = line[2: ]         #AESの実装上の理由から'0x'を取って読み込む
        state = []
        AES.char_to_state(cipher_text, state)           #文字列→状態の16バイト配列に

        HD = []

        for i in range(256):            #各バイトの鍵が0~255まで実施
            round_state = copy.copy(state)
            RoundKey = ((i << 24) | (i << 16) | (i << 8) | i)           #すべてのバイトの鍵をiとする
            AES.AddRoundKey(round_state, [RoundKey, RoundKey, RoundKey, RoundKey])
            AES.Inv_ShiftRows(round_state)
            AES.Inv_SubBytes(round_state)           #ここまででround_stateはラウンド9出力時の状態に

            dis = []
            Hamming_Distance(round_state, state, dis)           #配列dis = [ラウンド鍵がiのとき0バイト～15バイトまでのHD]
            HD.append(dis)          #配列HD = [[ラウンド鍵が0のとき0バイト～15バイトまでのHD], [ラウンド鍵が1のとき0バイト～15バイトまでのHD],..., [ラウンド鍵が255のとき0バイト～15バイトまでのHD]]

        for i in range(16):         #配列HDの転置
            Byte_HD = []
            for j in range(256):
                Byte_HD.append(HD[j][i])            #配列Byte_HD = [[0バイト目のラウンド鍵が0~255までのHD], [1バイト目のラウンド鍵が0~255までのHD],..., [15バイト目のラウンド鍵が0~255までのHD]]

            write_data(Byte_HD, i, data0, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15)
    
    text.close()
    data0.close()
    data1.close()
    data2.close()
    data3.close()
    data4.close()
    data5.close()
    data6.close()
    data7.close()
    data8.close()
    data9.close()
    data10.close()
    data11.close()
    data12.close()
    data13.close()
    data14.close()
    data15.close()


if __name__ == '__main__':
    main()