# views.py
from django.shortcuts import render
from .models import Student
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.express as px
import plotly.graph_objects as go

def calculate_age_intervals(max_age):
    intervals = np.arange(0, max_age + 11, 10)  # Adjusted to include maximum age
    labels = [f'{i}-{i+10}' for i in range(0, max_age + 1, 10)]  # Adjusted to include maximum age
    return intervals, labels

def index(request):
    # Load dataset from the model
    queryset = Student.objects.all()
    dataset = pd.DataFrame(list(queryset.values()))

    # Calculate age intervals and frequencies
    max_age = dataset['age'].max()
    intervals, labels = calculate_age_intervals(max_age)
    dataset['age_intervals'] = pd.cut(dataset['age'], bins=intervals, labels=labels, right=False)
    freq_table = dataset['age_intervals'].value_counts().reset_index()
    freq_table.columns = ['Age Interval', 'Frequency']
    freq_table['Age Interval'] = pd.Categorical(freq_table['Age Interval'], categories=labels, ordered=True)
    freq_table = freq_table.sort_values('Age Interval')

    # Filter out age intervals with zero frequency
    freq_table = freq_table[freq_table['Frequency'] > 0]

    # Calculate statistics
    mean = dataset['age'].mean()
    mode_value = freq_table.loc[freq_table['Frequency'].idxmax()]
    mode = f"{mode_value['Age Interval']} (Frequency: {mode_value['Frequency']})"
    median_class = freq_table.loc[freq_table['Frequency'].cumsum() >= (freq_table['Frequency'].sum() / 2)].iloc[0]['Age Interval']
    median = dataset['age'].median()
    std_dev = dataset['age'].std()
    mean_dev = dataset['age'].apply(lambda x: abs(x - mean)).mean()  # Calculate mean absolute deviation manually
    skew = dataset['age'].skew()

    # Calculate z-scores
    mean = dataset['age'].mean()
    std_dev = dataset['age'].std()
    dataset['z_score'] = (dataset['age'] - mean) / std_dev

    # Skewness visualization
    x = np.linspace(min(dataset['age']), max(dataset['age']), 100)
    p = norm.pdf(x, mean, std_dev)
    skew_fig = px.line(x=x, y=p, labels={'x': 'Age', 'y': 'Probability Density'})
    skew_fig.add_trace(go.Scatter(x=x, y=p, mode='lines', name='Normal Distribution'))
    skew_fig.update_layout(title="Skewness Visualization", xaxis_title="Age", yaxis_title="Probability Density",
                       plot_bgcolor='rgba(0,0,0,0)',  # Set background transparency
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))  # Adjust legend position
    skew_fig.add_annotation(
    x=x[0],
    y=p[0],
    text=f"Skewness: {skew:.2f}",
    showarrow=False,
    font=dict(color="red", size=12)
    )
    skew_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gray')  # Add gridlines on x-axis
    skew_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gray')  # Add gridlines on y-axis


    # Cumulative frequency vs. Upper Class Boundary
    freq_table['Cumulative Frequency'] = freq_table['Frequency'].cumsum()
    fig1 = px.scatter(freq_table, x=freq_table['Age Interval'].apply(lambda x: int(x.split('-')[1])), y='Cumulative Frequency', 
                labels={'x': 'Upper Class Boundary', 'y': 'Cumulative Frequency'}, 
                title='Cumulative Frequency vs. Upper Class Boundary')

    # Update traces to include lines and markers
    fig1.update_traces(mode='lines+markers')

    # Update layout to set background transparency, adjust legend position, and add gridlines
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set background transparency
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),  # Adjust legend position
                  xaxis=dict(showgrid=True, gridwidth=1, gridcolor='gray'),  # Add gridlines on x-axis
                  yaxis=dict(showgrid=True, gridwidth=1, gridcolor='gray'))  # Add gridlines on y-axis


    # Normal Curve of Z-Scores
    z_values = np.linspace(-3, 3, 1000)
    prob_values = norm.pdf(z_values)
    z_fig = px.line(x=z_values, y=prob_values, labels={'x': 'Z-score', 'y': 'Probability Density'})

    z_fig.update_layout(title="Normal Curve of Z-Scores", xaxis_title="Z-score", yaxis_title="Probability Density",
                    plot_bgcolor='rgba(0,0,0,0)',  # Set background transparency
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))  # Adjust legend position
    z_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gray')  # Add gridlines on x-axis
    z_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gray')  # Add gridlines on y-axis


    context = {
        'dataset': dataset,
        'freq_table': freq_table,
        'mean': mean,
        'mode': mode,
        'median': median,
        'median_class': median_class,
        'std_dev': std_dev,
        'mean_dev': mean_dev,
        'skew': skew,
        'skew_fig': skew_fig.to_html(full_html=False),
        'fig1': fig1.to_html(full_html=False),
        'z_fig': z_fig.to_html(full_html=False)
    }

    return render(request, "index.html", context)



 