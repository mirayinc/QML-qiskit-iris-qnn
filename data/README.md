# Iris dataset

`iris.csv` is a reference copy of the classic Iris dataset (150 samples, 4 features, 3 classes).
It was exported from `sklearn.datasets.load_iris()`.

**The notebooks do not read this file.** They load the data directly with
`sklearn.datasets.load_iris()`. The CSV is here for inspection and reuse.

| column | description |
|---|---|
| sepal_length_cm, sepal_width_cm, petal_length_cm, petal_width_cm | features |
| target | 0 = setosa, 1 = versicolor, 2 = virginica |
| species | class name |

Source: R. A. Fisher (1936), "The use of multiple measurements in taxonomic problems";
also available from the UCI Machine Learning Repository.
