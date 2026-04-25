<script>
  import { onMount } from "svelte";
  import { appState } from "./appState.svelte";
  import ProdInLoc from "./ProdInLoc.svelte";

  let data = $state([]);

  async function get_data() {
    try {
      let response = await fetch(
        `http://${appState.endpoint}/inventory_items/by_product/` +
          appState.product.id,
      );

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

  async function sendData() {
    let location_id =
      document.getElementById(`cmb_location`).selectedOptions[0].value;
    let expire_date = document.getElementById("txt_expire").value;

    try {
      let response = await fetch(
        `http://${appState.endpoint}/inventory_items`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            product_id: appState.barcode,
            location_id: location_id,
            expiration_date: expire_date,
          }),
        },
      );

      if (response.ok) {
        get_data();
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

  onMount(() => {
    get_data();
  });
</script>

{#if data.length > 0}
  <h1>Gestisci '{appState.product.name}'</h1>
  <table style="border: 2px solid rgb(140 140 140);">
    <thead>
      <tr>
        <th>Id</th>
        <th>Posizione</th>
        <th>Data Scadenza</th>
        <th>Operazioni</th>
      </tr>
    </thead>

    <tbody>
      {#each data as d}
        <tr>
          <ProdInLoc
            assoc_id={d.id}
            product_id={d.product_id}
            location_id={d.location_id}
            expiration_date={d.expiration_date}
            update_func={() => get_data()}
          />
        </tr>
      {/each}
      <tr>
        <td></td>
        <td>
          <select name="location" id="cmb_location">
            {#each appState.locations as location}
              <option value={location.id}>{location.name} </option>
            {/each}
          </select>
        </td>
        <td><input type="text" id="txt_expire" /></td>
        <td><button onclick={sendData}>Aggiungi</button></td>
      </tr>
    </tbody>
  </table>
{:else}
  Data is loading
{/if}
