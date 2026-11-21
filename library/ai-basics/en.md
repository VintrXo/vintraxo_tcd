# @lesson ai-intro
title: What AI is (and is not)
summary: AI, machine learning, deep learning and generative AI, and what each can do.
---
**Artificial intelligence (AI)** is the broad goal of making computers do tasks that normally need human judgement. Most AI today is **machine learning**: systems that learn patterns from examples instead of following hand-written rules.

| Term | What it means | Example |
|---|---|---|
| AI | Any technique that makes computers act "smart" | A chess program, a route planner |
| Machine learning | Learning patterns from data | Spam filter, sales forecast |
| Deep learning | Machine learning with large neural networks | Face recognition, speech to text |
| Generative AI | Models that create new text, images or code | ChatGPT, Claude, image generators |

```try python
# rules versus learning: a hand-written rule and a "learned" threshold for spam
emails = [("WIN a FREE prize now", 1), ("Meeting at 10", 0), ("free coffee in the kitchen", 0),
          ("Claim your FREE reward", 1), ("Invoice attached", 0), ("You WIN, click here", 1)]

def rule(text):                                   # a person wrote this rule
    return int("free" in text.lower())

def caps_score(text):                             # a feature the model can learn from
    return sum(w.isupper() and len(w) > 1 for w in text.split())

best = max(range(0, 3), key=lambda t: sum((caps_score(x) >= t) == bool(y) for x, y in emails))
print("rule accuracy   :", sum(rule(x) == y for x, y in emails), "of", len(emails))
print("learned threshold:", best, "capital words ->",
      sum((caps_score(x) >= best) == bool(y) for x, y in emails), "of", len(emails))
```

The rule ("contains free") makes mistakes on harmless messages; the learned threshold was chosen from the examples. Real systems learn from millions of examples and many signals at once.

```quiz
? Which of these is generative AI?
* A model that writes a summary of a report
- A thermostat that turns on at 20°C
- A spreadsheet SUM formula

? Machine learning systems learn patterns from examples.
= true
```

# @lesson ai-neuron
title: How a model learns: one neuron
summary: Weights, predictions, errors and gradient descent, in a few lines of NumPy.
---
A **neuron** multiplies each input by a **weight**, adds them up, and squashes the result into a number between 0 and 1. **Training** means adjusting the weights a little at a time to reduce the error on the examples.

```try python
import numpy as np

# hours studied, hours slept  ->  passed (1) or not (0)
X = np.array([[1, 4], [2, 8], [3, 5], [5, 7], [6, 8], [8, 6], [9, 7], [2, 5]], dtype=float)
y = np.array([0, 0, 0, 1, 1, 1, 1, 0], dtype=float)
X = (X - X.mean(axis=0)) / X.std(axis=0)          # put features on a similar scale

w = np.zeros(2); b = 0.0; lr = 0.5
sigmoid = lambda z: 1 / (1 + np.exp(-z))

for step in range(301):
    p = sigmoid(X @ w + b)                         # predictions between 0 and 1
    error = p - y
    w -= lr * X.T @ error / len(y)                 # move the weights against the error
    b -= lr * error.mean()
    if step % 100 == 0:
        loss = -np.mean(y * np.log(p + 1e-9) + (1 - y) * np.log(1 - p + 1e-9))
        print(f"step {step:3}  loss {loss:.3f}  weights {w.round(2)}")

print("predictions:", sigmoid(X @ w + b).round(2))
print("accuracy   :", ((sigmoid(X @ w + b) > 0.5) == y).mean())
```

The **loss** measures how wrong the model is, and it falls as training goes on. Large AI models do exactly this, with billions of weights instead of two.

```quiz
? What does training change inside the model?
* The weights
- The training examples
- The programming language

? The loss should usually go down during training.
= true
```

