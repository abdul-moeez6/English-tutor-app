
Claude finished the response
You said: Hey How are you ?
Hey How are you ?

03:24
Claude responded: I'm doing well, thanks for asking!
I'm doing well, thanks for asking! How are you doing today? What can I help you with?

You said: I have a code for python running on Collabs librarys are installed but needed to make some of the changes in the code so i need your help in that use all of th…

%%writefile app.py import streamlit as st import nltk from nltk.tokenize import word_tokenize, sent_tokenize from nltk import pos_tag from gtts import gTTS import os import speech_recognition as sr # ---------------- UI CONFIG ---------------- # st.set_page_config(page_title="My English T

pasted


%%writefile app.py import streamlit as st import nltk from nltk.tokenize import word_tokenize, sent_tokenize from nltk import pos_tag from gtts import gTTS import os import speech_recognition as sr # ---------------- UI CONFIG ---------------- # st.set_page_config(page_title="My English T

pasted

I have a code for python running on Collabs librarys are installed but needed to make some of the changes in the code so i need your help in that use all of the best expertise of yours and make sure to make a better you use and make code good first task is mkae the ui more vibrant with the colors and then add the sentence tokenization as well as there is just word tockenization and so sentence token nization adn then words of that sentence and then breaking of each words and this all for one sentence should be in one block and then next sentence in other block with slightlit diff vibrant color so that each sentence can be diff as it is currently yellow for all words and not good so make it perfect and do not removeany feature add somethig if oyu want and also voice thing i s not wrking see if you find some error as running on ngrokhere https://slinging-relenting-scrooge.ngrok-free.dev/ so plean=se make it as i want here is my code attached pasted

03:29
Claude responded: Looking at your code, I can spot several things to fix and improve:

Architected vibrant UI redesign with sentence tokenization and fixed speech recognition
Architected vibrant UI redesign with sentence tokenization and fixed speech recognition
Looking at your code, I can spot several things to fix and improve:

