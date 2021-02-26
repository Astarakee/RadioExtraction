import os
import pydicom
import SimpleITK as itk


data_dir = '/media/mehdi/KTH/DeepLearning/Data Repository/NSCLS/NSCLC-Radiomics/'
write_dir = '/media/mehdi/KTH/0_August/00_NSLC/Data/'

seg_dirs = []
img_dirs = []
for roots, dirs , files in os.walk(data_dir):
    if 'Segmentation' in roots:
        mask_dir = os.path.join(roots, files[0])
        seg_dirs.append(mask_dir)
    if len(files) > 20:
        img_dirs.append(roots)



# Write dicom series of main images as nifti files
for item in img_dirs:
    
    subject_name = item.split('Radiomics/')[1].split('/')[0]
    
    reader = itk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(item)
    reader.SetFileNames(dicom_names)
    image_itk = reader.Execute()
    
    subject_path = os.path.join(write_dir, subject_name)
    if not os.path.isdir(subject_path):
        os.makedirs(subject_path)
    subject_nifti = os.path.join(subject_path, (subject_name+'.nii.gz'))
    
    itk.WriteImage(image_itk, subject_nifti)
    
    
# Write dicom segmentation masks as nifti files

for item in seg_dirs:
    
    mask_name = item.split('Radiomics/')[1].split('/')[0]
    
    seg_file = pydicom.dcmread(item)
    seg_array = seg_file.pixel_array
    seg_itk = itk.GetImageFromArray(seg_array)
    
    mask_path = os.path.join(write_dir, mask_name)
    if not os.path.isdir(mask_path):
        os.makedirs(mask_path)
    mask_nifti = os.path.join(mask_path, (mask_name+'_seg.nii.gz'))
    
    itk.WriteImage(seg_itk, mask_nifti)
    
    
    

    
    