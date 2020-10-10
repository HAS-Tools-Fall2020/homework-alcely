## Assignment 7: Forecast #7, Code Review
**Author: Alcely Lau**

**Reviewer: Alexa Marcovecchi**

**Date: 10/12/2020**
___
#### Table of Contents:
1. [ Running script instructions](#instructions)
1. [ Flow Forecasts](#forecast)
1. [ Code Review](#Review)

___
<a name="instructions"></a>
#### Running script instructions
Welcome, Alexa to my repo!
I hope this task will be not time-consuming for you.

Please, follow the next steps:
1. Clone my repo `homework-alcely`.
1. Download the stream gauge observations from the USGS NWIS website using the following parameters:
  - Station  09506000 Verde River Near Camp Verde
  - Daily Data
  - Parameter 00060 Discharge (mean)
  - Quick access: **[go to dataset](https://waterdata.usgs.gov/nwis/dv?referred_module=sw&site_no=09506000)**
  - Start date = 1989-01-01
  - End date = 2020-10-10
  - Select 'tab separated'
  - Save the file in `homework-alcely\data` and called it `streamflow_week7.txt`.


3. Open the file `lau_HW7.py` in VS code. Close your eyes and run everything, if you trust me. But let's do it step by step. Check if you need to install any packages.
1. You need to run each cell.
1. If you have any error in line 72, replace the string `r'..\..\data'` with the complete path in your computer.
1. Everything was set to run the forecast #7. Thus, ignore the comments that said `MODIFY`, those input values were already modified to save you time.
1.The **Autoregressive model predictions** are generated in the cell between lines 167 and 185.
1. The **My_brain model predictions** are generated in the cell between lines 222 and 240. Use this flows for my forecast entries. I wish you bring me luck this week!
1. Then, you have an optional section for plots. If it shows an error probably we jump one cell without run.

___
<a name="forecast"></a>
#### Flow Forecasts
**Using Autoregressive Model**:
- Week1: *(insert value)*
- Week2: *(insert value)*

**Using My_brain Model**:
- Week1: *(insert value)*
- Week2: *(insert value)*

___
<a name="Review"></a>
#### Code Review

**1. Is the script easy to read and understand?**
 - Are variables and functions named descriptively when useful?
 - Are the comments helpful?
 - Can you run the script on your own easily?
 - Are the doc-strings useful?

*(insert comments)*

**Score:** *(insert value)*

**2. Does the code follow PEP8 style consistently?**
 - If not are there specific instances where the script diverges from this style?

*(insert comments)*

**Score:** *(insert value)*

**3. Is the code written succinctly and efficiently?**
 - Are there superfluous code sections?
 - Is the use of functions appropriate?
 - Is the code written elegantly without decreasing readability?

*(insert comments)*

**Score:** *(insert value)*

___
#### Rubric
(Adapted from Kyle Mandli [Intro to Numerical Methods](https://github.com/mandli/intro-numerical-methods))
![](assets/code_review_rubric-ff0ecab3.png)
