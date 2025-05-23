import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
Restore images using image processing

in a single image, there is not much information because the true luminance values are unknown

Entire columns are affected because shutter travels horizontally

We can average luminance values by column and try a few things to correct


1. find energy minimization within a single image
    Find mean and move each column to match the mean

2. Choose a well exposed column and have each column match that one

3. Match groups of columns to further reduce noise
    could do column pyramid type thing

4. joint minimization across images with same shutter speed to reduce noise from world

could look at column histogram and correct by histogram (find a similar histogram and move the mean)




expert assumptions from world

1. shutters move with constant velocity, but different velocity, so difference in timing should be linear between left and right side

2. assume that film exposes linearly, (2x longer exposure = 2x brighter). none of these exposures should be bright enought to need to model reciprocity?




'''

def main():
    image_path = 'data/028318020013.jpg'
    single_column_histogram_correct(image_path)

def column_histogram():
    pass

def single_column_histogram_correct(path_to_image, target=0.5):
    '''
    1. choose a target column, we will try to match the exposure setting in this column, or group of columns
    2. calculate histogram, really just need mean, for each column, move mean to match, or move such that minimize malhalanobis distance/stadistical distance (distnace between distributiosn) to match
        2a. reason to use a distribution or median or something is to reject outliers
    3. move each column in brightness to match
        3a. maybe some color theory here especially when it comes to color film
    '''
    image = cv2.imread(path_to_image)

    r,c = image.shape[:2]

    target_c = int(target * c)

    target_mean = np.mean(image[:, target_c])
    target_std = np.std(image[:, target_c])

    # experiment with treating gain as a multiplication or as an addition

    out_image_mult = np.zeros(image.shape, dtype=np.uint8)
    out_image_add = np.zeros(image.shape, dtype=np.uint8)

    gains = []

    add_gains = []
    mult_gains = []

    means = []

    stds = []
    for rectify_column in range(len(image[0])):
        # compare this column to the target
        check_mean = np.mean(image[:, rectify_column])
        check_std = np.std(image[:, rectify_column])

        means.append(check_mean)
        stds.append(check_std)

        # calculate gain using addition
        add_gain = target_mean - check_mean
        add_gains.append(add_gain)
        out_image_add[:, rectify_column] = (image[:, rectify_column] + add_gain).astype(np.uint8)

        # calculate gain using multiplication
        mult_gain = target_mean / check_mean
        mult_gains.append(mult_gain)
        out_image_mult[:, rectify_column] = (image[:, rectify_column] * add_gain).astype(np.uint8)


    # save the images
    cv2.imwrite('add.png', out_image_add)
    cv2.imwrite('mult.png', out_image_mult)

    ### plot everything
    mean_ax,_ = plt.subplot(4,1,1)
    std_ax,_ = plt.subplot(4,1,2)
    add_gain_ax,_ = plt.subplot(4,1,3)
    mult_gain_ax,_ = plt.subplot(4,1,4)

    x = list(range(len(image[0])))
    # plot mean by column
    mean_ax.plot(x, means)
    mean_ax.set_title('mean by column')

    # plot std by column
    std_ax.plot(x, stds)
    std_ax.set_title('std by column')

    # plot add gain by column
    add_gain_ax.plot(x, add_gains)
    add_gain_ax.set_title('add gain by column')

    # plot mult gain by column
    mult_gain_ax.plot(x, mult_gains)
    mult_gain_ax.set_title('mult gain by column')

    plt.show()




if __name__=='__main__':
    main()