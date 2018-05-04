import os
import shutil

dataset_folderpath = 'D:/rtsd/rtsd-r3/rtsd-r3/'
output_dataset_folderpath = 'D:/rtsd/rtsd-r3/rtsd_classy_ok'

test_csv_filepath = 'D:/rtsd/rtsd-r3/rtsd-r3/gt_test.csv'
train_csv_filepath = 'D:/rtsd/rtsd-r3/rtsd-r3/gt_train.csv'


num_to_classes_csv = 'D:/rtsd/rtsd-r3/rtsd-r3/numbers_to_classes.csv'
with open(num_to_classes_csv, 'r') as file:
    c = [x.strip().split(',') for x in file]
mapping = dict()
c.remove(c[0])
for id, name in c:
    mapping[int(id)] = name


def process_csv(csv_filepath, dataset_folderpath, output_folderpath, category):
    dataset_folderpath = os.path.join(dataset_folderpath, category)
    output_folderpath = os.path.join(output_folderpath, category)
    if os.path.exists(output_folderpath):
        shutil.rmtree(output_folderpath)
    os.makedirs(output_folderpath)
    with open(csv_filepath, 'r') as file:
        contents = [ x.strip().split(',') for x in file]
    for i in range(1, len(contents)):
        filename, id = contents[i][0], int(contents[i][1])
        cl = mapping[id]
        class_folderpath = os.path.join(output_folderpath, cl)
        if not os.path.exists(class_folderpath):
            os.makedirs(class_folderpath)
        image_filepath = os.path.join(dataset_folderpath, filename)
        new_image_filepath = os.path.join(class_folderpath, filename)
        shutil.copy(image_filepath, new_image_filepath)

if __name__ == "__main__":

    process_csv(test_csv_filepath, dataset_folderpath, output_dataset_folderpath, 'test')
    process_csv(train_csv_filepath, dataset_folderpath, output_dataset_folderpath, 'train')