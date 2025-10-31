// Elementos da interface
const recordButton = document.getElementById('recordButton');
const statusText = document.getElementById('statusText');
const logContainer = document.getElementById('logContainer');
const logPlaceholder = document.getElementById('logPlaceholder');

// --- NOVOS ELEMENTOS ---
const micPanel = document.getElementById('micPanel');
const taskEntryPanel = document.getElementById('taskEntryPanel');
const taskTextArea = document.getElementById('taskTextArea');
const confirmTaskButton = document.getElementById('confirmTaskButton');
const cancelTaskButton = document.getElementById('cancelTaskButton');

// Variáveis de controle
let audioChunks = [];
let isRecording = false;
// isExtendedMode foi removido
let audioContext;
let processor;
let stream;
let recognitionTimer;

// --- Inicialização ---

// Atualiza status dos equipamentos a cada 2 segundos
setInterval(atualizarEstado, 2000);

// Atualiza no carregamento da página
document.addEventListener('DOMContentLoaded', atualizarEstado);

// Event listener do botão de gravação
recordButton.addEventListener('click', async () => {
    if (isRecording) {
        pararGravacao();
    } else {
        await iniciarGravacao();
    }
});

// --- NOVOS LISTENERS PARA O PAINEL DE TAREFA ---
confirmTaskButton.addEventListener('click', salvarTarefa);
cancelTaskButton.addEventListener('click', resetarPainelControle);


// Impede que a página recarregue ao dar F5 durante gravação
window.addEventListener('beforeunload', (e) => {
    if (isRecording) {
        e.preventDefault();
        e.returnValue = '';
    }
});

// --- Funções de Gravação (Simplificadas) ---

async function iniciarGravacao() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            audio: {
                sampleRate: 16000,
                channelCount: 1,
                echoCancellation: true,
                noiseSuppression: true
            }
        });

        audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        const input = audioContext.createMediaStreamSource(stream);
        processor = audioContext.createScriptProcessor(4096, 1, 1);

        audioChunks = [];
        isRecording = true;

        processor.onaudioprocess = (e) => {
            if (!isRecording) return;
            const channelData = e.inputBuffer.getChannelData(0);
            audioChunks.push(new Float32Array(channelData));
        };

        input.connect(processor);
        processor.connect(audioContext.destination);

        recordButton.classList.add('recording');
        recordButton.textContent = '⏹️';
        definirStatus('🔴 Gravando... Fale agora!', 'gravando');

        // Timer padrão de 5 segundos
        recognitionTimer = setTimeout(() => {
            if (isRecording) {
                pararGravacao();
            }
        }, 5000);

    } catch (error) {
        console.error('Erro ao acessar microfone:', error);
        adicionarLog(null, '❌ Erro ao acessar microfone. Verifique as permissões.', false);
        definirStatus('Erro ao acessar microfone', 'erro');
    }
}

function pararGravacao() {
    if (!isRecording) return;

    isRecording = false;

    if (recognitionTimer) {
        clearTimeout(recognitionTimer);
    }
    
    recordButton.disabled = true; // Desabilita o botão durante o processamento
    recordButton.classList.remove('recording');
    recordButton.textContent = '🎙️';
    definirStatus('⏳ Processando...', 'processando');

    // Para o processamento de áudio
    if (processor) processor.disconnect();
    if (stream) stream.getTracks().forEach(track => track.stop());
    if (audioContext) audioContext.close();

    processor = null;
    stream = null;
    audioContext = null;

    // Converte os chunks em WAV e envia
    const wavBlob = criarWAV(audioChunks);
    enviarComando(wavBlob); // Sempre envia para o endpoint de comando
}


// --- Processamento de Áudio e API ---

