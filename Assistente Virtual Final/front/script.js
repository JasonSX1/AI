// Elementos da interface
const recordButton = document.getElementById('recordButton');
const statusText = document.getElementById('statusText');
const logContainer = document.getElementById('logContainer');
const logPlaceholder = document.getElementById('logPlaceholder'); // Placeholder do log

// Variáveis de controle
let audioChunks = [];
let isRecording = false;
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

// Impede que a página recarregue ao dar F5 durante gravação
window.addEventListener('beforeunload', (e) => {
    if (isRecording) {
        e.preventDefault();
        e.returnValue = '';
    }
});


// --- Funções de Gravação ---

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

        // Cria contexto de áudio com 16kHz
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

        // Para automaticamente após 5 segundos
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

    // Desabilita o botão durante o processamento
    recordButton.disabled = true; 
    recordButton.classList.remove('recording');
    recordButton.textContent = '🎙️';
    definirStatus('⏳ Processando...', 'processando');

    // Para o processamento de áudio
    if (processor) {
        processor.disconnect();
        processor = null;
    }

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }

    if (audioContext) {
        audioContext.close();
    }

    // Converte os chunks em WAV
    const wavBlob = criarWAV(audioChunks);
    enviarAudio(wavBlob);
}

// --- Processamento de Áudio e API ---

async function enviarAudio(audioBlob) {
    const formData = new FormData();
    formData.append('fala', audioBlob, 'audio.wav');

    try {
        const response = await fetch('/reconhecer_comando', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();

            if (data.sucesso) {
                const mensagens = data.mensagens ? data.mensagens.join('\n') : 'Comando executado';
                adicionarLog(data.transcricao, mensagens, true);
                definirStatus('✅ Comando executado!', 'sucesso');
            } else {
                const mensagens = data.mensagens ? data.mensagens.join('\n') : 'Comando não reconhecido';
                adicionarLog(data.transcricao, mensagens, false);
                definirStatus('⚠️ Comando não reconhecido', 'aviso');
            }
        } else {
            const errorData = await response.json().catch(() => ({}));
            adicionarLog(null, '❌ Erro ao processar comando: ' + (errorData.erro || 'Erro desconhecido'), false);
            definirStatus('❌ Erro ao processar', 'erro');
        }
    } catch (error) {
        console.error('Erro ao enviar áudio:', error);
        adicionarLog(null, '❌ Erro de conexão: ' + error.message, false);
        definirStatus('❌ Erro de conexão', 'erro');
    } finally {
        // Reabilita o botão
        recordButton.disabled = false;
        
        // Atualiza estado dos equipamentos
        setTimeout(atualizarEstado, 500);

        // Reseta o texto de status
        setTimeout(() => {
            definirStatus('Clique no microfone e fale');
        }, 3000);
    }
}

async function atualizarEstado() {
    try {
        const response = await fetch('/estado');
        if (response.ok) {
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
        }
    } catch (error) {
        console.error('Erro ao atualizar estado:', error);
        // Opcional: Adicionar um indicador de falha na UI
    }
}

// --- Funções Auxiliares (UI) ---

/**
 * Define o texto e a classe de estilo para o statusText.
 * @param {string} texto - O texto a ser exibido.
 * @param {'gravando' | 'processando' | 'sucesso' | 'aviso' | 'erro' | null} tipo - A classe de estilo.
 */
function definirStatus(texto, tipo = null) {
    statusText.textContent = texto;
    // Remove todas as classes de estado e adiciona a nova (se houver)
    statusText.className = 'status-text';
    if (tipo) {
        statusText.classList.add(tipo);
    }
}

function adicionarLog(transcricao, mensagem, sucesso) {
    // Remove mensagem de "Aguardando" se ela existir
    if (logPlaceholder.parentNode === logContainer) {
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

    // Limita a 10 entradas no log
    while (logContainer.children.length > 10) {
        logContainer.removeChild(logContainer.lastChild);
    }
}


// --- Funções Auxiliares (Criação de WAV) ---
// (Sem alterações, pois esta lógica é específica para o seu backend)

function criarWAV(audioData) {
    // Concatena todos os chunks
    let totalLength = 0;
    audioData.forEach(chunk => {
        totalLength += chunk.length;
    });

    const samples = new Float32Array(totalLength);
    let offset = 0;
    audioData.forEach(chunk => {
        samples.set(chunk, offset);
        offset += chunk.length;
    });

    // Converte Float32 para Int16
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);

    // WAV Header
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + samples.length * 2, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true); // fmt chunk size
    view.setUint16(20, 1, true); // PCM format
    view.setUint16(22, 1, true); // mono
    view.setUint32(24, 16000, true); // sample rate
    view.setUint32(28, 16000 * 2, true); // byte rate
    view.setUint16(32, 2, true); // block align
    view.setUint16(34, 16, true); // bits per sample
    writeString(view, 36, 'data');
    view.setUint32(40, samples.length * 2, true);

    // PCM data
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