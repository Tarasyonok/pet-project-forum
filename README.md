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

**Night Coder** is a full-stack developer community platform built for those magical hours when creativity flows best. It's where students, and passionate developers come together to ask questions, share knowledge, and grow their skills.

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
- **Python 3.13** - Core programming language
- **Django 5.2** - High-level Python Web framework
- **SQLite** - Development & production database 

### **Frontend**
- **Bootstrap 5** - Responsive CSS framework
- **JavaScript** - Interactive features
- **HTML5 & CSS3** - Modern web standards
- **Font Awesome** - Icons and emojis

### **DevOps & Tools**
- **Render** - Cloud deployment platform
- **Ruff** - Ultra-fast Python linter and formatter
- **Tests** - Unit & Integration tests
- **Git** - Version control with clean commit history
- **CI/CD** - Automated linting and testing

## 🎨 Key Features

### 💬 **Smart Q&A Forum**
- Ask programming questions and get answers
- Vote system with reputation rewards
- Mark answers as accepted
- Full-text search across questions and answers

### ⭐ **Course Reviews**
- Share experiences with programming courses
- 5-star rating system with detailed reviews
- Vote on helpful reviews
- Search by course name or technology

### 🏆 **Gamification System**
- **Reputation Points** - Earn through helpful contributions
- **Leaderboards** - Compete with other developers
- **Monthly Top Contributors** - Recognition for active members
- **Footer statistics** - Context processor for community stats on every page

### 👤 **Rich User Profiles**
- Avatar upload and personal bios
- Activity history (questions, answers, reviews)
- Reputation breakdown and statistics
- Social proof with contribution metrics

### 🌐 **Internationalization**
- Full English/Russian language support
- Language switcher
- SEO-friendly URL structure

### 🎯 **Developer Experience**
- Dark theme optimized for coding
- Mobile-responsive design
- Accessible and keyboard-navigation friendly

## 📁 Project Structure

```
night-coder/
├── 🏠 home/                # Homepage app
├── 💬 forum/               # Q&A functionality
├── ⭐ reviews/             # Course reviews
├── 👤 users/               # Authentication & profiles
├── 👍 votes/               # Content votes
├── 🏆 leaderboards/        # Gamification system
├── 🔧 core/                # Shared utilities & mixins
├── 📁 templates/           # Django templates
├── 📁 static/              # CSS, JS, images
└── 📁 locale/              # Translation files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tarasyonok/pet-project-forum
   cd pet-project-forum
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install poetry
   poetry install
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

Visit `http://localhost:8000` and create your first question! 🌙

## 🧪 Testing

```bash
python manage.py test
```

## 🔧 Code Quality

```bash
# Lint and format code
ruff check .          # Linting
ruff format .         # Formatting
```

## 🌐 Deployment

Night Coder is deployed on **Render** with automatic CI/CD:

1. **Push to main branch** → Automatic deployment
2. **build.sh and start.sh** → Automatic deployment
3. **Environment** → Production-ready configuration

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

**Kir Tarasov**  
*Full-Stack Developer*

- 🌐 **Portfolio**: [your-portfolio.com](https://your-portfolio.com)
- 💼 **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/your-profile)
- 🐙 **GitHub**: [@your-username](https://github.com/your-username)
- 📧 **Email**: your.email@domain.com

> "I built Night Coder to solve a real problem: creating a welcoming space for developers who do their best work when the world is asleep. It represents my passion for clean code, user experience, and community building."

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### **Ready to join our night coding community?** 🌙

[![Try Night Coder](https://img.shields.io/badge/Try_Night_Coder-Live_Demo-orange?style=for-the-badge)](https://your-night-coder-app.onrender.com)

*⭐ Don't forget to star this repo if you found it interesting/helpful!*

</div>
