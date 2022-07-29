import os
import copy
import numpy as np
import matplotlib.pyplot as plt

def FFT(data, off_set):
    N = len(data)
    #print(N)
    dt = 0.01
    for i in range(0, len(data)):
        data[i] = data[i] - off_set          #直列成分除去

    window_n = np.hamming(N)            #ハミング窓
    acf  = 1 / (sum(window_n) / N)          #窓関数の補正値

    copy_data = copy.copy(data)
        
    copy_data = copy_data * window_n            #窓関数をかける
 
    F = np.fft.fft(copy_data)
    fq = np.linspace(0, 1.0/dt, N)
    '''
    F_abs = np.abs(F)
    F_abs_amp = acf * F_abs / N * 2     # 交流成分はデータ数で割って2倍する（窓関数補正）
    plt.xlabel('freqency', fontsize=14)
    plt.ylabel('signal amplitude', fontsize=14)
    plt.plot(fq[:int(N/2)+1], F_abs_amp[:int(N/2)+1])
    plt.show()
    '''
    F2 = np.copy(F)
    fc = 4.3          # カットオフ（周波数）(LPF)
    F2[(fq > fc)] = 0
    '''
    F2_abs = np.abs(F2)
    F2_abs_amp = acf * F2_abs / N * 2     # 交流成分はデータ数で割って2倍する（窓関数補正）
    plt.xlabel('freqency', fontsize=14)
    plt.ylabel('signal amplitude', fontsize=14)
    plt.plot(fq[:int(N/2)+1], F2_abs_amp[:int(N/2)+1])
    plt.show()
    '''
    F2_ifft = np.fft.ifft(F2)
    F2_ifft_real = F2_ifft.real * 2 / window_n
    '''
    t = range(0, len(data))
    plt.plot(t, data, label='original')
    plt.plot(t, F2_ifft_real, c="r", linewidth=1, alpha=0.7, label='filtered')
    plt.legend(loc='best')
    plt.xlabel('data', fontsize=14)
    plt.ylabel('singnal', fontsize=14)
    plt.show()
    '''
    return(F2_ifft_real.tolist())
    

def main():
    wave = open(os.path.dirname(__file__) + '/week2/aes_tv_0000001-0005000_power.csv', "r", encoding="utf_8")
    print(wave)
    '''
    data = []
    for line in wave:
        line = line.rstrip() 
        data.append(line.split(','))
    for i in range(len(data[100])):
        data[0][i] = int(data[0][i])
    mean = sum(data[0]) / len(data[0])
    FFT(data[0], mean)
    '''
    wave.close()

if __name__ == '__main__':
    main()
