
# CBIR

Content-Based Image Retrieval (CBIR) is a technique for searching and retrieving images from a database based on their visual content, like color, texture, and shape, rather than metadata or keywords. 

## Content

- [Preview](#preview)
- [Todo List](#todo)
- [Features](#features)
- [Preprocessing](#preprocessing)
    - [Extract Features](#extract-features)
        - [color](#color)
        - [texture](#texture)
        - [shape](#shape)
    - [Normalization](#normalize)
    - [Combine](#combine-features)
- [Relevance Feedback](#relevance-feedback)
- [VGG Modle](#vgg-model)
- [Django](#django)


## Preview

![](./static/preview.gif)

## Todo

- [x] Custom model implementation
- [x] VGG model implementation
- [x] Relevance Feedback
- [x] Web based Application
- [x] Basic UI with Bootstrap
- [X] Readme
- [ ] Documents
- [ ] User ability to choose model
- [ ] Migrate to a real host


## Features

- Image upload and processing
- Retrieval of similar images using CBIR techniques
- Relevance feedback for refining results
- Responsive design with Bootstrap for seamless user experience

## Preprocessing

Image upload and processing
Retrieval of similar images using CBIR techniques
Relevance feedback for refining results
Responsive design with Bootstrap for seamless user experience

### Extract Features

Means converting images into numerical data that represent key visual properties.

#### Color
    Used histograms, color moments in `LAB` color space.

#### Texture
    Used `Gabor` filters, Local Binary Patterns (LBP), or wavelet transforms.

#### Shape
    Used edge detection algorithms like `Canny`, or `Sobel`.

### Normalize

 Scale features to ensure consistency.


### Combine Features

Fuse different features into a single vector if needed.

## Relevance Feedback

in CBIR is an interactive process where users mark retrieved images as relevant or not. The system then updates and refines search results based on this feedback, improving accuracy in finding similar images.

## VGG Model

The **VGG model** is a type of deep learning network used for image recognition. It uses many small 3x3 filters stacked on top of each other to find patterns in images. The most common versions are **VGG16** and **VGG19**, with 16 and 19 layers. It’s popular because it works well for tasks like classifying and comparing images.

## Django

Django is a Python web framework that simplifies building secure, scalable applications with features like ORM and authentication. Bootstrap is a front-end framework for creating responsive, visually appealing interfaces. Together, they streamline backend development and UI design.

