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

  onMount(() => {
    get_data();
  });
</script>

{#if data.length > 0}
  <table style="border: 2px solid rgb(140 140 140);">
    <thead>
      <tr>
        <th>Id</th>
        <th>Prodotto</th>
        <th>Posizione</th>
        <th>Data Scadenza</th>
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
          />
        </tr>
      {/each}
    </tbody>
  </table>
{:else}
  Data is loading
{/if}
