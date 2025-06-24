const periodeRadios = document.querySelectorAll('input[name="periode"]');
const boursierContainer = document.getElementById("boursier-graphs-container");
const justEtfContainer = document.getElementById("justetf-graphs-container");
const boursoramaContainer = document.getElementById(
  "boursorama-graphs-container"
);
const loadingIndicator = document.getElementById("loading-indicator");
const errorMessageDiv = document.getElementById("error-message-area");
const chartsArea = document.getElementById("charts-area");

let activeCharts = [];

function formatDateForTradingView(dateInput) {
  const date = new Date(dateInput);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

const chartsResizeObserver = new ResizeObserver((entries) => {
  entries.forEach((entry) => {
    requestAnimationFrame(() => {
      const { width, height } = entry.contentRect;
      const chartToResize = activeCharts.find(
        (c) => c.container === entry.target
      );
      if (chartToResize) {
        chartToResize.chart.resize(width, height);
      }
    });
  });
});

async function fetchAndRenderGraphs(period) {
  loadingIndicator.classList.remove("hidden");
  chartsArea.classList.add("hidden");
  errorMessageDiv.classList.add("hidden");
  errorMessageDiv.querySelector("p").textContent = "";

  activeCharts.forEach((c) => {
    chartsResizeObserver.unobserve(c.container);
    c.chart.remove();
  });
  activeCharts = [];

  boursierContainer.innerHTML = "";
  justEtfContainer.innerHTML = "";
  boursoramaContainer.innerHTML = "";

  try {
    const response = await fetch(`/api/period/${period}`);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erreur HTTP ${response.status}: ${errorText}`);
    }
    const results = await response.json();

    if (!results || results.length === 0) {
      errorMessageDiv.querySelector("p").textContent =
        "Aucune donnée reçue de l'API.";
      errorMessageDiv.classList.remove("hidden");
      return;
    }

    chartsArea.classList.remove("hidden");

    results.forEach((item, index) => {
      // ... (la logique pour `item.type === "boursier"` reste la même, elle est omise ici pour la clarté)
      const card = document.createElement("div");
      card.className = "bg-white p-4 rounded-lg shadow-md";
      const title = document.createElement("h3");
      title.className = "text-lg font-semibold mb-3 text-gray-700 truncate";
      title.textContent = item.name || `Graphique ${index + 1}`;
      card.appendChild(title);
      let contentAddedToCard = false;

      if (item.error) {
        const errorP = document.createElement("p");
        errorP.className = "text-red-500 text-sm";
        errorP.textContent = `Erreur: ${item.error}`;
        card.appendChild(errorP);
        contentAddedToCard = true;
      }

      if (item.type === "boursier") {
        if (item.iframe_url) {
          const iframe = document.createElement("iframe");
          try {
            const urlObject = new URL(item.iframe_url);
            const finalIframeSrc = urlObject
              .toString()
              .replace(/%2C/g, ",")
              .replace(/%3A/g, ":");
            iframe.src = finalIframeSrc;
            iframe.style.width = "100%";
            iframe.style.height = "350px";
            iframe.setAttribute("frameborder", "0");
            iframe.setAttribute("scrolling", "no");
            card.appendChild(iframe);
            contentAddedToCard = true;
          } catch (e) {
            const errorP = document.createElement("p");
            errorP.className = "text-red-500 text-sm";
            errorP.textContent = `Erreur: URL d'iframe invalide.`;
            card.appendChild(errorP);
            contentAddedToCard = true;
          }
        } else if (!item.error) {
          const noDataP = document.createElement("p");
          noDataP.className = "text-gray-500 text-sm";
          noDataP.textContent =
            "Données insuffisantes pour afficher ce graphique (iframe).";
          card.appendChild(noDataP);
          contentAddedToCard = true;
        }
        if (contentAddedToCard) {
          boursierContainer.appendChild(card);
        }
      } else if (item.type === "justetf" || item.type === "boursorama") {
        if (item.series && item.series.length > 1) {
          // Il faut au moins 2 points pour une bougie
          if (item.type === "justetf" && item.performance) {
            const performanceDiv = document.createElement("div");
            performanceDiv.className = "mb-2 text-sm text-gray-600";
            performanceDiv.textContent = `Performance: ${
              item.performance?.localized || "N/A"
            }`;
            card.appendChild(performanceDiv);
          }

          const chartContainerDiv = document.createElement("div");
          chartContainerDiv.style.height = "350px";
          chartContainerDiv.style.width = "100%";
          card.appendChild(chartContainerDiv);

          setTimeout(() => {
            const chart = LightweightCharts.createChart(chartContainerDiv, {
              width: chartContainerDiv.clientWidth,
              height: chartContainerDiv.clientHeight,
              layout: {
                background: { color: "#ffffff" },
                textColor: "rgba(31, 41, 55, 1)",
              },
              grid: {
                vertLines: { color: "#f0f0f0" },
                horzLines: { color: "#f0f0f0" },
              },
            });

            // --- MODIFICATION 1 : Transformer les données en format OHLC ---
            const candlestickData = [];
            for (let i = 1; i < item.series.length; i++) {
              const open = item.series[i - 1].value.raw;
              const close = item.series[i].value.raw;
              candlestickData.push({
                time: formatDateForTradingView(item.series[i].date),
                open: open,
                high: Math.max(open, close),
                low: Math.min(open, close),
                close: close,
              });
            }

            // --- MODIFICATION 2 : Utiliser CandlestickSeries ---
            const candlestickSeries = chart.addSeries(
              LightweightCharts.CandlestickSeries,
              {
                upColor: "#10b981", // Vert pour la hausse
                downColor: "#ef4444", // Rouge pour la baisse
                borderDownColor: "#ef4444",
                borderUpColor: "#10b981",
                wickDownColor: "#ef4444",
                wickUpColor: "#10b981",
              }
            );

            candlestickSeries.setData(candlestickData);

            chart.timeScale().fitContent();

            activeCharts.push({ chart, container: chartContainerDiv });
            chartsResizeObserver.observe(chartContainerDiv);
          }, 0);

          contentAddedToCard = true;
        } else if (!item.error) {
          const noDataP = document.createElement("p");
          noDataP.className = "text-gray-500 text-sm";
          noDataP.textContent =
            "Données de série insuffisantes pour afficher ce graphique.";
          card.appendChild(noDataP);
          contentAddedToCard = true;
        }

        if (contentAddedToCard) {
          if (item.type === "justetf") justEtfContainer.appendChild(card);
          else if (item.type === "boursorama")
            boursoramaContainer.appendChild(card);
        }
      }
    });
  } catch (error) {
    console.error("Erreur lors du chargement des graphiques:", error);
    errorMessageDiv.querySelector(
      "p"
    ).textContent = `Erreur: ${error.message}. Veuillez réessayer.`;
    errorMessageDiv.classList.remove("hidden");
  } finally {
    loadingIndicator.classList.add("hidden");
  }
}

periodeRadios.forEach((radio) => {
  radio.addEventListener("change", (event) =>
    fetchAndRenderGraphs(event.target.value)
  );
});

document.addEventListener("DOMContentLoaded", () => {
  const checkedRadio = document.querySelector('input[name="periode"]:checked');
  if (checkedRadio) fetchAndRenderGraphs(checkedRadio.value);
});
