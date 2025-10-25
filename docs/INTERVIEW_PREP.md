# Interview Preparation - TaskMind AI

## 🎯 Demo Strategy (15 minutes)

### Part 1: Architecture Overview (3 min)

**What to show:**

- Diagram from ARCHITECTURE.md
- Explain Clean Architecture layers
- "Notice domain layer has ZERO Django imports"

**Script:**

> "TaskMind uses Clean Architecture with SOLID principles. The domain layer is pure Python - no framework dependencies. This makes it testable and allows us to swap Django for FastAPI tomorrow if needed."

**Backup slides:**

- ARCHITECTURE.md diagram
- Code snippets ready

---

### Part 2: Live API Demo (4 min)

**What to show:**

1. Postman collection (pre-prepared)
2. Create task with urgent keywords
3. Show AI analysis in response
4. Show `/prioritized` endpoint

**Script:**

> "Let me show it working. I'll create a task with urgent keywords... see how the AI analyzed it and assigned urgency_score 0.92? Now watch the prioritized endpoint - tasks are sorted by AI intelligence, not manual priority."

**Preparation:**

```bash
# Have this running beforehand
docker-compose up -d
# Have Postman open with requests ready
```

**Backup:**

- Screenshots if demo fails
- cURL commands as backup

---

### Part 3: Code Walkthrough (5 min)

**What to show:**

**A) SOLID Principle (2 min)**

```python
# Show Dependency Inversion
class CreateTaskUseCase:
    def __init__(
        self,
        repository: TaskRepository,  # ← Abstraction
        ai_service: AIService         # ← Abstraction
    ):
        pass
```

**Script:**

> "This use case depends on interfaces, not concrete implementations. I can inject a mock repository for testing or a real PostgreSQL repository for production. That's Dependency Inversion."

**B) Domain Entity (1 min)**

```python
# Show pure domain logic
class Task:
    def mark_as_high_priority(self):
        if self.urgency_score >= 0.8:
            self.priority = Priority.HIGH
```

**Script:**

> "Business rules live in the domain layer. No Django, no database, just pure Python. Easy to test, easy to reason about."

**C) AI Integration (2 min)**

```python
# Show HuggingFace engine
class HuggingFaceEngine:
    def analyze_urgency(self, text: str):
        result = self.classifier(text, candidate_labels)
        return Analysis(urgency_score=...)
```

**Script:**

> "I'm using Hugging Face transformers with zero-shot classification. No training needed, no API costs. The model analyzes the text and assigns an urgency score in under 2 seconds."

---

### Part 4: Testing Demo (2 min)

**What to show:**

```bash
pytest --cov=apps --cov-report=term-missing
```

**Script:**

> "I have 89% test coverage. Unit tests run in under 1 second because they're fully mocked. Integration tests use a real database. I follow the testing pyramid - mostly unit tests."

---

### Part 5: Q&A Prep (1 min)

**Transition:**

> "That's TaskMind. I built this in a weekend to demonstrate I can deliver production-quality Django code. Happy to answer any questions or dive deeper into any part."

---

## 🎤 Expected Questions & Answers

### Technical Questions

**Q: "Why Clean Architecture for a small project?"**
A: "Two reasons: (1) To demonstrate I understand architectural patterns beyond MVC, and (2) it's actually easier to test. My domain logic has 100% coverage because it's pure Python with no framework dependencies."

**Q: "Your CV shows Node.js experience. Why Django?"**
A: "This role requires Python/Django, so I wanted to prove I can deliver quality code in your stack. I applied the same architectural principles I use in Node.js - Clean Architecture, dependency injection, repository pattern. The concepts transfer; the syntax is just different."

**Q: "How does the AI part work?"**
A: "I'm using Hugging Face's BART model for zero-shot classification. I give it a text and candidate labels like 'urgent', 'normal', 'low priority', and it classifies without any training. Then I convert the classification confidence into an urgency score. It's practical AI, not a toy example."

**Q: "What would you improve with more time?"**
A: "Three things: (1) Add authentication with JWT, (2) implement WebSocket for real-time updates when priorities change, (3) Add a simple React frontend. But I focused on backend quality first since that's what you need."

**Q: "How would you scale this?"**
A: "Current architecture is ready. I'd add Redis caching for frequently-accessed tasks, move AI processing to dedicated workers with autoscaling, and add database read replicas. The repository pattern makes it easy to add caching without changing business logic."

**Q: "Why RabbitMQ instead of Redis for Celery?"**
A: "RabbitMQ is more reliable for critical tasks. It has better message persistence and acknowledgment. Redis is faster but can lose messages. For task analysis, I prefer reliability over speed."

---

### Behavioral Questions

**Q: "Tell me about a time you learned a new technology quickly."**
A: _[Talk about this project!]_
"Just this week. Your job description mentioned Django/Python, which isn't my primary stack. So I built TaskMind in a weekend to prove I can deliver quality Python code. I researched Django best practices, implemented Clean Architecture, integrated AI, and achieved 89% test coverage. That's typical of how I learn - by building real projects, not just tutorials."

**Q: "How do you handle ambiguous requirements?"**
A: "I start with the user problem, not the technical solution. For TaskMind, the problem was 'prioritizing tasks is hard.' So I asked: what would make it easier? AI-powered analysis. Then I worked backward: what architecture supports that? Clean Architecture with injectable AI service. I document decisions in ADRs so the team understands the 'why'."