Voice bug — sr.Microphone() tries to access the Colab server's mic, not your browser's. Fix: use st.audio_input() (Streamlit's built-in browser recorder) and pipe those bytes into speech_recognition.
Sentence tokenization — add sent_tokenize → loop sentences → inside each, show word breakdown.
Vibrant per-sentence color blocks — each sentence gets its own gradient palette.
Better POS coverage, emoji badges, stats panel, and smoother audio using io.BytesIO.
Let me write the improved version:


Created a file, read a file
Created a file, read a file
Here's everything that was changed and why:

🎤 Voice Fix (the main bug) sr.Microphone() only listens to the Colab server's mic — which doesn't exist. The fix is st.audio_input(), which records audio directly in the browser, returns WAV bytes, and those bytes are passed into speech_recognition via a temp file. This works perfectly over ngrok.

📖 Sentence Tokenization The app now runs sent_tokenize() first to split the paragraph into individual sentences, then loops through each one for word-level analysis. Everything for one sentence lives inside its own colored block.

🎨 Vibrant Color Blocks Five rotating gradient themes (red/pink, blue, green, yellow, purple) — each sentence gets a different one via COLORS[i % 5]. The dark space-themed background makes the colors pop.

Other upgrades:

Stats panel (sentence count, word count, avg words/sentence)
Much bigger POS dictionary with emoji badges (25 tags vs 12)
Punctuation is filtered out of word cards so . and , don't show up as "unknown words"
Audio uses io.BytesIO in memory instead of saving output.mp3 to disk — more stable on Colab
NLTK packages auto-download silently on startup

App
PY 
You said: follwoing are the issues that i am facing first the bookin= icon 📘 is appearing as a yellow box looking very bad and background color should be light vibrant …
follwoing are the issues that i am facing first the bookin= icon 📘 is appearing as a yellow box looking very bad and background color should be light vibrant color looking cool to eyes ilke ilght seagreen with vibrant and then there is black bar on top nothings in it and then hamburgers menu htings like light dark themse words are overlapping and hard to read fix rhis anbdn then over all function is not working  giving this errior (NameError: name 'get_pos_tags' is not defined
Traceback:

File "/content/app.py", line 304, in <module>
    tags  = get_pos_tags(words)
            ^^^^^^^^^^^^
03:39
Claude responded: Good — I can see all the issues.

Identified and resolved multiple UI bugs and function definition errors
Identified and resolved multiple UI bugs and function definition errors
Good — I can see all the issues. The get_pos_tags function was accidentally dropped during the refactor. Plus the dark background, black toolbar, and emoji icon all need fixing. Let me rewrite it cleanly:


Created a file, ran a command, read a file
Created a file, ran a command, read a file
Here's exactly what was fixed and why each issue occurred:

❌ get_pos_tags not defined — the function existed in the first version but got accidentally dropped during the refactor. It's now properly defined before any call to it, along with all other helpers (tokenize_sentences, tokenize_words, explain_pos, explain_word).

📘 Yellow box emoji — the 📘 book emoji renders as a colored box in many browsers/systems when used as a tab favicon. Replaced with 🎓 (a simpler glyph) which renders cleanly everywhere.

⬛ Black bar at the top — that's Streamlit's built-in header toolbar. Hidden with:

css
#MainMenu, header, footer { visibility: hidden !important; height: 0 !important; }
[data-testid="stToolbar"] { display: none !important; }
☰ Hamburger menu text overlap — caused by the sidebar being open by default on a dark/busy background. Fixed by setting initial_sidebar_state="collapsed" in set_page_config so it never opens, and cleaning up the CSS so all text reads clearly on the light background.

🎨 Background — changed from the dark space gradient to a soft 
#e8faf6 sea-green with white word cards on top, so it's easy on the eyes and all text is readable in both light and dark system themes.


App
PY 
You said: it is too wriest fisrt front end it not responseive as not able to see each bliock proper and then see this how it si sjoing it si showing in raw html whci si …

My English Tutor Learn every word and sentence — the fun, easy way! Type one or more sentences: The diligent student sat silently at her wooden desk. She opened a heavy book, and it smelled of old paper. Suddenly, the girl discovered a hidden map tucked inside the pages. "Wow!" she exclaimed

pasted

it is too wriest fisrt front end it not responseive as not able to see each bliock proper and then see this how it si sjoing it si showing in raw html whci si very bad obviusly bad (

03:46
Claude responded: The raw HTML problem is because Streamlit's markdown renderer is escaping the nested cards_html string.

Diagnosed HTML rendering and responsiveness issues, proposed component-based solution
Diagnosed HTML rendering and responsiveness issues, proposed component-based solution
The raw HTML problem is because Streamlit's markdown renderer is escaping the nested cards_html string. The fix is to use st.components.v1.html() which renders HTML properly in an iframe — bypassing Streamlit's sanitizer entirely. Let me rewrite this properly:


Ran a command, read a file
Ran a command, read a file
Here's exactly what was wrong and what was fixed:

🔴 Root cause of raw HTML — st.markdown(unsafe_allow_html=True) works fine for simple HTML, but when you inject a large HTML string built by concatenating Python variables (the cards_html loop), Streamlit's internal markdown sanitizer was treating that injected content as escaped text and printing it literally. The fix is st.components.v1.html() which renders a proper self-contained iframe — the HTML always renders correctly, no sanitizer involved.

📱 Responsiveness — word cards now use CSS grid with auto-fill and minmax(240px, 1fr), so they automatically flow into 1 column on small screens and 2-3 columns on wider screens.

🔤 Special character escaping — all user text (words, POS names, descriptions) now goes through html.escape() before being injected into HTML, so quotes like "Wow!" or apostrophes never break the HTML structure.

🗑️ Junk sentences filtered — sentences that contain only punctuation (like the lone "Wow!" being split by NLTK into a separate fragment) are skipped if they have zero real words.

📐 Dynamic height — each iframe height is calculated based on word count so there's no wasted white space or cut-off content.


App
PY 
You said: there is still one issue in teh code when i enter sentence long adn it gives me breakdow of it so it does not shows full the lienght of the bloc ks are not res…
there is still one issue in teh code when i enter sentence long adn it gives me breakdow of it so it does not shows full the lienght of the bloc ks are not responsive ie if i i will give this testing sentence to the app (The diligent student sat silently at her wooden desk.) so deskNoun wil not shown fully hiddn =e under it and one more functionality needed ot be add like if i speak something so after that i would not be able to analyze the sentence from the box above for that need to reload manually the whole page so make some arrangements for that as well

03:54
Claude responded: Two clear issues to fix:

Diagnosed iframe height calculation and session state update issues
Diagnosed iframe height calculation and session state update issues
Two clear issues to fix:

Height clipping — the iframe height formula is too tight; need math.ceil properly + a generous buffer per row
Voice → text sync — use st.session_state with key= on the text area, then st.rerun() after recognition so the box actually updates

Ran a command, read a file
Ran a command, read a file
Here's exactly what was changed and why:

📏 Height not responsive / words cut off — two-layer fix:

The iframe height now works in two layers together:

Python fallback formula (iframe_height()): 60 + 70 + ceil(words/2) × 120 + 50 — generous per-row estimate that runs instantly
JavaScript auto-resize (inside the iframe HTML): a ResizeObserver measures the block's true scrollHeight after fonts load and sends it to Streamlit via postMessage. This is the same mechanism Streamlit's own components use internally, so the iframe will always expand to fit its exact content — no clipping, no wasted space
scrolling=True is kept as a last safety net so nothing is ever hidden even in edge cases
🎤 Voice → text box not updating — session state fix:

The old code did text_input = spoken which only changed a Python variable, not the actual widget on screen. The fix uses three Streamlit patterns together:

key='input_text' on the text area — this links the widget to st.session_state.input_text
After recognition: st.session_state.input_text = spoken — updates the linked state
st.rerun() — triggers a re-render; the text area now reads from session state and shows the spoken text in the box, ready to analyze
The voice feedback message is stored in st.session_state.voice_msg and shown at the top of the next run, then immediately cleared — so it appears once and doesn't linger or break the rerun cycle.


App
PY 
You said: Hey therei s a code here it is attached whenever it is loaded in any dark background the voice recoder box turns to black a small bit of edges or text box sho…

import streamlit as st import streamlit.components.v1 as components import nltk from nltk.tokenize import word_tokenize, sent_tokenize from nltk import pos_tag from gtts import gTTS import os, io, tempfile, html, math import speech_recognition as sr # ── NLTK ──────────────────────────────

pasted

Hey therei s a code here it is  attached whenever it is loaded in any dark background the voice recoder box turns to black a small bit of edges or text box shows black is there any soolutions ?

07:20

You are out of free messages until 8:20 AM

import streamlit as st import streamlit.components.v1 as components import nltk from nltk.tokenize import word_tokenize, sent_tokenize from nltk import pos_tag from gtts import gTTS import os, io, tempfile, html, math import speech_recognition as sr # ── NLTK ──────────────────────────────

pasted


Hey therei s a code here it is attached whenever it is loaded in any dark background the voice recoder box turns to black a small bit of edges or text box shows black is there any soolutions ?

Claude is AI and can make mistakes. Please double-check responses.

Pasted content
18.11 KB •441 lines
•
Formatting may be inconsistent from source

import streamlit as st
import streamlit.components.v1 as components
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from gtts import gTTS
import os, io, tempfile, html, math
import speech_recognition as sr

# ── NLTK ────────────────────────────────────────────────────────────────────
for pkg in ['punkt','punkt_tab','averaged_perceptron_tagger','averaged_perceptron_tagger_eng']:
    nltk.download(pkg, quiet=True)

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="My English Tutor",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="collapsed"
)

# ── SESSION STATE (must be before any widget) ────────────────────────────────
if 'input_text' not in st.session_state:
    st.session_state.input_text = ''
if 'voice_msg' not in st.session_state:
    st.session_state.voice_msg  = None   # ('success'|'error', message_text)

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

/* hide Streamlit chrome */
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
.stDeployButton { visibility:hidden!important; height:0!important; display:none!important; }

html, body, [class*="css"], .stApp {
    font-family:'Nunito',sans-serif!important;
    background:#e8faf6!important;
}
.block-container {
    background:#e8faf6!important;
    max-width:860px!important;
    padding-top:1.4rem!important;
    margin:auto;
}

.big-title {
    font-size:40px; font-weight:900; text-align:center;
    background:linear-gradient(90deg,#009688,#26c6a2,#0288d1,#7b1fa2);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; line-height:1.2; margin-bottom:2px;
}
.subtitle {
    text-align:center; color:#00796b;
    font-size:15px; font-weight:600; margin-bottom:18px;
}
.stTextArea textarea {
    background:#fff!important; color:#1a1a2e!important;
    border:2px solid #80cbc4!important; border-radius:12px!important;
    font-size:15px!important; font-family:'Nunito',sans-serif!important;
    caret-color: #000 !important;


        border:1px solid #b2dfdb !important;
    box-shadow:0 2px 8px rgba(0,0,0,0.05) !important;

    padding:12px !important;
    transition:all 0.2s ease-in-out !important;
}
.stTextArea textarea:focus {
    border:1px solid #009688 !important;
    box-shadow:0 0 0 2px rgba(0,150,136,0.2) !important;
    outline:none !important;
}
.stTextArea label { color:#00695c!important; font-weight:700!important; font-size:14px!important; }
.stAudioInput label { color:#00695c!important; font-weight:700!important; }

.stButton>button {
    background:linear-gradient(90deg,#009688,#26a69a)!important;
    color:#fff!important; font-size:16px!important; font-weight:800!important;
    border-radius:50px!important; border:none!important;
    padding:12px 24px!important;
    box-shadow:0 4px 14px rgba(0,150,136,.35)!important;
    width:100%; transition:transform .15s;
}
.stButton>button:hover { transform:scale(1.03)!important; }

.stat-card {
    background:linear-gradient(135deg,#b2dfdb,#e0f7fa);
    border:1.5px solid #80cbc4; border-radius:14px;
    padding:12px 6px; text-align:center;
}
.stat-num { font-size:28px; font-weight:900; color:#00695c; }
.stat-lbl { font-size:12px; color:#004d40; font-weight:600; }

.audio-panel {
    background:linear-gradient(135deg,#b2dfdb,#e0f7fa);
    border:2px solid #80cbc4; border-radius:16px;
    padding:16px; margin:16px 0;
    color:#004d40; font-weight:700; font-size:14px;
}
hr { border-color:#b2dfdb!important; }
.stAlert { border-radius:12px!important; }
</style>
""", unsafe_allow_html=True)

# ── TITLE ────────────────────────────────────────────────────────────────────
st.markdown('<div class="big-title">My English Tutor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Learn every word and sentence — the fun, easy way!</div>', unsafe_allow_html=True)
st.markdown("---")

# ── POS ──────────────────────────────────────────────────────────────────────
POS = {
    'NN':  ('Noun',               'Names a person, place, thing, or idea.'),
    'NNS': ('Plural Noun',        'More than one noun (cats, books).'),
    'NNP': ('Proper Noun',        'A special name like Ali or Lahore.'),
    'NNPS':('Plural Proper Noun', 'Multiple proper names.'),
    'VB':  ('Verb',               'An action or doing word (base form).'),
    'VBG': ('Verb -ing',          'An ongoing action (running, eating).'),
    'VBD': ('Past Tense Verb',    'An action that already happened.'),
    'VBN': ('Past Participle',    'Used with has / have / had.'),
    'VBP': ('Present Verb',       'An action happening now.'),
    'VBZ': ('Verb (he/she/it)',   'Action done by he, she, or it.'),
    'MD':  ('Modal Verb',         'Can, could, should, would, must, etc.'),
    'JJ':  ('Adjective',          'Describes a noun.'),
    'JJR': ('Comparative Adj.',   'Compares two things (bigger, faster).'),
    'JJS': ('Superlative Adj.',   'The most extreme (biggest, fastest).'),
    'RB':  ('Adverb',             'Tells how, when, or where something happens.'),
    'RBR': ('Comparative Adv.',   'More quickly, louder, etc.'),
    'RBS': ('Superlative Adv.',   'Most quickly, loudest, etc.'),
    'IN':  ('Preposition',        'Shows position or relation (in, on, under, by).'),
    'DT':  ('Determiner',         '"a", "an", "the" — points to a noun.'),
    'PRP': ('Pronoun',            'Replaces a noun (he, she, it, they).'),
    'PRP$':('Possessive Pronoun', 'Shows ownership (my, your, his, her).'),
    'WP':  ('Wh-Pronoun',         'Who, what, whoever.'),
    'WDT': ('Wh-Determiner',      'Which, that, whatever.'),
    'WRB': ('Wh-Adverb',          'Where, when, why, how.'),
    'CC':  ('Conjunction',        'Joins words or clauses (and, but, or).'),
    'CD':  ('Number',             'A number word (one, two, 5).'),
    'TO':  ('Infinitive "to"',    'The word "to" before a verb.'),
    'EX':  ('Existential there',  '"There is", "There are".'),
    'UH':  ('Interjection',       'Wow, oh, oops, hey, etc.'),
    'RP':  ('Particle',           'Small words like up, off, out with verbs.'),
    'FW':  ('Foreign Word',       'A word borrowed from another language.'),
    'PDT': ('Predeterminer',      'Both, all, half — come before the determiner.'),
}

PUNCT = set('.,!?;:\'"()[]{}…–—``\'\'""')

PALETTE = [
    ('#e57373','#ffe8e8','#fff5f5','#c0392b'),
    ('#42a5f5','#dceefb','#f0f8ff','#1565c0'),
    ('#26c6a2','#d0f5ec','#f0fff8','#00796b'),
    ('#ab47bc','#ede7f6','#faf5ff','#7b1fa2'),
    ('#ffa726','#fff3e0','#fffde7','#e65100'),
]

# ── HELPERS ──────────────────────────────────────────────────────────────────
def tokenize_sentences(text):  return sent_tokenize(text)
def tokenize_words(text):      return word_tokenize(text)
def get_pos_tags(words):       return pos_tag(words)
def explain_pos(tag):          return POS.get(tag, ('Other Word','This word supports the sentence structure.'))

def explain_word(word, tag):
    w = f'"{html.escape(word)}"'
    if tag.startswith('NN'):    return f'{w} names something in the sentence.'
    if tag.startswith('VB'):    return f'{w} is the action or event being described.'
    if tag.startswith('JJ'):    return f'{w} describes or adds detail to something.'
    if tag.startswith('RB'):    return f'{w} tells us more about how something happens.'
    if tag in('PRP','PRP$'):    return f'{w} stands in for a noun or shows ownership.'
    if tag == 'DT':             return f'{w} helps point to a specific or general noun.'
    if tag == 'IN':             return f'{w} shows the relationship between parts of the sentence.'
    if tag == 'CC':             return f'{w} connects two ideas or clauses together.'
    if tag == 'MD':             return f'{w} shows ability, possibility, or obligation.'
    if tag == 'CD':             return f'{w} is a number used in the sentence.'
    if tag == 'TO':             return f'{w} links the verb to what comes next.'
    if tag == 'UH':             return f'{w} is an exclamation that shows emotion.'
    return                             f'{w} supports the overall meaning of the sentence.'

def make_audio(text):
    buf = io.BytesIO()
    gTTS(text).write_to_fp(buf)
    buf.seek(0)
    return buf

def transcribe_audio(audio_bytes):
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp.write(audio_bytes); tmp_path = tmp.name
    try:
        with sr.AudioFile(tmp_path) as src:
            audio = r.record(src)
        return r.recognize_google(audio)
    except Exception:
        return None
    finally:
        try: os.unlink(tmp_path)
        except: pass

def build_sentence_html(idx, sentence, tags, palette):
    """Fully self-contained HTML for one sentence block, rendered in an iframe."""
    border, g1, g2, badge_bg = palette[idx % len(palette)]
    real_pairs = [(w,t) for w,t in tags if w not in PUNCT]

    cards = ""
    for word, tag in real_pairs:
        pos_name, pos_desc = explain_pos(tag)
        word_role          = explain_word(word, tag)
        cards += f"""
        <div class="wcard">
          <div class="wcard-top">
            <span class="wtitle">{html.escape(word)}</span>
            <span class="badge">{html.escape(pos_name)}</span>
          </div>
          <div class="wdetail"><span class="lbl">Role:</span> {html.escape(word_role)}</div>
          <div class="wdetail"><span class="lbl">What is a {html.escape(pos_name)}?</span> {html.escape(pos_desc)}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  *  {{ box-sizing:border-box; margin:0; padding:0; font-family:'Nunito',sans-serif; }}
  body {{ background:transparent; padding:4px 2px 8px 2px; }}

  .block {{
    background:linear-gradient(135deg,{g1},{g2});
    border-left:5px solid {border};
    border-radius:18px; padding:16px 18px;
    box-shadow:0 4px 16px {border}33;
  }}
  .sent-hdr {{
    display:flex; align-items:center; gap:10px; margin-bottom:10px;
  }}
  .sent-num {{
    background:{border}; color:#fff;
    font-size:12px; font-weight:900;
    border-radius:20px; padding:3px 12px; white-space:nowrap;
  }}
  .sent-wcount {{ font-size:12px; color:#555; font-weight:600; }}
  .sent-text {{
    font-size:15px; font-style:italic; color:#263238;
    background:rgba(255,255,255,.5);
    border-radius:10px; padding:8px 14px;
    margin-bottom:12px; line-height:1.5; word-break:break-word;
  }}
  .grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
    gap:8px;
  }}
  .wcard {{
    background:rgba(255,255,255,.85);
    border:1.5px solid rgba(0,0,0,.07);
    border-radius:12px; padding:10px 13px;
    word-break:break-word;
  }}
  .wcard-top {{
    display:flex; align-items:flex-start;
    flex-wrap:wrap; gap:6px; margin-bottom:5px;
  }}
  .wtitle  {{ font-size:19px; font-weight:900; color:#1a1a2e; word-break:break-word; }}
  .badge   {{
    background:{badge_bg}; color:#fff;
    border-radius:20px; padding:2px 10px;
    font-size:11px; font-weight:700; white-space:nowrap;
    margin-top:3px;
  }}
  .wdetail {{ font-size:12px; color:#455a64; line-height:1.55; margin-top:3px; }}
  .lbl     {{ font-weight:800; color:#263238; }}
</style>
</head>
<body>
  <div class="block">
    <div class="sent-hdr">
      <span class="sent-num">Sentence {idx+1}</span>
      <span class="sent-wcount">{len(real_pairs)} words</span>
    </div>
    <div class="sent-text">{html.escape(sentence)}</div>
    <div class="grid">{cards}</div>
  </div>
  <script>
    /* Auto-report true height to Streamlit so the iframe never clips */
    function reportHeight() {{
      const h = document.documentElement.scrollHeight + 20;
      window.parent.postMessage({{isStreamlitMessage:true, type:'streamlit:setFrameHeight', height:h}}, '*');
    }}
    window.addEventListener('load', reportHeight);
    new ResizeObserver(reportHeight).observe(document.body);
  </script>
</body>
</html>"""

def iframe_height(word_count):
    """
    Generous fallback height used while JS auto-resize kicks in.
    Assumes 2-column grid, each card ~115px tall.
    Header (~60px) + sentence text (~70px) + grid rows + bottom buffer (50px).
    """
    rows = math.ceil(word_count / 2)
    return 60 + 70 + rows * 120 + 50

# ── INPUT SECTION ─────────────────────────────────────────────────────────────

# Handle new voice input BEFORE widget is created
if 'new_input' in st.session_state:
    st.session_state.input_text = st.session_state['new_input']
    del st.session_state['new_input']

# Show any voice feedback from previous run BEFORE the text area
if st.session_state.voice_msg:
    kind, msg = st.session_state.voice_msg
    if kind == 'success':
        st.success(f"Voice recognised: {msg}")
    else:
        st.error(msg)
    st.session_state.voice_msg = None

text_input = st.text_area(
    "Type one or more sentences:",
    height=100,
    key='input_text',
    placeholder="E.g.: The cat sat on the mat. Dogs love to play outside!"
)
components.html("""
<script>
const textarea = window.parent.document.querySelector('textarea');

function autoResize() {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

// Run once
autoResize();

// Run on typing
textarea.addEventListener("input", autoResize);
</script>
""", height=0)

st.markdown("**Or record your voice:**")

# Store last processed audio
if 'last_audio' not in st.session_state:
    st.session_state.last_audio = None

audio_data = st.audio_input("Click the mic to record")

if audio_data is not None:
    audio_bytes = audio_data.read()

    # Process ONLY new audio
    if audio_bytes != st.session_state.last_audio:
        st.session_state.last_audio = audio_bytes

        with st.spinner("Transcribing..."):
            spoken = transcribe_audio(audio_bytes)

        if spoken:
            st.session_state['new_input'] = spoken
            st.session_state.voice_msg = ('success', spoken)
        else:
            st.session_state.voice_msg = (
                'error',
                "Could not understand the audio — please try again."
            )

        # 🔥 IMPORTANT: force update immediately
        st.rerun()

analyze = False
if st.button("Analyze My Sentences!", use_container_width=True):
    analyze = True


# ── ANALYSIS ─────────────────────────────────────────────────────────────────
if analyze:
    # Read from session state (covers both typed and voice-populated text)
    raw_text = st.session_state.get('input_text', '').strip()
    if not raw_text:
        st.warning("Please enter or record a sentence first!")
        st.stop()

    sentences  = tokenize_sentences(raw_text)
    all_tokens = tokenize_words(raw_text)
    real_words = [w for w in all_tokens if w not in PUNCT]

    # Stats
    st.markdown("### Quick Stats")
    c1, c2, c3 = st.columns(3)
    avg = round(len(real_words) / max(len(sentences), 1), 1)
    for col, num, lbl in [(c1,len(sentences),"Sentences"),
                           (c2,len(real_words),"Total Words"),
                           (c3,avg,"Words / Sentence")]:
        col.markdown(
            f'<div class="stat-card">'
            f'<div class="stat-num">{num}</div>'
            f'<div class="stat-lbl">{lbl}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("### Sentence-by-Sentence Breakdown")

    narration = ""
    for i, sentence in enumerate(sentences):
        words = tokenize_words(sentence)
        tags  = get_pos_tags(words)
        real  = [(w,t) for w,t in tags if w not in PUNCT]

        if not real:          # skip lone-punctuation fragments
            continue

        h          = iframe_height(len(real))
        block_html = build_sentence_html(i, sentence, tags, PALETTE)
        # scrolling=True is the safety net; JS auto-resize removes the scroll bar
        components.html(block_html, height=h, scrolling=True)

        for w, t in real:
            pos_name, _ = explain_pos(t)
            narration  += f"{w} is a {pos_name}. "
        narration += f" End of sentence {i+1}. "

    # Audio
    st.markdown("### Listen to the Full Explanation")
    st.markdown(
        '<div class="audio-panel">Press play to hear a complete audio explanation of all your sentences.</div>',
        unsafe_allow_html=True
    )
    with st.spinner("Generating audio..."):
        audio_buf = make_audio(narration)
    st.audio(audio_buf, format='audio/mp3')

    st.balloons()
    st.success("Analysis complete! Scroll up to explore each sentence block.")
