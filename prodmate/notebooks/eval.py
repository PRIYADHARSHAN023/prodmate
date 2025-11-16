import requests, json, time
TESTS = [
    {"text":"Add task: finish assignment by tomorrow"},
    {"text":"Remember: I prefer to study at night"},
    {"text":"Set reminder: Pay bills tomorrow at 9am"},
    {"text":"What's my next free slot to study?"}
]
for t in TESTS:
    r = requests.post("http://localhost:8000/api/v1/handle", json={"user_id":"u1","text":t["text"]})
    print(t["text"], "->", r.json())
    time.sleep(0.5)
