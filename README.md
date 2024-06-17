# Snapp MLE Task 🤖

<div align="center">

[![Build status](https://github.com/rezashabrang/content-duplication-detector/workflows/build/badge.svg?branch=master&event=push)](https://github.com/rezashabrang/content-duplication-detector/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/badge/python-3.12-yellow)](https://www.python.org/downloads/release/python-3120/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/rezashabrang/content-duplication-detector/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/rezashabrang/content-duplication-detector/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/rezashabrang/content-duplication-detector/releases)
![Coverage Report](assets/images/coverage.svg)

Snapp Machine Learning Engineer Task.

</div>

## Overview 📝

This repo focuses on analyzing the Snapp ride dataset from Tehran, from geospatial information for each journey's origin and destination.

-   The `rd` folder contains a notebook for R&D part. `entrances.html` visualizes the entrance points for each location.
-   In [Task Journey](#task-journey-️) part you can view the step-by-step process of the task.

## Task Journey 🗺️

<img src="./images/journey.svg" alt="overall journey"/>

Here we are going to explain the steps of the task that happened. You can view the image at top to get the general idea.

### Pre-Processing

First off, the given data was exploded. We wanted the points independently regardless of their type (origin, destination).

### Data Visualzition

Then we visualized the data on the map to see what we are dealing with, how the data is distributed and the density of points around the places mentioned in the hint, specially the entrances.

`Kepler` was used for this visualization.

### Finding Polygons

After inspecting the data now we had a sense of data. We needed to see how we can break the problem so we can solve it. The ideas are explained throughly inside the R&D notebook. In the end we found that the best way to break the problem is to find the polygons of the places. We gathered the polygons from open source data sources.

### Buffered polygons

Then depending on the characteristics of the polygons we buffered them.

### Assigning points

Based on the buffered polygon points were filtered and assigned to each individual place.

### Polygon X Points Visualization

The original polygons, buffered polygons and the points were visualized on the map.

### Clustering

Here resides the ML algorithm used for clustering which by reasoning between algorithms the chosen one is `HDBSCAN`.

### Assessing Entrances

After clustering and finding the entrances we now visualized them on the map and tried to reason visually as to where the entrances are.

The Snapp app was used to check the accuracy of the entrances.

After inspecting the entrances we went through a cycle of tuning the buffer distance for each polygon and finding the optimal hyper-parameter for the clustering algorithm. The cycle is shown with red background on the image. In this cycle we fine-tuned our approach for the end goal of finding the optimal entrances.

### Final Visualization

After finding the best parameters for each step of our approach, the final visualiztion containing only the entrances was created (`rd/entrances.html`).

## Future Enhancements 🚀

Although this repo is in a scope of a task but here some tips, improvements and enhancements are listed that are out-of-scope for this task but could be elaborated more on later.

-   <b>Defining a metric for the clustering evaluation</b>

    The entrances were assesed visually but looking at the big picture maybe some metrics like `Silhouette Score` or `Davies-Bouldin Index` could be used for automatic evaluation.

-   <b>DBSCAN Algorithm</b>

    As mentioned one of the reasons. `HDBSCAN` was used because of its flexibility. But by inspecting the geospatial data more and even consulting with domain expertise the `DBSCAN` can be the better choice of algorithm by tuning the parametrs accurately. That of course need to be researched (For example by defining groundtruth entrance locations and then comparing the distance of centroids each algorithm calculates with the entrances).

-   <b>Finding Crowded Places</b>

    In hint part the places were given beforehand but in real life scenario we may not know all the crowded places like malls and hospitals. Also new structures may be opened in time. So we can develop a system to find these existing places using clustering and alongside some other helpers. Also we could develop an anomaly detection system for finding new emerging places.

-   <b>Better Heuristic for `min_cluster_size`</b>

    This parameter was choosen by trial and error. We could have used some heuristics to find the optimal value. This is pure speculation but for example we could use `K-means` and some automatic clustering method for it to find some clusters and calulate the density for each of them to get a rough estimate for this parameter and then perform `HDBSCAN`. This would leads to more accurate clusters.
