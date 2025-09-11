async function carregarOrbita(data) {
      
  const orbit = {
    x: data.frames.map(f => f.x),
    y: data.frames.map(f => f.y),
    mode: "lines",
    line: { color: "lightblue" },
    name: "Órbita"
  };

  const comet = {
    x: [data.frames[0].x],
    y: [data.frames[0].y],
    mode: "markers",
    marker: { size: 10, color: "darkred" },
    name: "Cometa"
  };

  const sun = {
    x: [0],
    y: [0],
    mode: "markers",
    marker: { size: 15, color: "yellow", line: { color: "orange", width: 2 } },
    name: "Sol"
  };

  // frames só para o cometa
  const frames = data.frames.map((f, i) => ({
    name: i.toString(),
    data: [
      {}, // orbita
      {}, // sol
      { x: [f.x], y: [f.y] } // cometa
    ]
  }));

  const layout = {
    title: `Órbita (e=${data.e.toFixed(3)})`,
    xaxis: { scaleanchor: "y" },
    paper_bgcolor: '#eaedf7',
    plot_bgcolor: '#040c24',
    //  font: { color: "white" },
    updatemenus: [{
      type: "buttons",
      x: 0.5,         // posição horizontal (0 = esquerda, 1 = direita)
      y: -0.2,        // posição vertical (negativo = fora do gráfico, embaixo)
      xanchor: "center",
      yanchor: "top",
      direction: "left",   // botões lado a lado
      buttons: [
        {
          label: "▶ Play",
          method: "animate",
          args: [null, {
            frame: { duration: 30, redraw: true },
            fromcurrent: true,
            transition: { duration: 0 }
          }],
          pad: { l: 0, r: 20, t: 0, b: 0 } 
        },
        {
          label: "⏸ Pause",
          method: "animate",
          args: [[null], { frame: { duration: 0 }, mode: "immediate" }],
          pad: { l: 20, r: 0, t: 0, b: 0 } // adiciona espaço à esquerda
        }
      ]
    }]
  };


  Plotly.newPlot("grafico", [orbit, sun, comet], layout).then(() => {
    Plotly.addFrames("grafico", frames);
  });
}

async function fetchOrbita(e) {
  e.preventDefault(); // evita o reload do form

  // Pega os valores dos inputs
  const massaCorporal = document.getElementById("massaCorporal").value;
  const excentricidade = document.getElementById("excentricidade").value;
  const semieixo = document.getElementById("semieixo").value;
  const angulo = document.getElementById("angulo").value;
  const numPontos = document.getElementById("numPontos").value;

  // Monta a query string
  const params = new URLSearchParams({
    massaCorporal,
    excentricidade,
    semieixo,
    angulo,
    numPontos
  });

  const resp = await fetch(`/orbita?${params.toString()}`)
  const data = await resp.json()

  carregarOrbita(data);
}

async function fetchVelocidade(e) {
  e.preventDefault();
  
  // Pega os valores do formulário
  const massaCorporal = document.getElementById("massaCorporal").value;
  const excentricidade = document.getElementById("excentricidade").value;
  const semieixo = document.getElementById("semieixo").value;

  // Monta query params
  const params = new URLSearchParams({
    massaCorporal,
    excentricidade,
    semieixo
  });

  // Faz requisição para a rota Flask
  const resp = await fetch(`/velocidades?${params.toString()}`);
  const data = await resp.json();

  if (data.error) {
    alert("Erro: " + data.error);
    return;
  }

  // Monta a mensagem
  let msg = `Tipo de Órbita: ${data.tipo}\n`;
  msg += `Velocidade no Periélio: ${data.v_perielio_kms.toFixed(2)} km/s\n`;
  msg += `Distância no Periélio: ${data.r_perielio_km.toExponential(2)} km\n`;

  if (data.tipo === "eliptica") {
    msg += `Velocidade no Afélio: ${data.v_afelio_kms.toFixed(2)} km/s\n`;
    msg += `Distância no Afélio: ${data.r_afelio_km.toExponential(2)} km\n`;
  }

  alert(msg);

}

async function startApp(){
  const resp = await fetch("/orbita");
  const data = await resp.json();
  const btnOrbita = document.querySelector('#btnOrbita');
  const btnVelocidade = document.querySelector('#btnVelocidade');

  btnOrbita.addEventListener('click', fetchOrbita);
  btnVelocidade.addEventListener('click', fetchVelocidade);

  carregarOrbita(data);
}

startApp()