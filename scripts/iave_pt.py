#!/usr/bin/env python3
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def brute_force_portugues():
    output_dir = os.path.expanduser("~/dev/iave/data/pdfs/portugues")
    os.makedirs(output_dir, exist_ok=True)
    
    existing_files = set(os.listdir(output_dir))
    
    phases = ['F1', 'F2', 'EE']
    
    # Removidos os sufixos "-CC" para sacar APENAS os enunciados puros!
    suffixes = [
        '.pdf',
        '-V1.pdf',
        '-V1_net.pdf',
        '_net.pdf',
        '-V2.pdf',
        '-V2_net.pdf'
    ]
    
    prefixes = [
        "EX-Port639", 
        "EX-Port-639", 
        "Prova-639", 
        "639", 
        "EX-639"
    ]
    
    urls_to_test = []
    
    print("📚 1. A gerar a matriz de ataque para Português (639)...")
    
    for exam_year in range(2015, 2026):
        for phase in phases:
            for prefix in prefixes:
                for suffix in suffixes:
                    filename = f"{prefix}-{phase}-{exam_year}{suffix}"
                    
                    if filename in existing_files:
                        continue
                        
                    for upload_year in range(exam_year, 2026):
                        for month in range(1, 13):
                            month_str = f"{month:02d}"
                            url = f"https://iave.pt/wp-content/uploads/{upload_year}/{month_str}/{filename}"
                            urls_to_test.append((url, filename))
                            
    print(f"🔥 Matriz criada: {len(urls_to_test)} links para testar.")
    print("⚡ 2. A iniciar disparos (Força Bruta com 50 Threads)...")
    
    valid_urls = []
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    def check_url(item):
        url, filename = item
        try:
            response = session.head(url, timeout=3)
            if response.status_code == 200:
                return (True, url, filename)
        except:
            pass
        return (False, url, filename)

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_url, item): item for item in urls_to_test}
        
        for i, future in enumerate(as_completed(futures)):
            success, url, filename = future.result()
            if success:
                valid_urls.append((url, filename))
                print(f"🎯 ENCONTRADO: {url}")
                
            if i % 2000 == 0 and i > 0:
                print(f"⏳ Progresso: Testados {i}/{len(urls_to_test)} links...")

    print(f"\n🧠 Força Bruta terminada! Descobrimos {len(valid_urls)} exames de Português.")
    
    if valid_urls:
        print("📥 3. A extrair os PDFs reais para a tua pasta...\n")
        total_downloaded = 0
        
        for url, filename in valid_urls:
            file_path = os.path.join(output_dir, filename)
            if not os.path.exists(file_path): 
                try:
                    pdf_data = session.get(url, timeout=15).content
                    with open(file_path, 'wb') as f:
                        f.write(pdf_data)
                    print(f"✅ Guardado: {filename}")
                    total_downloaded += 1
                except Exception as e:
                    print(f"❌ Erro ao sacar {filename}: {e}")
                    
        print(f"\n🚀 Concluído! Tens {total_downloaded} novos exames de Português no disco.")
    else:
        print("❌ Não foram descobertos ficheiros novos.")

if __name__ == "__main__":
    brute_force_portugues()