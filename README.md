# Dashboard
An interactive Dashboard developped with Plotly for data visualization.

Please note that the file 'Dash_board.py' is the main file of the dashboard application to be run. The second python file 'backend_logic.py' contains the functions that are called within the callback functions.

When running the dashboard:

1- Select a csv or excel file to be processed.
![image](https://github.com/user-attachments/assets/6bc5c956-0545-4731-86cb-485a7b13081c)

When you see the file name appears on the right hand side of the upload button, it means your data is uploaded and ready to be used 

2- Select the tab 'Data analysis' to see a summary of the data analysis for numerical features (1st table) and categorical features (2nd table).
The data analysis summary for numerical features include: percentage of missing values, number of zeros, statistical measurements (mean, std, median, min, max), distribution plot.
The data analysis summary for categorical features include: percentage of missing values, number of unique values, top frequent value and its count, average length of string, and the distribution plot.
#### Below is the numerical features
![Data analysis - numeric features](https://github.com/user-attachments/assets/a53c07ac-9f61-4fdc-a2f3-ee40324d2283)
#### Below is the categorical features
![Data analysis - categorical features](https://github.com/user-attachments/assets/03382c65-7acc-472c-9e6f-de306ce76d23)

3- Select 'Charts' tab to generate plots (scatter, line, area, bar plots) by selecting the plot the xaxis feature (mandatory field for all the chart types), the yaxis of the plot (mandatory field for all chart types except bar plot) and the color (Optional). 
For the Bar plot selecting xaxis without selecting the yaxis result in bar plot with values on the xaxis and their counts on the yaxis.
The color is the paramater color in the plots functions (Line, Scatter, Area, and Bar). It serves like a 3rd dimension where it gives more insights to the selected data in the xaxis and yaxis.
![scatter chart](https://github.com/user-attachments/assets/86d3ea30-39d4-4d14-b75c-a2512b05df29)

4- Select 'Exploratory Data Analysis' to visualize the correlation or the Parallel coordinate plot between numerical features by selecting them from the dropdown list 'Select the features'. The dropdown list of 'Select the nan handling strategy' is set by default as 'Drop', so that when the Parallel coordinate or the correlation plot is generated it drops the missing values rows of the features selected. If the handling strategy is set to 'Mean', then the Parallel coordinate and the correlation plot will be generated with all the data including the missing values set to the average.
#### Below is a Correlation plot
![Correlation](https://github.com/user-attachments/assets/adf9ecbe-d809-487a-8b28-f7494fab638d)
#### Below is a Parallel coordinate plot
![parallel coordinate](https://github.com/user-attachments/assets/679632fb-8b7f-4f75-8e73-2dfc2326411a)


Please kindly note that the processing of large data with more than 30k records may seems slow in this version of code especially for the case of excel files extension.

