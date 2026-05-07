<script lang="ts">
  import { onMount } from "svelte";
  import Counter from "./lib/Counter.svelte";
  import Reader from "./lib/Reader.svelte";
  import AddNewForm from "./lib/AddNewForm.svelte";
  import { appState, Operation } from "./lib/appState.svelte";
  import ManageProdInLoc from "./lib/ManageProdInLoc.svelte";
  import app from "./main";
  import SearchProduct from "./lib/SearchProduct.svelte";

  onMount(() => {
    appState.fetchLocations();
  });

  async function test_get_data() {
    let url = `http://${appState.endpoint}/products/` + appState.barcode;
    try {
      const response = await fetch(url);

      if (response.status == 404) {
        appState.setOperation(Operation.AddNew);
        return;
      }

      if (response.ok) {
        let test = await response.json();
        appState.setProductName(test.name);
        appState.setProductDesc(test.description);
        console.log(appState);
        appState.setOperation(Operation.Manage);
        return;
      }

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      // …
    } catch (error) {
      console.error(error.message);
    }
  }

  function skip_qr() {
    appState.setBarcode("2000");
    appState.setOperation(Operation.Lookup);
  }

  function go_home() {
    appState.setOperation(Operation.Scanning);
  }

  function formatBarcode(): string {
    let type = appState.barcodeType;
    let code = appState.barcode;
    console.log(type);
    console.log(code);
    switch (type) {
      case "ean_13":
        // EAN-13: X-XXXXXX-XXXXXX (1-6-6)
        if (code.length === 13) {
          return `${code[0]}-${code.slice(1, 7)}-${code.slice(7, 13)}`;
        }
        return code;
      case "ean_8":
        // EAN-8: XXXX-XXXX (6-2)
        if (code.length === 8) {
          return `${code.slice(0, 4)}-${code.slice(4, 8)}`;
        }
        return code;
      case "upc_a":
        // UPC-A: X-XXXXX-XXXXX-X (1-6-5)
        if (code.length === 12) {
          return `${code[0]}-${code.slice(1, 6)}-${code.slice(6, 11)}-${code[11]}`;
        }
        return code;
      case "upc_e":
        // UPC-E: XXXXXX-XX (6-2)
        if (code.length >= 6) {
          return `${code[0]}-${code.slice(1, 7)}-${code[7]}`;
        }
        return code;
      default:
        // Code 128, Code 39, Codabar, Interleaved 2of5 — no grouping
        return code;
    }
  }
</script>

<header>
  <div
    style="display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: space-evenly; width: 100%;"
  >
    <button onclick={go_home}>Scanning</button>

    <!--    {#each Object.keys(Operation) as operation}
      <div style="border: 1px solid white;">{operation}</div>
    {/each} -->
  </div>
</header>

Current status: {appState.operation}

<section id="center">
  {#if appState.operation === Operation.Menu}
    <button onclick={() => appState.setOperation(Operation.Scanning)}>
      Scan Code
    </button>
    <button onclick={() => appState.setOperation(Operation.Search)}>
      Search Product
    </button>
  {:else if appState.operation === Operation.Scanning}
    <button onclick={() => skip_qr()}> Skip to management </button>
    <Reader />
  {:else if appState.operation === Operation.Lookup}
    <div class="lookup-view">
      <p>The code we got is: <strong>{formatBarcode()}</strong></p>
      <button onclick={() => appState.setOperation(Operation.Scanning)}>
        Scan Again
      </button>
      <button onclick={test_get_data}> Get Data </button>
    </div>
  {:else if appState.operation === Operation.AddNew}
    <AddNewForm />
  {:else if appState.operation === Operation.Manage}
    <ManageProdInLoc />
  {:else if appState.operation === Operation.Search}
    <SearchProduct />
  {/if}
</section>

<style>
  #center {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    padding: 20px;
  }

  .lookup-view {
    text-align: center;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
  }

  .controls {
    display: flex;
    gap: 10px;
  }
</style>
