# 用于测试封装后函数的代码



import os
import soundfile as sf
from nara_wpe.utils import stft, istft
from toolbox import projection_back
import numpy as np
######################################################################################################################




n_sources = 3
mixed_sig_path = 'mixed/'+str(n_sources) + 'ch/'
save_path = 'wped/'+str(n_sources) + 'ch/'

file_list = os.listdir(mixed_sig_path)

stft_options = dict(size=1024, shift=1024//4)
sampling_rate = 16000
delay = 2
iterations = 100
taps = 5

wav_name = file_list[4]
y = sf.read(mixed_sig_path+wav_name)[0]
y = y.T
Y = stft(y, **stft_options)
X = Y.transpose(2, 0, 1).copy()
del Y, y# 把可能混淆的变量删除
#######################################################################################################################
# input&output X: n_freq, n_ch, n_frame

X = X.transpose(2, 0, 1)
n_iter = 20
n_components = 2

######################################################################################################################
from ilrma_t_function import *
Y = ilrma_t_iss_joint(X)


Z = Y.transpose(1, 2, 0)


#######################################################################################################################
z = istft(Z.transpose(1, 2, 0), size=stft_options['size'], shift=stft_options['shift'])
for i in range(n_sources):
    sf.write('test_wav/test_f_'+str(i)+'.wav', z[i] , 16000)