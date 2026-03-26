<script>
  import { appState } from "./appState.svelte";
  let { assoc_id, product_id, location_id, expiration_date } = $props();

  let location_name = $derived(
    appState.locations.find((l) => l.id === location_id)?.name || "Unknown",
  );

  async function updateLocation() {
    try {
      let response = await fetch(
        `http://${appState.endpoint}/inventory_items/move`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            assoc_id: assoc_id,
            location_id: document.getElementById(`sel_location_${assoc_id}`)
              .selectedOptions[0].value,
          }),
        },
      );

      if (response.ok) {
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

<!-- TODO: Add a delete button. Maybe also a notes section? -->
<td>{assoc_id}</td>
<td>{appState.product.name}</td>
<td>
  <select
    name="location"
    id="sel_location_{assoc_id}"
    onchange={updateLocation}
  >
    {#each appState.locations as location}
      {#if location_id === location.id}
        <option value={location.id} selected>{location.name} </option>
      {:else}
        <option value={location.id}>{location.name} </option>
      {/if}
    {/each}
  </select>
</td>
<td>{expiration_date}</td>
