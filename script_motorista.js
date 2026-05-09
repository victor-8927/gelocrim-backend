// 1. CAPTURA DE GPS EM TEMPO REAL
function iniciarRastreador() {
    if ("geolocation" in navigator) {
        navigator.geolocation.watchPosition(position => {
            const { latitude, longitude } = position.coords;
            console.log(`Localização: ${latitude}, ${longitude}`);
            
            // Aqui enviamos para o seu banco de dados
            // atualizarPosicaoNoServidor(latitude, longitude);
        }, error => {
            console.error("Erro ao capturar GPS:", error);
        }, {
            enableHighAccuracy: true,
            maximumAge: 30000,
            timeout: 27000
        });
    }
}

// 2. LÓGICA DA CÂMERA (Captura de Foto)
function tirarFoto() {
    // Cria um input de arquivo oculto que aciona a câmera no celular
    const inputId = document.createElement('input');
    inputId.type = 'file';
    inputId.accept = 'image/*';
    inputId.capture = 'camera'; // Força abrir a câmera no Android/iOS

    inputId.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                // Exibe a miniatura na tela (se você tiver um elemento <img> com id 'preview')
                // document.getElementById('preview').src = event.target.result;
                alert("Foto capturada com sucesso!");
            };
            reader.readAsDataURL(file);
        }
    };
    inputId.click();
}

// 3. FUNÇÃO PARA O BOTÃO "CHEGUEI"
function irParaBaixa() {
    // Aqui você pode redirecionar para a tela de comprovação
    // ou abrir um modal de assinatura e foto
    alert("Iniciando processo de baixa da entrega...");
    tirarFoto();
}

// Inicia o rastreamento assim que o app abre
window.onload = iniciarRastreador;// --- LÓGICA DO MOTORISTA GELOCRIM ---

// 1. RASTREAMENTO GPS
function iniciarRastreador() {
    if ("geolocation" in navigator) {
        navigator.geolocation.watchPosition(position => {
            console.log("GPS Ativo:", position.coords.latitude, position.coords.longitude);
        }, error => console.error("Erro GPS:", error), { enableHighAccuracy: true });
    }
}

// 2. FUNÇÃO DA CÂMERA
function tirarFoto() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.capture = 'camera'; 

    input.onchange = e => {
        const file = e.target.files[0];
        if (file) alert("Foto capturada com sucesso!");
    };
    input.click();
}

// 3. VINCULAR BOTÃO
function irParaBaixa() {
    tirarFoto();
}

window.onload = iniciarRastreador;// --- LÓGICA DO MOTORISTA GELOCRIM ---

// 1. RASTREAMENTO GPS
function iniciarRastreador() {
    if ("geolocation" in navigator) {
        navigator.geolocation.watchPosition(position => {
            console.log("GPS Ativo:", position.coords.latitude, position.coords.longitude);
        }, error => console.error("Erro GPS:", error), { enableHighAccuracy: true });
    }
}

// 2. FUNÇÃO DA CÂMERA
function tirarFoto() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.capture = 'camera'; 

    input.onchange = e => {
        const file = e.target.files[0];
        if (file) alert("Foto capturada com sucesso!");
    };
    input.click();
}

// 3. VINCULAR BOTÃO
function irParaBaixa() {
    tirarFoto();
}

window.onload = iniciarRastreador;
// FAZ O QUADRO DE ASSINATURA APARECER
function irParaBaixa() {
    document.getElementById('area-assinatura').style.display = 'block';
    window.scrollTo(0, document.body.scrollHeight); // Rola para baixo
    tirarFoto(); // Abre a câmera
}

// LÓGICA DO DESENHO NO CANVAS
const canvas = document.getElementById('canvas-assinatura');
if(canvas) {
    const ctx = canvas.getContext('2d');
    let desenhando = false;

    // Ajusta o tamanho interno do canvas para não ficar serrilhado
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    function obterPosicao(e) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: (e.clientX || e.touches[0].clientX) - rect.left,
            y: (e.clientY || e.touches[0].clientY) - rect.top
        };
    }

    const iniciar = (e) => { desenhando = true; ctx.beginPath(); const pos = obterPosicao(e); ctx.moveTo(pos.x, pos.y); };
    const mover = (e) => { 
        if (!desenhando) return; 
        const pos = obterPosicao(e); 
        ctx.lineTo(pos.x, pos.y); 
        ctx.strokeStyle = "#000"; 
        ctx.lineWidth = 3; 
        ctx.stroke(); 
    };
    const parar = () => { desenhando = false; };

    canvas.addEventListener('mousedown', iniciar);
    canvas.addEventListener('mousemove', mover);
    window.addEventListener('mouseup', parar);
    canvas.addEventListener('touchstart', (e) => { e.preventDefault(); iniciar(e); });
    canvas.addEventListener('touchmove', (e) => { e.preventDefault(); mover(e); });
    canvas.addEventListener('touchend', parar);
}

function limparAssinatura() {
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function salvarBaixa() {
    alert("GELOCRIM INFORMA: Entrega confirmada com sucesso!");
    location.reload(); // Simula o envio e limpa a tela para a próxima
}