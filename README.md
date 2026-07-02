# 📖 Bible RAG Agent

A Retrieval Augmented Generation (RAG) chatbot answering **Hebrew** questions about the Hebrew Bible, using a local Chroma vector store and the OpenAI API. It retrieves the relevant passages, then answers with verse citations.

---

# ✨ Features

* 🇮🇱  Hebrew only chat
* 📄 PDF knowledge source
* 🧠 OpenAI embeddings + generation
* 🔎 Local Chroma vector store
* 📚 Verse aware chunking
* 💬 In-memory conversation history
* 🔄 Follow up refinement
* 📍 Source citations in every answer

---

# 🚀 Getting Started

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Configure

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
OPENAI_CHAT_MODEL=gpt-5.5
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

BIBLE_PDF_PATH=./data/input/hebrew_bible.pdf
CHROMA_PERSIST_DIR=./data/chroma

CHUNK_WINDOW_SIZE=6
CHUNK_OVERLAP=2
RETRIEVER_TOP_K=15
CONVERSATION_MAX_TURNS=10
CENSOR_GODS_NAMES=True
```

### 3. Add the Bible PDF

```text
data/input/hebrew_bible.pdf
```

### 4. Build the vector store

```bash
python src/indexing/build_index.py
```

### 5. Start chatting

```bash
python src/main.py
```

---

# ⚙️ System Flow

**📦 Indexing**

```text
PDF → Extract → Clean → Parse → Chunk → Embed → Chroma
```

**💬 Chat**

```text
User → CLI → Refiner → Retriever → Prompt → OpenAI → Validator → Answer
```

---

# 💬 Chat Example

```text
צ'אט תנ״ך - שאל כל שאלה...

> מי היה אברהם?

אברהם, שנקרא בתחילה אברם, היה אדם שאליו דיבר ה’ וכרת עמו ברית. שמו שונה לאברהם: “כי אב המון גוים נתתיך”. נאמר עליו שיהיה “לגוי גדול ועצום”, ש“ונברכו בו כל גויי הארץ”, ושמלכים וגויים יצאו ממנו.

הוא נקרא גם “נביא” ו“אברהם עבדו”. אשתו הייתה שרה, ובניו המוזכרים בקטעים הם יצחק וישמעאל. הברית הוקמה עם יצחק, ואברהם נתן “את כל אשר לו ליצחק”. אברהם חי “מאת שנה ושבעים שנה וחמש שנים”, מת “בשיבה טובה זקן ושבע”, ונקבר ב“מערת המכפלה”.

מקורות:
- בראשית 17:1-6
- בראשית 18:17-22
- בראשית 20:5-10
- תהלים 105:41-45
- בראשית 17:17-22
- בראשית 25:5-10

> ספר לי עליו יותר

אברהם נקרא בתחילה אברם. כשהיה “בן תשעים שנה ותשע שנים” נראה אליו ה’ ואמר לו: “התהלך לפני והיה תמים”. אלוקים כרת עמו ברית, הבטיח להרבות אותו “במאד מאד”, ושינה את שמו לאברהם: “כי אב המון גוים נתתיך”. נאמר עליו: “ונתתיך לגוים ומלכים ממך יצאו”.

הברית נגעה גם לזרעו אחריו: “לברית עולם”, ולארץ כנען “לאחזת עולם”. חלק מן הברית שנמסרה לו היה: “המול לכם כל זכר”.

אשתו הייתה שרה. אלוקים אמר ששרה תלד לו בן ושמו יהיה יצחק, ושאת הברית יקים עם יצחק. אברהם ביקש גם על ישמעאל, ואלוקים אמר: “ולישמעאל שמעתיך”, והבטיח: “ונתתיו לגוי גדול”.

אברהם מתואר גם כ“נביא”, וכ“אברהם עבדו”. ה’ אמר עליו שיצווה “את בניו ואת ביתו אחריו”, ושישמרו “דרך ה’ לעשות צדקה ומשפט”. עוד נאמר עליו: “ואברהם היו יהיה לגוי גדול ועצום ונברכו בו כל גויי הארץ”.

