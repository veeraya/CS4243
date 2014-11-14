import numpy as np
import cv2
import math
import sys
import pickle

"""
Code for combining two data file
"""

def main():
    file_in1 = "data.pkl"
    file_in2 = "data(master).pkl"
    file_out = "combined_data.pkl"
    combined_data(file_in1, file_in2, file_out)

def combined_data(file_in1, file_in2, file_out):
    print "Reading file1"
    pkl_file = open(file_in1, 'rU')
    pts1 = pickle.load(pkl_file)
    print "Reading file2"
    pkl2_file = open(file_in2, 'rU')
    pts2= pickle.load(pkl2_file)

    num_row = pts1.shape[0]
    num_col = pts1.shape[1]

    for r in range(0, num_row):
        for c in range(0, num_col):
            z1 = pts1[r,c,0]
            z2 = pts2[r,c,0]
            if type(z1) == int and type(z2) != int:
                pts1[r,c,0] = z2
            elif type(z1) != int and type(z2) != int:
                pts1[r,c,0] = np.concatenate((z1, z2)).tolist()


    output = open(file_out, 'wb')
    pickle.dump(pts1, output)
    output.close()

if __name__ == "__main__":
    main()