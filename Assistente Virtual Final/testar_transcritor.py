"""
Teste simples do transcritor para verificar se o carregamento de áudio funciona
"""
print("Testando módulo transcritor...")

try:
    from transcritor import carregar_fala, iniciar_modelo, MODELO
    import torch
    import os
    
    print("✅ Imports OK")
    
    # Testa se consegue iniciar o modelo
    print("\nIniciando modelo (isso pode demorar na primeira vez)...")
    dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Usando dispositivo: {dispositivo}")
    
    iniciado, processador, modelo = iniciar_modelo(MODELO, dispositivo)
    
    if iniciado:
        print("✅ Modelo iniciado com sucesso!")
        print(f"   Modelo: {MODELO}")
    else:
        print("❌ Falha ao iniciar modelo")
    
    print("\n" + "="*60)
    print("TESTE DO TRANSCRITOR CONCLUÍDO")
    print("="*60)
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
