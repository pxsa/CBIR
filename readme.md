
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
- [Django](#django)


## Preview


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

## Django

Django is a Python web framework that simplifies building secure, scalable applications with features like ORM and authentication. Bootstrap is a front-end framework for creating responsive, visually appealing interfaces. Together, they streamline backend development and UI design.

