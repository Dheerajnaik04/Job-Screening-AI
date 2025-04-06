import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 1. Candidate Experience Improvement
candidate_exp = {
    'Metric': ['Application Response Time', 'Process Transparency', 'Feedback Quality', 'Interview Scheduling', 'Communication'],
    'Traditional (hrs)': [72, 48, 96, 48, 24],
    'With AI (hrs)': [1, 1, 2, 1, 0.5]
}
df_exp = pd.DataFrame(candidate_exp)
fig1 = go.Figure()
fig1.add_trace(go.Bar(name='Traditional Process', x=df_exp['Metric'], y=df_exp['Traditional (hrs)']))
fig1.add_trace(go.Bar(name='With Job Screening AI', x=df_exp['Metric'], y=df_exp['With AI (hrs)']))
fig1.update_layout(title='Candidate Experience: Response Time Improvement',
                  yaxis_title='Hours',
                  barmode='group')
fig1.write_image("images/candidate_experience.png")

# 2. ROI Analysis
months = list(range(1, 13))
traditional_cost = [5000 * x for x in months]  # Monthly cost increasing linearly
ai_cost = [10000] + [2000 * x for x in months[1:]]  # Initial investment + lower monthly cost
savings = [t - a for t, a in zip(traditional_cost, ai_cost)]

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=months, y=traditional_cost, name='Traditional Cost', line=dict(color='red')))
fig2.add_trace(go.Scatter(x=months, y=ai_cost, name='AI Solution Cost', line=dict(color='green')))
fig2.add_trace(go.Scatter(x=months, y=savings, name='Cost Savings', line=dict(color='blue')))
fig2.update_layout(title='ROI Analysis: 12-Month Cost Comparison',
                  xaxis_title='Months',
                  yaxis_title='Cost (USD)')
fig2.write_image("images/roi_analysis.png")

# 3. Quality of Hire Improvement
quality_metrics = {
    'Metric': ['Skills Match', 'Cultural Fit', 'Performance Score', 'Retention Rate', 'Team Satisfaction'],
    'Traditional (%)': [65, 70, 75, 60, 72],
    'With AI (%)': [95, 90, 92, 88, 94]
}
df_quality = pd.DataFrame(quality_metrics)
fig3 = px.line(df_quality, x='Metric', y=['Traditional (%)', 'With AI (%)'],
               title='Quality of Hire: Key Metrics Improvement',
               markers=True)
fig3.write_image("images/quality_improvement.png")

# 4. Process Automation Level
automation_data = {
    'Process': ['Resume Screening', 'Skill Assessment', 'Interview Scheduling', 'Candidate Communication', 'Documentation'],
    'Automation Level': [95, 90, 85, 88, 92]
}
fig4 = px.funnel(automation_data, x='Automation Level', y='Process',
                 title='Process Automation Levels (%)')
fig4.write_image("images/automation_levels.png")

# 5. Time-to-Hire Distribution
time_to_hire = {
    'Hiring Stage': ['Job Posting', 'Initial Screening', 'Assessment', 'Interviews', 'Decision Making', 'Offer'],
    'Time Saved (%)': [80, 85, 75, 50, 70, 60]
}
fig5 = px.bar(time_to_hire, x='Hiring Stage', y='Time Saved (%)',
              title='Time Saved in Each Hiring Stage',
              color='Time Saved (%)',
              color_continuous_scale='Viridis')
fig5.write_image("images/time_saved.png")

# 6. AI System Accuracy
accuracy_metrics = {
    'Metric': ['Resume Analysis', 'Skill Matching', 'Cultural Fit Assessment', 'Performance Prediction', 'Overall Accuracy'],
    'Score': [96, 94, 92, 88, 93]
}
fig6 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = accuracy_metrics['Score'][-1],
    title = {'text': "Overall System Accuracy (%)"},
    gauge = {'axis': {'range': [None, 100]},
             'steps': [
                 {'range': [0, 60], 'color': "lightgray"},
                 {'range': [60, 80], 'color': "gray"},
                 {'range': [80, 100], 'color': "darkblue"}],
             'threshold': {
                 'line': {'color': "red", 'width': 4},
                 'thickness': 0.75,
                 'value': 90}}))
fig6.write_image("images/system_accuracy.png")

# 7. Compliance and Risk Management
compliance_data = {
    'Category': ['Data Protection', 'Equal Opportunity', 'Documentation', 'Audit Trail', 'Legal Compliance'],
    'Traditional': [70, 65, 75, 60, 72],
    'With AI': [98, 95, 100, 100, 97]
}
df_compliance = pd.DataFrame(compliance_data)
fig7 = go.Figure()
fig7.add_trace(go.Scatterpolar(
    r=df_compliance['Traditional'],
    theta=df_compliance['Category'],
    fill='toself',
    name='Traditional'
))
fig7.add_trace(go.Scatterpolar(
    r=df_compliance['With AI'],
    theta=df_compliance['Category'],
    fill='toself',
    name='With AI'
))
fig7.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    title="Compliance and Risk Management Improvement (%)"
)
fig7.write_image("images/compliance_improvement.png")

print("Additional solution benefit visualizations have been generated in the images directory.") 