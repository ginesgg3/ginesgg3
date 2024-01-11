# -*- coding: utf-8 -*-
"""
Author: Ginés González Guirado

Email: ginesgg3@gmail.com

Date: 26/10/2023

Objective: Manage information from an astronomical image. Open two images and
add them. Then, finding the brighter pixel and, finally, applying a mask
to measure the noise of the image, creating 10 randomly distributed
apertures of (10,10) pixels.
"""

# Libraries
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import os


# Functions

# Function for section (1)
"""
This function is used to open and check the existence and the path of the 
.fits files. It also checks that the dimensions of both images are the same.
"""
def open_and_check_files_existence(v_file: str, i_file: str):
    # Check if both files exist using os.path.isfile
    if not os.path.isfile(v_file) or not os.path.isfile(i_file):
        if not os.path.isfile(v_file) and not os.path.isfile(i_file):
            raise FileNotFoundError("Both files do not exist. \
                                    Please provide valid file paths.")
        elif not os.path.isfile(v_file):
            raise FileNotFoundError(f"The file '{v_file}' does not exist. \
                                   Please provide a valid path for this file.")
        else:
            raise FileNotFoundError(f"The file '{i_file}' does not exist. \
                                   Please provide a valid path for this file.")

    # Open the V-band FITS file
    hdu1 = fits.open(v_file)    # To open the file
    image1 = hdu1[0].data       # Image: matrix with the values of the pixels
    header1 = hdu1[0].header    # Header of the image
    naxis1_1 = header1.get("NAXIS1")   # dimension of the image in the x axis
    naxis2_1 = header1.get("NAXIS2")   # dimension of the image in the y axis

    # Open the I-band FITS file
    hdu2 = fits.open(i_file)    # To open the file
    image2 = hdu2[0].data       # Image: matrix with the values of the pixels
    header2 = hdu2[0].header    # Header of the image
    naxis1_2 = header2.get("NAXIS1")   # dimension of the image in the x axis
    naxis2_2 = header2.get("NAXIS2")   # dimension of the image in the y axis
    
    
    # Check dimensions between both images
    if image1.ndim != image2.ndim:
        raise ValueError("Image dimensions do not match between the two files")
    # Check the shape and therefore the dimension between both images
    if image1.shape != image2.shape:
        raise ValueError("Image dimensions do not match between the two files")
    
    # Check dimensions between image V and what appear in NAXIS of its header
    if image1.shape != (naxis1_1,naxis2_1):
        raise ValueError("The dimensions of image V, do not match with the \
                         dimensions that appear in NAXIS of its header")
    
    # Check dimensions between image I and what appear in NAXIS of its header
    if image2.shape != (naxis1_2,naxis2_2):
        raise ValueError("The dimensions of image I, do not match with the \
                         dimensions that appear in NAXIS of its header")
    
    # Check dimensions between NAXIS of image V header and NAXIS of image I header
    if naxis1_1 != naxis1_2 or naxis2_1 != naxis2_2:
        raise ValueError("Image dimensions do not match between the two \
                         files or with the header values.")

    return image1, header1, image2, header2


# Functions for section (2)

#This is a function to sum the images V and I.
def sum_images(image_1,image_2):
    image = image_1 + image_2   # Sum of the images
    if image.shape != image_1.shape and image.shape != image_2.shape:
        raise ValueError("Image dimensions do not match, so the sum is wrong \
                         and it is not element by element.")
    return image

# Function to find the brighter pixel in section (2)
def most_brighter_pixel(img):
    # Find the index (row, column) of the brightest pixel while ignoring NaN values
    brightest_pixel_index = np.unravel_index(np.nanargmax(img), img.shape)
    
    # Get the value of the brightest pixel
    brightest_pixel_value = img[brightest_pixel_index]
    
    return brightest_pixel_value, brightest_pixel_index
  
  
# Function for the combination of the mask and the image in section (3)
def open_mask_and_multiply_by_image(mask: str, image):
    # Check if mask file exists
    if not os.path.isfile(mask):
        raise FileNotFoundError("Mask file does not exist. \
                                Please provide valid file paths.")
    # Open the mask FITS file
    hdu_mask = fits.open(mask)        # To open the file
    image_mask = hdu_mask[0].data     # Image: matrix with the values of the pixels
    header_mask = hdu_mask[0].header  # Header of the image
    
    noise_image = image_mask * image  # Multiplication of the elements in the same position
    
    return noise_image, image_mask

# Function to calculate the percentage of the image that the mask (the NaN elements) is covering
def calculate_mask_coverage_with_nan(mask):
    # Count the number of NaN pixels in the mask
    nan_mask_coverage = np.sum(np.isnan(mask))
    
    # Get the total number of pixels in the image
    total_pixels = mask.size
    
    # Calculate the percentage of coverage
    coverage_percentage = (nan_mask_coverage / total_pixels) * 100.0
    
    return coverage_percentage



