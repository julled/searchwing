#!/usr/bin/env python
####################################################################################
# This file contains all the functions to manipulate images 
# It contains basic functions to detect rois in the given images
####################################################################################
import cv2
import numpy as np


def load_pic(inpath):
    """
    Load rgb picture from specific path with cv2
    :param inpath: path to the image as RGB
    :return: image as BGR
    """
    img = cv2.imread(inpath, cv2.IMREAD_COLOR)  # IMREAD_COLOR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def split_pic(inpic):
    """
    Split picture in 3 channels
    :param inpic: 3 channel picture
    :return: the 3 channles
    """
    img_a, img_b, img_c = cv2.split(inpic)
    return img_a, img_b, img_c

def adjust_contrast_pic(inpic, alpha, beta):
    """
    adjust img contrast
    :param inpic: inputimg
    :param alpha: Simple contrast control - Enter the alpha value [1.0-3.0]
    :param beta: brightness
    :return:
    """
    # alpha = 1.3
    # beta = brightness
    contrast_img = cv2.addWeighted(inpic, alpha, np.zeros(inpic.shape, inpic.dtype), 0, beta)
    return contrast_img


def gauss_blur_pic(inpic, kernelsize, sigmaSize):
    """
    gaussian smoothing of img
    :param inpic:
    :param kernelsize: size of the gaussian blur kernel
    :param sigmaSize: sigma size
    :return:
    """
    gauss_img = cv2.GaussianBlur(inpic, (kernelsize, kernelsize), sigmaX=sigmaSize, sigmaY=sigmaSize)
    return gauss_img


def percentile_threshold_Pic(inpic, percentile):
    """
    threshold input image by a given percentile
    only pixel with a value above the given percentile gets returned
    :param inpic:
    :param percentile: input percentile as integer
    :return:
    """
    tresh = np.percentile(inpic, percentile)
    ret, img_threshed = cv2.threshold(inpic, tresh, 255, cv2.THRESH_BINARY)
    return img_threshed


def Or_Pics(inpic1, inpic2):
    """
    combine 2 pictures by applying logical OR to every single pixel
    :param inpic1: in1
    :param inpic2: in2
    :return:
    """
    ORedPic = cv2.bitwise_or(inpic1, inpic2)
    return ORedPic

def Add_Pics(inpic1, inpic2):
    """
    combine 2 pictures by applying logical AND to every single pixel
    :param inpic1: in1
    :param inpic2: in2
    :return:
    """
    addedPic = cv2.add(inpic1, inpic2)
    return addedPic

def denoise_pic(inpic, kernelsize, iterations):
    """
    denoise binary picture by applying cv2.erode to the picture
    check cv2 docu for params
    :param inpic: inpic
    :param kernelsize:
    :param iterations:
    :return:
    """
    kernel = np.ones((kernelsize, kernelsize), np.uint8)
    denoised = cv2.erode(inpic, kernel, iterations=iterations)
    return denoised

def morph_pic(inpic, kernelsize, operation):
    """
    apply morphologic operation on the binary image
    check cv2 docu for morphologyEx
    :param inpic: inpic
    :param kernelsize:
    :param operation:
    :return:
    """
    kernel = np.ones((kernelsize, kernelsize), np.uint8)
    opening = cv2.morphologyEx(inpic, operation, kernel)
    return opening


def dilate_pic(inpic, kernelsize):
    """
    dilate image
    :param inpic: inpic
    :param kernelsize: kernelsize of the dilate
    :return:
    """
    kernel = np.ones((kernelsize, kernelsize), np.uint8)  # 4,4
    img_dilated = cv2.dilate(inpic, kernel, iterations=1)
    return img_dilated

