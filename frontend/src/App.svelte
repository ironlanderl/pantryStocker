<script>
  import { onMount } from "svelte";
  import Counter from "./lib/Counter.svelte";
  import Reader from "./lib/Reader.svelte";
  import AddNewForm from "./lib/AddNewForm.svelte";
  import { appState, Operation } from "./lib/appState.svelte";
  import ManageProdInLoc from "./lib/ManageProdInLoc.svelte";

  onMount(() => {
    appState.fetchLocations();
  });

  async function test_get_data() {
    let url = "http://192.168.178.26:8000/products/" + appState.barcode;
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
    appState.setBarcode("1000");
    appState.setOperation(Operation.Lookup);
  }
</script>

Current status: {appState.operation}

<section id="center">
  {#if appState.operation === Operation.Scanning}
    <button onclick={() => skip_qr()}> Skip to management </button>
    <Reader />
  {:else if appState.operation === Operation.Lookup}
    <div class="lookup-view">
      <p>The code we got is: <strong>{appState.barcode}</strong></p>
      <button onclick={() => appState.setOperation(Operation.Scanning)}>
        Scan Again
      </button>
      <button onclick={test_get_data}> Get Data </button>
    </div>
  {:else if appState.operation === Operation.AddNew}
    <AddNewForm />
  {:else if appState.operation === Operation.Manage}
    <ManageProdInLoc />
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
