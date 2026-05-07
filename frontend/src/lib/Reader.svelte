<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import Quagga from "@ericblade/quagga2";
  import { appState, Operation } from "./appState.svelte";

  let textCopy = $state(false);
  let _scannerIsRunning = $state(false);
  let lastScanTime = $state(0);
  let _selectedCameraId = $state("environment");
  let _selectedCameraLabel = $state("Rear Camera");
  let _showDebug = $state(false);
  let scannerContainer: HTMLElement | undefined;

  // Available barcode readers — toggle checkboxes to enable/disable
  const readers = [
    { id: "ean_reader", label: "EAN-13", default: false },
    { id: "ean_8_reader", label: "EAN-8", default: false },
    { id: "code_128_reader", label: "Code 128", default: false },
    { id: "code_39_reader", label: "Code 39", default: false },
    { id: "upc_reader", label: "UPC-A", default: false },
    { id: "upc_e_reader", label: "UPC-E", default: true },
    { id: "codabar_reader", label: "Codabar", default: false },
    { id: "i2of5_reader", label: "Interleaved 2of5", default: false },
  ];

  // Reactive set of enabled reader IDs
  let enabledReaders = $state(
    readers.filter((r) => r.default).map((r) => r.id),
  );

  function toggleReader(id: string) {
    if (enabledReaders.includes(id)) {
      enabledReaders = enabledReaders.filter((r) => r !== id);
    } else {
      enabledReaders = [...enabledReaders, id];
    }
    // Restart scanner with new config
    if (_scannerIsRunning) {
      stopScanner();
      startScanner();
    }
  }

  function controlL(text) {
    return text.replace(/[\$\@\?]/g, "L").replace(/[\!\-\^]/g, "0");
  }

  function handleDetected(result) {
    const currentTime = Date.now();
    if (currentTime - lastScanTime > 2000) {
      lastScanTime = currentTime;
      textCopy = true;
      setTimeout(() => (textCopy = false), 2000);

      console.log(result);
      const code = result.codeResult.code;
      const barcodeType = result.codeResult.format;
      const formattedCode = controlL(code);

      // Store results and switch view
      appState.setBarcode(formattedCode, barcodeType);
      appState.setOperation(Operation.Lookup);

      stopScanner();

      navigator.clipboard.writeText(code).catch(console.error);

      let context = new AudioContext();
      let oscillator = context.createOscillator();
      oscillator.type = "sine";
      oscillator.frequency.value = 800;
      oscillator.connect(context.destination);
      oscillator.start();
      setTimeout(() => oscillator.stop(), 150);
    }
  }

  function startScanner() {
    if (!scannerContainer) return;

    Quagga.init(
      {
        inputStream: {
          name: "Live",
          type: "LiveStream",
          target: scannerContainer,
          constraints: {
            width: { min: 640 },
            height: { min: 480 },
            facingMode: _selectedCameraId,
          },
          locate: true,
        },
        decoder: {
          readers: enabledReaders,
          debug: {
            showCanvas: _showDebug,
            showPatches: _showDebug,
            showFoundPatches: _showDebug,
            showSkeleton: _showDebug,
            showLabels: _showDebug,
            showPatchLabels: _showDebug,
            showRemainingPatchLabels: _showDebug,
            boxFromPatches: {
              showTransformed: _showDebug,
              showTransformedBox: _showDebug,
              showBB: _showDebug,
            },
          },
        },
      },
      function (err) {
        if (err) {
          console.error(err);
          return;
        }
        Quagga.start();
        _scannerIsRunning = true;
        Quagga.onDetected(handleDetected);
      },
    );
  }

  function stopScanner() {
    Quagga.stop();
    Quagga.offDetected(handleDetected);
    _scannerIsRunning = false;
  }

  function toggleScanner() {
    if (_scannerIsRunning) {
      stopScanner();
    } else {
      startScanner();
    }
  }

  function switchCamera() {
    _selectedCameraId =
      _selectedCameraId === "environment" ? "user" : "environment";
    _selectedCameraLabel =
      _selectedCameraId === "environment" ? "Rear Camera" : "Front Camera";

    if (_scannerIsRunning) {
      stopScanner();
      startScanner();
    }
  }

  onMount(() => {
    startScanner();
  });

  onDestroy(() => {
    if (_scannerIsRunning) stopScanner();
  });
</script>