# @lesson ai-neural-network
title: Neural networks
summary: Layers of neurons learn patterns one neuron cannot, such as XOR.
---
One neuron can only draw a straight line between classes. Stacking neurons in **layers** lets a network learn curved, complex patterns. The classic test is **XOR**: the output is 1 when exactly one input is 1.

```try python
import numpy as np

rng = np.random.default_rng(0)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)
sigmoid = lambda z: 1 / (1 + np.exp(-z))

W1, b1 = rng.normal(0, 1, (2, 4)), np.zeros(4)    # hidden layer: 4 neurons
W2, b2 = rng.normal(0, 1, (4, 1)), np.zeros(1)    # output layer: 1 neuron

for step in range(5001):
    h = sigmoid(X @ W1 + b1)                       # forward pass
    out = sigmoid(h @ W2 + b2)
    d_out = (out - y) * out * (1 - out)            # backward pass (backpropagation)
    d_h = d_out @ W2.T * h * (1 - h)
    W2 -= 1.0 * h.T @ d_out;  b2 -= 1.0 * d_out.sum(0)
    W1 -= 1.0 * X.T @ d_h;    b1 -= 1.0 * d_h.sum(0)
    if step % 1000 == 0:
        print(f"step {step:4}  loss {np.mean((out - y) ** 2):.4f}")

for inputs, prediction in zip(X, out.round(2)):
    print(inputs.astype(int), "->", prediction[0])
```

- The **forward pass** computes predictions layer by layer.
- **Backpropagation** works out how much each weight contributed to the error, from the output back to the input, so every weight can be nudged in the right direction.
- Deep learning uses many layers and special designs (convolutional networks for images, transformers for language).

```quiz
? Why can a network with a hidden layer learn XOR when one neuron cannot?
* Layers can combine simple boundaries into a more complex one
- It uses more training examples
- XOR needs no training
```

# @lesson ai-language-models
title: How language models predict text
summary: Tokens, next-word prediction, and a tiny model trained on a few sentences.
---
A **language model** reads text as **tokens** (words or pieces of words) and learns to predict the next token. Large language models (LLMs) are trained on huge amounts of text, so their predictions capture grammar, facts and styles. The tiny model below only counts which word follows which:

```try python
import random
from collections import Counter, defaultdict

text = """the customer opened a ticket . the agent answered the ticket .
the customer thanked the agent . the agent closed the ticket .
the manager reviewed the ticket . the customer opened a new ticket ."""
tokens = text.split()
print("tokens:", len(tokens), "| vocabulary:", len(set(tokens)))

next_words = defaultdict(Counter)
for a, b in zip(tokens, tokens[1:]):
    next_words[a][b] += 1

print("after 'the':", next_words["the"].most_common(4))

random.seed(8)
word, sentence = "the", ["the"]
for _ in range(9):
    options = next_words[word]
    word = random.choices(list(options), weights=options.values())[0]
    sentence.append(word)
    if word == ".":
        break
print("generated:", " ".join(sentence))
```

The generated sentence is **new**: it is not in the training text. It is also nonsense ("the customer thanked the ticket"), because this tiny model only knows which word tends to follow which. Real LLMs look at much longer context (thousands of tokens) with a neural network instead of a count table, but the core task is the same: predict the next token.

:::warning Fluent is not the same as true
A language model produces what is **likely** to come next, not what is **verified**. That is why AI answers can sound confident and still be wrong ("hallucinations").
:::

```quiz
? What is the basic task a language model is trained on?
* Predicting the next token
- Searching the internet live
- Checking facts in a database

? A fluent AI answer is always factually correct.
= false
```

# @lesson ai-temperature
title: Probabilities and temperature
summary: How a model turns scores into choices, and why answers vary.
---
For each next token, the model produces **scores** for every possible token. **Softmax** turns them into probabilities, and the model **samples** one. The **temperature** setting controls how adventurous that choice is.

