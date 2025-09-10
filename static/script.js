async function carregarOrbita() {
      const resp = await fetch("/orbita");
      const data = await resp.json();

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
        updatemenus: [{
          type: "buttons",
          buttons: [
            {
              label: "▶ Play",
              method: "animate",
              args: [null, {
                frame: { duration: 30, redraw: true },
                fromcurrent: true,
                transition: { duration: 0 }
              }]
            },
            {
              label: "⏸ Pause",
              method: "animate",
              args: [[null], { frame: { duration: 0 }, mode: "immediate" }]
            }
          ]
        }]
      };

      Plotly.newPlot("grafico", [orbit, sun, comet], layout).then(() => {
        Plotly.addFrames("grafico", frames);
      });
    }

    carregarOrbita();