היו לו מפגשים עם אבימלך: אברהם אמר על שרה “אחתי הוא”, ואחר כך הסביר שפחד כי אמר: “אין יראת אלהים במקום הזה והרגוני על דבר אשתי”. אבימלך אמר אליו: “אלהים עמך בכל אשר אתה עשה”, ואברהם כרת עמו ברית בעניין באר המים.

בסוף ימיו נתן אברהם “את כל אשר לו ליצחק”, חי “מאת שנה ושבעים שנה וחמש שנים”, ומת “בשיבה טובה זקן ושבע”. יצחק וישמעאל בניו קברו אותו “אל מערת המכפלה”, ושם נקברה גם שרה אשתו.

מקורות:
- בראשית 17:1-6
- בראשית 17:5-10
- בראשית 17:17-22
- בראשית 20:5-10
- בראשית 20:9-14
- בראשית 21:21-26
- בראשית 21:25-30
- תהלים 105:41-45
- בראשית 18:17-22
- בראשית 25:5-10

> במה הוא דומה ליצחק?

אברהם דומה ליצחק בכמה עניינים המופיעים בקטעים:

- לשניהם היה מקרה עם אבימלך סביב האישה: על אברהם נאמר “אחתי הוא”, ועל יצחק נאמר על רבקה “אחתי הוא”, מפני שאמר: “פן אמות עליה”.
- אצל שניהם הולדת הבנים קשורה בקושי ובמעורבות אלהית: אצל אברהם נאמר “הלבן מאה שנה יולד ואם שרה הבת תשעים שנה תלד”, ואצל יצחק נאמר שרבקה “עקרה הוא”, ו“ויעתר יצחק לה’... ויעתר לו ה’ ותהר רבקה אשתו”.
- שניהם מתוארים בקשר של שמיעה או פנייה לה’: על אברהם נאמר “שמע אברהם בקלי וישמר משמרתי מצותי חקותי ותורתי”, ועל יצחק נאמר “ויעתר יצחק לה’”.
- שניהם קשורים להמשך הזרע והברכה במשפחה: לאברהם נאמר “את בריתי אקים את יצחק”, ויצחק עצמו היה אב לעשו וליעקב.

מקורות:
- בראשית 20:5-10
- בראשית 26:5-10
- בראשית 17:17-22
- בראשית 25:21-26
- בראשית 26:5-10

> מי הייתה אישתו? תצטט מהפסוקים

אשתו הייתה שרה, שנקראה גם שרי בקטעים: “שרי אשתו” וכן “שרה אשתו”. אברהם גם אמר עליה: “ותהי לי לאשה”.

מקורות:
- בראשית 12:9-14
- בראשית 20:1-6
- בראשית 20:9-14

> כשאמרת 'ברית' למה התכוונת בדיוק לפי הטקסט?

לפי הטקסט, כשנאמרה “ברית” על אברהם, הכוונה בעיקר להתחייבות שה’ כרת עם אברהם ועם זרעו:

- ה’ אמר לאברם: “ואתנה בריתי ביני ובינך” ו“וארבה אותך במאד מאד”.
- הברית כללה שינוי שם: “והיה שמך אברהם כי אב המון גוים נתתיך”.
- היא כללה ריבוי ועמים: “והפרתי אתך במאד מאד ונתתיך לגוים ומלכים ממך יצאו”.
- היא הוגדרה כברית לדורות: “והקמתי את בריתי ביני ובינך ובין זרעך אחריך לדרתם לברית עולם”.
- היא כללה יחס של אלהים לזרע אברהם: “להיות לך לאלהים ולזרעך אחריך”.
- היא כללה את הארץ: “ונתתי לך ולזרעך אחריך את... כל ארץ כנען לאחזת עולם”.
- היא כללה מצווה/אות של מילה: “זאת בריתי אשר תשמרו... המול לכם כל זכר”, וכן “ונמלתם את בשר ערלתכם והיה לאות ברית ביני וביניכם”.

