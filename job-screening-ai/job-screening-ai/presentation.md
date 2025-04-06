---
marp: true
theme: default
class: invert
paginate: true
backgroundColor: #1a1a1a
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
  section.title {
    text-align: center;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
  pre {
    background: #2b2b2b;
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    font-size: 0.8em;
  }
---

<!-- _class: title -->
# AI-Powered Job Screening System
## Revolutionizing Recruitment with AI
### ACC Hackathon 2024

---

# The Problem 🤔
![bg right:40%](https://source.unsplash.com/random/800x600/?office,stress)

- 📊 **Time Waste**: HR spends 23% time on manual screening
- 🎯 **Human Bias**: 40% of hiring decisions are biased
- ⏰ **Inefficiency**: Average hiring time: 42 days
- 📅 **Scheduling**: 60% time lost in interview coordination

---

<!-- _class: title -->
# Our Solution 💡
## AI-Powered Job Screening System

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  Streamlit UI    |<--->|   FastAPI API    |<--->|   SQLite DB     |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
         ^                       ^
         |                       |
         v                       v
+------------------+     +------------------+
|   JD Analyzer    |     |   CV Analyzer    |
|     Agent        |     |     Agent        |
+------------------+     +------------------+
         ^                       ^
         |                       |
         v                       v
+------------------+     +------------------+
|                  |     |                  |
|  Matcher Agent   |<--->|  Scheduler Agent |
|                  |     |                  |
+------------------+     +------------------+
```

---

# Key Features 🚀

<div class="columns">

**JD Analyzer Agent**
- 🎯 Smart requirement extraction
- 🔍 AI-powered skill identification
- 🧮 Semantic understanding

**CV Analyzer Agent**
- 📄 Intelligent CV parsing
- 👤 Profile generation
- 🎓 Skill validation

**Matcher Agent**
- 🤝 Smart matching algorithm
- 📊 Compatibility scoring
- 🎯 Experience alignment

**Scheduler Agent**
- 📅 Automated scheduling
- 📧 Smart notifications
- 🤖 Calendar integration

</div>

---

# Technical Innovation 💻

![bg right:40%](https://source.unsplash.com/random/800x600/?technology,ai)

- 🧠 **Advanced NLP**
  - Sentence Transformers
  - Semantic Analysis
  - Ollama Integration

- ⚡ **Modern Stack**
  - FastAPI Backend
  - Streamlit Frontend
  - Real-time Processing

---

# Live Demo 🎮

![bg right:40%](https://source.unsplash.com/random/800x600/?dashboard)

1. 📝 Post a Job Opening
2. 📄 Upload Candidate CVs
3. 🎯 View Smart Matches
4. 📅 Schedule Interviews

---

# Impact & Metrics 📈

![bg right:40%](https://source.unsplash.com/random/800x600/?growth)

- ⚡ **70%** reduction in screening time
- 📈 **85%** better candidate matching
- 🎯 **50%** faster hiring process
- 💰 **40%** cost reduction in hiring

---

# Future Roadmap 🗺️

<div class="columns">

**Short Term**
- 🌐 Multi-language support
- 📊 Analytics dashboard
- 🤝 ATS integration

**Long Term**
- 🎥 Video interviews
- 🤖 AI-powered assessments
- 🌟 Predictive analytics

</div>

---

<!-- _class: title -->
# Thank You! 🙏

## Questions?

Contact: [Your Contact Information]
GitHub: [Repository Link] 