import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Time Savings Comparison
time_comparison = {
    'Process': ['CV Screening', 'Interview Coordination', 'Administrative Tasks', 'Candidate Evaluation', 'Other Tasks'],
    'Traditional': [23, 60, 8, 5, 4],
    'With AI': [5, 15, 3, 75, 2]
}
df_time = pd.DataFrame(time_comparison)
fig1 = go.Figure(data=[
    go.Bar(name='Traditional Process', x=df_time['Process'], y=df_time['Traditional']),
    go.Bar(name='With Job Screening AI', x=df_time['Process'], y=df_time['With AI'])
])
fig1.update_layout(title='Time Distribution: Traditional vs AI-Powered Recruitment (%)',
                  barmode='group')
fig1.write_image("images/time_savings.png")

# Process Timeline Improvement
timeline_comparison = {
    'Stage': ['Initial Screening', 'Shortlisting', 'First Interview', 'Second Interview', 'Final Decision', 'Offer'],
    'Traditional': [10, 7, 8, 7, 5, 5],
    'With AI': [1, 2, 5, 5, 2, 3]
}
df_timeline = pd.DataFrame(timeline_comparison)
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_timeline['Stage'], y=df_timeline['Traditional'],
                         name='Traditional Process', line=dict(color='red')))
fig2.add_trace(go.Scatter(x=df_timeline['Stage'], y=df_timeline['With AI'],
                         name='With Job Screening AI', line=dict(color='green')))
fig2.update_layout(title='Hiring Timeline: Traditional vs AI-Powered (Days)',
                  yaxis_title='Days')
fig2.write_image("images/timeline_improvement.png")

# Cost Reduction
cost_comparison = {
    'Category': ['Bad Hire Risk', 'Vacancy Cost', 'Screening Cost', 'Total Process Cost'],
    'Traditional': [240000, 42000, 15000, 4129],
    'With AI': [48000, 12600, 3000, 1500]
}
df_cost = pd.DataFrame(cost_comparison)
fig3 = go.Figure()
fig3.add_trace(go.Bar(name='Traditional Process', x=df_cost['Category'], y=df_cost['Traditional']))
fig3.add_trace(go.Bar(name='With Job Screening AI', x=df_cost['Category'], y=df_cost['With AI']))
fig3.update_layout(title='Cost Comparison: Traditional vs AI-Powered (USD)',
                  barmode='group')
fig3.write_image("images/cost_reduction.png")

# Efficiency Improvement
efficiency_data = {
    'Metric': ['Screening Speed', 'Match Accuracy', 'Bias Reduction', 'Process Automation', 'Data-Driven Decisions'],
    'Improvement': [95, 85, 90, 88, 92]
}
fig4 = px.bar(efficiency_data, x='Metric', y='Improvement',
              title='Job Screening AI: System Improvements (%)',
              color='Improvement',
              color_continuous_scale='Viridis')
fig4.write_image("images/efficiency_improvement.png")

# Bias Reduction
bias_reduction = {
    'Type': ['Unconscious Bias', 'Gender Bias', 'Cultural Bias', 'Name-based Discrimination', 'Subjective Decisions'],
    'Before': [40, 65, 55, 29, 55],
    'After': [5, 8, 7, 3, 10]
}
df_bias = pd.DataFrame(bias_reduction)
fig5 = go.Figure()
fig5.add_trace(go.Bar(name='Traditional Process', x=df_bias['Type'], y=df_bias['Before']))
fig5.add_trace(go.Bar(name='With Job Screening AI', x=df_bias['Type'], y=df_bias['After']))
fig5.update_layout(title='Bias Reduction: Traditional vs AI-Powered (%)',
                  barmode='group')
fig5.write_image("images/bias_reduction.png")

# Technology Integration
tech_improvement = {
    'Category': ['AI Integration', 'Automated Screening', 'Skill Assessment', 'Database Management', 'Analytics'],
    'Coverage': [95, 98, 92, 96, 94]
}
fig6 = go.Figure()
fig6.add_trace(go.Scatterpolar(
    r=tech_improvement['Coverage'],
    theta=tech_improvement['Category'],
    fill='toself'
))
fig6.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=False,
    title="Job Screening AI: Technology Coverage (%)"
)
fig6.write_image("images/tech_coverage.png")

# Global Recruitment Solutions
global_improvement = {
    'Feature': ['Multilingual Processing', '24/7 Availability', 'Standardized Assessment', 'Global Database', 'Cost Efficiency'],
    'Effectiveness': [92, 100, 95, 88, 85]
}
fig7 = px.line_polar(global_improvement, r='Effectiveness', theta='Feature', line_close=True,
                     title="Job Screening AI: Global Solutions (%)")
fig7.write_image("images/global_solutions.png")

print("All solution visualizations have been generated in the images directory.") 