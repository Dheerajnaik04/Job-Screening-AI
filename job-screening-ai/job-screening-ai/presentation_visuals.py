import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Time Waste in Recruitment
time_waste_data = {
    'Activity': ['Manual CV Screening', 'Interview Coordination', 'Administrative Tasks', 'Actual Evaluation', 'Other Tasks'],
    'Percentage': [23, 60, 8, 5, 4]
}
fig1 = px.pie(time_waste_data, values='Percentage', names='Activity', 
              title='HR Time Distribution in Recruitment Process',
              color_discrete_sequence=px.colors.qualitative.Set3)
fig1.write_image("images/time_waste.png")

# Hiring Process Timeline
timeline_data = {
    'Stage': ['Initial Screening', 'Shortlisting', 'First Interview', 'Second Interview', 'Final Decision', 'Offer & Negotiation'],
    'Days': [10, 7, 8, 7, 5, 5]
}
fig2 = go.Figure(go.Waterfall(
    name="Days", orientation="v",
    measure=["relative"] * len(timeline_data['Stage']),
    x=timeline_data['Stage'],
    y=timeline_data['Days'],
    connector={"line":{"color":"rgb(63, 63, 63)"}},
))
fig2.update_layout(title="42-Day Hiring Process Breakdown",
                  showlegend=False)
fig2.write_image("images/timeline.png")

# Cost Impact
cost_data = {
    'Category': ['Bad Hire Cost', 'Extended Vacancy Cost', 'Manual Screening Cost', 'Traditional Recruitment Cost'],
    'Amount': [240000, 42000, 15000, 4129]
}
fig3 = px.bar(cost_data, x='Category', y='Amount',
              title='Cost Impact of Traditional Recruitment (USD)',
              color='Amount',
              color_continuous_scale='Viridis')
fig3.write_image("images/cost_impact.png")

# Application Funnel
funnel_data = {
    'Stage': ['Total Applications', 'Screened Applications', 'Interview Stage', 'Final Round', 'Hired'],
    'Count': [250, 58, 5, 2, 1]
}
fig4 = go.Figure(go.Funnel(
    y=funnel_data['Stage'],
    x=funnel_data['Count'],
    textinfo="value+percent initial"))
fig4.update_layout(title="Recruitment Funnel (Per Position)")
fig4.write_image("images/funnel.png")

# Bias in Recruitment
bias_data = {
    'Type': ['Unconscious Bias', 'Gender Bias', 'Cultural Bias', 'Name-based Discrimination', 'Subjective Decisions'],
    'Percentage': [40, 65, 55, 29, 55]
}
fig5 = px.bar(bias_data, x='Type', y='Percentage',
              title='Types of Bias in Traditional Recruitment (%)',
              color='Percentage',
              color_continuous_scale='Reds')
fig5.write_image("images/bias.png")

# Technology Gap Radar
tech_gap_data = {
    'Category': ['AI Tools', 'Automated Screening', 'Skill Assessment', 'Database Management', 'Metric Tracking'],
    'Gap Percentage': [82, 65, 91, 77, 89]
}
fig6 = go.Figure()
fig6.add_trace(go.Scatterpolar(
    r=tech_gap_data['Gap Percentage'],
    theta=tech_gap_data['Category'],
    fill='toself'
))
fig6.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=False,
    title="Technology Gap in Recruitment (%)"
)
fig6.write_image("images/tech_gap.png")

# Global Recruitment Challenges
global_data = {
    'Challenge': ['International Assessment', 'Language Barriers', 'Qualification Validation', 'Timezone Issues', 'Cost Increase'],
    'Percentage': [85, 92, 78, 66, 81]
}
fig7 = px.line_polar(global_data, r='Percentage', theta='Challenge', line_close=True,
                     title="Global Recruitment Challenges (%)")
fig7.write_image("images/global_challenges.png")

print("All visualizations have been generated in the images directory.") 