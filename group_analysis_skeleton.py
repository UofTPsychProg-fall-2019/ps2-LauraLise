#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#

os.chdir('C:\\Users\\laura\\OneDrive\\Documents\\GitHub\\ps2-LauraLise') #change current wd to where course files are stored
os.getcwd()  # Prints the current working directory, a check to ensure directory is correct
testingrooms = ['A','B','C']
for room in testingrooms:
    shutil.copy('testingroom'+room+'\\experiment_data.csv', 'rawdata') #note to self: do not need to reference the entire file path
    os.rename('rawdata\\experiment_data.csv', 'rawdata\\experiment_data_room_'+ room + '.csv')
#make sure all the files are in the rawdata directory
rawdata = os.listdir('C:\\Users\\laura\\OneDrive\\Documents\\GitHub\\ps2-LauraLise\\rawdata') 
print(rawdata)



#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
os.chdir('C:\\Users\\laura\\OneDrive\\Documents\\GitHub\\ps2-LauraLise\\rawdata')
for room in testingrooms:
    filename = 'experiment_data_room_'+room+'.csv'
    print(filename)
    tmp = sp.loadtxt(filename,delimiter=',') 
    data = np.vstack([data,tmp])



#%%
# calculate overall average accuracy and average median RT
#

#used the round function to specify the number of decimal points 
acc_avg = np.mean(data[:,3])*100 # 91.48%
mrt_avg = np.mean(data[:,4]) # 477.3ms



#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms

mrt_sum_words = 0
acc_sum_words = 0
mrt_sum_faces = 0
acc_sum_faces = 0
num_faces = 0 
num_words = 0  

for i in range(len(data)): #looping through each row in the NumPy array
    if (data[i,1]==1).any(): #have to use .any() because data[i,1]==1 is a NumPy array of Booleans
        mrt_sum_words += data[i,4] 
        acc_sum_words +=  data[i,3]
        num_words += 1
    elif (data[i,1]==2).any(): #again, have to use .any() 
        mrt_sum_faces += data[i,4]
        acc_sum_faces += data[i,3] 
        num_faces += 1
mrt_avg_words = mrt_sum_words/num_words
acc_avg_words = acc_sum_words/num_words*100
mrt_avg_faces = mrt_sum_faces/num_faces
acc_avg_faces = acc_sum_faces/num_faces*100
print('faces:',round(mrt_avg_faces,1),'ms',',',round(acc_avg_faces,1),'%')
print('words:',round(mrt_avg_words,1),'ms',',',round(acc_avg_words,1),'%')





#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)

#select rows of the numpy.ndarray where the pairing is white/pleasant (i.e. where the value in the 3rd column is 1),
#then select the accuracy data (in the 4th column)
acc_avg_wp = np.mean(data[data[:,2]==1,3])*100 # 94.0%
print('wp words:',acc_avg_wp,'%')

#select rows of the numpy.ndarray where the pairing is black/pleasant (i.e. where the value in the 3rd column is 2),
#then select the accuracy data (in the 4th column)
acc_avg_bp = np.mean(data[data[:,2]==2,3])*100  # 88.9%
print('bp words:',acc_avg_bp,'%')

#select rows of the numpy.ndarray where the pairing is white/pleasant (i.e. where the value in the 3rd column is 1),
#then select the median RT data (in the 5th column)
mrt_avg_wp = np.mean(data[data[:,2]==1,4]) # 469.6ms
print('wp words:',mrt_avg_wp,'ms')

#select rows of the numpy.ndarray where the pairing is black/pleasant (i.e. where the value in the 3rd column is 2),
#then select the median RT data (in the 5th column)
mrt_avg_bp = np.mean(data[data[:,2]==2,4])  # 485.1ms
print('bp words:',mrt_avg_bp,'ms')


#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)

#easiest to use indexing, involves the fewest lines of code 
mrt_avg_wp_words = np.mean(data[(data[:,1]==1) & (data[:,2]==1),4])
print('wp words:',mrt_avg_wp_words,'ms') # words - white/pleasant: 478.4ms
       
mrt_avg_bp_words = np.mean(data[(data[:,1]==1) & (data[:,2]==2),4])
print('bp words:',mrt_avg_bp_words,'ms') # words - black/pleasant: 500.3ms

mrt_avg_wp_faces = np.mean(data[(data[:,1]==2) & (data[:,2]==1),4])
print('wp faces:',mrt_avg_wp_faces,'ms') # faces - white/pleasant: 460.8ms

mrt_avg_bp_faces = np.mean(data[(data[:,1]==2) & (data[:,2]==2),4])
print('bp faces:',mrt_avg_bp_faces,'ms') # faces - black/pleasant: 469.8ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats

#comparing wp words to bp words 
(t_words, p_words) = scipy.stats.ttest_rel((data[(data[:,1]==1) & (data[:,2]==1),4]), (data[(data[:,1]==1) & (data[:,2]==2),4]))
print('\nwp words to bp words:','t =',t_words,'p =',p_words)

#comparing wp faces to bp faces 
(t_faces, p_faces) = scipy.stats.ttest_rel((data[(data[:,1]==2) & (data[:,2]==1),4]), (data[(data[:,1]==2) & (data[:,2]==2),4]))
print('\nwp faces to bp faces:','t =',t_faces,'p =',p_faces)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
#print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))

#\n is used to skip a line before printing the results
# :.2f is used to indicate the number of decimal places to round to (:.2f is two, :.1f is one)
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(acc_avg,mrt_avg))

print(f'\nOVERALL: {acc_avg:.2f}%, {mrt_avg:.1f} ms') #can also use use this more concise formatting

print('\nWORDS: {:.2f}%, {:.1f} ms'.format(acc_avg_words,mrt_avg_words))

print('\nFACES: {:.2f}%, {:.1f} ms'.format(acc_avg_faces,mrt_avg_faces))

print('\nWHITE/PLEASANT: {:.2f}%, {:.1f} ms'.format(acc_avg_wp,mrt_avg_wp))

print('\nBLACK/PLEASANT: {:.2f}%, {:.1f} ms'.format(acc_avg_bp,mrt_avg_bp))

print('\nWHITE/PLEASANT WORDS: {:.1f} ms'.format(mrt_avg_wp_words))

print('\nBLACK/PLEASANT WORDS: {:.1f} ms'.format(mrt_avg_bp_words))

print('\nWHITE/PLEASANT FACES: {:.1f} ms'.format(mrt_avg_wp_faces))

print('\nBLACK/PLEASANT FACES: {:.1f} ms'.format(mrt_avg_bp_faces))

print('\nPAIRED T-TEST of mrt WHITE/PLEASANT WORDS to BLACK/PLEASANT WORDS: t = {:.2f}, p = {:.3g}'.format(t_words,p_words))

print('\nT-TEST of mrt comparing BLACK/PLEASANT FACES to BLACK/PLEASANT FACES:  t = {:.2f}, p = {:.4f}'.format(t_faces,p_faces))



