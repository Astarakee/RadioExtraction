import os
import six
import glob
import random
import pandas as pd
import SimpleITK as sitk
from radiomics import featureextractor
from funcs import read_csv_names, get_filepath, match_img_label


# Path to save features
csv_file_dir = os.path.join(os.getcwd(),'radiomic_feature.csv')


# Data handling
data_path = '/media/mehdi/KTH/DeepLearning/Data Repository/Lung Nodule/data/Lung_CT/train/'
data_csv_path = '/media/mehdi/KTH/DeepLearning/Data Repository/Lung Nodule/data/Lung_CT/'

data_csv_path = glob.glob(data_csv_path + "*.csv")[0]
subjects_id_label = read_csv_names(data_csv_path)

img_path = get_filepath(data_path, 'cropped')
mask_path = get_filepath(data_path, 'mask')

samples_img = match_img_label(img_path, subjects_id_label, '/train/')
samples_msk = match_img_label(mask_path, subjects_id_label, '/train/')

# Shuffling
random.seed(4)
random.shuffle(samples_img)
random.seed(4)
random.shuffle(samples_msk)


# Instantiating Radiomics Feature Extraction
extractor = featureextractor.RadiomicsFeatureExtractor()
param_path = os.path.join(os.getcwd(), 'params.yaml')
extractor = featureextractor.RadiomicsFeatureExtractor(param_path)
print('Extraction parameters:\n\t', extractor.settings)
print('Enabled filters:\n\t', extractor.enabledImagetypes)
print('Enabled features:\n\t', extractor.enabledFeatures)

#for ind in range(len(samples_img)):
for ind in range(2):
    # Get full dir to mask and image
    subject_img = samples_img[ind][0]
    subject_mask = samples_msk[ind][0]
    # Get target label
    subject_label = int(samples_img[ind][1])
    # Get subject name for saving    
    subject_name = subject_img.split('train/')[1]. \
    split('/')[1].split('.nii')[0]
    # Feature extraction
    img_itk = sitk.ReadImage(subject_img)
    mask_itk = sitk.ReadImage(subject_mask)
    features = extractor.execute(img_itk, mask_itk)
    # Including subject name, label and extracted featues in a dictionary
    features_all = {}
    for key, value in six.iteritems(features):
        if key.startswith('original') or key.startswith('wavelet') or \
        key.startswith('log'):
            features_all['Subject_ID'] = subject_name
            features_all['Subject_Label'] = subject_label
            features_all[key] = features[key]
            
    df = pd.DataFrame(data=features_all,  index=[ind])
    if ind == 0:
        df.to_csv(csv_file_dir, mode='a')
    else:
        df.to_csv(csv_file_dir, header = None, mode='a')