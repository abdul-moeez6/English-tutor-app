import streamlit as st
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from gtts import gTTS
import os, io, tempfile
import speech_recognition as sr

# ── NLTK downloads ────────────────────────────────────────────────────────────
for pkg in ['punkt', 'punkt_tab', 'averaged_perceptron_tagger',
            'averaged_perceptron_tagger_eng']:
    nltk.download(pkg, quiet=True)

# ── PAGE CONFIG  (no emoji icon → avoids yellow-box rendering bug) ────────────
st.set_page_config(
    page_title="My English Tutor",
    layout="centered",
    page_icon="🎓",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

/* ── hide Streamlit chrome (top black bar, hamburger, footer) ── */
#MainMenu, header, footer { visibility: hidden !important; height: 0 !important; }
[data-testid="stToolbar"]   { display: none !important; }
[data-testid="stDecoration"]{ display: none !important; }
.stDeployButton             { display: none !important; }

/* ── global font & light sea-green background ── */
html, body, [class*="css"], .stApp {
    font-family: 'Nunito', sans-serif !important;
    background-color: #e8faf6 !important;
}
.block-container {
    background: #e8faf6 !important;
    padding-top: 2rem !important;
}

/* ── title ── */
.big-title {
    font-size: 46px; font-weight: 900; text-align: center;
    background: linear-gradient(90deg, #009688, #26c6a2, #0288d1, #7b1fa2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.15; margin-bottom: 2px;
}
.subtitle {
    text-align: center; color: #00796b;
    font-size: 16px; font-weight: 600; margin-bottom: 20px;
}

/* ── text area ── */
.stTextArea textarea {
    background: #ffffff !important; color: #1a1a2e !important;
    border: 2px solid #80cbc4 !important; border-radius: 14px !important;
    font-size: 15px !important; font-family: 'Nunito', sans-serif !important;
}
.stTextArea label { color: #00695c !important; font-weight: 700 !important; font-size: 15px !important; }

/* ── analyze button ── */
.stButton > button {
    background: linear-gradient(90deg, #009688, #26a69a) !important;
    color: #ffffff !important; font-size: 17px !important; font-weight: 800 !important;
    border-radius: 50px !important; border: none !important;
    padding: 13px 28px !important; box-shadow: 0 4px 16px rgba(0,150,136,.35) !important;
    width: 100%; transition: transform .15s;
}
.stButton > button:hover { transform: scale(1.03) !important; }

/* ── audio recorder label ── */
.stAudioInput label { color: #00695c !important; font-weight: 700 !important; }

/* ── stat cards ── */
.stat-card {
    background: linear-gradient(135deg, #b2dfdb, #e0f7fa);
    border: 1.5px solid #80cbc4; border-radius: 16px;
    padding: 14px 8px; text-align: center;
}
.stat-num { font-size: 30px; font-weight: 900; color: #00695c; }
.stat-lbl { font-size: 13px; color: #004d40; font-weight: 600; }

/* ══ Sentence colour themes ════════════════════════════════════════════════ */
.s0 { background: linear-gradient(135deg,#ffe0e0,#fff5f5);
      border-left:6px solid #e57373; border-radius:20px;
      padding:18px; margin:18px 0; box-shadow:0 4px 18px rgba(229,115,115,.18); }
.s1 { background: linear-gradient(135deg,#dceefb,#f0f8ff);
      border-left:6px solid #42a5f5; border-radius:20px;
      padding:18px; margin:18px 0; box-shadow:0 4px 18px rgba(66,165,245,.18); }
.s2 { background: linear-gradient(135deg,#d4f5ec,#f0fff8);
      border-left:6px solid #26c6a2; border-radius:20px;
      padding:18px; margin:18px 0; box-shadow:0 4px 18px rgba(38,198,162,.18); }
.s3 { background: linear-gradient(135deg,#ede7f6,#faf5ff);
      border-left:6px solid #ab47bc; border-radius:20px;
      padding:18px; margin:18px 0; box-shadow:0 4px 18px rgba(171,71,188,.18); }
.s4 { background: linear-gradient(135deg,#fff3e0,#fffde7);
      border-left:6px solid #ffa726; border-radius:20px;
      padding:18px; margin:18px 0; box-shadow:0 4px 18px rgba(255,167,38,.18); }

/* ── sentence header ── */
.sent-hdr {
    font-size:16px; font-weight:800; color:#1a1a2e;
    background:rgba(0,0,0,.07); border-radius:10px;
    padding:7px 14px; margin-bottom:12px; display:inline-block;
}

/* ── word cards ── */
.wcard {
    background: rgba(255,255,255,.80);
    border: 1.5px solid rgba(0,0,0,.08);
    border-radius:13px; padding:10px 15px; margin:7px 0; color:#1a1a2e;
}
.wtitle { font-size:21px; font-weight:900; color:#1a1a2e; }
.badge  {
    display:inline-block; background:#009688; color:#fff;
    border-radius:30px; padding:2px 11px;
    font-size:12px; font-weight:700;
    margin-left:8px; vertical-align:middle;
}
.wdetail { font-size:13px; margin-top:4px; color:#37474f; }

/* ── audio panel ── */
.audio-panel {
    background: linear-gradient(135deg,#b2dfdb,#e0f7fa);
    border:2px solid #80cbc4; border-radius:18px;
    padding:18px; margin:20px 0;
    color:#004d40; font-weight:700; font-size:15px;
}

hr { border-color: #b2dfdb !important; }
.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TITLE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="big-title">My English Tutor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Learn every word and sentence — the fun, easy way!</div>',
    unsafe_allow_html=True
)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
#  POS DICTIONARY
# ══════════════════════════════════════════════════════════════════════════════
POS = {
    'NN':   ('Noun',                  'Names a person, place, thing, or idea.'),
    'NNS':  ('Plural Noun',           'More than one noun (cats, books).'),
    'NNP':  ('Proper Noun',           'A special name like Ali or Lahore.'),
    'NNPS': ('Plural Proper Noun',    'Multiple proper names.'),
    'VB':   ('Verb',                  'An action or doing word (base form).'),
    'VBG':  ('Verb -ing',             'An ongoing action (running, eating).'),
    'VBD':  ('Past Tense Verb',       'An action that already happened.'),
    'VBN':  ('Past Participle',       'Used with has / have / had.'),
    'VBP':  ('Present Verb',          'An action happening now.'),
    'VBZ':  ('Verb (he/she/it)',      'Action done by he, she, or it.'),
    'MD':   ('Modal Verb',            'Can, could, should, would, must, etc.'),
    'JJ':   ('Adjective',             'Describes a noun.'),
    'JJR':  ('Comparative Adjective', 'Compares two things (bigger, faster).'),
    'JJS':  ('Superlative Adjective', 'The most extreme (biggest, fastest).'),
    'RB':   ('Adverb',                'Tells how, when, or where something happens.'),
    'RBR':  ('Comparative Adverb',    'More quickly, louder, etc.'),
    'RBS':  ('Superlative Adverb',    'Most quickly, loudest, etc.'),
    'IN':   ('Preposition',           'Shows position or relation (in, on, under, by).'),
    'DT':   ('Determiner',            '"a", "an", "the" — points to a noun.'),
    'PRP':  ('Pronoun',               'Replaces a noun (he, she, it, they).'),
    'PRP$': ('Possessive Pronoun',    'Shows ownership (my, your, his, her).'),
    'WP':   ('Wh-Pronoun',            'Who, what, whoever.'),
    'WDT':  ('Wh-Determiner',         'Which, that, whatever.'),
    'WRB':  ('Wh-Adverb',             'Where, when, why, how.'),
    'CC':   ('Conjunction',           'Joins words or clauses (and, but, or).'),
    'CD':   ('Number',                'A number word (one, two, 5).'),
    'TO':   ('"to"',                  'The word "to" before a verb.'),
    'EX':   ('Existential there',     '"There is", "There are".'),
    'UH':   ('Interjection',          'Wow, oh, oops, hey, etc.'),
    'RP':   ('Particle',              'Small words like up, off, out with verbs.'),
    'FW':   ('Foreign Word',          'A word borrowed from another language.'),
    'PDT':  ('Predeterminer',         'Both, all, half — come before the determiner.'),
}

PUNCT = set('.,!?;:\'"()[]{}…–—``\'\'')

# ══════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS  (all defined before any use)
# ══════════════════════════════════════════════════════════════════════════════

def tokenize_sentences(text):
    """Split text into individual sentences."""
    return sent_tokenize(text)

def tokenize_words(sentence):
    """Split a sentence into word tokens."""
    return word_tokenize(sentence)

def get_pos_tags(words):
    """Return list of (word, POS-tag) tuples."""
    return pos_tag(words)

def explain_pos(tag):
    """Return (name, description) for a POS tag."""
    return POS.get(tag, ('Other Word', 'This word supports the sentence structure.'))

def explain_word(word, tag):
    """Return a simple explanation of this word's role."""
    w = f'"{word}"'
    if tag.startswith('NN'):   return f'{w} names something in the sentence.'
    if tag.startswith('VB'):   return f'{w} is the action or event being described.'
    if tag.startswith('JJ'):   return f'{w} describes or adds detail to something.'
    if tag.startswith('RB'):   return f'{w} tells us more about how something happens.'
    if tag in ('PRP', 'PRP$'): return f'{w} stands in for a noun or shows ownership.'
    if tag == 'DT':            return f'{w} helps point to a specific or general noun.'
    if tag == 'IN':            return f'{w} shows how parts of the sentence relate.'
    if tag == 'CC':            return f'{w} connects two ideas or clauses together.'
    if tag == 'MD':            return f'{w} shows ability, possibility, or obligation.'
    if tag == 'CD':            return f'{w} is a number used in the sentence.'
    if tag == 'TO':            return f'{w} links the verb to what comes next.'
    return                            f'{w} supports the overall meaning of the sentence.'

def make_audio(text):
    """Generate TTS audio and return as in-memory BytesIO (no disk write)."""
    buf = io.BytesIO()
    gTTS(text).write_to_fp(buf)
    buf.seek(0)
    return buf

def transcribe_audio(audio_bytes):
    """
    Transcribe WAV bytes from st.audio_input() via Google Speech Recognition.
    Works over ngrok because audio is captured in the browser, not on the server.
    Returns recognised string, or None on failure.
    """
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        with sr.AudioFile(tmp_path) as src:
            audio = r.record(src)
        return r.recognize_google(audio)
    except Exception:
        return None
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

# ══════════════════════════════════════════════════════════════════════════════
#  INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════
text_input = st.text_area(
    "Type one or more sentences:",
    height=110,
    placeholder="E.g.: The cat sat on the mat. Dogs love to play outside!"
)

st.markdown("**Or record your voice:**")
audio_data = st.audio_input("Click the mic to record")

if audio_data is not None:
    raw_bytes = audio_data.read()
    with st.spinner("Transcribing your voice..."):
        spoken = transcribe_audio(raw_bytes)
    if spoken:
        st.success(f"You said: {spoken}")
        text_input = spoken
    else:
        st.error("Could not understand the audio — please try again or type instead.")

st.markdown("")
analyze = st.button("Analyze My Sentences!", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
COLORS = ['s0', 's1', 's2', 's3', 's4']

if analyze:
    raw_text = (text_input or "").strip()
    if not raw_text:
        st.warning("Please enter or record a sentence first!")
        st.stop()

    sentences  = tokenize_sentences(raw_text)
    all_tokens = tokenize_words(raw_text)
    real_words = [w for w in all_tokens if w not in PUNCT]

    # ── Stats strip ──────────────────────────────────────────────────────────
    st.markdown("### Quick Stats")
    c1, c2, c3 = st.columns(3)
    avg = round(len(real_words) / max(len(sentences), 1), 1)
    for col, num, lbl in [(c1, len(sentences),  "Sentences"),
                           (c2, len(real_words), "Total Words"),
                           (c3, avg,             "Words / Sentence")]:
        col.markdown(
            f'<div class="stat-card">'
            f'<div class="stat-num">{num}</div>'
            f'<div class="stat-lbl">{lbl}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("### Sentence-by-Sentence Breakdown")

    narration = ""

    for i, sentence in enumerate(sentences):
        color      = COLORS[i % len(COLORS)]
        words      = tokenize_words(sentence)
        tags       = get_pos_tags(words)          # ← properly called now
        real_count = sum(1 for w, _ in tags if w not in PUNCT)
        cards_html = ""
        sent_narr  = f"Sentence {i + 1}: {sentence}. "

        for word, tag in tags:
            if word in PUNCT:
                continue
            pos_name, pos_desc = explain_pos(tag)
            word_desc          = explain_word(word, tag)
            sent_narr         += f"{word} is a {pos_name}. "

            cards_html += f"""
            <div class="wcard">
              <span class="wtitle">{word}</span>
              <span class="badge">{pos_name}</span>
              <div class="wdetail"><b>Role in sentence:</b> {word_desc}</div>
              <div class="wdetail"><b>What is a {pos_name}?</b> {pos_desc}</div>
            </div>"""

        st.markdown(f"""
        <div class="{color}">
          <div class="sent-hdr">Sentence {i + 1} &bull; {real_count} words</div>
          <p style="color:#263238;font-size:16px;font-style:italic;margin-bottom:10px;">
            "{sentence}"
          </p>
          {cards_html}
        </div>
        """, unsafe_allow_html=True)

        narration += sent_narr

    # ── Audio ─────────────────────────────────────────────────────────────────
    st.markdown("### Listen to the Full Explanation")
    st.markdown(
        '<div class="audio-panel">'
        'Press play to hear a complete audio explanation of all your sentences.'
        '</div>',
        unsafe_allow_html=True
    )
    with st.spinner("Generating audio..."):
        audio_buf = make_audio(narration)
    st.audio(audio_buf, format='audio/mp3')

    st.balloons()
    st.success("Analysis complete! Scroll up to explore each sentence block.")