יש גם שימוש נוסף במילה “ברית” בין אברהם לאבימלך, סביב באר: “ויקח אברהם צאן ובקר ויתן לאבימלך ויכרתו שניהם ברית”, ואברהם אמר על שבע הכבשות: “בעבור תהיה לי לעדה כי חפרתי את הבאר הזאת”.

מקורות:
- בראשית 17:1-6
- בראשית 17:5-10
- בראשית 17:9-14
- בראשית 21:25-30

> תן תשובה קצרה ואז הרחבה

**תשובה קצרה:**  
לפי הטקסט, “ברית” היא התחייבות שכרת ה’ עם אברהם וזרעו: ריבוי זרע, “ארץ כנען”, קשר של “להיות לך לאלהים”, וסימן של מילה — “המול לכם כל זכר”.

**הרחבה:**  
הברית מתחילה בדברי ה’ לאברם: “ואתנה בריתי ביני ובינך” ו“וארבה אותך במאד מאד”. היא כוללת שינוי שם: “והיה שמך אברהם כי אב המון גוים נתתיך”, וגם הבטחה: “ונתתיך לגוים ומלכים ממך יצאו”.

הברית נמשכת גם לזרעו: “והקמתי את בריתי ביני ובינך ובין זרעך אחריך לדרתם לברית עולם”. היא כוללת את הארץ: “את כל ארץ כנען לאחזת עולם”, וכן נאמר: “לזרעך נתתי את הארץ הזאת”.

הטקסט גם מגדיר מה אברהם וזרעו צריכים לשמור: “זאת בריתי אשר תשמרו... המול לכם כל זכר”. המילה נקראת “אות ברית”: “ונמלתם את בשר ערלתכם והיה לאות ברית ביני וביניכם”.

בנוסף, המילה “ברית” מופיעה גם בהקשר אנושי בין אברהם לאבימלך: “ויקח אברהם צאן ובקר ויתן לאבימלך ויכרתו שניהם ברית”, סביב “באר המים”.

מקורות:
- בראשית 17:1-6
- בראשית 17:5-10
- בראשית 17:9-14
- בראשית 15:13-18
- בראשית 21:25-30

> מי זכה במונדיאל 2022?

לא מצאתי לכך תמיכה מספקת בטקסט שסופק.

> מהי בירת יפן?

לא מצאתי לכך תמיכה מספקת בטקסט שסופק.
.
```

---

# 🔍 Engineering Challenges

* Extracting Hebrew with nikud & te'amim
* Parsing chapter/verse numbering
* Keeping verse boundaries through normalization
* Resolving follow ups via history
* Modular RAG with clear separation
* Hebrew UX over an English codebase

---

# ⚠️ Known Limitations

* Answer quality scales with the model - set a stronger `OPENAI_CHAT_MODEL` in `.env`.
* RTL Hebrew may render awkwardly in some terminals.

---

# 🚧 Future Ideas + Modifications

* 🫚 Refine sources output - eliminate dups & shorten list
* 📝 Persistent history
* 👤 Multi user sessions
* 🤖 LLM assisted indexing
* 🧗 Per task model routing
* 📄 More formats (DOCX, Markdown, TXT)
* 🌐 More interfaces (Web, REST, package)
* ⚡ Incremental indexing
* 🧠 Long chat summarization
* 🧪 Broader test coverage

---

# 🤖 AI Usage

* **ChatGPT** - design pushback
* **Claude Code** - expediting implementation from my specs

**AI in the implementation phase**

Working from my designs and detailed instructions, Claude Code helped me:

* Speed through heavy Hebrew parsing boilerplate
* Setup logging
* Implement basic unit tests
* Suggest refactors and review diffs
* Improve documentation (like this README🙃)

**Mine**

- Requirements and technical direction
- Architecture, data pipeline, and project structure
- Technology selection and key design decisions
- System orchestration
- Review and final approval of all AI-generated changes