{#if textCopy}
  <div class="message">
    <div class="success">Barcode Copied</div>
  </div>
{/if}

<div id="scanner-container" bind:this={scannerContainer}>
  <div onclick={switchCamera} class="cameraaa" role="button" tabindex="0">
    <i class="fa-thin fa-camera-rotate"></i>
    <span>{_selectedCameraLabel}</span>
  </div>
  <div class="target"></div>
</div>

<div class="reader-controls">
  <label class="debug-toggle">
    <input type="checkbox" bind:checked={_showDebug} />
    Debug overlay
  </label>
  <div class="reader-checkboxes">
    {#each readers as reader}
      <label class="reader-checkbox">
        <input
          type="checkbox"
          checked={enabledReaders.includes(reader.id)}
          onchange={() => toggleReader(reader.id)}
        />
        {reader.label}
      </label>
    {/each}
  </div>

  <div class="reader-help">
    <details>
      <summary style="cursor:pointer;font-size:13px;color:#888;"
        >ℹ️ Cosa legge ogni codice</summary
      >
      <div class="help-grid">
        <div class="help-item">
          <strong>EAN-13</strong> — Standard supermercati EU. Es:
          <code>8006312001234</code> (latte)
        </div>
        <div class="help-item">
          <strong>EAN-8</strong> — Versione corta EAN-13, prodotti piccoli. Es:
          <code>96385074</code>
        </div>
        <div class="help-item">
          <strong>UPC-A</strong> — Standard USA/Canada. Es:
          <code>01234567895</code> (cereal)
        </div>
        <div class="help-item">
          <strong>UPC-E</strong> — UPC compresso, 6 cifre + check. Es:
          <code>012345</code>
        </div>
        <div class="help-item">
          <strong>Code 128</strong> — Dati alfanumerici, logistica. Es:
          <code>SHIPPING-2026-0042</code>
        </div>
        <div class="help-item">
          <strong>Code 39</strong> — Industriale, militare. Es:
          <code>CAR-001-A</code>
        </div>
        <div class="help-item">
          <strong>Codabar</strong> — Biblioteche, sangue. Es:
          <code>A001234567B</code>
        </div>
        <div class="help-item">
          <strong>Interleaved 2of5</strong> — Solo numeri, imballaggio. Es:
          <code>9876543210</code>
        </div>
      </div>
    </details>
  </div>
</div>

<center>
  <input id="result" type="text" value={appState.barcode} readonly />
</center>

<div class="barcode-type-display">
  <small>Barcode type: {appState.barcodeType || "—"}</small>
</div>

<center>
  <button id="btn" onclick={toggleScanner}>
    {_scannerIsRunning ? "Stop Scanning" : "Start Scanning"}
  </button>
</center>

<style>
  #scanner-container {
    width: 100%;
    max-width: 640px;
    height: 480px;
    position: relative;
    overflow: hidden;
    background: #000;
    border-radius: 8px;
    margin: 0 auto;
  }

  #scanner-container :global(video) {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  #scanner-container :global(canvas.drawingBuffer) {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .cameraaa {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 10;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    padding: 8px 12px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .target {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 70%;
    height: 40%;
    border: 2px solid rgba(0, 255, 0, 0.5);
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 5;
    box-shadow: 0 0 0 1000px rgba(0, 0, 0, 0.3);
  }

  .reader-controls {
    width: 100%;
    max-width: 640px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: center;
  }

  .debug-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: #aaa;
    cursor: pointer;
  }

  .debug-toggle input {
    cursor: pointer;
  }

  .reader-checkboxes {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
  }

  .reader-checkbox {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    color: #ccc;
    cursor: pointer;
    user-select: none;
  }

  .reader-checkbox input {
    cursor: pointer;
  }

  .reader-help {
    width: 100%;
    max-width: 640px;
    padding: 0 10px 10px;
  }

  .reader-help details {
    background: #1a1a2e;
    border-radius: 8px;
    padding: 8px 12px;
  }

  .reader-help summary {
    list-style: none;
  }

  .reader-help summary::-webkit-details-marker {
    display: none;
  }

  .help-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 12px;
    margin-top: 8px;
    font-size: 12px;
    color: #bbb;
  }

  .help-item {
    line-height: 1.4;
  }

  .help-item code {
    background: #16213e;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 11px;
    color: #7fdbca;
  }

  .message {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;
  }

  .success {
    background: #4caf50;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }

  input {
    margin-top: 20px;
    padding: 10px;
    width: 80%;
    max-width: 400px;
    font-size: 18px;
    text-align: center;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  button {
    margin-top: 10px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
  }

  button:hover {
    background: #0056b3;
  }

  .barcode-type-display {
    margin-top: 8px;
    color: #aaa;
    font-size: 12px;
  }
</style>