**Q: "Describe your development process."**
A: "I follow TDD when possible - write the test first, make it pass, refactor. You can see this in my commit history. I also believe in small, focused commits with descriptive messages. For this project, I created ROADMAP.md first to break the work into phases, then executed phase by phase."

---

### Zebra-Specific Questions

**Q: "Why Zebra?"**
A: "Three reasons: (1) You work on diverse projects from scratch - that's where I thrive. I get bored with maintenance. (2) Your focus on applied AI aligns with my career direction - I'm doing a Master's in AI Development. (3) Small teams with autonomy appeal to me. I want to own outcomes, not just write tickets."

**Q: "What interests you about our AI projects?"**
A: "I'm interested in practical AI - not research, but real products that solve business problems. Your description mentioned 'conversational agents' and 'internal tools' - that's engineering, not science experiments. I want to build AI features that users actually benefit from."

**Q: "How do you handle working in cells/small teams?"**
A: "I prefer it. At ITA, I worked in a small team on the IoT project and we moved fast. I like collaborative decision-making and shared ownership. In larger teams, communication overhead slows things down."

**Q: "Your experience is 2+ years but we ask for 3+. Why should we hire you?"**
A: "Quality over quantity. In 2 years I've: built IoT systems with computer vision, created digital twins in VR, developed BIM viewers, and earned recommendation letters from ITA and Pikolin. I've also done two technical degrees and currently pursuing an AI Master's. I learn fast and deliver - this demo project proves it."

---

## 🎯 Your Unique Selling Points

### 1. **Rapid Learner**

- Proof: Built production-quality Django app in 1 weekend
- Proof: Master's in Digital Transformation (8.8/10)
- Proof: Currently doing AI Master's while working

### 2. **Full-Stack + AI**

- Backend: Node.js, Django
- Frontend: React, Next.js
- AI: Computer vision (EfficientNet), NLP (Transformers)
- IoT: MQTT, CoAP, BLE

### 3. **Production Experience**

- ITA: Delivered projects selected for business continuity
- UB Manufacturing: Resolved 200+ incidents monthly
- Pikolin: 40% performance improvement

### 4. **Verifiable References**

- Recommendation letters from ITA and Pikolin
- GitHub portfolio with 10+ projects
- 4th place in The Wave hackathon 2025

---

## 🚫 What NOT to Say

❌ "I'm still learning Python/Django"
✅ "I've applied my backend experience to Python/Django with this project"

❌ "I don't have 3 years experience"
✅ "I have 2+ years of intensive, diverse experience with proven results"

❌ "I'm not sure about [technical detail]"
✅ "Let me show you in the code" OR "That's not in the current implementation, but here's how I'd approach it"

❌ "This is just a demo project"
✅ "This demonstrates production-quality architecture and practices"

---

## 📋 Pre-Interview Checklist

**24 Hours Before:**

- [ ] Review your CV - know every project cold
- [ ] Read Zebra's website thoroughly
- [ ] Check Sergio's LinkedIn for context
- [ ] Prepare 3 questions to ask them
- [ ] Test docker-compose up works
- [ ] Review SOLID_PRINCIPLES.md

**1 Hour Before:**

- [ ] Start docker-compose
- [ ] Open Postman with requests ready
- [ ] Have code editor open to key files
- [ ] Have GitHub repo open (README visible)
- [ ] Test your camera/microphone
- [ ] Have water ready

**During Interview:**

- [ ] Share screen with code ready
- [ ] Take notes on their questions
- [ ] Mirror their energy level
- [ ] Ask for clarification if needed
- [ ] Show enthusiasm but stay professional

---

## 🎁 Leave-Behind Materials

After interview, send:

```
Subject: TaskMind AI Demo - Follow-up

Hi Sofía and team,

Thank you for the interview today. As promised, here are the materials:

📦 GitHub Repository: [link]
📄 Live API Docs: [link to deployed version if you have time]
📊 Architecture Diagrams: [link to ARCHITECTURE.md]
📹 Video Demo: [if you made one]

Key highlights:
- Clean Architecture with SOLID principles
- 89% test coverage
- AI-powered prioritization with Hugging Face
- Docker-ized for easy deployment

Looking forward to next steps!

Alberto Guinda Sevilla
```

---

## 💡 Confidence Boosters

**Remember:**

1. You built a complete, production-ready system in 48 hours
2. You understand advanced architecture patterns
3. You have recommendation letters from previous companies
4. You're currently studying AI (differentiator!)
5. You've delivered real value in IoT, BIM, and manufacturing

**Worst case:** They say Python experience is a dealbreaker
**Your response:** "I understand. If you have other roles focused on Node.js/TypeScript or IoT, I'd love to hear about them. Otherwise, I'm happy to keep in touch for future opportunities."

**Best case:** They're impressed and want to move forward
**Your response:** "I'm excited about this opportunity. What are the next steps?"

---

## 🎤 Closing Statement (Memorize This)

> "Thanks for the opportunity to interview. I'm genuinely excited about Zebra because you're building diverse projects from scratch with practical AI - exactly what I want to do. I've proven I can learn fast and deliver quality code, and I bring experience in IoT, computer vision, and full-stack development that's unique for a backend role. I'd love to join your team."

---
