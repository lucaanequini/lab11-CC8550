import requests
import numpy as np
import time

def teste_desempenho():
    tempos_resposta = []
    url_produto = "https://fakestoreapi.com/products/1"
    print(f"[1/3] Executando Teste de Desempenho...")

    for i in range(50):
        try:
            start_time = time.time()
            response = requests.get(url_produto, timeout=10)
            end_time = time.time()
            if response.status_code == 200:
                tempos_resposta.append((end_time - start_time) * 1000)
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.05)
    
    if not tempos_resposta:
        return {"status": "FALHOU", "p95": "N/A", "media": "N/A", "motivo": "Nenhuma requisição bem-sucedida."}

    p95 = np.percentile(tempos_resposta, 95)
    media = np.mean(tempos_resposta, axis=0)
    meta_p95 = 500.0
    status = "APROVADO" if p95 < meta_p95 else "REPROVADO"
    return {"status": status, "p95": f"{p95:.2f} ms", "media": f"{media:.2f} ms"}

def teste_escalabilidade_simulado():
    print("[2/3] Executando Teste de Escalabilidade (Simulado)...")
    throughput_1_servidor = 1100
    throughput_4_servidores = 3800
    ideal_4_servidores = throughput_1_servidor * 4
    eficiencia = (throughput_4_servidores / ideal_4_servidores) * 100
    meta_eficiencia = 80.0
    status = "APROVADO" if eficiencia > meta_eficiencia else "REPROVADO"
    return {"status": status, "eficiencia": f"{eficiencia:.2f}%"}

def teste_seguranca_rate_limit():
    url_login = "https://fakestoreapi.com/auth/login"
    print(f"[3/3] Executando Teste de Segurança (Rate Limiting)...")
    
    for i in range(100):
        try:
            response = requests.post(url_login, json={"username": "johnd", "password": "m38rmF$"})
            if response.status_code == 429:
                return {"status": "APROVADO", "resultado": "Recebido status 429."}
        except requests.exceptions.RequestException:
            return {"status": "FALHOU", "resultado": "Erro de conexão."}
        time.sleep(0.1)
    
    return {"status": "REPROVADO", "resultado": "Rate limiting não detectado."}

def gerar_relatorio_md(resultados):
    print("\n--- GERANDO RELATÓRIO ---")
    res_desempenho = resultados["desempenho"]
    res_escalabilidade = resultados["escalabilidade"]
    res_seguranca = resultados["seguranca"]

    report_content = f"""
# Relatório de Testes Não Funcionais

## Resumo dos Resultados
| Tipo de Teste | Métrica Principal | Meta | Resultado | Status |
|---|---|---|---|---|
| Desempenho | Tempo de Resposta P95 | < 500ms | {res_desempenho['p95']} | **{res_desempenho['status']}** |
| Escalabilidade| Eficiência Horizontal | > 80% | {res_escalabilidade['eficiencia']} | **{res_escalabilidade['status']}** |
| Segurança | Rate Limiting | Detectar 429 | Não detectado | **{res_seguranca['status']}** |

---

## Detalhes dos Testes

### 1. Teste de Desempenho
- **Métrica P95:** {res_desempenho['p95']}
- **Tempo Médio:** {res_desempenho['media']}
- **Status Final:** {res_desempenho['status']}

### 2. Teste de Carga e Estresse
- **Execução:** Use o arquivo `locustfile.py` para estes testes.
- **Comando:** `locust -f locustfile.py --host=https://fakestoreapi.com`
- **Status Final:** (A ser preenchido após execução manual do Locust)

### 3. Teste de Escalabilidade (Simulado)
- **Eficiência Calculada:** {res_escalabilidade['eficiencia']}
- **Status Final:** {res_escalabilidade['status']}

### 4. Teste de Segurança (Rate Limiting)
- **Resultado:** {res_seguranca['resultado']}
- **Status Final:** {res_seguranca['status']}
"""
    try:
        with open("relatorio_testes.md", "w", encoding="utf-8") as f:
            f.write(report_content)
        print("\nRelatório 'relatorio_testes.md' gerado com sucesso!")
    except IOError as e:
        print(f"\nErro ao salvar o relatório: {e}")

if __name__ == "__main__":
    resultados = {
        "desempenho": teste_desempenho(),
        "escalabilidade": teste_escalabilidade_simulado(),
        "seguranca": teste_seguranca_rate_limit()
    }
    gerar_relatorio_md(resultados)