```try python
import numpy as np

words = ["report", "summary", "table", "poem", "banana"]
scores = np.array([3.0, 2.6, 1.8, 0.5, -1.0])        # model scores for the next word

def softmax(z, temperature):
    z = z / temperature
    e = np.exp(z - z.max())
    return e / e.sum()

rng = np.random.default_rng(1)
for t in [0.2, 1.0, 2.0]:
    p = softmax(scores, t)
    picks = rng.choice(words, size=12, p=p)
    print(f"temperature {t}: " + ", ".join(f"{w} {q:.0%}" for w, q in zip(words, p)))
    print("   12 samples:", " ".join(picks))
```

| Temperature | Behaviour | Good for |
|---|---|---|
| Low (0 to 0.3) | Almost always the most likely token | Facts, extraction, code |
| Medium (about 0.7) | Some variety | General writing |
| High (above 1) | Surprising, sometimes nonsense | Brainstorming |

```quiz
? You want the AI to extract invoice numbers exactly. Which temperature fits?
* Low
- High
- It does not matter

? With a higher temperature, unlikely words are chosen more often.
= true
```

# @lesson ai-embeddings
title: Embeddings and semantic search
summary: Turning meaning into vectors, cosine similarity, and finding related documents.
---
An **embedding** is a list of numbers that represents the meaning of a word, sentence or document. Texts with similar meaning get vectors that point in similar directions, which lets computers search by **meaning** instead of exact words.

```try python
import numpy as np

# tiny hand-made "embeddings": [money, time off, technology, people]
docs = {
    "How to submit an expense claim": [0.9, 0.0, 0.1, 0.2],
    "Annual leave policy": [0.1, 0.9, 0.0, 0.3],
    "Reset your laptop password": [0.0, 0.0, 0.9, 0.1],
    "Requesting a salary advance": [0.8, 0.1, 0.0, 0.3],
    "Working from home rules": [0.0, 0.6, 0.4, 0.3],
}
def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

questions = {
    "I paid for a taxi for a client visit, how do I get the money back?": [0.85, 0.05, 0.05, 0.2],
    "How many vacation days do I have?": [0.1, 0.95, 0.0, 0.2],
}
for q, vec in questions.items():
    ranked = sorted(docs, key=lambda d: cosine(vec, docs[d]), reverse=True)
    print(q)
    for d in ranked[:2]:
        print(f"   {cosine(vec, docs[d]):.2f}  {d}")
```

The first question shares almost no words with "expense claim", yet it is matched correctly because the vectors are close. Real embedding models produce vectors with hundreds of dimensions, learned from text.

```reference python
embedding | Vector that represents meaning | [0.12, -0.4, ...]
cosine similarity | Closeness of two vectors (1 = same direction) | a @ b / (|a| |b|)
semantic search | Rank documents by similarity to the question | sorted(docs, key=similarity)
vector database | Stores embeddings and finds the nearest quickly | pgvector, FAISS
```

```quiz
? What does semantic search compare?
* The meaning of the question and documents, as vectors
- Only identical words
- The length of the documents
```

# @lesson ai-rag
title: Retrieval-augmented generation (RAG)
summary: Answering from your own documents: retrieve, then generate with sources.
---
LLMs do not know your company's policies, and they may invent answers. **RAG** fixes much of this: first **retrieve** the most relevant passages from your own documents, then give them to the model with the question and ask it to answer **only from them**, citing the source.

```try python
import math, re
from collections import Counter

policies = {
    "Leave policy §2": "Employees have 21 days of annual leave. Unused leave up to 5 days can move to next year.",
    "Expenses §4": "Taxi and meals for client visits are refunded within 30 days with a receipt.",
    "IT policy §1": "Passwords must be unique. Report lost laptops to IT within 24 hours.",
    "Remote work §3": "Staff may work from home two days a week with manager approval.",
}
words = lambda t: re.findall(r"[a-z]+", t.lower())
df = Counter(w for text in policies.values() for w in set(words(text)))

def score(question, text):                         # simple TF-IDF keyword relevance
    q, t = Counter(words(question)), Counter(words(text))
    return sum(t[w] * math.log(1 + len(policies) / df[w]) for w in q if w in t)

question = "How many days of annual leave can I move to next year?"
best = sorted(policies, key=lambda k: score(question, policies[k]), reverse=True)[:2]

prompt = "Answer ONLY from the sources below. If the answer is not there, say you do not know.\n"
prompt += "Cite the source name.\n\n"
for name in best:
    prompt += f"[{name}] {policies[name]}\n"
prompt += f"\nQuestion: {question}"
print(prompt)
```

