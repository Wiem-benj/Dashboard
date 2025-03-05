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
![image](https://github.com/user-attachments/assets/69cb3f87-40f8-4ac1-adf1-8345b27c473d)
#### Below is the categorical features
![image](https://github.com/user-attachments/assets/3cf015dd-1491-4cd0-9939-3b610069548a)

3- Select 'Charts' tab to generate plots (scatter, line, area, bar plots) by selecting the plot the xaxis feature (mandatory field for all the chart types), the yaxis of the plot (mandatory field for all chart types except bar plot) and the color (Optional). 
For the Bar plot selecting xaxis without selecting the yaxis result in bar plot with values on the xaxis and their counts on the yaxis.
The color is the paramater color in the plots functions (Line, Scatter, Area, and Bar). It serves like a 3rd dimension where it gives more insights to the selected data in the xaxis and yaxis.
![image](https://github.com/user-attachments/assets/505cb273-64fc-44a7-82c7-67a64b3146c9)

4- Select 'Exploratory Data Analysis' to visualize the correlation or the Parallel coordinate plot between numerical features by selecting them from the dropdown list 'Select the features'. The dropdown list of 'Select the nan handling strategy' is set by default as 'Drop', so that when the Parallel coordinate or the correlation plot is generated it drops the missing values rows of the features selected. If the handling strategy is set to 'Mean', then the Parallel coordinate and the correlation plot will be generated with all the data including the missing values set to the average.
#### Below is a Correlation plot
![image](https://github.com/user-attachments/assets/f029dcc0-d957-4f5a-9183-83a1e9364c7c)
#### Below is a Parallel coordinate plot
![image](https://github.com/user-attachments/assets/08ef9e16-e0c0-4ac3-a063-cf7b62537304)


Please kindly note that the processing of large data with more than 30k records may seems slow in this version of code especially for the case of excel files extension.

