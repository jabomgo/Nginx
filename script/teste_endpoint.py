import argparse
import requests
import time
from collections import Counter

def main():
    parser = argparse.ArgumentParser(description="Script para fazer requisições a um endpoint.")
    parser.add_argument("endpoint", help="URL do endpoint")
    parser.add_argument("--tempo", type=float, default=1, help="Tempo de espera entre requisições (em segundos)")
    parser.add_argument("--max-iter", type=int, default=0, help="Número máximo de iterações (0 = infinito)")
    args = parser.parse_args()

    endpoint = args.endpoint
    delay = args.tempo
    max_iter = args.max_iter

    contagem = Counter()
    total_requisicoes = 0

    while True:
        if max_iter > 0 and total_requisicoes >= max_iter:
            break

        try:
            resp = requests.get(endpoint, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            _id = data.get("id")
            domain = data.get("domain")

            if _id is not None and domain is not None:
                print(f"id: {_id}, domain: {domain}")
                contagem[(str(_id), str(domain))] += 1
                total_requisicoes += 1
            else:
                print("⚠️ Resposta não contém 'id' e 'domain'.")

        except Exception as e:
            print(f"Erro na requisição: {e}")

        time.sleep(delay)

    print("\n=== Resumo final ===")
    print(f"Total de requisições válidas: {total_requisicoes}")
    for (id_, domain), count in contagem.items():
        print(f"id: {id_}, domain: {domain} → {count} requisições")

if __name__ == "__main__":
    main()
