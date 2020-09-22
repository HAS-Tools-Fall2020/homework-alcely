## Assignment 4: Forecast week 4 & Numpy Arrays
**Name: Alcely Lau**

**Date: 09/20/2020**

___
### Grade
3/3 - Great Job, really nice write up!  Next time maybe use the Atom plug in for your graphics though that way I can  see them in atom and not just online. 
___

#### Forecast summary

I have a good feeling about this forecast.

For this week I followed the next steps:

1. Download the stream gauge observations from the USGS NWIS website, [mapper](https://maps.waterdata.usgs.gov/mapper/).

2. Explore the data using **numpy arrays**. First, checking the streamflow registered in the last 3 weeks (*I am getting closer to the real weekly mean!*). Then, I analyzed the mean, quantiles (0%, 33%, 50%, 66%, and 100%) and the histograms for an specific period:
  + Using all years in the dataset, without the year 2020, for September.
  + Using the last 10 years, without the year 2020, for September.
  + Using the year 2019, for September.
  + Using the average of the previous week and the forecast week.

____
#### Assignment questions

1. Include discussion of the quantitative analysis that lead to your prediction. This can include any analysis you complete but must include at least two histograms and some quantitative discussion of flow quantiles that helped you make your decision.

**Last 1 week summary:**
  + min: 53.3
  + max: 58.2
  + mean: 56.2
  + std: 1.75

**Statics analysis**

|      years|    mean|    q=0%|   q=33%|   q=50%|   q=66%|  q=100%|
|:---------:|:------:|:------:|:------:|:------:|:------:|:------:|
|  All years|  180.08|    48.6|   95.98|  115.00|  141.00| 5590.00|
|    >= 2009|  126.28|    48.6|   91.74|  105.50|  130.94|  776.00|
|       2019|   66.49|    48.6|   52.76|   58.85|   **61.31**|  121.00|

**Histograms**

![alt text](https://github.com/HAS-Tools-Fall2020/homework-alcely/blob/master/assignment_4/Histogram_historical.png "Histogram_historical")

![alt text](https://github.com/HAS-Tools-Fall2020/homework-alcely/blob/master/assignment_4/Histogram_2019_09.png "Histogram_2019_09")

Observing at the histogram of September 2019 (*the second histogram*), the most frequent streamflows are in the range between ~35 to ~65 cfs. Hence, let think that the intensity of the 2020 drought will decrease and my week 1 forecast will be the 66% quantile of the year 2019.

-----
2. Describe the variable flow_data:
  - What is it?
  - What type of values it is composed of?
  - What is are its dimensions, and total size?


   **Response:** The variable `flow_data` is a **numpy.ndarray** . It is composed of **floats** (*in a numpy array must be the same data type*). It has **2 dimensions** and its total size is: **(11585, 4)** , where (rows, columns).

-----
3. How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?
**Response:**

| September | Forecast value (cfs) | Number of times | Percentage |
|:---------:|:--------------------:| :--------------:|:----------:|
|    week 1 |                   65 |             876 |    92.31 % |
|    week 2 |                   67 |             870 |    91.68 % |
|    week 3 |                54.05 |             921 |    97.05 % |
|   average |                62.02 |             883 |    93.04 % |

-----

4. How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)
**Response:**

| Years | September | Forecast value (cfs) | Number of times | Percentage |
|:-----:|:---------:|:--------------------:| :--------------:|:----------:|
|<= 2000|    week 1 |                   65 |             359 |    37.83 % |
|<= 2000|    week 2 |                   67 |             356 |    37.51 % |
|<= 2000|    week 3 |                54.05 |             360 |    37.93 % |
|<= 2000|   average |                62.02 |             360 |    37.93 % |
|>= 2010|    week 1 |                   65 |             276 |    29.08 % |
|>= 2010|    week 2 |                   67 |             273 |    28.77 % |
|>= 2010|    week 3 |                54.05 |             302 |    31.82 % |
|>= 2010|   average |                62.02 |             279 |    29.40 % |

-----

5. How does the daily flow generally change from the first half of September to the second?

   **Response:** The average daily flows on the first half of September is: **178.07** cfs , in contrast, on the second half of September is: **168.88** cfs.
