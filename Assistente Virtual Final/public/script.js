const recordButton = document.getElementById('recordButton');
const statusDisplay = document.getElementById('status');
const transcriptionDisplay = document.getElementById('transcription');

let recorder;
let audioContext;
let stream;
let isRecording = false;

recordButton.addEventListener('click', async () => {
    if (!isRecording) {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createMediaStreamSource(stream);
            recorder = new Recorder(source, { numChannels: 1 });
            recorder.record();

            statusDisplay.textContent = 'Gravando...';
            recordButton.textContent = 'Parar Gravação';
            isRecording = true;
        } catch (err) {
            console.error('Erro ao acessar microfone:', err);
            statusDisplay.textContent = 'Erro ao acessar microfone.';
        }
    } else {
        recorder.stop();
        stream.getTracks().forEach(track => track.stop());

        statusDisplay.textContent = 'Processando...';
        recordButton.textContent = 'Iniciar Gravação';
        isRecording = false;

        recorder.exportWAV(async (audioBlob) => {
            const formData = new FormData();
            formData.append('fala', audioBlob, 'fala.wav');

            console.log("dentro do export wave");
            try {
                const response = await fetch('reconhecer_comando', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                transcriptionDisplay.textContent = result.transcricao || "Erro ao processar a transcrição";
            } catch (error) {
                transcriptionDisplay.textContent = "Erro na comunicação com o servidor.";
                console.error("Erro:", error);
            }

            statusDisplay.textContent = 'Parado';
        });
    }
});