def getContors_pic(inpic):
    """
    extract contours from binary image by combine all connected pixel
    :param inpic: inpic
    :return:
    """
    im2, contours, _ = cv2.findContours(inpic, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def getBoundingBoxesFromContours(contours):
    """
    convert contoures to boundingboxes
    :param contours:
    :return:
    """
    boundingBoxes = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        bb = [x, y, x + w, y + h]
        boundingBoxes.append(bb)
    return boundingBoxes

def drawBoundingBoxesToImg(inpic,boundingBoxes):
    """
    draw boundingboxes to given image
    :param inpic: inpic
    :param boundingBoxes:
    :return:
    """
    img_bb = inpic.copy()
    for oneBB in boundingBoxes:
        cv2.rectangle(img_bb, (oneBB[0], oneBB[1]), (oneBB[2], oneBB[3]), (255, 0, 0), 3)
    return  img_bb

def calc_grad_pic(inPic, ksize, mode):
    """
    calculate gradient for given picture
    :param inPic: inpic
    :param ksize: size of the kernel
    :param mode: either "sobel", "scharr", "laplace"
    :return:
    """
    ddepth = cv2.CV_16S
    if (mode == "sobel"):
        kw = dict(ksize=ksize, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        grad_x = cv2.Sobel(inPic, ddepth, 1, 0, **kw)
        grad_y = cv2.Sobel(inPic, ddepth, 0, 1, **kw)
        # Converting back to uint8.
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        sobel = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        # sobel_no_blend = cv2.add(abs_grad_x, abs_grad_y)

    if (mode == "scharr"):
        grad_x = cv2.Scharr(inPic, ddepth, 1, 0)
        grad_y = cv2.Scharr(inPic, ddepth, 0, 1)
        # Converting back to uint8.
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        scharr = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        # scharr_no_blend = cv2.add(abs_grad_x, abs_grad_y)

    if (mode == "laplace"):
        # Laplacian.
        lapksize = ksize
        grad = cv2.Laplacian(inPic, ddepth, ksize=lapksize, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        laplace = cv2.convertScaleAbs(grad)

    if (mode == "sobel"):
        return sobel
    if (mode == "scharr"):
        return scharr
    if (mode == "laplace"):
        return laplace


def remove_median(inpic, maxValue):
    """
    remove median from single channel image
    :param inpic: inpic
    :param maxValue: max. possible value of a pixel in the image
    :return:
    """
    histsize = 32
    hist = cv2.calcHist([inpic], [0], None, [histsize], [0, maxValue]).astype(np.int).transpose()

    pixelCount = inpic.shape[0] * inpic.shape[1]
    binPixelCounts = 0
    medianBin = -1
    m = pixelCount / 2
    for idx, oneBin in enumerate(hist[0]):
        binPixelCounts += oneBin
        if (binPixelCounts > m):
            medianBin = idx
            break

    img_m = cv2.subtract(inpic, ((maxValue / histsize) * medianBin))
    return img_m


def write_pic(inpic, path):
    """
    write image to disk
    :param inpic: inpic
    :param path: path to write img to
    :return:
    """
    compr = cv2.IMWRITE_PNG_COMPRESSION;
    quality = 0  # PNG quality is in [0,9] range
    params = [compr, quality]
    cv2.imwrite(path, inpic, params)


def extractImagesFromROIs(boundingBoxes, inpic):
    """
    extract images from given ROIs
    :param boundingBoxes: input bounding boxes
    :param inpic: inpic
    :return: a vector of all the images inside the ROIs
    """
    RoiImages = []
    i = 0
    for bb in boundingBoxes:
        roi = inpic[bb[1]:bb[3], bb[0]:bb[2]]
        RoiImages.append(roi)
        i = i + 1
    return RoiImages


def imgProcess2Gradients(inpic, maxPixelVal, gradMode, gradSize, gaussKernelSize, gausssigmaSize):
    """
    calculate gradient of a given image
    :param inpic: inpic
    :param maxPixelVal: max. possible value of a pixel in the image
    :param gradMode:  either "sobel", "scharr", "laplace"
    :param gradSize: size of the gradient kernel
    :param gaussKernelSize: size of the gaussian blur kernel
    :param gausssigmaSize: gaussian blur sigma
    :return:
    """
    contrasted_img = adjust_contrast_pic(inpic, 1.3, 0)
    # medianed_img=remove_median(contrasted_img,maxPixelVal)
    blurred_pic = gauss_blur_pic(contrasted_img, gaussKernelSize, gausssigmaSize)
    img_grad = calc_grad_pic(blurred_pic, ksize=gradSize, mode=gradMode)  # (blurred_pic)
    return img_grad

def detectROIs(img, gradSize=1, gaussBlurKernelSize=15, openSize=3):
    """
    detect all ROIs in the given image
    :param img: inpic as RGB
    :param gradSize: size of the gradient kernel
    :param gaussBlurKernelSize: size of the gaussian blur kernel
    :param openSize: size of the kernel of the morphologic open operation
    :return:
    """
    #Convert RGB->HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    img_hsv_h, img_hsv_s, img_hsv_v = split_pic(img_hsv)

    gradMode = "sobel"
    gradients_a = imgProcess2Gradients(img_hsv_h, 180, gradMode=gradMode, gradSize=gradSize,
                                       gaussKernelSize=gaussBlurKernelSize, gausssigmaSize=0)
    gradients_b = imgProcess2Gradients(img_hsv_s, 256, gradMode=gradMode, gradSize=gradSize,
                                       gaussKernelSize=gaussBlurKernelSize, gausssigmaSize=0)
    gradients_c = imgProcess2Gradients(img_hsv_v, 256, gradMode=gradMode, gradSize=gradSize,
                                       gaussKernelSize=gaussBlurKernelSize, gausssigmaSize=0)

    gradients_combined_1 = Add_Pics(gradients_a, gradients_b)
    gradients_combined_2 = Add_Pics(gradients_combined_1, gradients_c)

    grad_threshed = percentile_threshold_Pic(gradients_combined_2, 99)
    # img_threshed_denoised = denoise_pic(img_threshed,kernelsize=2,iterations=1)
    img_morph_opened = morph_pic(grad_threshed, openSize, cv2.MORPH_OPEN)  # openSize=2
    img_dilated = dilate_pic(img_morph_opened, 10)
    contours = getContors_pic(img_dilated)
    boundingBoxes = getBoundingBoxesFromContours(contours)

    return boundingBoxes, contours, grad_threshed

def getExtreme2dPoints(contour, debug):
    """
    Approximate start and end points (maximas) of the contour by fitting rotated Rectangle to contour
    Then get centerpoints of the shorter sides of the rotated rectangle
    :param contour: in contour
    :param debug: not used
    :return: Approximated start and end points of contour
    """
    rect = cv2.minAreaRect(contour)

    # get longer side and get angle from longer side against y-axis
    # from: https://stackoverflow.com/a/21427814
    if rect[1][0] < rect[1][1]:
        longer = rect[1][1]
        angle = rect[2] + 180
    else:
        longer = rect[1][0]
        angle = rect[2] + 90

    # generate points from rotated recangle
    # add rotated longer distance to center of rotated Rect to get points
    px = rect[0][0] + longer / 2 * np.sin(np.deg2rad(angle))
    py = rect[0][1] - longer / 2 * np.cos(np.deg2rad(angle))
    pt1 = np.array([px, py], np.int)

    px = rect[0][0] - longer / 2 * np.sin(np.deg2rad(angle))
    py = rect[0][1] + longer / 2 * np.cos(np.deg2rad(angle))
    pt2 = np.array([px, py], np.int)
    """
    if debug == True:
        contour_img = np.zeros((1400, 2100), np.uint8)
        cv2.drawContours(contour_img, [contour], 0, (255, 0, 0), 1)
        cv2.circle(contour_img, (int(pt1[0]), int(pt1[1])), 20, (255, 0, 0), 2)
        cv2.circle(contour_img, (int(pt2[0]), int(pt2[1])), 20, (255, 0, 0), 2)
        box = cv2.boxPoints(rect)  # cv2.boxPoints(rect) for OpenCV 3.x
        box = np.int0(box)
        cv2.drawContours(contour_img, [box], 0, (255, 0, 0), 1)
        plt.imshow(contour_img, cmap="gray")
        plt.show()
    """
    return pt1, pt2