async function enviarComando(audioBlob) {
    const formData = new FormData();
    formData.append('fala', audioBlob, 'audio.wav');

    try {
        const response = await fetch('/reconhecer_comando', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
           const errorData = await response.json().catch(() => ({}));
           throw new Error(errorData.mensagens ? errorData.mensagens[0] : 'Erro de servidor');
        }
        
        const data = await response.json();

        if (data.sucesso) {
            
            // --- LÓGICA DE UI MODIFICADA ---
            if (data.modo_registro) {
                // SUCESSO! O comando foi "iniciar tarefa"
                // Mostra o painel de texto em vez de continuar gravando
                mostrarPainelTarefa();
                adicionarLog(data.transcricao, "📝 Modo de registro ativado. Digite a tarefa.", true);
            } else {
                // É um comando normal (ligar fonte, etc)
                const mensagens = data.mensagens ? data.mensagens.join('\n') : 'Comando executado';
                adicionarLog(data.transcricao, mensagens, true);
                definirStatus('✅ Comando executado!', 'sucesso');
                resetarPainelControle(); // Reseta para o microfone
            }
            // --- FIM DA LÓGICA DE UI ---

        } else {
            // Comando não reconhecido
            const mensagens = data.mensagens ? data.mensagens.join('\n') : 'Comando não reconhecido';
            adicionarLog(data.transcricao, mensagens, false);
            definirStatus('⚠️ ' + (data.sugestao || 'Comando não reconhecido'), 'aviso');
            resetarPainelControle(); // Reseta para o microfone
        }
    } catch (error) {
        console.error('Erro ao enviar áudio:', error);
        adicionarLog(null, '❌ Erro de conexão: ' + error.message, false);
        definirStatus('❌ Erro de conexão', 'erro');
        resetarPainelControle(); // Reseta para o microfone
    }
}

// --- NOVAS FUNÇÕES DE PAINEL DE TAREFA ---

function mostrarPainelTarefa() {
    micPanel.style.display = 'none'; // Esconde o microfone
    taskEntryPanel.style.display = 'flex'; // Mostra o painel de texto
    taskTextArea.value = ''; // Limpa o texto
    taskTextArea.focus();
    recordButton.disabled = false; // Garante que o botão de microfone (agora escondido) não está travado
}

function resetarPainelControle() {
    micPanel.style.display = 'block'; // Mostra o microfone
    taskEntryPanel.style.display = 'none'; // Esconde o painel de texto
    taskTextArea.value = '';
    recordButton.disabled = false;
    
    // Reseta o status após um tempo
    setTimeout(() => {
        if (!isRecording) { // Só reseta se não estiver gravando
            definirStatus('Clique no microfone e fale');
        }
    }, 2000);
}

async function salvarTarefa() {
    const textoTarefa = taskTextArea.value;
    if (!textoTarefa.trim()) {
        alert("Por favor, digite uma descrição para a tarefa.");
        return;
    }

    // Mostra o status no painel do microfone (que está escondido)
    // para que ele apareça quando o painel for resetado
    definirStatus('⏳ Salvando tarefa...', 'processando');
    
    try {
        const response = await fetch('/salvar_tarefa_texto', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tarefa: textoTarefa })
        });
        
        const data = await response.json();
        
        if (!response.ok || !data.sucesso) {
            throw new Error(data.mensagens ? data.mensagens[0] : 'Erro desconhecido ao salvar');
        }

        // Sucesso!
        definirStatus('✅ Tarefa salva!', 'sucesso');
        adicionarLog(`Tarefa Manual`, `📝: ${textoTarefa}\n✅: ${data.mensagens[0]}`, true);

    } catch (error) {
        console.error('Erro ao salvar tarefa:', error);
        definirStatus('❌ Erro ao salvar', 'erro');
        adicionarLog(`Tarefa Manual`, `Falha ao salvar: ${error.message}`, false);
    } finally {
        // Reseta a UI de volta para o microfone
        resetarPainelControle();
    }
}


// --- Funções de Estado e Log (Sem grandes mudanças) ---