This prompt is what would be sent to the language model. Because the right passage is included and the model is told to stay within it, the answer ("up to 5 days, Leave policy §2") is grounded and checkable.

:::tip Why RAG instead of retraining
Documents change every week. With RAG you update the documents, not the model, and every answer can point to its source so people can verify it.
:::

```quiz
? What are the two steps of RAG?
* Retrieve relevant passages, then generate an answer from them
- Retrain the model, then delete the documents
- Translate the question, then guess
```

# @lesson ai-prompting
title: Writing good prompts
summary: Role, context, task, format and examples, with before-and-after prompts.
---
A **prompt** is the instruction you give an AI assistant. Clear prompts get better results. A useful checklist:

1. **Context**: who you are, who the output is for, what you already have.
2. **Task**: exactly what to do, with the important details.
3. **Format**: length, structure, tone, language.
4. **Examples**: show one or two of what good looks like.
5. **Limits**: what to avoid, and "say if you are not sure".

| Weak prompt | Better prompt |
|---|---|
| "Write about our new policy." | "Write a 120-word announcement for all staff about our new remote-work policy: 2 days a week from 1 March, manager approval needed. Friendly tone, Arabic and English versions, end with who to contact." |
| "Fix this Excel formula." | "This formula should sum column C when column A is 'Cairo', but it returns 0: `=SUMIF(A:A,Cairo,C:C)`. Explain the mistake in one sentence and give the corrected formula." |
| "Summarise this." | "Summarise the meeting notes below in 5 bullet points for a manager who missed the meeting. List decisions and owners separately. If something is unclear, say so." |

```try python
def build_prompt(task, audience, facts, fmt, extra=""):
    parts = [f"Task: {task}", f"Audience: {audience}", "Facts:"]
    parts += [f"- {f}" for f in facts]
    parts += [f"Format: {fmt}", "If any fact is missing, ask instead of guessing."]
    if extra:
        parts.append(extra)
    return "\n".join(parts)

print(build_prompt(
    task="Write an announcement about the new training platform",
    audience="all employees, mostly non-technical",
    facts=["launches 1 March", "courses in Arabic and English", "sign in with your work email"],
    fmt="under 100 words, friendly, a title and 3 short paragraphs",
))
```

:::warning Never paste confidential data into public AI tools
Customer data, salaries, passwords, contracts and unreleased plans must not go into AI tools that your company has not approved. Use the approved tool, or remove the sensitive parts first.
:::

```quiz
? Which addition most improves the prompt "Summarise this report"?
* The audience, the length and what to focus on
- Writing it in capital letters
- Adding "please" several times

? It is fine to paste customer data into any public AI chatbot.
= false
```

# @lesson ai-limits
title: Limits, bias and checking AI output
summary: Hallucinations, outdated knowledge, bias in data, and how to verify answers.
---
AI tools are powerful assistants, but they have predictable weaknesses:

- **Hallucinations**: confident answers that are invented, including fake sources.
- **Out-of-date knowledge**: a model only knows what was in its training data, up to a cut-off date.
- **Bias**: models learn from human data, including its unfairness.
- **No real understanding of your situation**: they do not know your contracts, systems or customers unless you provide them.

The example shows how biased training data produces a biased model, even with no bad intent:

