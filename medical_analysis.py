import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#import csv file
df =pd.read_csv('medical_exam.csv')

#use dataframe to create new height and BMI column
new_h = df['height'] * 10**-2
BMI = df['weight']/(new_h **2)
# if BMI > 25:
# over_weight = 1
# else:
#     over_weight = 0
# over_weight = pd.Series(['1', '0']

df['overweight'] = BMI.apply(lambda x: 1 if x > 25 else 0)

#categorical plot function
def draw_cat_plot():
    # df_cat =df[['cholesterol', 'gluc']].value_counts()
    # df_cat.plot(kind= 'bar', color = 'blue')
    # plt.show()
    df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
    df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)
    df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2)).apply(lambda x: 1 if x > 25 else 0)

    df_cat =  pd.melt(df, id_vars=['cardio'], value_vars =['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    df_cat = df_cat.rename(columns = {'variable': 'variable', 'value':'value'})

    # plot categorical data
 
    catplot = sns.catplot(x = 'variable', hue = 'value', data = df_cat, kind= 'count', col = 'cardio')
    catplot.set_axis_labels('variable', 'total')
    fig = catplot.fig
    # Use fig.savefig('catplot.png') to save cat plot in png format
    return fig
fig = draw_cat_plot()
plt.show()

# heat map function and correlation matrix
def draw_heat_map():
    # 1. Filter for valid systolic and diastolic pressure (ap_lo <= ap_hi)
   
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                 (df['height'] >= df['height'].quantile(0.025)) & 
                 (df['height'] <= df['height'].quantile(0.975)) & 
                 (df['weight'] >= df['weight'].quantile(0.025)) & 
                 (df['weight'] <= df['weight'].quantile(0.975))]

     # Calculate the correlation matrix
    corr = df_heat.corr()

      # Generate a mask for the upper triangle of the heatmap
    mask = np.triu(np.ones_like(corr, dtype='bool'))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    sns.heatmap(corr, ax= ax, mask=mask, annot =True, fmt='.1f', cmap = 'coolwarm', center=0)
    # Use fig.savefig('heatmap.png') to save heat map in png format
    return fig
fig = draw_heat_map()
plt.show()
