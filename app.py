import streamlit as st
from groq import Groq

# Injection de CSS personnalisé pour le style des liens
st.markdown("""
    <style>
    /* Cible les liens dans la barre latérale */
    [data-testid="stSidebar"] a {
        text-decoration: none; 
        color: #0077B5;
        font-weight: bold;
    }
    
    /* Effet au survol */
    [data-testid="stSidebar"] a:hover {
        text-decoration: underline; 
        color: #FF4B4B; /* Change de couleur au survol */
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Configuration de la page
st.set_page_config(page_title="IA Portfolio - Sarah Hamri", page_icon="🔎")

# 2. Barre latérale
with st.sidebar:
    st.title("💻 Profil")
    st.write("Je suis une développeuse passionnée par la technologie et la résolution de problèmes.")
    
    # Liens
    st.write("[🔗 GitHub](https://github.com/shamizuken)")
    st.write("[🔗 LinkedIn](https://www.linkedin.com/in/sarah-hamri-ab1b74310/)")
    
    st.divider()
    st.write("### Tech Stack")
    st.code("Python\nStreamlit\nGroq API\nLlama 3.1")

st.title("💬 Mon assistant IA")

# 3. Sécurité de la clé API

if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    st.error("Clé API introuvable. Veuillez configurer les secrets.")
    st.stop() 

client = Groq(api_key=GROQ_API_KEY)

# 4. Historique du chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Logique de discussion
if prompt := st.chat_input("Posez-moi une question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system", 
                        "content": """
                        Tu es l'assistant personnel de Sarah. 
                        Ton rôle est d'aider les recruteurs à découvrir son profil.
                        Voici les informations cruciales à transmettre :
    - Sa base technique principale est le développement Web : HTML, CSS et JavaScript.
    - Elle apprends Python en autodidacte par curiosité pour l'IA.
    - Ce chatbot prouve sa capacité à sortir de sa zone de confort et à apprendre un nouveau langage (Python) très rapidement pour répondre à un besoin technique.
    - Elle a su gérer toute la chaîne : installation de l'environnement, intégration d'API (Groq), gestion des secrets et déploiement.
    
    Ton ton doit être :
    - Fier de son parcours : insiste sur le fait que même si Python n'est pas son langage n°1, elle a réussi à livrer un projet fonctionnel et sécurisé.
    - Professionnel et dynamique.
    
    Si on te pose des questions sur ses projets, mentionne que son expertise Front-end (HTML/CSS/JS) lui permet de créer des interfaces soignées, et que ce projet Python montre sa polyvalence.
                        
                        Voici les infos clés sur elle:
                        - Elle apprend le développement Python en autodidacte.
                        - Elle a construit ce chatbot elle-même en utilisant Streamlit et l'API de Groq par défi.
                        - Elle sait gérer les API, l'installation d'environnements et le débogage (erreurs 400/401).
                        - Elle maîtrise HTML et CSS. 
                        - Elle à de bonnes bases en JS.
                        - Elle apprends Python dans son temps libre.
                        - Elle est passionnée par la technologie et la résolution de problèmes.
                        - Elle à un esprit carré, structuré et organisé ce qui rend la réflexion "code" plus naturelle. 
                        CONSIGNE CRUCIALE SUR SA FORMATION :
                         - Elle à un bachelier en Ecriture Multimédia de l'ISFSC, Bruxelles. Mais elle n'a pas eu l'impression d'être complète dans son apprentissage.
                         - IMPORTANT : L'acronyme 'ISFSC' ne doit JAMAIS être traduit ou détaillé. C'est le nom propre de l'école. Ne cherche pas à donner une définition à chaque lettre, utilise simplement le nom 'ISFSC'. 
                        - Elle avait commencer une formation en UX-UI Design à l'EFP mais ça ne lui plaisait plus tant que ça, à part les cours de Conception Web, Front-end et Back-end. 
                        - Elle s'est décidé de faire une formation en Développeuse Web Front-end car les cours de code lors de ses précédentes formations lui ont plu. 
                        - Elle est curieuse, persévérante, autonome, ponctuelle et aidante.
                        - Loisirs : Lecture (mangas/romans), sitcoms, nature et musique.
                        - Elle parle français (langue maternelle), anglais (niveau C1) et apprends le coréen dans son temps libre.
                        
                        Instructions : Sois pro, accueillant, et mets en avant sa vitesse d'apprentissage.
                        """
                    },
                    {"role": "user", "content": prompt}
                ],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:

            st.error(f"Oups, une erreur est survenue : {e}")

