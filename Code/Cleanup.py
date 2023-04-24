import numpy as np
import math
import pandas as pd

WORD_LABEL_ORDER_OF_PRESENTATIONS = {
    'Photos Presentation 1': [
                                'Blank', 'Earth',
                                'Blank', 'Forest', 
                                'Blank', 'Fire',
                                'Blank', 'Galaxy',
                                'Blank', 'Spider',
                                'Blank', 'Snake',
                                'Blank', 'Beach',
                                'Blank', 'Waterfall',
                                'Blank', 'City',
                                'Blank', 'Butterfly',
                                'Blank', 'Car',
                                'Blank', 'Moon',
                                'Blank', 'Lion',
                                'Blank', 'Bird',
                                'Blank', 'Desert',
    ],

    'Photos Presentation 2': [
                                'Blank', 'Forest',
                                'Blank', 'Fire',
                                'Blank', 'Spider',
                                'Blank', 'Earth',
                                'Blank', 'Snake',
                                'Blank', 'Galaxy',
                                'Blank', 'Waterfall',
                                'Blank', 'Beach',
                                'Blank', 'Butterfly',
                                'Blank', 'Car',
                                'Blank', 'Moon',
                                'Blank', 'Lion',
                                'Blank', 'City',
                                'Blank', 'Desert',
                                'Blank', 'Bird',
    ],

    'Photos Presentation 3': [
                                'Blank', 'Spider',
                                'Blank', 'Fire',
                                'Blank', 'Forest',
                                'Blank', 'Snake',
                                'Blank', 'Galaxy',
                                'Blank', 'Earth',
                                'Blank', 'Beach',
                                'Blank', 'Waterfall',
                                'Blank', 'Butterfly',
                                'Blank', 'Car',
                                'Blank', 'Lion',
                                'Blank', 'Desert',
                                'Blank', 'Moon',
                                'Blank', 'Bird',
                                'Blank', 'City',
    ],

    'Photos Presentation 4': [
                                'Blank', 'Car',
                                'Blank', 'Fire',
                                'Blank', 'Forest',
                                'Blank', 'Spider',
                                'Blank', 'Galaxy',
                                'Blank', 'Earth',
                                'Blank', 'Beach',
                                'Blank', 'Waterfall',
                                'Blank', 'Butterfly',
                                'Blank', 'Moon',
                                'Blank', 'Lion',
                                'Blank', 'Desert',
                                'Blank', 'City',
                                'Blank', 'Bird',
                                'Blank', 'Snake',
    ],

    'Photos Presentation 5': [
                                'Blank', 'Fire',
                                'Blank', 'Car',
                                'Blank', 'Galaxy',
                                'Blank', 'Spider',
                                'Blank', 'Desert',
                                'Blank', 'Moon',
                                'Blank', 'Earth',
                                'Blank', 'Waterfall',
                                'Blank', 'Beach',
                                'Blank', 'Butterfly',
                                'Blank', 'Lion',
                                'Blank', 'Snake',
                                'Blank', 'City',
                                'Blank', 'Bird',
                                'Blank', 'Forest',
    ],

}

NUMBERS_ASSOCIATED_WITH_LABELS = {
    'Blank': 0,
    'Earth': 1,
    'Forest': 2,
    'Fire': 3,
    'Galaxy': 4,
    'Spider': 5,
    'Snake': 6,
    'Beach': 7,
    'Waterfall': 8,
    'City': 9,
    'Butterfly': 10,
    'Car': 11,
    'Moon': 12,
    'Lion': 13,
    'Bird': 14,
    'Desert': 15,
}

def get_number_label_order_from_presentation_number(presentation_number):
    word_labels = WORD_LABEL_ORDER_OF_PRESENTATIONS['Photos Presentation {}'.format(presentation_number)]
    number_labels = [NUMBERS_ASSOCIATED_WITH_LABELS[label] for label in word_labels]

    return number_labels

def read_data(file_path):
    data = pd.read_csv(file_path, sep='\t', names="Sample Index, EXG Channel 0 (Fp1), EXG Channel 1 (Fp2), EXG Channel 2 (C3), EXG Channel 3 (C4), EXG Channel 4 (P7), EXG Channel 5 (P8), EXG Channel 6 (O1), EXG Channel 7 (O2), EXG Channel 8 (F7), EXG Channel 9 (F8), EXG Channel 10 (F3), EXG Channel 11 (F4), EXG Channel 12 (T7), EXG Channel 13 (T8), EXG Channel 14 (P3), EXG Channel 15 (P4), Accel Channel 0, Accel Channel 1, Accel Channel 2, Other1, Other2, Other3, Other4, Other5, Other6, Other7, Analog Channel 0, Analog Channel 1, Analog Channel 2, Timestamp, Other8".split(", "))
    return data

def clean_data(data):

    Timestamps = data['Timestamp']

    EEG_values = data.loc[:, 'EXG Channel 0 (Fp1)':'EXG Channel 15 (P4)']

    data = pd.concat([Timestamps, EEG_values], axis=1)

    # only keep the first 125*6*15 + 125*3*15 rows
    data = data.iloc[:125*6*15 + 125*3*15, :]

    return data

def add_labels(data, presentation_number):
    # get the labels
    labels = get_number_label_order_from_presentation_number(presentation_number)
    data.insert(1, 'Label', [-1 for i in range(len(data))])

    #add the labels to the data. change labels every 125*6 rows if the label is not 0 otherwise 125*3 rows
    label_index = 0
    for i in range(0, len(data), 125*3):
        current_label = labels[math.floor(label_index)]
        if current_label != 0:
            data.iloc[i:i+125*3, 1] = current_label
            label_index += 0.5
        else:
            data.iloc[i:i+125*3, 1] = current_label
            label_index += 1

    
    return data


def save_data(data, file_path):
    data.to_csv(file_path, index=False)

def main():
    # read the data
    data = read_data(r'../Data/OpenBCISession_2023-03-31_12-10-22/BrainFlow-RAW_2023-03-31_12-10-22_2_visual_3.csv')
    presentation_number = 3
    # clean the data
    data = clean_data(data)

    # add labels
    data = add_labels(data, presentation_number)

    # save the data
    save_data(data, r'../Data/Pre Processed Data/Cleaned/cleaned_data_2023-03-31_12-10-22.csv')


if __name__ == '__main__':
    main()