```try python
from collections import Counter

# past hiring decisions used as "training data" (department, hired)
history = [("sales", "hired")] * 40 + [("sales", "rejected")] * 10 + \
          [("design", "hired")] * 5 + [("design", "rejected")] * 15

rates = {}
for dept in ["sales", "design"]:
    outcomes = Counter(o for d, o in history if d == dept)
    rates[dept] = outcomes["hired"] / sum(outcomes.values())
    print(f"{dept:7} past hire rate: {rates[dept]:.0%}")

def naive_model(dept):                       # "learns" only from the past
    return "recommend" if rates[dept] >= 0.5 else "reject"

for dept in ["sales", "design"]:
    print(f"new {dept} applicant ->", naive_model(dept))
print("The model repeats past patterns. If the past was unfair, so is the model.")
```

How to check AI output:

1. **Verify facts and numbers** against a trusted source before you use them.
2. **Ask for sources** and open them; reject sources you cannot find.
3. **Test code** before using it, and read it.
4. **Keep a human decision** for anything that affects people's jobs, money or rights.

```quiz
? An AI tool gives you a law article number to quote in a contract. What should you do?
* Check the article in the official source before using it
- Use it, AI tools do not make mistakes with numbers
- Ask the AI if it is sure and accept its answer

? A model trained on biased historical data can repeat that bias.
= true
```

# @lesson ai-at-work
title: Using AI at work responsibly
summary: Good use cases, a simple decision checklist, and the rules to follow.
---
| Good uses | Use with care | Avoid |
|---|---|---|
| Drafting emails and documents | Summaries of long reports (check them) | Final decisions about people |
| Brainstorming ideas | Translations of contracts (have them reviewed) | Pasting confidential data into unapproved tools |
| Explaining a formula or code | Data analysis (verify numbers) | Presenting AI output as checked fact |
| Turning notes into a checklist | Customer replies (review before sending) | Generating fake reviews or impersonating people |

```try python
def ai_check(task, confidential=False, affects_people=False, tool_approved=True, will_review=True):
    issues = []
    if confidential and not tool_approved:
        issues.append("use the company-approved tool or remove confidential details")
    if affects_people:
        issues.append("a person must make and own the final decision")
    if not will_review:
        issues.append("review and fact-check the output before using it")
    return "OK to use AI" if not issues else "Careful: " + "; ".join(issues)

print("Draft a training announcement      ->", ai_check("announcement"))
print("Summarise customer complaints      ->", ai_check("summary", confidential=True, tool_approved=False))
print("Rank job applicants automatically  ->", ai_check("ranking", affects_people=True, will_review=False))
```

:::tip Be open about AI use
Follow your company's AI policy, say when a document was drafted with AI if your team expects it, and stay responsible for anything you send or publish: the AI helps, but you sign.
:::

```quiz
? Who is responsible for a report you send that was drafted with AI?
* You, the person who sends it
- The AI tool
- Nobody
```

# @lesson ai-reference
title: AI basics quick reference
summary: Key terms and good practice on one page.
---
| Term | Meaning |
|---|---|
| Model | A program with learned weights that makes predictions |
| Training / weights | Adjusting numbers inside the model to reduce errors |
| Neural network | Layers of simple units that together learn complex patterns |
| Token | A piece of text the model reads and writes |
| LLM | A large language model that predicts the next token |
| Temperature | How random the model's choices are |
| Embedding | A vector that represents meaning |
| RAG | Retrieve your documents, then generate an answer from them |
| Hallucination | A confident but invented answer |
| Prompt | The instruction and context you give the model |

:::tip Where to go next
Pick one repeated writing task in your job and try an approved AI assistant with a well-built prompt (context, task, format, examples). Compare the result with your usual work, and keep a short list of prompts that work. Technical learners can continue with the Machine learning and Python courses in this library.
:::

```quiz
? What is the best protection against AI hallucinations in your work?
* Checking important facts against trusted sources
- Using a higher temperature
- Writing longer prompts only
```
