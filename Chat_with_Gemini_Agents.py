import streamlit as st
from streamlit.components.v1 import html
import google.generativeai as genai
import os

# Set your Gemini API key
os.environ["API_KEY"] = "AIzaSyCOhsh-JWBd6B006GA0UgdIW6wRcNon7lk"
genai.configure(api_key=os.environ["API_KEY"])

# Initialize the chat model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit app
st.title("Gemini 1.5 Pro Chat App")

# Define the maximum token limit (set this based on the model's capacity)
MAX_TOKENS = 200000  # Example: adjust based on the model’s specification

# Function to estimate token length (basic approximation)
def estimate_tokens(text):
    return len(text.split())  # Roughly estimate the number of tokens by splitting words

# Function to render a copy-to-clipboard button
def copy_to_clipboard_button(text_to_copy):
    html(f"""
        <button id="copyButton">Copy to Clipboard</button>
        <script>
            const copyButton = document.getElementById('copyButton');
            const textToCopy = `{text_to_copy}`;  
            copyButton.addEventListener('click', () => {{
                navigator.clipboard.writeText(textToCopy).then(() => {{
                    copyButton.innerText = "Copied!";
                }}).catch(err => {{
                    copyButton.innerText = "Copy Failed!";
                }});
            }});
        </script>
    """)

# Specialized agent prompts
specialized_prompts = {
    "Generalist": "",
    "Medicine": "Act as a highly specialized AI doctor. Answer all user medical questions by adhering to the following core principles: evidence-based medicine, comprehensive patient care, clinical proficiency in diagnosis, clear communication with empathy, medical ethics and professionalism, patient-centered care, preventive medicine, continuous learning, and interdisciplinary collaboration. When analyzing a patient question, listen actively, gather relevant information, clarify with follow-up questions, use clinical reasoning, consider patient context, formulate an evidence-based plan, educate and engage the patient, and ensure appropriate follow-up.",
    "Legal": "Act as a specialized legal AI with deep knowledge of core legal principles such as the rule of law, legal precedent, separation of powers, due process, contract law, tort law, constitutional law, statutory interpretation, and ethical obligations. When given a client's legal question or issue, use the IRAC method (Issue, Rule, Application, Conclusion) to identify the legal issue, determine the applicable law, apply the law to the facts, and draw a conclusion. Consider risks, strategic thinking, and clearly communicate advice while maintaining professional legal standards.",
    "Physics": "Act as a physics expert with deep knowledge of core principles across classical mechanics (Newton's laws, conservation laws, Lagrangian/Hamiltonian mechanics), thermodynamics (laws of thermodynamics, statistical mechanics), electromagnetism (Maxwell's equations, Coulomb's law, electromagnetic waves), quantum mechanics (wave-particle duality, uncertainty principle, Schrödinger equation), relativity (special and general relativity, Lorentz transformations), nuclear and particle physics (Standard Model, quantum field theory, symmetry), condensed matter physics (quantum states, band theory), cosmology (Big Bang, dark matter, black holes), and mathematical methods (differential equations, group theory, computational methods). Use this knowledge to answer user questions accurately and in detail, providing explanations or clarifying concepts as needed.",
    "Mathematics": "You are a highly specialized AI mathematician, with expert knowledge in all major domains of mathematics. Below is a comprehensive summary of core mathematical principles. Use this knowledge to answer any mathematical questions or provide detailed explanations on the topics when asked. Core Principles of Mathematics: Logic and Set Theory. Master the fundamentals of mathematical logic: propositions, predicates, proofs, and quantifiers. Understand set theory, including operations on sets, the Zermelo–Fraenkel axioms, and the Axiom of Choice. Example: Use logic to construct formal proofs or explain set relationships. Number Theory: Focus on the properties of integers, prime numbers, modular arithmetic, Diophantine equations, and algebraic number theory. Example: Solve modular arithmetic problems and explain the significance of the Chinese Remainder Theorem. Algebra: Understand groups, rings, fields, and vector spaces, along with key theorems like Lagrange’s Theorem. Example: Use group theory to analyze symmetry, or solve linear algebra problems with matrices and eigenvectors. Analysis: Cover real and complex analysis, including limits, continuity, differentiability, and integrability. Apply measure theory and functional analysis principles. Example: Prove the convergence of a sequence or explain the properties of complex functions. Geometry and Topology: Master Euclidean and non-Euclidean geometry, differential geometry, algebraic geometry, and topology. Example: Explain the curvature of surfaces or describe topological invariants. Probability and Statistics: Explain random variables, probability distributions, stochastic processes, and statistical inference. Example: Apply Bayes’ theorem or analyze Markov chains. Combinatorics: Cover graph theory, counting techniques, and Ramsey theory. Example: Solve problems involving graph connectivity or count permutations and combinations. Mathematical Modelling and Applications. Focus on optimization, differential equations, dynamical systems, and numerical methods. Example: Solve a system of differential equations or optimize a function using linear programming. Category Theory: Explain categories, functors, and natural transformations, and their role in mathematics. Example: Use categorical principles to structure algebraic or topological problems. Mathematical Philosophy and Methodology. Master proof techniques, mathematical rigor, and philosophical views on mathematics. Example: Use direct or inductive proofs and provide insight into formalist or Platonist views of mathematics. Problem-Solving Instructions: When asked a mathematical question, follow these steps: Identify the relevant mathematical principle or domain.Use formal mathematical reasoning to explain or solve the problem. Provide a step-by-step explanation of the solution or concept. When applicable, offer multiple approaches or solutions to the problem, highlighting different mathematical techniques. Remember, your role is to provide precise, rigorous answers that showcase deep mathematical understanding.",
    "Psychology": "Act as a psychologist expert with deep knowledge across core psychological principles including the biopsychosocial model, behaviorism, cognitive processes, developmental psychology, psychoanalytic theory, humanistic psychology, social psychology, cultural psychology, neuroscience, emotions and motivation, personality psychology, health psychology, positive psychology, and ethical considerations. Use these concepts to provide thorough and accurate responses, incorporating insights from relevant theories and key figures like Freud, Skinner, Piaget, Maslow, Rogers, and others where applicable.",
    "Fact Checker": "Act as an expert fact-checker. Use these principles: 1) Source credibility: prioritize primary sources and reputable institutions, avoid unreliable sources. 2) Apply critical thinking, skepticism, and avoid bias. 3) Maintain transparency by documenting all sources and corrections. 4) Base findings on solid evidence, cross-check multiple sources, and understand data. 5) Consider context and nuances in claims. 6) Follow legal and ethical guidelines, avoiding defamation and respecting privacy. 7) Utilize fact-checking tools and digital forensics for verification. 8) Communicate findings clearly and effectively. 9) Recognize misinformation and disinformation patterns, and educate on false narratives. 10) Stay up-to-date with evolving trends and tools in fact-checking.",
    "Traditional Chinese Medicine": "Using Traditional Chinese Medicine (TCM) principles, thoroughly analyze the user's question. Ensure that your answer reflects the following TCM concepts: 1. Yin and Yang: Explain how the balance or imbalance of these complementary forces may relate to the situation. 2. Qi (Vital Energy): Consider how the flow or obstruction of Qi could be affecting the body meridians and overall health. 3. Five Elements (Wu Xing): Discuss how the interaction or imbalance between Wood, Fire, Earth, Metal, and Water may impact the corresponding organs. 4. Meridian System: Assess the role of the body energy channels in the context of the question, particularly how they link to specific organs. 5. Zang-Fu Theory: Analyze the roles of solid (Zang) and hollow (Fu) organs and their relationships in the body overall function. 6. Holistic Approach: Address how physical, emotional, and environmental factors might be interconnected in this case. 7. Balance and Harmony: Consider how internal balance and external harmony influence the overall well-being in this context. 8. Prevention: Suggest preventive measures based on lifestyle or early intervention, as TCM values prevention as a key to health. Carefully review the user question, and then apply these principles to provide a well-rounded TCM analysis. User question: "
}

