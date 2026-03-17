<script>
  import { appState, Operation } from "./appState.svelte";

  async function sendData() {
    let product_name = document.getElementById("product_name").value;
    let product_desc = document.getElementById("product_desc").value;

    try {
      let response = await fetch("http://192.168.178.26:8000/products", {
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

<div>
  <input type="text" name="id" value={appState.barcode} />
  <input type="text" name="name" id="product_name" value="" />
  <input type="text" name="description" id="product_desc" value="" />
  <button type="button" onclick={() => sendData()}> Send data </button>
</div>
