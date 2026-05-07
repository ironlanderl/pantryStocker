<script lang="ts">
  import { appState, Operation } from "./appState.svelte";

  let data = $state([]);

  async function send_search_data() {
    let product_name = document.getElementById("name").value;

    let url = `http://${appState.endpoint}/products/search/` + product_name;
    try {
      const response = await fetch(url);
      console.log(response);

      if (response.status == 404) {
        data = [];
        return;
      }

      if (response.ok) {
        data = await response.json();
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

<form
  onsubmit={(e) => {
    e.preventDefault();
    send_search_data();
  }}
>
  <label for="name">Nome Prodotto</label>
  <input type="text" id="name" />
  <button type="submit">Search</button>
</form>

{#if data.length > 0}
  <table
    style="border: 2px solid rgb(140 140 140); width: 100%; border-collapse: collapse;"
  >
    <thead>
      <tr>
        <th>Barcode</th>
        <th>Nome</th>
        <th>Descrizione</th>
        <th>Azione</th>
      </tr>
    </thead>
    <tbody>
      {#each data as d}
        <tr>
          <td style="border: 1px solid #ccc; padding: 8px;">{d.id}</td>
          <td style="border: 1px solid #ccc; padding: 8px;">{d.name}</td>
          <td style="border: 1px solid #ccc; padding: 8px;"
            >{d.description || ""}</td
          >
          <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">
            <button
              onclick={() => {
                appState.setBarcode(d.id);
                appState.operation = Operation.Lookup;
              }}>Seleziona</button
            >
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
{/if}