async function atualizarEstado() {
    try {
        const response = await fetch('/estado');
        if (!response.ok) {
            document.getElementById('fonteEstado').textContent = 'Erro de conexão';
            document.getElementById('estacaoEstado').textContent = 'Erro de conexão';
            document.getElementById('statusAmbiente').textContent = 'Erro de conexão';
            return;
        }
        
        const data = await response.json();

        // Atualiza Fonte de Bancada
        const fonte = data.fonte;
        document.getElementById('fonteStatus').className = 'status-indicator ' + (fonte.ligada ? 'status-on' : 'status-off');
        document.getElementById('fonteEstado').textContent = fonte.ligada ? 'Ligada ✅' : 'Desligada ⭕';
        document.getElementById('fonteTensao').textContent = fonte.tensao.toFixed(1);
        document.getElementById('fonteCorrente').textContent = fonte.corrente.toFixed(2);
        document.getElementById('fontePotencia').textContent = fonte.potencia.toFixed(2);

        // Atualiza Estação de Solda
        const estacao = data.estacao;
        document.getElementById('estacaoStatus').className = 'status-indicator ' + (estacao.ligada ? 'status-on' : 'status-off');
        document.getElementById('estacaoEstado').textContent = estacao.ligada ? 'Ligada ✅' : 'Desligada ⭕';
        document.getElementById('estacaoTemp').textContent = estacao.temperatura_atual;
        document.getElementById('estacaoPronta').textContent = estacao.pronta ? 'Pronta ✅' : (estacao.ligada ? 'Aquecendo 🔥' : '-');

        // Atualiza Temperatura Ambiente
        if (data.temperatura_ambiente !== undefined && data.temperatura_ambiente !== null) {
            const tempAmbiente = data.temperatura_ambiente;
            document.getElementById('tempAmbiente').textContent = tempAmbiente.toFixed(1);
            let statusAmb = '';
            if (tempAmbiente < 20) statusAmb = '❄️ Frio';
            else if (tempAmbiente <= 26) statusAmb = '✅ Ideal';
            else if (tempAmbiente <= 30) statusAmb = '🌡️ Morno';
            else statusAmb = '🔥 Quente';
            document.getElementById('statusAmbiente').textContent = statusAmb;
        } else {
             document.getElementById('tempAmbiente').textContent = '--';
             document.getElementById('statusAmbiente').textContent = 'Indisponível';
        }
    } catch (error) {
        console.error('Erro ao atualizar estado:', error);
        document.getElementById('fonteEstado').textContent = 'Erro de conexão';
        document.getElementById('estacaoEstado').textContent = 'Erro de conexão';
        document.getElementById('statusAmbiente').textContent = 'Erro de conexão';
    }
}

function definirStatus(texto, tipo = null) {
    statusText.textContent = texto;
    statusText.className = 'status-text';
    if (tipo) {
        statusText.classList.add(tipo);
    }
}

function adicionarLog(transcricao, mensagem, sucesso) {
    if (logPlaceholder && logPlaceholder.parentNode === logContainer) {
        logContainer.removeChild(logPlaceholder);
    }
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry ' + (sucesso ? 'success' : 'error');
    const timestamp = new Date().toLocaleTimeString('pt-BR');
    logEntry.innerHTML = `
        <div class="timestamp">⏰ ${timestamp}</div>
        ${transcricao ? `<div class="transcription">🎤 "${transcricao}"</div>` : ''}
        <div class="message">${mensagem}</div>
    `;
    logContainer.insertBefore(logEntry, logContainer.firstChild);
    while (logContainer.children.length > 15) {
        logContainer.removeChild(logContainer.lastChild);
    }
}


// --- Função Auxiliar (Criação de WAV) ---
// (Sem alterações)

function criarWAV(audioData) {
    let totalLength = 0;
    audioData.forEach(chunk => { totalLength += chunk.length; });
    const samples = new Float32Array(totalLength);
    let offset = 0;
    audioData.forEach(chunk => {
        samples.set(chunk, offset);
        offset += chunk.length;
    });
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + samples.length * 2, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, 16000, true);
    view.setUint32(28, 16000 * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeString(view, 36, 'data');
    view.setUint32(40, samples.length * 2, true);
    let index = 44;
    for (let i = 0; i < samples.length; i++) {
        const s = Math.max(-1, Math.min(1, samples[i]));
        view.setInt16(index, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
        index += 2;
    }
    return new Blob([view], { type: 'audio/wav' });
}

function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}