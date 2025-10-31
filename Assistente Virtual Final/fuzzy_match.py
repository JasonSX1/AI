"""
Módulo para matching fuzzy de comandos
Aumenta a tolerância a erros de transcrição
"""

def distancia_levenshtein(s1, s2):
    """Calcula a distância de Levenshtein entre duas strings"""
    if len(s1) < len(s2):
        return distancia_levenshtein(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    linha_anterior = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        linha_atual = [i + 1]
        for j, c2 in enumerate(s2):
            insercoes = linha_anterior[j + 1] + 1
            delecoes = linha_atual[j] + 1
            substituicoes = linha_anterior[j] + (c1 != c2)
            linha_atual.append(min(insercoes, delecoes, substituicoes))
        linha_anterior = linha_atual
    
    return linha_anterior[-1]

def similaridade(s1, s2):
    """Retorna similaridade normalizada entre 0 e 1"""
    distancia = distancia_levenshtein(s1.lower(), s2.lower())
    tamanho_maximo = max(len(s1), len(s2))
    if tamanho_maximo == 0:
        return 1.0
    return 1 - (distancia / tamanho_maximo)

def encontrar_melhor_match(palavra, opcoes, threshold=0.7):
    """
    Encontra a melhor correspondência para uma palavra em uma lista de opções
    
    Args:
        palavra: palavra a procurar
        opcoes: lista de opções válidas
        threshold: similaridade mínima (0-1)
        
    Returns:
        melhor opção ou None se não houver match suficientemente bom
    """
    melhor_opcao = None
    melhor_score = 0
    
    for opcao in opcoes:
        score = similaridade(palavra, opcao)
        if score > melhor_score:
            melhor_score = score
            melhor_opcao = opcao
    
    if melhor_score >= threshold:
        return melhor_opcao
    return None

def corrigir_acao(acao, acoes_validas):
    """Corrige uma ação usando fuzzy matching"""
    nomes_acoes = [a["nome"] for a in acoes_validas]
    return encontrar_melhor_match(acao, nomes_acoes, threshold=0.65)

def corrigir_dispositivo(dispositivo, dispositivos_validos):
    """Corrige um dispositivo usando fuzzy matching"""
    return encontrar_melhor_match(dispositivo, dispositivos_validos, threshold=0.65)