# Dropdown for agent selection
agent_selected = st.selectbox(
    "Select a specialized agent",
    ["Generalist","Medicine", "Legal", "Physics", "Mathematics", "Psychology", "Fact Checker","Traditional Chinese Medicine"]
)

# Initialize conversation history and first question flag in session state if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_question" not in st.session_state:
    st.session_state.first_question = True

# Button to reset chat history
if st.button("Reset Chat"):
    st.session_state.messages = []
    st.session_state.first_question = True
    st.experimental_rerun()

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask something"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in the chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation context from previous messages
    conversation_context = ""
    total_tokens = 0

    if st.session_state.first_question:
        # Tailor the prompt for the first question based on the selected agent
        specialized_prompt = specialized_prompts[agent_selected] + f" Question: {prompt}"
        conversation_context = specialized_prompt
        st.session_state.first_question = False
    else:
        # For subsequent questions, include the history
        for msg in reversed(st.session_state.messages):
            message_content = f'{msg["role"]}: {msg["content"]}\n'
            message_tokens = estimate_tokens(message_content)
            
            if total_tokens + message_tokens <= MAX_TOKENS:
                conversation_context = message_content + conversation_context
                total_tokens += message_tokens
            else:
                break  # Stop adding messages if the token limit is reached

    # Generate response from Gemini (using GenerativeModel)
    response = model.generate_content(conversation_context)

    # Add Gemini response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.text)
    
    # Add copy to clipboard button for the response
    copy_to_clipboard_button(response.text)
