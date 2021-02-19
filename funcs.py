import os
import re
import csv

# Sorting the strings
_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def read_csv_names(csv_file):
    """
    Open and read a csv file and returns a list containing
    patient IDs and corresponding labels.
    """
    patient_id = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data_list = list(reader)
    for ind in range(1,len(data_list)):   
        row = data_list[ind]
        name = row
        patient_id.append(name)
    return patient_id


def get_filepath(path, pattern):
    """
    Path: path to the data
    Pattern: string pattern in filenames of interest
    Returns the full path of each file containing
    pattern in the filename.
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if pattern in file:
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    file_list.sort(key=natural_sort_key)     
    return file_list


def match_img_label(img_path, csv_file, datafolder):
    """
    img_path: full path of the image files
    csv_file: patient ID + labels in list
    datafolder: name of the data folder e.g,: '/lung/'
    
    It searches the names between CSV and data to find 
    the correspoding ones and return them in list along
    with related labels.
    """
    img_label = []
    for image_path in img_path:
        for csv_data in csv_file:
            
            img_name = image_path.split(datafolder)[1].split('/')[0]
            csv_name = csv_data[0]
            csv_label = csv_data[1]
            
            if img_name == csv_name:
                temp = []
                temp.append(image_path)
                temp.append(csv_label)
                img_label.append(temp)
                
    return img_label
