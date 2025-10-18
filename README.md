# 🌙 Night Coder

> **Where Developers Code Together, Grow Together**  
> *Because code doesn't sleep, and neither do we* 🚀

![CI/CD](https://github.com/Tarasyonok/pet-project-forum/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2-darkgreen?logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.2-purple?logo=bootstrap)
![PostgreSQL](https://img.shields.io/badge/Ruff-14-lightgreen?logo=ruff)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 What is Night Coder?

**Night Coder** is a full-stack developer community platform built for those magical hours when creativity flows best. It's where students 👨‍🎓, and passionate developers 💻 come together to ask questions, share knowledge, and grow their skills.

### ✨ Why Night Coder Exists

- 🕒 **Community** - Someone is always awake somewhere in the world
- 🏆 **Gamified Learning** - Earn reputation and climb leaderboards
- 🌐 **Bilingual** - English and Russian support for global reach
- 🎨 **Beautiful UI** - Dark theme optimized for night coding sessions
- 🤝 **Real Connections** - Build your developer reputation and portfolio

## 🚀 Live Demo

👉 **[Try Night Coder Live](https://your-night-coder-app.onrender.com)** 👈

**Demo Credentials:**
- Email: `demo@nightcoder.com`
- Password: `demopass123`

## 📸 Screenshots

| Homepage | Forum | User Profile |
|----------|-------|--------------|
| ![Home](https://via.placeholder.com/300x200/667eea/ffffff?text=Beautiful+Homepage) | ![Forum](https://via.placeholder.com/300x200/764ba2/ffffff?text=Q%26A+Forum) | ![Profile](https://via.placeholder.com/300x200/2c3e50/ffffff?text=User+Profile) |

## 🛠️ Tech Stack

### **Backend**
- **Python 3.11** - Core programming language
- **Django 4.2** - High-level Python Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Production database
- **SQLite** - Development database

### **Frontend**
- **Bootstrap 5** - Responsive CSS framework
- **JavaScript (ES6+)** - Interactive features
- **HTML5 & CSS3** - Modern web standards
- **Font Awesome** - Icons and emojis

### **DevOps & Tools**
- **Render** - Cloud deployment platform
- **Ruff** - Ultra-fast Python linter and formatter
- **Pytest** - Testing framework
- **Git** - Version control
- **CI/CD** - Automated testing and deployment

## 🎨 Key Features

### 💬 **Smart Q&A Forum**
- Ask programming questions and get answers
- Vote system with reputation rewards
- Mark answers as accepted
- Full-text search across questions and answers
- Real-time updates without page reloads

### ⭐ **Course Reviews**
- Share experiences with programming courses
- 5-star rating system with detailed reviews
- Vote on helpful reviews
- Search by course name or technology

### 🏆 **Gamification System**
- **Reputation Points** - Earn through helpful contributions
- **Leaderboards** - Compete with other developers
- **Achievement System** - Milestones and badges
- **Monthly Top Contributors** - Recognition for active members

### 👤 **Rich User Profiles**
- Avatar upload and personal bios
- Activity history (questions, answers, reviews)
- Reputation breakdown and statistics
- Social proof with contribution metrics

### 🌐 **Internationalization**
- Full English/Russian language support
- SEO-friendly URL structure
- Language switcher with user preferences

### 🎯 **Developer Experience**
- Dark theme optimized for coding
- Mobile-responsive design
- Fast loading times
- Accessible and keyboard-navigation friendly

## 📁 Project Structure

```
night-coder/
├── 🏠 home/                 # Homepage app
├── 💬 forum/               # Q&A functionality
├── ⭐ reviews/             # Course reviews
├── 👤 users/              # Authentication & profiles
├── 🏆 leaderboards/       # Gamification system
├── 🎨 stickers/           # Telegram sticker packs
├── 🔧 core/               # Shared utilities & mixins
├── 📁 templates/          # Django templates
├── 📁 static/            # CSS, JS, images
└── 📁 locale/            # Translation files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (optional, SQLite for development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/night-coder.git
   cd night-coder
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database and secret key
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` and start coding! 🌙

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific app tests
pytest forum/ -v
```

## 🔧 Code Quality

```bash
# Lint and format code
ruff check .          # Linting
ruff format .         # Formatting

# Security check
bandit -r .

# Type checking (if using mypy)
mypy .
```

## 🌐 Deployment

Night Coder is deployed on **Render** with automatic CI/CD:

1. **Push to main branch** → Automatic deployment
2. **Database** → Render PostgreSQL
3. **Static files** → Whitenoise serving
4. **Environment** → Production-ready configuration

### Environment Variables
```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=your-domain.com
```

## 🤝 Contributing

We love contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use meaningful commit messages

## 📈 Project Impact

### 🎯 **For Job Seekers**
- **Showcase full-stack skills** with a complete, production-ready project
- **Demonstrate Django expertise** with advanced features
- **Prove ability to ship** from idea to deployment
- **Internationalization experience** with Russian/English support

### 🌍 **For the Community**
- 500+ developers helped
- 1,000+ questions answered
- 200+ course reviews shared
- 10,000+ reputation points earned

## 🏆 Achievements

This project demonstrates mastery in:

- ✅ **Full-Stack Development** - End-to-end web application
- ✅ **Database Design** - Complex relationships and optimization
- ✅ **User Experience** - Intuitive and engaging interface
- ✅ **DevOps** - CI/CD and cloud deployment
- ✅ **Internationalization** - Multi-language support
- ✅ **Testing & Quality** - Comprehensive test coverage
- ✅ **Performance** - Fast loading and efficient queries

## 👨‍💻 About the Developer

**Your Name**  
*Full-Stack Developer & Night Owl* 🦉

- 🌐 **Portfolio**: [your-portfolio.com](https://your-portfolio.com)
- 💼 **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/your-profile)
- 🐙 **GitHub**: [@your-username](https://github.com/your-username)
- 📧 **Email**: your.email@domain.com

> "I built Night Coder to solve a real problem: creating a welcoming space for developers who do their best work when the world is asleep. It represents my passion for clean code, user experience, and community building."

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Community** - For an amazing web framework
- **Bootstrap Team** - For beautiful UI components
- **Render** - For generous free hosting
- **All Night Coders** - For being part of this community

---

<div align="center">

### **Ready to join our night coding community?** 🌙

[![Deploy on Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
[![Try Night Coder](https://img.shields.io/badge/Try_Night_Coder-Live_Demo-orange?style=for-the-badge)](https://your-night-coder-app.onrender.com)

*⭐ Don't forget to star this repo if you found it helpful!*

</div>


## 🎯 Why This README Works:

### **For Recruiters** 💼:
- **Immediate understanding** of what the project does
- **Technical depth** showing your skills
- **Business impact** with user metrics
- **Professional presentation** that stands out

### **For Developers** 👨‍💻:
- **Clear setup instructions**
- **Technical specifications**
- **Architecture overview**
- **Contribution guidelines**

### **Key Psychological Triggers** 🧠:
- **Social proof** - User numbers and impact
- **Visual appeal** - Badges, emojis, structure
- **Credibility** - Live demo, tests, deployment
- **Storytelling** - Your personal journey

## 🚀 Next Steps:

1. **Replace placeholder URLs** with your actual links
2. **Add real screenshots** from your deployed app
3. **Update metrics** with your actual user numbers
4. **Customize the "About Developer"** section
5. **Add your actual deployment badge**

This README will make recruiters immediately see you as a senior-level developer who can ship production-ready applications! 🎉

Want me to help you customize any specific section? Or ready to deploy this masterpiece to your GitHub? 😊