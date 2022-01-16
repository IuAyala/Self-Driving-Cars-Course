# Road Sign Classification Section
This section we will perform road sign classification using Machine Learning algorithms.

# TODO:
- Open the file "1_hot.ipynb" run all the cells of the notebook and make sure that you understand how HOG works
- Open the "hog_svm.py" file and run it to make sure it works as expected
    - Modify the code to do exactly the same but without using "sklearn.pipeline.Pipeline"
    - You will have to implement the operations sequentially (RGB2Grayscale, Hogtransform, ...) ensure that you understand the difference between "fit" and "transform"
- Run the file "3_cnn.ipynb", you don't have to understand it yet (you will be able to understand it after the deep learning section), simply compare the results of using HOG+SVM vs Deep Learning (CNN)