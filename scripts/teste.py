import requests

urls = [
    "https://www.examesnacionais.com.pt/exames-nacionais/12ano/Historia-A.php",
    "https://www.examesnacionais.com.pt/exames-nacionais/12ano/historia-a.php",
    "https://www.examesnacionais.com.pt/exames-nacionais/12-ano/Historia-A.php",
    "https://www.examesnacionais.com.pt/exames-nacionais/12-ano/historia-a.php"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

for u in urls:
    print(f"A testar: {u}")
    try:
        r = requests.get(u, headers=headers, timeout=5)
        print(f"➤ Status Code: {r.status_code}\n")
    except Exception as e:
        print(f"➤ Erro Fatal: {e}\n")