# Function to measure the noise in ten random apertures (10,10)
def measure_noise_with_random_apertures(noise_image, num_apertures, aperture_shape):
    # Create an array to store the noise measurements for each aperture
    noise_measurements = np.empty(num_apertures)
    noise_measurements[:] = np.nan  # Initialize all values as NaN

    # Get the dimensions of the noise image
    noise_image_height, noise_image_width = noise_image.shape

    # Loop to create and measure noise in random apertures
    aperture_counter = 0
    while aperture_counter < num_apertures:
        # Generate random coordinates for the top-left corner of the aperture
        top_left_x = np.random.randint(0, noise_image_width - 
                                       aperture_shape[1] + 1)
        top_left_y = np.random.randint(0, noise_image_height - 
                                       aperture_shape[0] + 1)

        # Extract the aperture from the image
        aperture = noise_image[top_left_y:top_left_y + aperture_shape[0],
                               top_left_x:top_left_x + aperture_shape[1]]

        # Count the number of NaN values in the aperture
        num_nan_values = np.sum(np.isnan(aperture))

        # Calculate the total number of pixels in the aperture
        total_pixels = aperture_shape[0] * aperture_shape[1]

        # Check if the percentage of NaN values exceeds 40%
        if (num_nan_values / total_pixels) <= 0.4:
            # Calculate the standard deviation of the pixels within the aperture while ignoring NaN measurements
            aperture_noise = np.nanstd(aperture)
            # Store the noise measurement in the array
            noise_measurements[aperture_counter] = aperture_noise
            aperture_counter += 1  # Move to the next aperture

    # Calculate the average noise value while ignoring NaN measurements
    average_noise = np.nanmean(noise_measurements)

    return average_noise




"""
Constants.
"""
# Files that I want to open with the functions that I have done
v_file = "10049_cosmos_V.fits"
i_file = "10049_cosmos_I.fits"
mask = "mask_for_10049_cosmos.fits"


"""
Code.
"""
# Calling the function to open and check the files existence and storing the return values in variables
image1,header1,image2,header2 = open_and_check_files_existence(v_file, i_file)

# Graphical representation of image V using matplotlib
fig, ax = plt.subplots(figsize=(10,10),nrows=1,ncols=1)
image11 = ax.imshow(-2.5*np.log10(image1)+26.493+(5*np.log10(0.03)), 
                    origin="lower", cmap="viridis", vmin=18, vmax=30)
fig.colorbar(image11, ax=ax, fraction=0.046, pad=0.04)

# Graphical representation of image I using matplotlib
fig, ax = plt.subplots(figsize=(10,10),nrows=1,ncols=1)
image22 = ax.imshow(-2.5*np.log10(image2)+26.493+(5*np.log10(0.03)), 
                    origin="lower", cmap="viridis", vmin=18, vmax=30)
fig.colorbar(image22, ax=ax, fraction=0.046, pad=0.04)



# Calling the function to add the images and storing the return value in variable (image)
image = sum_images(image1,image2)

# Graphical representation of the sum of the images using matplotlib
fig, ax = plt.subplots(figsize=(10,10),nrows=1,ncols=1)
image_ = ax.imshow(-2.5*np.log10(image)+26.493+(5*np.log10(0.03)), 
                   origin="lower", cmap="viridis", vmin=18, vmax=30)
fig.colorbar(image_, ax=ax, fraction=0.046, pad=0.04)

# Calling the function to find the brighter pixel, assuming the image is an array
# and storing the return values in variables and printing them on the screen
brightest_value, brightest_position = most_brighter_pixel(image)

print(f"Brightest Pixel Value: {brightest_value}")
print(f"Brightest Pixel Position (Row, Column): {brightest_position}")




# Calling the function to multiply the image by the mask and storing the return values in variables
noise_image, image_mask = open_mask_and_multiply_by_image(mask, image)

# Calling the function to calculate the mask coverage percentage
mask_coverage_percentage = calculate_mask_coverage_with_nan(image_mask)

# Printing the mask coverage percentage
print(f"Image percentage covered by the mask:{mask_coverage_percentage:.2f}%")


# Graphical representation of noise image using matplotlib
fig, ax = plt.subplots(figsize=(10,10),nrows=1,ncols=1)
image_ = ax.imshow(-2.5*np.log10(noise_image)+26.493+(5*np.log10(0.03)), origin="lower", cmap="viridis", vmin=18, vmax=30)
fig.colorbar(image_, ax=ax, fraction=0.046, pad=0.04)




# Measure noise in 10 random 10x10 pixel apertures in noise_image
num_apertures = 10   # Number of apertures
aperture_shape = (10,10)  # tuple with the shape of the aperture

# Calling the function to create the apertures and calculate the average noise
average_noise = measure_noise_with_random_apertures(noise_image,num_apertures,aperture_shape)

# Display the final noise value
print(f"Final noise value (average of {num_apertures} apertures): {average_noise}")




