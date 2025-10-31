# Assistente Virtual - Bancada de Eletrônica Automatizada

## Descrição do Projeto

Este é um assistente virtual desenvolvido para auxiliar técnicos em bancadas de eletrônica através de comandos de voz. O sistema automatiza o controle de equipamentos e o gerenciamento de tarefas em ambientes de manutenção e reparo eletrônico.

## Mini-mundo

O assistente será utilizado em uma bancada de eletrônica automatizada, com o objetivo de auxiliar o técnico a gerenciar tarefas, medições e rotinas de diagnóstico por meio de comandos de voz. Ele atua simulando sensores que representam os dispositivos típicos de uma bancada técnica, como uma fonte de alimentação e estação de solda.

## Comandos Disponíveis

### 1. Ligar/Desligar Fonte de Bancada
- **Comando**: "Ligar fonte de bancada" / "Desligar fonte de bancada"
- **Função**: Ativa ou desativa a simulação da fonte de energia, exibindo o status atual (tensão, corrente e potência).

### 2. Ligar/Desligar Estação de Solda
- **Comando**: "Ligar estação de solda" / "Desligar estação de solda"
- **Função**: Controla o funcionamento da estação simulada e registra seu estado, incluindo temperatura.

### 3. Monitorar Energia Consumida
- **Comando**: "Monitorar energia consumida"
- **Função**: Calcula e exibe um valor estimado de consumo energético dos equipamentos ativos.

### 4. Verificar Temperatura dos Equipamentos
- **Comando**: "Verificar temperatura dos equipamentos"
- **Função**: Simula leituras de sensores de temperatura e emite alertas em caso de superaquecimento.

### 5. Registrar Nova Tarefa de Reparo
- **Comando**: "Registrar nova tarefa de reparo"
- **Função**: Armazena em um arquivo JSON uma nova entrada com data, hora e descrição do reparo realizado.

## Tecnologias Utilizadas

- **Python 3.8+**
- **Transformers** (Hugging Face) - Modelo Wav2Vec2 para reconhecimento de fala
- **NLTK** - Processamento de linguagem natural
- **PyAudio** - Captura de áudio do microfone
- **Flask** - Interface web (opcional)
- **unittest** - Testes automatizados

## Estrutura do Projeto

```
Assistente Virtual Final/
├── assistente.py                 # Script principal do assistente
├── config.json                   # Configurações de comandos e dispositivos
├── inicializador_modelo.py       # Inicialização do modelo Wav2Vec2
├── inicializador_nltk.py         # Download de recursos NLTK
├── transcritor.py                # Transcrição de áudio para texto
├── test_assistente.py            # Testes automatizados (UNITTEST)
├── requirements.txt              # Dependências do projeto
├── fonte_bancada.py              # Controle da fonte de alimentação
├── estacao_solda.py              # Controle da estação de solda
├── monitor_energia.py            # Monitoramento de consumo energético
├── sensor_temperatura.py         # Verificação de temperatura
├── registro_tarefas.py           # Sistema de registro de tarefas
├── audios/                       # Áudios de teste pré-gravados
│   ├── ligar_fonte.wav
│   ├── desligar_fonte.wav
│   ├── ligar_solda.wav
│   ├── desligar_solda.wav
│   ├── monitorar_energia.wav
│   ├── verificar_temperatura.wav
│   └── registrar_tarefa.wav
├── logs/                         # Logs e registros de tarefas
│   └── tarefas_reparo.json
├── temp/                         # Arquivos temporários de áudio
└── public/                       # Interface web (opcional)
    ├── index.html
    └── script.js
```

## Instalação

### 1. Clone ou baixe o projeto

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o inicializador do NLTK

```bash
python inicializador_nltk.py
```

### 4. Grave os áudios de teste

Grave os seguintes comandos e salve na pasta `audios/`:
- ligar_fonte.wav - "Ligar fonte de bancada"
- desligar_fonte.wav - "Desligar fonte de bancada"
- ligar_solda.wav - "Ligar estação de solda"
- desligar_solda.wav - "Desligar estação de solda"
- monitorar_energia.wav - "Monitorar energia consumida"
- verificar_temperatura.wav - "Verificar temperatura dos equipamentos"
- registrar_tarefa.wav - "Registrar nova tarefa de reparo"

## Como Executar

### Modo Linha de Comando

1. Abra o arquivo `assistente.py`
2. Configure: `MODO_DE_FUNCIONAMENTO = MODO_LINHA_DE_COMANDO`
3. Execute:

```bash
python assistente.py
```

### Modo Web

1. Abra o arquivo `assistente.py`
2. Configure: `MODO_DE_FUNCIONAMENTO = MODO_WEB`
3. Execute:

```bash
python assistente.py
```

4. Acesse: http://localhost:7001

## Como Executar os Testes

```bash
python test_assistente.py
```

Os testes validam:
- ✓ Reconhecimento correto de todos os comandos de voz
- ✓ Validação do arquivo de configuração JSON
- ✓ Funcionamento de todos os atuadores
- ✓ Processamento correto das transcrições

## Arquivos de Configuração

### config.json

Define as ações e dispositivos reconhecidos pelo assistente. Todas as configurações são externas ao código principal, facilitando a manutenção e expansão.

Exemplo:
```json
{
    "acoes": [
        {
            "nome": "ligar",
            "dispositivos": ["fonte", "fonte de bancada", "solda", "estação"]
        }
    ]
}
```

## Atuadores (Simulados)

- **Fonte de Bancada**: Simula fonte de alimentação ajustável (tensão, corrente, potência)
- **Estação de Solda**: Simula estação com controle de temperatura
- **Monitor de Energia**: Calcula consumo energético total
- **Sensor de Temperatura**: Monitora temperatura e emite alertas
- **Registro de Tarefas**: Armazena histórico de reparos em JSON

## Requisitos Atendidos

✓ Arquivo de configuração JSON externo  
✓ Automação de dispositivos/ambiente de produção  
✓ Uso de sensores (microfone)  
✓ Uso de atuadores (5 módulos distintos)  
✓ Reconhecimento de fala com Wav2Vec2  
✓ Processamento com NLTK  
✓ Mínimo de 4 comandos (7 comandos implementados)  
✓ Testes automatizados com UNITTEST  
✓ Documentação completa  

## Autor

Desenvolvido para a disciplina de Inteligência Artificial  
Professor: Luis Paulo da Silva Carvalho  
Data: Outubro/2025

## Licença

Projeto acadêmico - IFBA
