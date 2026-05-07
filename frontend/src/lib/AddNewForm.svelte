<script>
  import { appState, Operation } from "./appState.svelte";

  async function sendData() {
    let product_name = document.getElementById("product_name").value;
    let product_desc = document.getElementById("product_desc").value;

    try {
      let response = await fetch(`http://${appState.endpoint}/products`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: appState.barcode,
          name: product_name,
          description: product_desc,
        }),
      });

      if (response.ok) {
        appState.setOperation(Operation.Lookup);
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
</script>

<div style="display: flex; flex-direction: row; gap: 10px;">
  <div class="input-group">
    <label for="id">Id Prodotto</label>
    <input type="text" name="id" value={appState.barcode} />
  </div>
  <div class="input-group">
    <label for="product_name">Nome Prodotto</label>
    <input type="text" name="name" id="product_name" value="" />
  </div>
  <div class="input-group">
    <label for="product_desc">Descrizione Prodotto</label>
    <input type="text" name="description" id="product_desc" value="" />
  </div>
</div>
<button type="button" onclick={() => sendData()}> Send data </button>

<style>
  .input-group {
    display: flex;
    flex-direction: column;
  }
</style>
