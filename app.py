from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# Correct answers + answer text for detailed results page
answer_key = [
    {
        "question": "1. Миний орд аль нь вэ?",
        "options": ["Загас", "Хонь", "Хумх", "Матар"],
        "correct": 2
    },
    {
        "question": "2. Миний хамгийн дуртай өнгө аль нь вэ?",
        "options": ["Цагаан", "Ягаан", "Нил ягаан", "Улаан"],
        "correct": 1
    },
    {
        "question": "3. Миний хамгийн дуртай баяр аль нь вэ?",
        "options": ["Шинэ жил", "Наадам", "Цагаан сар", "Валентин"],
        "correct": 0
    },
    {
        "question": "4. Миний хамгийн дуртай уух зүйл аль нь вэ?",
        "options": ["Lemon water", "Сүү", "Beer", "Алимны шүүс"],
        "correct": 1
    },
    {
        "question": "5. Болзооны өмнө чи юу хийх ёстой вэ?",
        "options": [
            "Зөвхөн ямар ресторанд хооллохоо л хайна",
            "Хаашаа явах вэ гэж надаас асуугаад орхино",
            "Болзооны төлөвлөгөө, хийх зүйлсийг урьдчилж бодно",
            "\"Ямар болзоо?\" гэж асууна"
        ],
        "correct": 2
    },
    {
        "question": "6. Гадуур хооллож байхад хоол хүлээх хугацаанд чи юу хийх ёстой вэ?",
        "options": [
            "Утсаа ухна",
            "Өөр охидын story үзнэ",
            "Надтай ярилцана",
            "Унтана"
        ],
        "correct": 2
    },
    {
        "question": "7. Чи надаас \"юм авчирч өгөх үү\" гэж асуухад би \"үгүй\" гэвэл чи юу хийх ёстой вэ?",
        "options": [
            "Хүсэлтийг минь хүндлээд юу ч авчрахгүй",
            "Өөртөө л юм авчирна",
            "Just in case гээд миний дуртай snack-ийг авчирна",
            "Юм авахыг зөвшөөрүүлэх гэж ятгана"
        ],
        "correct": 2
    },
    {
        "question": "8. Би чиний хамгийн дуртай hoodie-г өмсөөд авбал чи яах ёстой вэ?",
        "options": [
            "Цагдаа дуудна",
            "Надаас буцаагаад булааж авна",
            "\"Чамд илүү гоё зохиж байна\" гэнэ",
            "Өөр нэг hoodie санал болгоно"
        ],
        "correct": 2
    },
    {
        "question": "9. Өөр эмэгтэй хүн чам руу хэт ойртож эхэлбэл чи юу хийх ёстой вэ?",
        "options": [
            "Тэр хүнийг гомдоохгүй гэж бодоод зүгээр орхино",
            "Ignore хийнэ",
            "\"Зүгээр social interaction\" гэж бодно",
            "Хүндэтгэлтэйгээр зай барьж, хил хязгаараа тодорхой тавина"
        ],
        "correct": 3
    },
    {
        "question": "10. Би \"ямар нэг юм идмээр байна\" гэвэл чи юу хийх ёстой вэ?",
        "options": [
            "Надад авч өгнө",
            "Кардаа өгөөд өөрөөр минь авахуулна",
            "\"Дараа\" гэнэ",
            "Сэдвээ солино"
        ],
        "correct": 0
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "answers": data.get("answers", []),
        "score": data.get("score", 0),
        "percent": data.get("percent", 0),
        "result_title": data.get("result_title", "")
    }

    with open("results.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return jsonify({"status": "saved"})

@app.route("/results")
def view_results():
    try:
        with open("results.json", "r", encoding="utf-8") as f:
            lines = f.readlines()
            records = [json.loads(line) for line in lines]
    except Exception:
        records = []

    detailed_results = []

    for record in records:
        answers = record.get("answers", [])
        breakdown = []

        for i, selected_index in enumerate(answers):
            if i >= len(answer_key):
                continue

            question_data = answer_key[i]
            options = question_data["options"]
            correct_index = question_data["correct"]

            selected_text = (
                options[selected_index]
                if isinstance(selected_index, int) and 0 <= selected_index < len(options)
                else "Invalid answer"
            )

            correct_text = options[correct_index]

            breakdown.append({
                "question_number": i + 1,
                "question": question_data["question"],
                "your_answer_index": selected_index,
                "your_answer_text": selected_text,
                "correct_answer_index": correct_index,
                "correct_answer_text": correct_text,
                "is_correct": selected_index == correct_index
            })

        detailed_results.append({
            "timestamp": record.get("timestamp", ""),
            "score": record.get("score", 0),
            "percent": record.get("percent", 0),
            "result_title": record.get("result_title", ""),
            "details": breakdown
        })

    return jsonify(detailed_results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
