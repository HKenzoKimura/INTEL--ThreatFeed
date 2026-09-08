# Feed Intelligence Collector

Script Python para coleta e consolidação de endereços IP maliciosos a partir de múltiplos feeds públicos e privados de Threat Intelligence (blocklists, IOCs, listas de reputação), com exportação para um arquivo `.pkl` (Pandas Pickle) para uso posterior em pipelines de detecção/enriquecimento.

## `Developed by: HKK`

## Funcionalidades

- Consulta uma lista configurável de feeds de TI (`feeds`), suportando respostas em **texto puro** (uma entrada por linha) e **JSON**.
- Extrai endereços IPv4 de cada linha/registro via regex, mesmo quando o feed traz informações adicionais junto ao IP.
- Deduplica os IPs coletados de todos os feeds.
- Persiste o resultado final em `feedIntelligence.pkl`, um DataFrame Pandas com a coluna `IP Address`.
- Desabilita avisos de SSL não verificado (`urllib3` warnings) para feeds com certificado inválido/self-signed.

## Feeds incluídos

O script já vem configurado com feeds como:

- FireHOL blocklist-ipsets (cybercrime, Tor, botscout, blocklist.de, myip, etc.)
- Botvrij.eu
- Binary Defense Banlist
- Brute Force Blocker (danger.rulez.sk)
- CINS Score (ci-badguys)
- GreenSnow
- OpenPhish
- AbuseIPDB (via API, com `confidenceMinimum=75`)
- Ipsum (stamparm)
- Emerging Threats (compromised-ips)
- Pushing Inertia Blocklist

## Requisitos

```bash
pip install requests pandas PyQt5
```

## Uso

```bash
python feed_intelligence.py
```

Ao final da execução, será gerado o arquivo `feedIntelligence.pkl` no diretório atual, contendo todos os IPs únicos coletados.

Para carregar o resultado posteriormente:

```python
import pandas as pd
df = pd.read_pickle('feedIntelligence.pkl')
print(df.head())
print(f"Total de IPs: {len(df)}")
```

## Estrutura de saída

| Coluna     | Tipo   | Descrição                          |
|------------|--------|-------------------------------------|
| IP Address | string | Endereço IPv4 único extraído dos feeds |
