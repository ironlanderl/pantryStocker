<script>
  import { onMount, onDestroy } from "svelte";
  import Quagga from "@ericblade/quagga2";
  import { appState, Operation } from "./appState.svelte";

  let textCopy = $state(false);
  let _scannerIsRunning = $state(false);
  let lastScanTime = $state(0);
  let _selectedCameraId = $state("environment");
  let _selectedCameraLabel = $state("Rear Camera");
  let scannerContainer = $state();

  function controlL(text) {
    return text.replace(/[\$\@\?]/g, "L").replace(/[\!\-\^]/g, "0");
  }

  function handleDetected(result) {
    const currentTime = Date.now();
    if (currentTime - lastScanTime > 2000) {
      lastScanTime = currentTime;
      textCopy = true;
      setTimeout(() => (textCopy = false), 2000);

      const code = result.codeResult.code;
      const formattedCode = controlL(code);

      // Store results and switch view
      appState.setBarcode(formattedCode);
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
          readers: [
            // "code_128_reader",
            "ean_reader",
            // "ean_8_reader",
            // "code_39_reader",
            "upc_reader",
            // "upc_e_reader",
            // "codabar_reader",
            // "i2of5_reader",
          ],
          debug: {
            showCanvas: true,
            showPatches: true,
            showFoundPatches: true,
            showSkeleton: true,
            showLabels: true,
            showPatchLabels: true,
            showRemainingPatchLabels: true,
            boxFromPatches: {
              showTransformed: true,
              showTransformedBox: true,
              showBB: true,
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

<center>
  <input id="result" type="text" value={appState.barcode} readonly />
</center>

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
</style>
