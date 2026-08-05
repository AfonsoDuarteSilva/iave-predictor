#!/usr/bin/env python3
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def brute_force_iave():
    output_dir = os.path.expanduser("~/dev/iave/data/pdfs/historia")
    os.makedirs(output_dir, exist_ok=True)
    
    # Ver o que já tens na pasta para não testar o que já sacaste
    existing_files = set(os.listdir(output_dir))
    
    # Padrões comuns da nomenclatura dos exames do IAVE
    phases = ['F1', 'F2', 'EE']
    suffixes = [
        '.pdf',
        '-V1.pdf',
        '-V1_net.pdf',
        '_net.pdf',
        '-V2.pdf',
        '-CC.pdf',
        '-CC-VD.pdf',
        '_CC.pdf',
        '-Adp-CC.pdf'
    ]
    
    urls_to_test = []
    
    print("🎯 1. A gerar a matriz de ataque (URLs possíveis)...")
    
    for exam_year in range(2015, 2026):
        for phase in phases:
            for suffix in suffixes:
                filename = f"EX-HistA623-{phase}-{exam_year}{suffix}"
                
                # Se já temos o ficheiro, ignoramos e saltamos à frente
                if filename in existing_files:
                    continue
                    
                # Como vimos com o exame de 2019 na pasta de 2020, 
                # vamos procurar desde o ano do exame até ao ano atual.
                for upload_year in range(exam_year, 2026):
                    for month in range(1, 13):
                        month_str = f"{month:02d}"  # Adiciona o zero (01, 02, etc.)
                        url = f"https://iave.pt/wp-content/uploads/{upload_year}/{month_str}/{filename}"
                        urls_to_test.append((url, filename))
                        
    print(f"🔥 Matriz criada: {len(urls_to_test)} links para testar.")
    print("⚡ 2. A iniciar disparos (Força Bruta com 50 Threads)...")
    
    valid_urls = []
    
    # Sessão global melhora o tempo de resposta
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    def check_url(item):
        url, filename = item
        try:
            # HEAD request: saca apenas o cabeçalho (demora milissegundos)
            response = session.head(url, timeout=3)
            if response.status_code == 200:
                return (True, url, filename)
        except:
            pass
        return (False, url, filename)

    # Disparar 50 requests em simultâneo
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_url, item): item for item in urls_to_test}
        
        for i, future in enumerate(as_completed(futures)):
            success, url, filename = future.result()
            if success:
                valid_urls.append((url, filename))
                print(f"🎯 ENCONTRADO: {url}")
                
            # Feedback visual para não parecer que bloqueou
            if i % 2000 == 0 and i > 0:
                print(f"⏳ Progresso: Testados {i}/{len(urls_to_test)} links...")

    print(f"\n🧠 Força Bruta terminada! Descobrimos {len(valid_urls)} ficheiros invisíveis.")
    
    if valid_urls:
        print("📥 3. A extrair os PDFs reais para a tua pasta...\n")
        total_downloaded = 0
        
        for url, filename in valid_urls:
            file_path = os.path.join(output_dir, filename)
            # Prevenir sobreposições de ficheiros encontrados noutros meses
            if not os.path.exists(file_path): 
                try:
                    pdf_data = session.get(url, timeout=15).content
                    with open(file_path, 'wb') as f:
                        f.write(pdf_data)
                    print(f"✅ Guardado: {filename}")
                    total_downloaded += 1
                except Exception as e:
                    print(f"❌ Erro ao sacar {filename}: {e}")
                    
        print(f"\n🚀 Hack concluído. {total_downloaded} ficheiros perdidos agora estão no teu disco.")
    else:
        print("❌ Não foram descobertos ficheiros novos.")

if __name__ == "__main__":
    brute_force_iave()